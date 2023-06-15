import dash
from dash import html
from dash import dcc
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash import html, Input, Output

from app import app

dash.register_page(__name__, path='/pie_chart')


@app.callback(
Output('dataset2', 'children'),
Input('dropdown-df', 'value'),
)
def update_df(path):
    global df
    df = pd.read_csv('datasets/'+path+'.csv')
    return 0


# get percentage of each sentiment for each airline (positive, negative, neutral)
def get_percentage(df):
    df['percentage'] = df['counts'] / df['counts'].sum() * 100
    return df

# create graphic for each company
@app.callback(
Output('pie-charts', 'children'),
Input('dataset2', 'children')
)
def create_pie_charts(callback_df):
    global df
    #df = pd.read_csv('datasets/tweets_formatted.csv')
    graphs = []
    for airline in ['All', 'United', 'Southwest', 'Delta', 'American']:
        df_temp = df.copy()
        if airline != 'All':
            df_temp = df_temp.drop(df[df['airline'] != airline].index)

        # count number of tweets for class 0, 1, -1 for each airline and get percentage
        df_temp = df_temp.groupby(['airline_sentiment']).size().reset_index(name='counts')

        # create a pie chart (x=airline_sentiment, y=percentage)
        pie_graph = go.Pie(labels=df_temp['airline_sentiment'], values=df_temp['counts'], hole=.2)
        data_pie = [pie_graph]
        layout_pie = go.Layout(title='Pie chart ' + airline)
        fig_pie = go.Figure(data=data_pie, layout=layout_pie)

        # update layout
        # change color of each class (-1 = red, 0 = grey, 1 = green)
        fig_pie.update_traces(marker=dict(colors=['fe6d73', 'ffcb77', '17c3b2']))
        fig_pie.update_layout(
            title={
                'text': "Répartition des classes " + airline,
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
        ))

        graphs.append(dcc.Graph(
                        id='pie_chart-'+airline,
                        figure=fig_pie
                    ))
    return graphs

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

#graphs = create_pie_charts()

options_df = ['reddit', 'tweets']
df = pd.read_csv('datasets/reddit.csv')


# Créer le layout de la page d'accueil
layout = html.Div(children=[
    navbar,  # Ajouter le menu à la page
    html.Div(children=[
        html.H1(children='Pie charts'),
        html.Div(children='''
            Cette page comporte des graphiques de type pie chart pour représenter les proportions des sentiments pour chaque 
            compagnie aérienne.
        '''),
        html.Br(),
        html.H3(children='Choix du dataset'),
        dcc.Dropdown(options=options_df, id='dropdown-df', value=options_df[0], clearable=False, style={'width': '50%'}),
        html.Hr(),
        html.Div(id='pie-charts'),
        html.Div(id='dataset2', style={'display':'none'})
        
    ])
])