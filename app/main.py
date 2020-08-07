import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import json
import requests

data_codiv = requests.get('https://api.covid19api.com/summary')
df = pd.DataFrame(data_codiv.json()['Countries'])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

fig = px.bar(df[df['Country'].isin(['Argentina','Uruguay', 'Peru', 'Chile', 'Paraguay'])], x="Country", y="TotalConfirmed", color="Country", barmode="group")


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])


'''@app.route('/')
def hello_world():
    return 'Hello World!'''