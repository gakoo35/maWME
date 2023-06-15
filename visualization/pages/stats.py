import dash
from dash import html, Input, Output
from dash import dcc
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from wordcloud import WordCloud, STOPWORDS
import emoji

# import app
from app import app

dash.register_page(__name__, path='/stats')


@app.callback(
Output('dataset4', 'children'),
Input('dropdown-df', 'value')
)
def update_df(path):
    global df
    df = pd.read_csv('datasets/'+path+'.csv')
    return 0


update_wordclouds = False # TODO: check if we put like a button on the interface to update the wordclouds --> but I think not because data will not change

if(update_wordclouds):
    df = pd.read_csv('datasets/reddit.csv')
 
    stopwords = ["airline", "airlines", "american", 'american airlines', 'delta', 'southwest', 'united', 'flight', 'will', 
                 'now', 'one', 'see', 's', 'aa', 'flights', 'americanair', 'southwestair', 'plane', 't', 'co', 'u', 'air', 
                 'american', 'southwest', 'know'] + list(STOPWORDS)

    all_companies = df['airline'].unique()
    all_companies = np.append('All', all_companies)
    print('word_cloud progress : start')
    for company in all_companies:
        comment_words = ''
        print(company)
        df_temp = df.copy()
        if(company != 'All'):
            df_temp = df_temp.drop(df[df['airline'] != company].index)
        # iterate through the csv file
        for val in df_temp['text'].values:
            # typecaste each val to string
            val = str(val)
            # split the value
            tokens = val.split()
            # Converts each token into lowercase
            for i in range(len(tokens)):
                tokens[i] = tokens[i].lower()
            comment_words += " ".join(tokens)+" "
        
        wordcloud = WordCloud(width = 800, height = 800,
                        background_color ='white',
                        stopwords = stopwords,
                        font_path='arial',
                        relative_scaling=0,
                        min_font_size = 10).generate(comment_words)
        
        wordcloud.to_file('assets/wordclouds/'+company+'.png')
    print('word_cloud progress : end')



