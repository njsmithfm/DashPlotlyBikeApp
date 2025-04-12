from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.io as pio
from datetime import datetime, timedelta

# Set default template
pio.templates.default = "plotly_dark"
app = Dash(__name__, 
                external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP],
                meta_tags=[{'name': 'viewport', 
                          'content': 'width=device-width, initial-scale=1.0'}]
               )
initial_days=7
df = pd.read_json('https://data.cityofnewyork.us/resource/h9gi-nx95.json?$query=SELECT%0A%20%20%60crash_date%60%2C%0A%20%20%60crash_time%60%2C%0A%20%20%60borough%60%2C%0A%20%20%60zip_code%60%2C%0A%20%20%60latitude%60%2C%0A%20%20%60longitude%60%2C%0A%20%20%60location%60%2C%0A%20%20%60on_street_name%60%2C%0A%20%20%60off_street_name%60%2C%0A%20%20%60cross_street_name%60%2C%0A%20%20%60number_of_persons_injured%60%2C%0A%20%20%60number_of_persons_killed%60%2C%0A%20%20%60number_of_pedestrians_injured%60%2C%0A%20%20%60number_of_pedestrians_killed%60%2C%0A%20%20%60number_of_cyclist_injured%60%2C%0A%20%20%60number_of_cyclist_killed%60%2C%0A%20%20%60number_of_motorist_injured%60%2C%0A%20%20%60number_of_motorist_killed%60%2C%0A%20%20%60contributing_factor_vehicle_1%60%2C%0A%20%20%60contributing_factor_vehicle_2%60%2C%0A%20%20%60contributing_factor_vehicle_3%60%2C%0A%20%20%60contributing_factor_vehicle_4%60%2C%0A%20%20%60contributing_factor_vehicle_5%60%2C%0A%20%20%60collision_id%60%2C%0A%20%20%60vehicle_type_code1%60%2C%0A%20%20%60vehicle_type_code2%60%2C%0A%20%20%60vehicle_type_code_3%60%2C%0A%20%20%60vehicle_type_code_4%60%2C%0A%20%20%60vehicle_type_code_5%60%0AWHERE%20%60number_of_cyclist_injured%60%20%3E%200%0AORDER%20BY%20%60crash_date%60%20DESC%20NULL%20LAST')

df['crash_date'] = pd.to_datetime(df['crash_date'])
boroughs = ['MANHATTAN', 'BROOKLYN', 'QUEENS', 'BRONX', 'STATEN ISLAND']
color_sequence = px.colors.qualitative.Vivid

# Create borough summary data for bar chart
borough_crashSums = df.groupby('borough')['number_of_cyclist_injured'].sum().reset_index()


def create_map_fig(df, days):  
        map_fig = px.density_map(df, lat='latitude', lon='longitude', z='number_of_cyclist_injured', radius=10,
                                 labels={'number_of_cyclist_injured': 'Cyclists Injured'},
                                center=dict(lat = 40.7128, lon = -73.9560), zoom = 10,
                                map_style = "open-street-map",
                                title = f'Cyclist Injury Locations (Last {days} Days)')
        return map_fig

def create_bar_fig(df, days):   
        bar_fig = px.bar(borough_crashSums, x = 'number_of_cyclist_injured', y='borough',
                    title=f'Total Cyclist Injuries by Borough (Last {days} Days)',
                    orientation='h',
                    labels={'borough': 'Borough', 'number_of_cyclist_injured': 'Total Cyclist Injuries'},
                    color='borough',)
        return bar_fig


def create_line_fig(df, days):
        line_fig = px.line(df, x='crash_date', y='number_of_cyclist_injured', color='borough',
                                title=f'Cyclist Injuries by Borough (Last {days} Days)',
                                 labels={'crash_date': 'Date', 'number_of_cyclist_injured': 'Cyclist Injuries'},)
        return line_fig

# def create_counter_fig(df, days):
#       counter_fig = 

#       return counter_fig

bar_fig = create_bar_fig(df, initial_days)
map_fig=create_map_fig(df, initial_days)
line_fig = create_line_fig(df, initial_days)
# counter_fig = create_counter_fig(df, initial_days)



app.layout = html.Div([
    dbc.Container([
        html.H1('Where In NYC Are Cyclists Getting Injured?', className='text-center my-4'),
        
        html.P("This map shows geospatial data of traffic collisions in NYC in which at least one cyclist was injured. Use the dropdown to select a time range from today's date. The thermal map shows densities, to suggest areas that are comparatively more dangerous for cyclists. Vehicle data and a primary contributing factor are provided where available."),

        dbc.Row([
            dbc.Col([
                html.Label("Select Timeframe", className="fw-bold me-2"),
                dcc.Dropdown(
                    id='timeframe-dropdown',
                    options=[
                        {'label': 'Previous 7 Days', 'value': 7},
                        {'label': 'Previous 2 Weeks', 'value': 14},
                        {'label': 'Previous 30 Days', 'value': 30},
                        {'label': 'Previous 6 Months', 'value': 180},
                        {'label': 'Previous Year', 'value': 365}
                    ],
                    value=7,
                    clearable=False,
                    style={'backgroundColor': '#fcfcfc', 'color': 'black'}
                )
            ], xs=12, sm=12, md=6, lg=4, xl=3, className="mb-4")
        ], justify="left"),
        

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='map', figure=map_fig, responsive=True,
                    style={'height': '65vh'})
            ], className="mb-4")
        ]),
         dbc.Row([
                dbc.Col([
            dcc.Graph(id='line-chart', figure=line_fig, responsive=True,
                style={'height': '50vh'})
        ], width=12, className="mb-4"),
        ]),
        dbc.Row([
             dbc.Col([
                dbc.Card([ 
                   dbc.CardBody([
                        html.H5("Counter Card", className="card-title", id='counter-card',
                            # figure=counter_fig,
                            )]),
                        html.P("This is some card content that we'll reuse", className="card-text",             
            )], className="bg-dark text-white")
        ],  width=6, className="mb-4"
    ),
            dbc.Col([
                dcc.Graph(id='bar-chart', figure=bar_fig, responsive=True, 
                    style={'height': '50vh'})
            ], width=6, className="mb-4")
        ]),
        ]),
        ])

@app.callback(
    Output('map', 'figure'),
    Input('timeframe-dropdown','value')
)
def update_map_time(number_of_days):
    updated_map_chart = create_map_fig(df=df, days=number_of_days)
    return updated_map_chart

@app.callback(
    Output('line-chart', 'figure'),
    Input('timeframe-dropdown','value')
)
def update_line_time(number_of_days):
    updated_line_chart= create_line_fig(df=df, days=number_of_days)
    return updated_line_chart


@app.callback(
    Output('bar-chart', 'figure'),
    Input('timeframe-dropdown','value')
)
def update_bar_time(number_of_days):
    updated_bar_chart = create_bar_fig(df=df, days=number_of_days)
    return updated_bar_chart

# @app.callback(
#       Output('counter-card', 'figure'),
#       Input('timeframe-dropdown', 'value')
# )
# def update_counter_card(number_of_days):
#     updated_counter_card = create_counter_fig(df=df, days=number_of_days)
#     return updated_counter_card



if __name__ == '__main__':
    app.run(debug=True)