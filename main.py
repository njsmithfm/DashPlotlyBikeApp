from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.io as pio
from datetime import datetime, timedelta


pio.templates.default = "plotly_dark"
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
initial_days = 7

import constants

df = constants.NYC_BIKE_API_LINK

df["crash_date"] = pd.to_datetime(df["crash_date"])
boroughs = ["MANHATTAN", "BROOKLYN", "QUEENS", "BRONX", "STATEN ISLAND"]
color_sequence = px.colors.qualitative.Vivid


borough_crashSums = (
    df.groupby("borough")["number_of_cyclist_injured"].sum().reset_index()
)
borough_crash_dict = borough_crashSums.set_index("borough")[
    "number_of_cyclist_injured"
].to_dict()


def create_map_fig(df, days):
    map_fig = px.scatter_map(
        df,
        lat="latitude",
        lon="longitude",
        color="borough",
        hover_data={
            "number_of_cyclist_injured",
            "crash_date",
            "vehicle_type_code1",
            "vehicle_type_code2",
            "contributing_factor_vehicle_1",
        },
        labels={"number_of_cyclist_injured": "Cyclists Injured"},
        center=dict(lat=40.7128, lon=-73.9560),
        zoom=10,
        map_style="dark",
        title=f"Cyclist Injury Locations (Last {days} Days)",
    )

    return map_fig


def create_histogram_fig(df, days):
    histogram_fig = px.histogram(
        df,
        x="crash_date",
        y="number_of_cyclist_injured",
        color="borough",
        title=f"Cyclist Injuries By Borough (Last {days} Days)",
        labels={"crash_date": "Date", "number_of_cyclist_injured": "Cyclist Injuries"},
    )
    return histogram_fig


map_fig = create_map_fig(df, initial_days)
histogram_fig = create_histogram_fig(df, initial_days)


app.layout = html.Div(
    [
        dbc.Container(
            [
                html.H1(
                    "Where In NYC Are Cyclists Getting Injured?",
                    className="text-center my-4",
                ),
                html.P(
                    "This map shows geospatial data of traffic collisions in NYC in which at least one cyclist was injured. Use the dropdown to select a time range from today's date. The thermal map shows densities, to suggest areas that are comparatively more dangerous for cyclists. Vehicle data and a primary contributing factor are provided where available."
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label(
                                    "Select Timeframe", className="fw-bold me-2"
                                ),
                                dcc.Dropdown(
                                    id="timeframe-dropdown",
                                    options=[
                                        {"label": "Previous 7 Days", "value": 7},
                                        {"label": "Previous 2 Weeks", "value": 14},
                                        {"label": "Previous 30 Days", "value": 30},
                                        {"label": "Previous 6 Months", "value": 180},
                                        {"label": "Previous Year", "value": 365},
                                    ],
                                    value=7,
                                    clearable=False,
                                    style={
                                        "backgroundColor": "#fcfcfc",
                                        "color": "black",
                                    },
                                ),
                            ],
                            xs=12,
                            sm=12,
                            md=6,
                            lg=4,
                            xl=3,
                            className="mb-4",
                        )
                    ],
                    justify="left",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id="map",
                                    figure=map_fig,
                                    responsive=True,
                                    style={"height": "65vh"},
                                )
                            ],
                            className="mb-4",
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id="histogram",
                                    figure=histogram_fig,
                                    responsive=True,
                                    style={"height": "50vh"},
                                )
                            ],
                            width=12,
                            className="mb-4",
                        ),
                    ]
                ),
            ]
        ),
    ]
)


@app.callback(Output("map", "figure"), Input("timeframe-dropdown", "value"))
def update_map_time(number_of_days):
    updated_map_chart = create_map_fig(df=df, days=number_of_days)
    return updated_map_chart


@app.callback(Output("histogram", "figure"), Input("timeframe-dropdown", "value"))
def update_hisogram_time(number_of_days):
    updated_histogram = create_histogram_fig(df=df, days=number_of_days)
    return updated_histogram


if __name__ == "__main__":
    app.run(debug=True)
