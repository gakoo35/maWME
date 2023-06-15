import dash
from dash import html, Input, Output
from dash import dcc
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash.exceptions import PreventUpdate

# import app
from app import app

dash.register_page(__name__, path='/time')



@app.callback(
Output('dataset', 'children'),
Input('dropdown-df', 'value')
)
def update_df(path):
    global df
    df = pd.read_csv('datasets/'+path+'.csv')
    return 0




@app.callback(
Output('timeline-graph', 'figure'),
Input('dropdown-company', 'value'),
Input('dataset', 'children')
)
def timeline_graph(company, callback_df):
    global df
    #df = pd.read_csv('datasets/tweets_formatted.csv')
    df_temp = df.copy()
    fig_time = None
    colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA']
    company_names = sorted(df['airline'].unique())
    #company_names = df['airline'].unique()
    if(company == 'All'):
        df_temp['airline_sentiment']=df_temp['airline_sentiment'].replace(['neutral', 'positive', 'negative'], [0, 1, -1])
        df_temp.drop(['name', 'text'], axis=1, inplace=True)

        groups = df_temp.groupby(by='airline')

        data = []

        for group, dataframe in groups:
            dataframe['date'] = pd.to_datetime(dataframe['date'])
            dataframe = dataframe.set_index('date')
            dataframe = dataframe.groupby(['date']).sum()
            trace = go.Scatter(x=dataframe.index, 
                            y=dataframe['airline_sentiment'],
                            marker=dict(color=colors[len(data)]),
                            name=group)
            data.append(trace)

        layout =  go.Layout(xaxis={'title': 'Time'},
                            yaxis={'title': 'Sentiment'},
                            margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                            hovermode='closest',
                            title='')

        fig_time = go.Figure(data=data, layout=layout) 

        fig_time.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True
                ),
            type="date"
        ))
    else:
        df_temp = df_temp.drop(df[df['airline'] != company].index)

        df_temp['airline_sentiment']=df_temp['airline_sentiment'].replace(['neutral', 'positive', 'negative'], [0, 1, -1])
        df_temp.drop(['airline', 'name', 'text'], axis=1, inplace=True)
        df_temp['date'] = pd.to_datetime(df_temp['date'])
        df_temp = df_temp.set_index('date')
        df_temp = df_temp.groupby(['date']).sum()

        time_graph = go.Scatter(x=df_temp.index, y=df_temp['airline_sentiment'], fill='tozeroy', marker=dict(color=colors[np.where(np.asarray(company_names) == company)[0][0]]))
        data_time = [time_graph]
        layout_time = go.Layout(title='')
        fig_time = go.Figure(data=data_time, layout=layout_time)

        fig_time.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True
                ),
            type="date"
        )
        )
    return fig_time

@app.callback(
Output('timeline-graph2', 'figure'),
Input('dropdown-company-2', 'value'),
Input('dataset', 'children')
)
def timeline_graph2(company, callback_df):
    global df
    # df = pd.read_csv('datasets/tweets_formatted.csv')
    df_temp = df.copy()
    fig_time = None
    colors=['#aaabb1', '#61fa94', '#fa6161']
    company_names = sorted(df['airline'].unique())
    #company_names = df['airline'].unique()
    if(company == 'All'):
        #df_temp['airline_sentiment']=df_temp['airline_sentiment'].replace(['neutral', 'positive', 'negative'], [0, 1, -1])
        df_temp.drop(['name', 'text'], axis=1, inplace=True)

        data = []
        df_temp['date'] = pd.to_datetime(df_temp['date'])
        df_temp = df_temp.set_index('date')
        sentiments = ['neutral', 'positive', 'negative']
        i = 0
        for sentiment in sentiments:
            dataframe = df_temp[df_temp['airline_sentiment'] == sentiment].groupby(['date']).count()
            trace = go.Scatter(x=dataframe.index, 
                            y=dataframe['airline_sentiment'],
                            marker=dict(color=colors[i]),
                            name=sentiment)
            data.append(trace)
            i+=1

        layout =  go.Layout(xaxis={'title': 'Time'},
                            yaxis={'title': 'Sentiment'},
                            margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                            hovermode='closest',
                            title='')

        fig_time = go.Figure(data=data, layout=layout) 

        fig_time.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True
                ),
            type="date"
        ))
    else:
        df_temp = df_temp.drop(df[df['airline'] != company].index)

        #df_temp['airline_sentiment']=df_temp['airline_sentiment'].replace(['neutral', 'positive', 'negative'], [0, 1, -1])
        df_temp.drop(['airline', 'name', 'text'], axis=1, inplace=True)
        df_temp['date'] = pd.to_datetime(df_temp['date'])
        df_temp = df_temp.set_index('date')
        sentiments = ['neutral', 'positive', 'negative']
        i = 0
        data = []
        for sentiment in sentiments:
            dataframe = df_temp[df_temp['airline_sentiment'] == sentiment].groupby(['date']).count()
            trace = go.Scatter(x=dataframe.index, 
                            y=dataframe['airline_sentiment'],
                            marker=dict(color=colors[i]),
                            name=sentiment)
            data.append(trace)
            i+=1
        layout_time = go.Layout(title='')
        fig_time = go.Figure(data=data, layout=layout_time)

        fig_time.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True
                ),
            type="date"
        )
        )
    return fig_time

