from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.io as pio
from datetime import datetime, timedelta
import constants
from constants import (
    DAYS,
    NYC_BIKE_API_LINK_INJURED,
    NYC_BIKE_API_LINK_KILLED,
    BOROUGH_COLORS
)

pio.templates.default = "plotly_dark"
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

df = constants.NYC_BIKE_API_LINK_INJURED
df["crash_date"] = pd.to_datetime(df["Date"])


def create_map_fig(df, DAYS):
    df["crash_date_str"] = df["Date"].dt.strftime("%m/%d/%Y")
    map_fig = px.scatter_map(
        df,
        lat="Latitude",
        lon="Longitude",
        color_discrete_map=BOROUGH_COLORS,
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
        title=f"Cyclist Injuries By Location",
        
    )
    map_fig.update_layout(
        margin=dict(
            l=30,
            r=20,
            t=75,
            b=75,
        ),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return map_fig


def create_histogram_fig(df, DAYS):
    histogram_fig = px.histogram(
        df,
        x="Date",
        y="Cyclists_Injured",
        color_discrete_map=BOROUGH_COLORS,
        color="Borough",
        hover_data={
            "Borough": True,
            "crash_date_str": True,
            "Cyclists_Injured": True,
            # "f{Borough} Cyclists Injured": True,
            # "Total Daily Cyclists Injured: True,
        },
        labels={
            "crash_date_str": "",
            "borough": "Borough",
            "Cyclists_Injured": "Borough Cyclists Injured",
            # "f{Borough} Cyclists Injured": True,
            # "Total Daily Cyclists Injured: True,
        },
        nbins=30,
        title="Cyclist Injuries By Day",
        height=400,
    )
    histogram_fig.update_layout(
        margin=dict(l=80, r=20, t=30, b=5),
        bargap=0.1,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        # legend=dict(
        #     title_text="Legend: ",
        #     orientation="h",
        #     yanchor="top",
        #     xanchor="right",
        #     y=1.45,
        # #     x=1,
        # ),
    )


    histogram_fig.update_yaxes(title_text="Cyclist Injuries")
    histogram_fig.update_xaxes(title_text="")

    return histogram_fig


map_fig = create_map_fig(df, DAYS)
histogram_fig = create_histogram_fig(df, DAYS)

app.layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H2(
                                    "Where In NYC Are Cyclists Getting Injured?",
                                ),
                                html.P(
                                    "This map displays geospatial data of traffic crash events in NYC in which at least one cyclist was injured, within the past 30 days. Vehicle data and a primary contributing factor are provided where available."
                                ),
                            ],
                            xs=12,
                            sm=12,
                            md=2,
                            lg=2,
                            align="start",
                            className="bg-black-80",
                        ),
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dcc.Graph(
                                            id="map",
                                            figure=map_fig,
                                            responsive=True,
                                            style={"height": "65vh"},
                                        )
                                    ],
                                    className="bg-black",
                                ),
                                dbc.Row(
                                    [
                                        dcc.Graph(
                                            id="histogram",
                                            figure=histogram_fig,
                                            responsive=True,
                                            style={
                                                "height": "35vh",
                                                "margin-bottom": "10px",
                                            },
                                            className="bg-black",
                                        )
                                    ]
                                ),
                            ],
                            align="end",
                            xs=12,
                            sm=12,
                            md=10,
                            lg=10,
                            className="bg-black",
                        ),
                    ],
                ),
            ],
            fluid=True,
            className="bg-black-80",
        ),
    ],
    className="app-header--title",
)

if __name__ == "__main__":
    app.run(debug=True)
