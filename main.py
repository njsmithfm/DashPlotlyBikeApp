from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.io as pio
from datetime import datetime, timedelta
import constants

pio.templates.default = "plotly_dark"
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

days = 30
df = constants.NYC_BIKE_API_LINK

df["crash_date"] = pd.to_datetime(df["Date"])
boroughs = ["MANHATTAN", "BROOKLYN", "QUEENS", "BRONX", "STATEN ISLAND"]
color_sequence = px.colors.qualitative.Vivid


borough_crashSums = df.groupby("Borough")["Cyclists_Injured"].sum().reset_index()
borough_crash_dict = borough_crashSums.set_index("Borough")[
    "Cyclists_Injured"
].to_dict()


def create_map_fig(df, days):
    df["crash_date_str"] = df["Date"].dt.strftime("%m/%d/%Y")
    map_fig = px.scatter_map(
        df,
        lat="Latitude",
        lon="Longitude",
        color="Borough",
        hover_data={
            "crash_date_str": True,
            "Latitude": False,
            "Longitude": False,
            "Cyclists_Injured": True,
            "Vehicle_1": True,
            "Vehicle_2": True,
            "Contributing_Factor": True,
        },
        labels={
            "crash_date_str": "Date",
            "borough": "Borough",
            "Cyclists_Injured": "Cyclists Injured",
            "Vehicle_1": "Vehicle 1",
            "Vehicle_2": "Vehicle 2",
            "Contributing_Factor": "Contributing Factor",
        },
        center=dict(lat=40.7128, lon=-73.9560),
        zoom=10,
        map_style="dark",
        title=f"Cyclist Injury Locations (Last {days} Days)",
    )
    return map_fig


def create_histogram_fig(df, days):
    histogram_fig = px.histogram(
        df,
        x="Date",
        y="Cyclists_Injured",
        color="Borough",
        # marginal='violin',
        title="Recent Cyclist Injuries By Borough",
        labels={"Date": "Week", "Cyclists_Injured": f"Cyclist Injuries"},
    )
    histogram_fig.update_layout(bargap=0.1)
    return histogram_fig


map_fig = create_map_fig(df, days)
histogram_fig = create_histogram_fig(df, days)

app.layout = html.Div(
    [
        dbc.Container(
            [
                html.H1(
                    "Where In NYC Are Cyclists Getting Injured?",
                    className="text-center my-4",
                ),
                html.P(
                    "This map shows geospatial data of traffic crash events in NYC in which at least one cyclist was injured. Crash events inolving cyclist deaths are also marked with an 'X' icon. Vehicle data and a primary contributing factor are provided where available."
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
                            width=12,
                            className="mb-4",
                        )
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id="histogram",
                                    figure=histogram_fig,
                                    responsive=True,
                                    style={"height": "65vh"},
                                )
                            ],
                            width=12,
                            className="mb-4",
                        )
                    ],
                ),
            ]
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