@app.callback(
Output('post-count-company-graph', 'figure'),
Input('dropdown-company-3', 'value'),
Input('dataset', 'children')
)
def post_count_company_graph(company, callback_df):
    global df
    #df = pd.read_csv('datasets/tweets_formatted.csv')
    df_temp = df.copy()

    colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA']
    company_names = sorted(df['airline'].unique())

    data = []

    if(company == 'All'):
        
        for company in company_names:
            df_temp = df.copy()
            df_temp = df_temp.drop(df[df['airline'] != company].index)
            df_temp['date'] = pd.to_datetime(df_temp['date'])
            df_temp = df_temp.set_index('date')
            trace = go.Histogram(x=df_temp.index, y=df_temp['airline_sentiment'], histfunc='count', name=company, texttemplate="%{y}")
            data.append(trace)

        layout =  go.Layout(xaxis={'title': 'Time'},
                            yaxis={'title': 'Posts count'},
                            margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                            hovermode='closest',
                            title='',
                            bargap=0.1)

        figure = go.Figure(data=data, layout=layout) 
        figure.update_layout(barmode='stack')
    else:
        df_temp = df_temp.drop(df[df['airline'] != company].index)
        df_temp['date'] = pd.to_datetime(df_temp['date'])
        df_temp = df_temp.set_index('date')
        trace = go.Histogram(x=df_temp.index, y=df_temp['airline_sentiment'], histfunc='count', name='Posts count', texttemplate="%{y}", marker=dict(color=colors[np.where(np.asarray(company_names) == company)[0][0]]))
        data.append(trace)

        layout =  go.Layout(xaxis={'title': 'Time'},
                            yaxis={'title': 'Posts count'},
                            margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                            hovermode='closest',
                            title='',
                            bargap=0.1)

        figure = go.Figure(data=data, layout=layout) 
    return figure


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
        html.H1(children='Time graphs'),
        html.Div(children='''
            Cette page regroupe différents graphs démontrant l'évolution des sentiments concernant des compagnies aériennes au
            fil du temps.
        '''),
        html.Br(),
        html.H3(children='Choix du dataset'),
        dcc.Dropdown(options=options_df, id='dropdown-df', value=options_df[0], clearable=False, style={'width': '50%'}),
        html.Hr(),
        html.H3(children='Accumulation des sentiments au fil du temps'),
        html.Div(children='Choix de la compagnie aérienne'),
        dcc.Dropdown(options=options, id='dropdown-company', value=options[0], clearable=False, style={'width': '50%'}),
        html.Div(children='''Ce graphique montre l\'accumulation des sentiments au fil du temps pour une compagnie aérienne donnée.
                 Les lignes que l'on peut voir représente l'addition des sentiments positifs (+1), négatifs (-1) et neutres (0) pour chaque jour.'''),
        dcc.Graph(id='timeline-graph'),
        html.Hr(),
        html.H3(children='Evolution des sentiments au fil du temps'),
        html.Div(children='Choix de la compagnie aérienne'),
        dcc.Dropdown(options=options, id='dropdown-company-2', value=options[0], clearable=False, style={'width': '50%'}),
        html.Div(children='''Ce graphique montre l'évolution des sentiments au fil du temps. On y retrouve donc le nombre de 
        posts pour les 3 sentiments (positif, négatif et neutre) pour chaque jour'''),
        html.Br(),
        dcc.Graph(id='timeline-graph2'),
        html.Hr(),
        html.H3(children='Evolution du nombre de posts au fil du temps'),
        html.Div(children='Choix de la compagnie aérienne'),
        dcc.Dropdown(options=options, id='dropdown-company-3', value=options[0], clearable=False, style={'width': '50%'}),
        html.Div(children='''Ce graphique montre le nombre de posts au fil du temps. Cela permet de voir l'évolution 
        de la popularité et de l'activité sur les réseaux sociaux de chaque compagnie aérienne.'''),
        dcc.Graph(id='post-count-company-graph'),
        html.Div(id='dataset', style={'display':'none'})
    ])
])