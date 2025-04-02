from dash import Dash, dcc, html
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

borough_crashSums = df.groupby('borough')['number_of_cyclist_injured'].sum().reset_index()

manhattan_injured = borough_crashSums[borough_crashSums['borough'] == 'MANHATTAN']['number_of_cyclist_injured'].values[0]
brooklyn_injured = borough_crashSums[borough_crashSums['borough'] == 'BROOKLYN']['number_of_cyclist_injured'].values[0]
queens_injured = borough_crashSums[borough_crashSums['borough'] == 'QUEENS']['number_of_cyclist_injured'].values[0]
bronx_injured = borough_crashSums[borough_crashSums['borough'] == 'BRONX']['number_of_cyclist_injured'].values[0]
staten_island_injured = borough_crashSums[borough_crashSums['borough'] == 'STATEN ISLAND']['number_of_cyclist_injured'].values[0]

# Print the values for verification
print(f"Manhattan: {manhattan_injured}")
print(f"Brooklyn: {brooklyn_injured}")
print(f"Queens: {queens_injured}")
print(f"Bronx: {bronx_injured}")
print(f"Staten Island: {staten_island_injured}")

# Create a bar chart using Plotly
barChart = px.bar(borough_crashSums, x='number_of_cyclist_injured', y='borough',
             title='Total Cyclist Injuries by Borough', 
             orientation='h',
             labels={'borough': 'Borough', 'number_of_cyclist_injured': 'Cyclist Injuries'})

# Show the plot
barChart.show()



if __name__ == '__main__':
    crashApp.run(debug=True) 
