from dash import Dash, dcc, html
import plotly.express as px
import requests
from dash.dependencies import Input, Output
import pandas as pd

# Create a Dash app
crashApp = Dash(__name__)

# Function to fetch data from an API
def crashAPI():
    filtered_url = 'https://data.cityofnewyork.us/resource/h9gi-nx95.json?$query=SELECT%0A%20%20%60crash_date%60%2C%0A%20%20%60crash_time%60%2C%0A%20%20%60borough%60%2C%0A%20%20%60zip_code%60%2C%0A%20%20%60latitude%60%2C%0A%20%20%60longitude%60%2C%0A%20%20%60location%60%2C%0A%20%20%60on_street_name%60%2C%0A%20%20%60off_street_name%60%2C%0A%20%20%60cross_street_name%60%2C%0A%20%20%60number_of_persons_injured%60%2C%0A%20%20%60number_of_persons_killed%60%2C%0A%20%20%60number_of_pedestrians_injured%60%2C%0A%20%20%60number_of_pedestrians_killed%60%2C%0A%20%20%60number_of_cyclist_injured%60%2C%0A%20%20%60number_of_cyclist_killed%60%2C%0A%20%20%60number_of_motorist_injured%60%2C%0A%20%20%60number_of_motorist_killed%60%2C%0A%20%20%60contributing_factor_vehicle_1%60%2C%0A%20%20%60contributing_factor_vehicle_2%60%2C%0A%20%20%60contributing_factor_vehicle_3%60%2C%0A%20%20%60contributing_factor_vehicle_4%60%2C%0A%20%20%60contributing_factor_vehicle_5%60%2C%0A%20%20%60collision_id%60%2C%0A%20%20%60vehicle_type_code1%60%2C%0A%20%20%60vehicle_type_code2%60%2C%0A%20%20%60vehicle_type_code_3%60%2C%0A%20%20%60vehicle_type_code_4%60%2C%0A%20%20%60vehicle_type_code_5%60%0AWHERE%20%60number_of_cyclist_injured%60%20%3E%200%0AORDER%20BY%20%60crash_date%60%20DESC%20NULL%20LAST'
    response = requests.get(filtered_url)
    
    if response.status_code == 200:
        # Assuming the API returns JSON data
        return response.json()  # or process the response as needed
    else:
        return None

# Create the layout of the app
crashApp.layout = html.Div([
    html.H1('API Data in Dash'),
    dcc.Graph(id='api-graph'),
    html.Button("Fetch Data", id="fetch-data-btn", n_clicks=0),
])

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
            fig = px.line(df, x='date', y='value', title='API Data')
            return fig
        else:
            return px.line(title='No Data Available')
    return px.line(title='Press the button to fetch data')

if __name__ == '__main__':
    crashApp.run(debug=True)
