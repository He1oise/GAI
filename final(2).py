import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_auth
#import json
import numpy as np

df=pd.read_csv('C:/Users/yzhhu/Desktop/ploty/ipynb/final.csv')
df.sort_values(by=['year'],ascending=False,inplace=True)
app=dash.Dash()

USERNAME_PASSWORD_PAIRS=[['stanley','yuan']]
auth=dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server = app.server
features=df.columns
graphoptions=["equirectangular" ,"mercator" , "orthographic" , "natural earth" ,
              "kavrayskiy7" ,"miller" , "robinson" , "eckert4" , "azimuthal equal area" ,
              "azimuthal equidistant" , "conic equal area" ,"conic conformal" , "conic equidistant" ,"gnomonic" ,
              "stereographic" , "mollweide" , "hammer" , "transverse mercator" ,"albers usa" ,"winkel tripel" , "aitoff" , "sinusoidal" ]
#colors=['Greys','YlGnBu','Greens','YlOrRd','Bluered','RdBu','Reds','Blues','Jet','Hot','Blackbody']
year_options=[]
for year in df['year'].unique():
    year_options.append({'label':str(year),'value':year})

app.layout = html.Div([

    html.Div([
        dcc.Dropdown(id='year_pick',options= year_options, value= 2016),
    ],style={'width':"48%",'display':'inline-block'}),
    html.Div([
        dcc.Dropdown(id='feature_pick',options= [{'label':i,'value':i}for i in features], value= features[0]),
    ],style={'width':"48%",'display':'inline-block'}),
    html.Div([
        dcc.Dropdown(id='choose_plot',options=[{'label':i,'value':i}for i in graphoptions],value=graphoptions[2])
    ]),
    #html.Div([
            #dcc.Dropdown(id='pallet',options=[{'label':i,'value':i}for i in graphoptions],value=graphoptions[0])
    #]),

    
    #html.Div([
    #html.Pre(id='hover-data', style={'paddingTop':35})
    #], style={'width':'30%'}),

    html.Div([dcc.Graph(id='graph')],style={'width':'60%', 'float':'left'}),
   
    html.Div([dcc.Graph(id='scatterplot')],style={'width':'30%', 'float':'right'})
  

],style={'padding':10})

@app.callback(Output('graph', 'figure'),
              [Input('year_pick', 'value'),
               Input('feature_pick','value'),
               Input('choose_plot','value'),
               #Input('palette','value')
               ]

              )
def updata_figure (selected_year,selected_feature,selected_graph):
    filter_df= df[df['year']==selected_year]

    data = dict(
        type='choropleth',

        locations=filter_df['country'],
        locationmode='country names',
        z=filter_df[selected_feature],
        text=filter_df['country'],

        #colorscale='Portland',


        marker=go.choropleth.Marker(
            line=go.choropleth.marker.Line(
                color='rgb(180,180,180)',
                width=0.5
            )),
        colorscale=[
        [0, "rgb(228, 231, 237)"],
    [0.01,"rgb(255,255,255)"],
        [0.25, "rgb(131, 157, 199)"],
        [0.55, "rgb(104, 128, 166)"],
        [0.75, "rgb(82,102,133)"],
        [1, "rgb(63, 62, 92 )"]
    ],
     reversescale=False,
        colorbar={"thickness": 10, "len": 0.7, "x": 0.9, "y": 0.7,
                  'title': {"side": "bottom","size":1}}
        #colorbar={'title': {'text':'{}'.format(selected_feature),'font':'Open Sans','side':'top',"size":1}},
    )
    layout = dict(
        width= 900,
        height=600,
        title='World bank data for {}'.format(selected_feature),
        geo=dict(

            projection={'type': selected_graph
                        }
        )
    )
    return {'data':[data],"layout":layout}
'''
@app.callback(
    Output('hover-data', 'children'),
    [Input('graph', 'hoverData')])
def callback_image(hoverData):
    return json.dumps(hoverData, indent=2)
'''

@app.callback(
    Output('scatterplot', 'figure'),
    [Input('graph', 'hoverData'),
    Input('feature_pick','value')])
def callback_image(hoverData,selected_feature):
    
    country=hoverData['points'][0]['location']
    
    trace1 = go.Scatter(
    x = df[df['country']==country]['year'],
    y = df[df['country']==country][selected_feature],
    mode = 'lines+markers',
    name = 'lines+markers'
    )
    layout= go.Layout(
    title= 'line plot for {}'.format(country),
    hovermode= 'closest',
    xaxis= dict(
        title= 'year',
        ticklen= 5,
        zeroline= False,
        gridwidth= 2,
    ),
    yaxis=dict(
        title= '{}'.format(selected_feature) ,
        ticklen= 5,
        gridwidth= 2,
    ),
    showlegend= False
)
    return {'data':[trace1],'layout':layout}


if __name__ == '__main__':
    app.run_server()
