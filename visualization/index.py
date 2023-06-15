# Import necessary libraries 
from dash import html, dcc
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app

# Connect to your app pages
from pages import home, time, pie_chart, sankey, stats


# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False), 
    html.Div(id='page-content', children=[]), 
])

# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home.layout
    if pathname == '/time':
        return time.layout
    if pathname == '/pie_chart':
        return pie_chart.layout
    if pathname == '/sankey':
        return sankey.layout
    if pathname == '/stats':
        return stats.layout
    else: # if redirected to unknown link
        return "404 Page Error! Please choose a link"

# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True)