@app.callback(
Output('stats-plot', 'children'),
Input('dropdown-company', 'value'),
Input('dataset4', 'children')
)
def stats_plot(company, callback_df):
    global df
    # df = pd.read_csv('datasets/tweets_formatted.csv')
    df_temp = df.copy()
    childrens = []
    if(company != 'All'):
        df_temp = df_temp.drop(df_temp[df_temp['airline'] != company].index)
    df_temp['date'] = pd.to_datetime(df_temp['date'])
    df_temp = df_temp.set_index('date')
    #childrens.append(html.H1(children=company))
    childrens.append(html.Div(children='''Voici plusieurs statistiques sur les posts de la compagnie sélectionnée. 
    Vous pouvez changer de compagnie en utilisant le menu déroulant ci-dessus. On peut trouver plusieurs informations comme le nombre de posts, 
    les dates des posts, le nombre d'utilisateurs, ...'''))
    childrens.append(html.Br())
    # start and end date
    childrens.append(html.P(children=[html.Strong('First post date : '), html.Span(str(df_temp.index.min().strftime("%m.%d.%Y")))]))
    childrens.append(html.P(children=[html.Strong('Last post date : '), html.Span(str(df_temp.index.max().strftime("%m.%d.%Y")))]))
    # number of posts
    childrens.append(html.P(children=[html.Strong('Number of posts : '), html.Span(str(len(df_temp)))]))
    # count and percentage of positive, negative and neutral posts
    childrens.append(html.P(children=[html.Strong('Number of positive posts : '), html.Span(str(len(df_temp[df_temp['airline_sentiment'] == 'positive'])) + ' (' + str(round(len(df_temp[df_temp['airline_sentiment'] == 'positive'])/len(df_temp)*100, 2)) + '%)')]))
    childrens.append(html.P(children=[html.Strong('Number of negative posts : '), html.Span(str(len(df_temp[df_temp['airline_sentiment'] == 'negative'])) + ' (' + str(round(len(df_temp[df_temp['airline_sentiment'] == 'negative'])/len(df_temp)*100, 2)) + '%)')]))
    childrens.append(html.P(children=[html.Strong('Number of neutral posts : '), html.Span(str(len(df_temp[df_temp['airline_sentiment'] == 'neutral'])) + ' (' + str(round(len(df_temp[df_temp['airline_sentiment'] == 'neutral'])/len(df_temp)*100, 2)) + '%)')]))
    # random post
    random_post = df_temp.sample()
    color = '#aaabb1'
    if(random_post['airline_sentiment'].values[0] == 'positive'):
        color = '#61fa94'
    elif(random_post['airline_sentiment'].values[0] == 'negative'):
        color = '#fa6161'
    childrens.append(html.P(children=[html.Strong('Random post : '), html.Span(str(random_post['text'].values[0])), html.Span(' --> ' + str(random_post['airline_sentiment'].values[0]), style={'color': color})]))
    # number of users
    childrens.append(html.P(children=[html.Strong('Number of users : '), html.Span(str(len(df_temp['name'].unique())))]))
    # top 5 users
    # table = dbc.Table.from_dataframe(df_temp['name'].value_counts().head(30).reset_index(), striped=True, bordered=True, hover=True, style={'maxHeight': '300px', 'overflowY': 'auto'})
    table = html.Div(
        dbc.Table.from_dataframe(df_temp['name'].value_counts().head(30).reset_index(), striped=True, bordered=True, hover=True),
        className='table-wrapper'
    )
    childrens.append(html.P(children=[html.Strong('Top 30 users : ')]))
    childrens.append(table)
    # foreign characters count and 1 exemple
    foreigns = df_temp[(df_temp['text'].str.contains(r'[\u4e00-\u9FFF]', regex=True))]
    childrens.append(html.P(children=[html.Strong('Number of posts with foreign characters : '), html.Span(str(len(foreigns)))]))
    try:
        childrens.append(html.P(children=[html.Strong('Random foreign post : '), html.Span(str(foreigns.sample()['text'].values[0]))]))
    except:
        childrens.append(html.P(children=[html.Strong('Random foreign post : '), html.Span('No foreign post found')]))
    # wordcloud
    childrens.append(html.Br())
    childrens.append(html.H3(children='Wordcloud'))
    childrens.append(html.Div(children='''L\'image ci-dessous est un Wordcloud. Il permet de visualiser les mots les plus utilisés dans les posts. 
    Plus un mot est gros, plus il est utilisé. Cela permet de pouvoir détecter des "trends" dans les posts.'''))
    childrens.append(html.Br())
    childrens.append(html.Img(src='assets/wordclouds/'+company + '.png'))
    childrens.append(html.Hr())
    return childrens



# Créer le layout du menu
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Accueil", href="..")),
        dbc.NavItem(dbc.NavLink("Time graphs", href="time")),
        dbc.NavItem(dbc.NavLink("Pie charts", href="pie_chart")),
        dbc.NavItem(dbc.NavLink("Sankey", href="sankey")),
        dbc.NavItem(dbc.NavLink("Stats", href="stats")),
    ],
    brand="Airline Sentiment Analysis",
    brand_href="..",
    color="primary",
    dark=True,
)

options_df = ['reddit', 'tweets']
df = pd.read_csv('datasets/reddit.csv')

options = sorted(df['airline'].unique())
options = np.append('All', options)
# Créer le layout de la page d'accueil
layout = html.Div(children=[
    navbar,  # Ajouter le menu à la page
    html.Div(children=[
        html.H1(children='Stats'),
        html.Div(children='''
            Cette page contient différentes statistiques concernant les données et les compagnies aériennes. On 
            a une vue d'ensemble ainsi que quelques samples de données. On y retrouve le nombre de posts, le nombre 
            d'utilisateur, s'il y a des caractères étrangers, etc. On y retrouve aussi un wordcloud pour chaque 
            compagnie aérienne qui permet de voir les mots les plus fréquents.
        '''),
        html.Br(),
        html.H3(children='Choix du dataset'),
        dcc.Dropdown(options=options_df, id='dropdown-df', value=options_df[0], clearable=False, style={'width': '50%'}),
        html.Hr(),
        html.H3(children='Statistiques'),
        html.Div(children='Choix de la compagnie aérienne'),
        dcc.Dropdown(options=options, id='dropdown-company', value=options[0], clearable=False, style={'width': '50%'}),
        html.Br(),
        html.Div(id='stats-plot'),
        html.Div(id='dataset4', style={'display':'none'})
    ])
])