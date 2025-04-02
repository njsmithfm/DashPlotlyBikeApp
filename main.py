from dash import Dash, dcc, html
import plotly.express as px
import requests
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.io as pio

pio.templates.default = "plotly_dark"

# Initialize Dash app with Bootstrap
crashApp = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

df = pd.read_json('https://data.cityofnewyork.us/resource/h9gi-nx95.json?$query=SELECT%0A%20%20%60crash_date%60%2C%0A%20%20%60crash_time%60%2C%0A%20%20%60borough%60%2C%0A%20%20%60zip_code%60%2C%0A%20%20%60latitude%60%2C%0A%20%20%60longitude%60%2C%0A%20%20%60location%60%2C%0A%20%20%60on_street_name%60%2C%0A%20%20%60off_street_name%60%2C%0A%20%20%60cross_street_name%60%2C%0A%20%20%60number_of_persons_injured%60%2C%0A%20%20%60number_of_persons_killed%60%2C%0A%20%20%60number_of_pedestrians_injured%60%2C%0A%20%20%60number_of_pedestrians_killed%60%2C%0A%20%20%60number_of_cyclist_injured%60%2C%0A%20%20%60number_of_cyclist_killed%60%2C%0A%20%20%60number_of_motorist_injured%60%2C%0A%20%20%60number_of_motorist_killed%60%2C%0A%20%20%60contributing_factor_vehicle_1%60%2C%0A%20%20%60contributing_factor_vehicle_2%60%2C%0A%20%20%60contributing_factor_vehicle_3%60%2C%0A%20%20%60contributing_factor_vehicle_4%60%2C%0A%20%20%60contributing_factor_vehicle_5%60%2C%0A%20%20%60collision_id%60%2C%0A%20%20%60vehicle_type_code1%60%2C%0A%20%20%60vehicle_type_code2%60%2C%0A%20%20%60vehicle_type_code_3%60%2C%0A%20%20%60vehicle_type_code_4%60%2C%0A%20%20%60vehicle_type_code_5%60%0AWHERE%20%60number_of_cyclist_injured%60%20%3E%200%0AORDER%20BY%20%60crash_date%60%20DESC%20NULL%20LAST')

map_fig = px.density_map(df, lat='latitude', lon='longitude', z='number_of_cyclist_killed', radius=10,
                        center=dict(lat=40.7128, lon=-73.9560), zoom=12,
                        map_style="open-street-map",
                        title='Cyclist Injury Locations')

# Borough summary data for bar chart
borough_crashSums = df.groupby('borough')['number_of_cyclist_injured'].sum().reset_index()

bar_fig = px.bar(borough_crashSums, x='number_of_cyclist_injured', y='borough',
             title='Total Cyclist Injuries by Borough',
             orientation='h',
             labels={'borough': 'Borough', 'number_of_cyclist_injured': 'Cyclist Injuries'})

# Side by side layout using Bootstrap
crashApp.layout = html.Div([
    dbc.Container([
        html.H1('Where In NYC Are Cyclists Getting Injured?', className='text-center my-4'),
        dbc.Row([
            # Left column
            dbc.Col([
                dcc.Graph(id='map-graph', figure=map_fig)
            ], width=6),
            
            # Right column
            dbc.Col([
                dcc.Graph(id='bar-graph', figure=bar_fig)
            ], width=6)
        ])
    ], fluid=True)
])

if __name__ == '__main__':
    crashApp.run(debug=True, use_reloader=False)