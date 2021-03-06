import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import json
import requests

#data_codiv = requests.get('https://api.covid19api.com/summary')
#df = pd.DataFrame(data_codiv.json()['Countries'])
df_countries = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',parse_dates=True)
df_countries_total = df_countries.groupby('Country').max()

df_countries['Confirmed_daily'] = df_countries.groupby('Country')['Confirmed'].diff()
df_countries['Recovered_daily'] = df_countries.groupby('Country')['Recovered'].diff()
df_countries['Deaths_daily'] = df_countries.groupby('Country')['Deaths'].diff()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

#fig = px.bar(df[df['Country'].isin(['Argentina','Uruguay', 'Peru', 'Chile', 'Paraguay'])], x="Country", y="TotalConfirmed", color="Country", barmode="group")

top10 = df_countries_total.sort_values(by=['Confirmed'],ascending = False).head(10)
fig = px.bar(top10, x=top10.index, y=['Confirmed','Deaths','Recovered'])



app.layout = html.Div(children=[
    html.H1(children='Covid 2019 en Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    html.Div([
            dcc.Dropdown(
                id='country_dr',
                options=[{'label': i, 'value': i} for i in df_countries.Country.unique()],
                placeholder="Elija un pais",
                value='Argentina'

            )
        ],
        style={'width': '48%', 'display': 'inline-block'}
    ),
    dcc.Graph(id='country_graph'),
    dcc.Graph(id='country_daily_graph'),

    html.Footer(children = '© 2020 Powered by Alejandro Anachuri')
])


@app.callback(
    [Output('country_graph', 'figure'),
     Output('country_daily_graph', 'figure')],
    [Input('country_dr', 'value')])
def update_country_graph(country):
    if country == None: return None
    df_country = df_countries[(df_countries['Country'] == country) & (df_countries['Confirmed']>0)]

    line_data = df_country.melt(id_vars='Date', 
                 value_vars=['Confirmed', 
                             'Recovered', 
                             'Deaths'], 
                 var_name='Ratio', 
                 value_name='Value')

    totalfig = px.line(line_data, x="Date", y="Value", line_shape="spline",color='Ratio', 
              title=f'Casos confirmados, casos recuperados y muertes a lo largo del tiempo para {country}')

    line_daily_data = df_country.melt(id_vars='Date', 
                 value_vars=['Confirmed_daily', 
                             'Deaths_daily',
                             'Recovered_daily'], 
                 var_name='Ratio', 
                 value_name='Value')

    dailyfig = px.line(line_daily_data, x="Date", y="Value", line_shape="spline",color='Ratio', 
              title=f'Casos confirmados, casos recuperados y muertes por dia en {country}')

    return totalfig, dailyfig

@server.route('/hello')
def hello():
    return 'Hello, World!'

'''@app.route('/')
def hello_world():
    return 'Hello World!'''