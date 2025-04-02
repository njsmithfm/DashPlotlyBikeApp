from dash import Dash, dcc, html
from dash_mosaic import DashMosaic
import plotly.express as px
import requests
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc




# Create a Dash app
crashApp = Dash(__name__)

# Create the layout of the app
crashApp.layout = html.Div([
    html.H1('Where In NYC Are Cyclists Getting Injured?',),
])

# OPEN STREET MAP taken from https://plotly.com/python/density-heatmaps/
df = pd.read_json('https://data.cityofnewyork.us/resource/h9gi-nx95.json?$query=SELECT%0A%20%20%60crash_date%60%2C%0A%20%20%60crash_time%60%2C%0A%20%20%60borough%60%2C%0A%20%20%60zip_code%60%2C%0A%20%20%60latitude%60%2C%0A%20%20%60longitude%60%2C%0A%20%20%60location%60%2C%0A%20%20%60on_street_name%60%2C%0A%20%20%60off_street_name%60%2C%0A%20%20%60cross_street_name%60%2C%0A%20%20%60number_of_persons_injured%60%2C%0A%20%20%60number_of_persons_killed%60%2C%0A%20%20%60number_of_pedestrians_injured%60%2C%0A%20%20%60number_of_pedestrians_killed%60%2C%0A%20%20%60number_of_cyclist_injured%60%2C%0A%20%20%60number_of_cyclist_killed%60%2C%0A%20%20%60number_of_motorist_injured%60%2C%0A%20%20%60number_of_motorist_killed%60%2C%0A%20%20%60contributing_factor_vehicle_1%60%2C%0A%20%20%60contributing_factor_vehicle_2%60%2C%0A%20%20%60contributing_factor_vehicle_3%60%2C%0A%20%20%60contributing_factor_vehicle_4%60%2C%0A%20%20%60contributing_factor_vehicle_5%60%2C%0A%20%20%60collision_id%60%2C%0A%20%20%60vehicle_type_code1%60%2C%0A%20%20%60vehicle_type_code2%60%2C%0A%20%20%60vehicle_type_code_3%60%2C%0A%20%20%60vehicle_type_code_4%60%2C%0A%20%20%60vehicle_type_code_5%60%0AWHERE%20%60number_of_cyclist_injured%60%20%3E%200%0AORDER%20BY%20%60crash_date%60%20DESC%20NULL%20LAST')

import plotly.express as px
fig = px.density_map(df, lat='latitude', lon='longitude', z='number_of_cyclist_killed', radius=10,
                        center=dict(lat=40.7128, lon=-73.9560), zoom=12,
                        map_style="open-street-map")
fig.show()


# # Function to fetch data from an API
# def crashAPI():
#     filtered_url = 'https://data.cityofnewyork.us/resource/h9gi-nx95.json?$query=SELECT%0A%20%20%60crash_date%60%2C%0A%20%20%60crash_time%60%2C%0A%20%20%60borough%60%2C%0A%20%20%60zip_code%60%2C%0A%20%20%60latitude%60%2C%0A%20%20%60longitude%60%2C%0A%20%20%60location%60%2C%0A%20%20%60on_street_name%60%2C%0A%20%20%60off_street_name%60%2C%0A%20%20%60cross_street_name%60%2C%0A%20%20%60number_of_persons_injured%60%2C%0A%20%20%60number_of_persons_killed%60%2C%0A%20%20%60number_of_pedestrians_injured%60%2C%0A%20%20%60number_of_pedestrians_killed%60%2C%0A%20%20%60number_of_cyclist_injured%60%2C%0A%20%20%60number_of_cyclist_killed%60%2C%0A%20%20%60number_of_motorist_injured%60%2C%0A%20%20%60number_of_motorist_killed%60%2C%0A%20%20%60contributing_factor_vehicle_1%60%2C%0A%20%20%60contributing_factor_vehicle_2%60%2C%0A%20%20%60contributing_factor_vehicle_3%60%2C%0A%20%20%60contributing_factor_vehicle_4%60%2C%0A%20%20%60contributing_factor_vehicle_5%60%2C%0A%20%20%60collision_id%60%2C%0A%20%20%60vehicle_type_code1%60%2C%0A%20%20%60vehicle_type_code2%60%2C%0A%20%20%60vehicle_type_code_3%60%2C%0A%20%20%60vehicle_type_code_4%60%2C%0A%20%20%60vehicle_type_code_5%60%0AWHERE%20%60number_of_cyclist_injured%60%20%3E%200%0AORDER%20BY%20%60crash_date%60%20DESC%20NULL%20LAST'
#     response = requests.get(filtered_url)
    
#     if response.status_code == 200:
#         # Assuming the API returns JSON data
#         return response.json()  # or process the response as needed
#     else:
#         return None


# # App layout
# crashApp.layout = dbc.Container([
    
#     dbc.Row([
#         html.Div('My First App with Data, Graph, and Controls', className="text-primary text-center fs-3")
#     ]),

#     dbc.Row([
#         dbc.RadioItems(options=[{"label": x, "value": x} for x in ['pop', 'lifeExp', 'gdpPercap']],
#                        value='lifeExp',
#                        inline=True,
#                        id='radio-buttons-final')
#     ]),

#     dbc.Row([
#         dbc.Col([
#             dash_table.DataTable(data=df.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'})
#         ], width=6),

#         dbc.Col([
#             dcc.Graph(figure={}, id='my-first-graph-final')
#         ], width=6),
#     ])
# ])


# Callback to fetch and update data when the button is clicked
@crashApp.callback(
    Output('api-graph', 'figure'),
    Input('fetch-data-btn', 'n_clicks')
)
def update_graph(n_clicks):
    if n_clicks > 0:
        data = crashAPI()
        if data:
            # Assuming the data is in a format compatible with Plotly
            df = pd.DataFrame(data)
            print(df)
            fig = px.scatter(df, x='crash_date', y='borough', title='API Data')
            return fig
        else:
            return px.line(title='No Data Available')
    return px.line(title='Press the button to fetch data')

if __name__ == '__main__':
    crashApp.run(debug=True) 
