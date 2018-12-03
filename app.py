
# coding: utf-8

# In[37]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv("nama_10_gdp_1_Data.csv")
mask = df['GEO'].str.contains("^Euro")==False
df = df[mask]
mask2 = df['UNIT'].str.contains("Current prices, million euro")
df = df[mask2]


available_indicators = df['NA_ITEM'].unique()
available_countries = df['GEO'].unique()



app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='xaxis-type1',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],

        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Exports of goods and services'
            ),
            dcc.RadioItems(
                id='yaxis-type1',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),


    dcc.Graph(id='indicator-graphic1'),

    dcc.Slider(
        id='year--slider1',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df["TIME"].unique()}
    ),

    html.Div([
    ], 
        style = {'margin': '50px 10px 20px 10px', 'background-color': 'black', 'height': '2px'}
    ),
    
    html.Div([
    ], 
        style = {'margin': '50px 10px 20px 10px', 'background-color': 'weight', 'height': '10px'}
    ),

#TASK 2
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='country2',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Denmark'
            ),
            
        ],
            #style 48% of page width occupied
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Exports of goods and services'
            ),
            
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),


    dcc.Graph(id='indicator-graphic2'),

    
])



#Function 1
@app.callback(
    dash.dependencies.Output('indicator-graphic1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('xaxis-type1', 'value'),
     dash.dependencies.Input('yaxis-type1', 'value'),
     dash.dependencies.Input('year--slider1', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    # return a dictionariy with two keys 
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                #xaxid type linea or log based on input type
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }



@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('country2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])

def update_graph(country_name, yaxis_column_name):
    #dff = df[df['TIME'] == year_value]
    
    # return a dictionariy with two keys 
    return {
        'data': [go.Scatter(
            x = df[(df['GEO'] == country_name) & (df['NA_ITEM'] == yaxis_column_name)]['TIME'].values,
            y = df[(df['GEO'] == country_name) & (df['NA_ITEM'] == yaxis_column_name)]['Value'].values,
            mode='lines',
        )],
        'layout': go.Layout(
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }




if __name__ == '__main__':
    app.run_server()

