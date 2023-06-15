#import dash
#from dash import html
#from dash import dcc
#import plotly.graph_objs as go
#import dash_bootstrap_components as dbc3
#
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
#
## Créer un graphique simple
#trace = go.Scatter(x=[1, 2, 3], y=[4, 5, 6])
#data = [trace]
#layout = go.Layout(title='Mon premier graphique avec Dash Plotly')
#fig = go.Figure(data=data, layout=layout)
#
## Créer le layout du menu
#navbar = dbc.NavbarSimple(
#    children=[
#        dbc.NavItem(dbc.NavLink("Accueil", href="#")),
#        dbc.NavItem(dbc.NavLink("Page 1", href="time")),
#        dbc.NavItem(dbc.NavLink("Page 2", href="#")),
#    ],
#    brand="Mon site web",
#    brand_href="#",
#    color="primary",
#    dark=True,
#)
#
#
## Créer le layout de la page d'accueil
#app.layout = html.Div(children=[
#    navbar,  # Ajouter le menu à la page
#    html.Div(children=[
#        html.H1(children='Bienvenue sur mon site web'),
#        html.Div(children='''
#            Ceci est une page d'accueil basique pour mon site web Dash Plotly.
#        '''),
#
#        # Afficher le graphique
#        dcc.Graph(
#            id='example-graph',
#            figure=fig
#        )
#    ])
#])
#
#if __name__ == '__main__':
#    app.run_server(debug=True)
#




import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True)