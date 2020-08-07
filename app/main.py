"""import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import json
import requests


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

#data_codiv = requests.get('https://api.covid19api.com/summary')
#df = pd.DataFrame(data_codiv.json()['Countries'])


fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
#fig = px.bar(df[df['Country'].isin(['Argentina','Brazil', 'Chile'])], x="Country", y="TotalDeaths", color="Country", barmode="group")

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

if __name__ == '__main__':
    app.run_server(debug=True)"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import json
import requests

#app = Flask(__name__)
data_codiv = requests.get('https://api.covid19api.com/summary')
df = pd.DataFrame(data_codiv.json()['Countries'])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

'''df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})'''
fig = px.bar(df[df['Country'].isin(['Argentina','Uruguay', 'Peru', 'Chile', 'Paraguay'])], x="Country", y="TotalConfirmed", color="Country", barmode="group")

#fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

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

if __name__ == '__main__':
    app.run_server(debug=True)    