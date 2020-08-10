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


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

#fig = px.bar(df[df['Country'].isin(['Argentina','Uruguay', 'Peru', 'Chile', 'Paraguay'])], x="Country", y="TotalConfirmed", color="Country", barmode="group")

top10 = df_countries_total.sort_values(by=['Confirmed'],ascending = False).head(10)
fig = px.bar(top10, x=top10.index, y=['Confirmed','Deaths','Recovered'])
#fig = px.bar(top10, x=top10.Country, y='TotalConfirmed', labels={'x':'Country'},
#             color="TotalConfirmed", color_continuous_scale=px.colors.sequential.Brwnyl)


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
    html.Footer(children = '© 2020 Powered by Alejandro Anachuri')
])


@app.callback(
    Output('country_graph', 'figure'),
    [Input('country_dr', 'value')])
def update_country_graph(country):
    if country == None: return None
    print(country)
    df_country = df_countries[(df_countries['Country'] == country) & (df_countries['Confirmed']>0)]

    line_data = df_country.melt(id_vars='Date', 
                 value_vars=['Confirmed', 
                             'Recovered', 
                             'Deaths'], 
                 var_name='Ratio', 
                 value_name='Value')

    figure = px.line(line_data, x="Date", y="Value", line_shape="spline",color='Ratio', 
              title=f'Casos confirmados, casos recuperados y muertes a lo largo del tiempo para {country}')
    return figure

@server.route('/hello')
def hello():
    return 'Hello, World!'

'''@app.route('/')
def hello_world():
    return 'Hello World!'''