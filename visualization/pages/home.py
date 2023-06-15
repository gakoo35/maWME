import dash
from dash import html
from dash import dcc
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

# Créer un graphique simple
trace = go.Scatter(x=[1, 2, 3], y=[4, 5, 6])
data = [trace]
layout = go.Layout(title='Mon premier graphique avec Dash Plotly')
fig = go.Figure(data=data, layout=layout)

# Créer le layout du menu
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Accueil", href="")),
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


# Créer le layout de la page d'accueil
layout = html.Div(children=[
    navbar,  # Ajouter le menu à la page
    html.Div(children=[
        html.H1(children='Bienvenue'),
        html.Div(children='''
            Ce site contient différents graphiques réalisés avec Dash Plotly dans le but de 
            faire une analyse de sentiment sur des compagnies aériennes. 
        '''),
        html.Br(),
        html.Div(children='Voici les différents grahpiques et pages disponibles : '),
        html.Div(children=[html.Li('Time graphs : graphiques concernant les émotions en fonction du temps'), 
                           html.Li('Pie charts : graphiques camemberts pour représenté les proportions des sentiments'), 
                           html.Li('Sankey : graphiques en arbre pour représenter les sentiments en fonction des compagnies aériennes'),
                           html.Li('Stats : statistiques sur les données')]),
        html.Img(src='assets/home.jpg', ),

        # Afficher le graphique
        #dcc.Graph(
        #    id='example-graph',
        #    figure=fig
        #)
    ])
])