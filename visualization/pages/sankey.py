import dash
from dash import html, Input, Output
from dash import dcc
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

# import app
from app import app

dash.register_page(__name__, path='/sankey')

@app.callback(
Output('dataset3', 'children'),
Input('dropdown-df', 'value'),
)
def update_df(path):
    global df
    df = pd.read_csv('datasets/'+path+'.csv')
    return 0

# https://plotly.com/python/sankey-diagram/
# https://www.python-graph-gallery.com/sankey-diagram-with-python-and-plotly



@app.callback(
Output('sankey-graph', 'figure'),
Input('dataset3', 'children')
)
def sankey_graph(callback_df):
    global df
    #df = pd.read_csv('datasets/tweets_formatted.csv')
    df_temp = df.copy()

    #united : 	1
    #american : 	2
    #south		3
    #delta : 	4

    #0 -> 1 : count posts united
    #0 -> 2 : count posts american
    #0 -> 3 : count posts south
    #0 -> 4 : count posts delta

    #1 -> 5 : count united neutral
    #1 -> 6 : count united positive
    #1 -> 7 : count united negative

    #2 -> 8 : count american neutral
    #2 -> 9 : count american positive
    #2 -> 10 : count american negative

    #3 -> 11 : count south neutral
    #3 -> 12 : count south positive
    #3 -> 13 : count south negative

    #4 -> 14 : count delta neutral
    #4 -> 15 : count delta positive
    #4 -> 16 : count delta negative

    source = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    target = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ,11, 12, 13, 14, 15, 16]
    value = [df_temp['airline'].value_counts()[0], df_temp['airline'].value_counts()[1], df_temp['airline'].value_counts()[2], df_temp['airline'].value_counts()[3], 
            df_temp[df_temp['airline'] == 'United']['airline_sentiment'].value_counts()[sorted(df['airline_sentiment'].unique())][1], 
            df_temp[df_temp['airline'] == 'United']['airline_sentiment'].value_counts()[sorted(df['airline_sentiment'].unique())][2], df_temp[df_temp['airline'] == 'United']['airline_sentiment'].value_counts()[sorted(df['airline_sentiment'].unique())][0], 
            df_temp[df_temp['airline'] == 'American']['airline_sentiment'].value_counts()[sorted(df['airline_sentiment'].unique())][1],
            df_temp[df_temp['airline'] == 'American']['airline_sentiment'].value_counts()[sorted(df['airline_sentiment'].unique())][2], df_temp[df_temp['airline'] == 'American']['airline_sentiment'].value_counts()[sorted(df['airline_sentiment'].unique())][0],
            df_temp[df_temp['airline'] == 'Southwest']['airline_sentiment'].value_counts()[sorted(df['airline_sentiment'].unique())][1],
            df_temp[df_temp['airline'] == 'Southwest']['airline_sentiment'].value_counts()[sorted(df['airline_sentiment'].unique())][2], df_temp[df_temp['airline'] == 'Southwest']['airline_sentiment'].value_counts()[sorted(df['airline_sentiment'].unique())][0],
            df_temp[df_temp['airline'] == 'Delta']['airline_sentiment'].value_counts()[sorted(df['airline_sentiment'].unique())][1],
            df_temp[df_temp['airline'] == 'Delta']['airline_sentiment'].value_counts()[sorted(df['airline_sentiment'].unique())][2], df_temp[df_temp['airline'] == 'Delta']['airline_sentiment'].value_counts()[sorted(df['airline_sentiment'].unique())][0]]
    label_nodes = ['Posts', 'United', 'American', 'South', 'Delta', 'Neutral', 'Positive', 'Negative', 'Neutral', 'Positive', 'Negative', 'Neutral', 'Positive', 'Negative', 'Neutral', 'Positive', 'Negative']
    colors_nodes = ['#616bfa',
              '#616bfa', '#616bfa', '#616bfa', '#616bfa', '#aaabb1', '#61fa94', '#fa6161', '#aaabb1', '#61fa94', '#fa6161',
              '#aaabb1', '#61fa94', '#fa6161', '#aaabb1', '#61fa94', '#fa6161', '#aaabb1', '#61fa94', '#fa6161']
    label_links = ['United', 'American', 'South', 'Delta', 'Neutral', 'Positive', 'Negative', 'Neutral', 'Positive', 'Negative', 'Neutral', 'Positive', 'Negative', 'Neutral', 'Positive', 'Negative']
    colors_links = ['rgb(97, 107, 250, 0.05)', 'rgb(97, 107, 250, 0.05)', 'rgb(97, 107, 250, 0.05)', 'rgb(97, 107, 250, 0.05)', 'rgb(170, 171, 177, 0.05)', 'rgb(97, 250, 148, 0.05)', 'rgb(250, 97, 97, 0.05)', 'rgb(170, 171, 177, 0.05)', 'rgb(97, 250, 148, 0.05)', 'rgb(250, 97, 97, 0.05)',
              'rgb(170, 171, 177, 0.05)', 'rgb(97, 250, 148, 0.05)', 'rgb(250, 97, 97, 0.05)', 'rgb(170, 171, 177, 0.05)', 'rgb(97, 250, 148, 0.05)', 'rgb(250, 97, 97, 0.05)']


    # blue : 616bfa
    # grey : aaabb1
    # purple : b361fa
    # green : 61fa94
    # red : fa6161
    # yellow : faed61
    # pink : fa61db
    # orange : faa361
    # cyan : 61e6fa
    
    fig = go.Figure(data=[go.Sankey(
        valueformat = ".0f",
        valuesuffix = " posts",
        # Define nodes
        node = dict(
        pad = 15,
        thickness = 15,
        line = dict(color = "black", width = 0.5),
        label =  label_nodes,
        color =  colors_nodes
        ),
        # Add links
        link = dict(
        source =  source,
        target =  target,
        value =  value,
        label =  label_links,
        color =  colors_links
    ))])
    
    #link = dict(source = source, target = target, value = value, label = label, color = colors)
    #data = go.Sankey(link = link)
    #fig = go.Figure(data)

    return fig



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

# Créer le layout de la page d'accueil
layout = html.Div(children=[
    navbar,  # Ajouter le menu à la page
    html.Div(children=[
        html.H1(children='Sankey'),
        html.Div(children='''
            Cette page contient un diagramme Sankey. Ce type de graphique représente les proportions ainsi que les 
            différentes catégories et liens des données. Cela permet de voir comment les données sont distribué entre les 
            différentes compagnies ainsi que les sentiments. C'est utile pour voir les différences entre les compagnies.
        '''),
        html.Br(),
        html.H3(children='Choix du dataset'),
        dcc.Dropdown(options=options_df, id='dropdown-df', value=options_df[0], clearable=False, style={'width': '50%'}),
        html.Hr(),

        dcc.Graph(id='sankey-graph'),
        html.Div(id='dataset3', style={'display':'none'})
    ])
])