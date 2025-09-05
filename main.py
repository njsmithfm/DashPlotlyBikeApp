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
    BOROUGH_COLORS,
    NYC_BIKE_API_LINK_INJURED,
    NYC_BIKE_API_LINK_KILLED,
)


MAX_DAYS = 60
FULL_DF_INJURED, FULL_DF_KILLED = constants.get_crash_data(MAX_DAYS)
FULL_DF_INJURED["crash_date"] = pd.to_datetime(FULL_DF_INJURED["Date"])
FULL_DF_KILLED["crash_date"] = pd.to_datetime(FULL_DF_KILLED["Date"])


def filter_dataframe_by_days(df, days):
    if df.empty:
        return df

    max_date = df["crash_date"].max()
    cutoff_date = max_date - timedelta(days=days - 1)
    filtered_df = df[df["crash_date"] >= cutoff_date].copy()
    return filtered_df


pio.templates.default = "plotly_dark"
app = Dash(
    __name__,
    pages_folder="",
    title="NYC Bike Crashes",
    update_title="workin on it...",
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server

df = constants.NYC_BIKE_API_LINK_INJURED
df["crash_date"] = pd.to_datetime(df["Date"])


# Density fig is a scatter map with opaque traces for tooltips and Go density traces added on top
def create_density_fig(df, DAYS, BOROUGH_COLORS):
    df["crash_date_str"] = df["Date"].dt.strftime("%m/%d/%Y")

    density_fig = px.scatter_map(
        df,
        lat="Latitude",
        lon="Longitude",
        color_discrete_map=BOROUGH_COLORS,
        color="Borough",
        hover_name="Borough",
        hover_data={
            "Borough": False,
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
            "Cyclists_Injured": "Cyclists Injured",
            "Vehicle_1": "Vehicle 1",
            "Vehicle_2": "Vehicle 2",
            "Contributing_Factor": "Contributing Factor",
        },
        center=dict(lat=40.7128, lon=-73.9560),
        zoom=11,
        map_style="dark",
    )
    for trace in density_fig.data[:-1]:
        trace.marker.opacity = 0

    density_fig.add_trace(
        go.Densitymap(
            lat=df["Latitude"],
            lon=df["Longitude"],
            hoverinfo="skip",
            radius=10,
            opacity=0.90,
            zmin=0.55,
            zmax=1,
            showscale=False,
        )
    )

    density_fig.update_layout(
        margin=dict(l=30, r=20, t=75, b=30),
        title={
            "text": "Cyclist Injuries By Location",
            "font": {
                "size": 18,
                "color": "powderblue",
                "weight": "bold",
            },
            "x": 0.05,
            "y": 0.925,
            "xanchor": "left",
            "yanchor": "top",
        },
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[
            dict(
                text='© <a href="https://carto.com/about-carto/" style="color: #87CEEB;">CARTO</a>, © <a href="https://www.openstreetmap.org/copyright" style="color: #87CEEB;">OpenStreetMap</a>',
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.01,
                y=0.01,
                xanchor="left",
                yanchor="bottom",
                font=dict(size=10, color="rgba(255,255,255)"),
                bgcolor="rgba(0,0,0,0.75)",
                bordercolor="rgba(255,255,255,0.2)",
                borderwidth=1,
            )
        ],
    )
    hover_txt = (
        "Borough: "
        + FULL_DF_KILLED["Borough"]
        + "<br>"
        + "Date: "
        + FULL_DF_KILLED["Date"].dt.strftime("%m/%d/%Y")
        + "<br>"
        + "Cyclists Killed: "
        + FULL_DF_KILLED["Cyclists_Killed"].astype(str)
        + "<br>"
        "Vehicle 1: "
        + FULL_DF_KILLED["Vehicle_1"]
        + "<br>"
        # + "Vehicle 2: "
        # + FULL_DF_KILLED["Vehicle_2"]
        # + "<br>"
        + "Contributing Factor: "
        + FULL_DF_KILLED["Contributing_Factor"]
    )
    density_fig.add_scattermap(
        lat=FULL_DF_KILLED["Latitude"],
        lon=FULL_DF_KILLED["Longitude"],
        mode="markers",
        marker=dict(symbol="circle", size=10, color="#FFFFFF"),
        hoverinfo="text",
        hovertext=hover_txt,
        opacity=1,
    )

    return density_fig


def create_scatter_fig(df, DAYS):
    df["crash_date_str"] = df["Date"].dt.strftime("%m/%d/%Y")
    scatter_fig = px.scatter_map(
        df,
        lat="Latitude",
        lon="Longitude",
        color_discrete_map=BOROUGH_COLORS,
        color="Borough",
        hover_name="Borough",
        hover_data={
            "Borough": False,
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
            "Cyclists_Injured": "Cyclists Injured",
            "Vehicle_1": "Vehicle 1",
            "Vehicle_2": "Vehicle 2",
            "Contributing_Factor": "Contributing Factor",
        },
        center=dict(lat=40.7128, lon=-73.9560),
        zoom=11,
        map_style="dark",
    )
    scatter_fig.update_layout(
        margin=dict(
            l=30,
            r=20,
            t=75,
            b=0,
        ),
        title={
            "text": "Cyclist Injuries By Location",
            "font": {
                "size": 18,
                "color": "powderblue",
                "weight": "bold",
            },
            "x": 0.05,
            "y": 0.925,
            "xanchor": "left",
            "yanchor": "top",
        },
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[
            dict(
                text='© <a href="https://carto.com/about-carto/" style="color: #87CEEB;">CARTO</a>, © <a href="https://www.openstreetmap.org/copyright" style="color: #87CEEB;">OpenStreetMap</a>',
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.01,
                y=0.01,
                xanchor="left",
                yanchor="bottom",
                font=dict(size=10, color="rgba(255,255,255)"),
                bgcolor="rgba(0,0,0,0.75)",
                bordercolor="rgba(255,255,255,0.2)",
                borderwidth=1,
            )
        ],
    )
    
    hover_txt = (
        "Borough: "
        + FULL_DF_KILLED["Borough"]
        + "<br>"
        + "Date: "
        + FULL_DF_KILLED["Date"].dt.strftime("%m/%d/%Y")
        + "<br>"
        + "Cyclists Killed: "
        + FULL_DF_KILLED["Cyclists_Killed"].astype(str)
        + "<br>"
        "Vehicle 1: "
        + FULL_DF_KILLED["Vehicle_1"]
        + "<br>"
        # + "Vehicle 2: "
        # + FULL_DF_KILLED["Vehicle_2"]
        # + "<br>"
        + "Contributing Factor: "
        + FULL_DF_KILLED["Contributing_Factor"]
    )
    scatter_fig.add_scattermap(
        lat=FULL_DF_KILLED["Latitude"],
        lon=FULL_DF_KILLED["Longitude"],
        mode="markers",
        marker=dict(symbol="circle", size=10, color="#FFFFFF"),
        hoverinfo="text",
        hovertext=hover_txt,
        opacity=1,
    )

    return scatter_fig


def create_histogram_fig(df, DAYS):
    ordered_boroughs = list(BOROUGH_COLORS.keys())
    df["Borough"] = pd.Categorical(
        df["Borough"], categories=ordered_boroughs, ordered=True
    )
    df = df.sort_values("Borough")
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
        },
        labels={
            "crash_date_str": " ",
            "borough": "Borough ",
            "Cyclists_Injured": "Borough Cyclists Injured",
        },
        nbins=DAYS,
        title="",
    )
    histogram_fig.update_layout(
        margin=dict(l=80, r=20, t=30, b=5),
        bargap=0.1,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title={
            "text": "Cyclist Injuries By Day",
            "font": {
                "size": 18,
                "color": "powderblue",
                "weight": "bold",
            },
            "x": 0.05,
            "y": 1,
            "xanchor": "left",
            "yanchor": "top",
        },
        legend=dict(title_text=" "),
    ),

    histogram_fig.update_yaxes(title_text="Cyclist Injuries")
    histogram_fig.update_xaxes(title_text="")

    return histogram_fig


density_fig = create_density_fig(df, DAYS, BOROUGH_COLORS)
scatter_fig = create_scatter_fig(df, DAYS)
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
                                    "Where In NYC Are Cyclists Getting Hurt?",
                                ),
                                html.P(
                                    "This map displays traffic crash events in NYC wherein at least one cyclist was injured. Adjust the options below to explore different views of the most recent crash events. Hover over the graphs to see more granular contextual data, provided where available. White circles indicate cyclist deaths."
                                ),
                                html.Footer(
                                    [
                                        "Data courtesy of the NYC Open Data ",
                                        html.A(
                                            "Motor Vehicle Collisions-Crashes",
                                            href="https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/about_data",
                                            target="_blank",
                                        ),
                                        " API, which is stated to receive daily updates. (although it is usually not current up to the present day)",
                                    ],
                                ),
                                html.Div(
                                    [
                                        html.Label(id="slider-label"),
                                        dcc.Slider(
                                            min=7,
                                            max=MAX_DAYS,
                                            step=1,
                                            value=30,
                                            marks={
                                                7: {
                                                    "label": "Week",
                                                    "style": {"font-size": "10px"},
                                                },
                                                30: {
                                                    "label": "Month",
                                                    "style": {"font-size": "10px"},
                                                },
                                                60: {
                                                    "label": "2 Months",
                                                    "style": {
                                                        "font-size": "10px",
                                                        "white-space": "nowrap",
                                                    },
                                                },
                                            },
                                            id="slider",
                                            updatemode="drag",
                                        ),
                                    ],
                                    style={
                                        "margin-left": "30px",
                                        "margin-right": "30px",
                                        "margin-bottom": "10px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Label(
                                            "Select Map View",
                                        ),
                                        dcc.Dropdown(
                                            id="dropdown",
                                            options=[
                                                {
                                                    "label": "Density Map",
                                                    "value": "density",
                                                },
                                                {
                                                    "label": "Scatter Map",
                                                    "value": "scatter",
                                                },
                                            ],
                                            value="density",
                                            clearable=False,
                                        ),
                                    ],
                                    style={
                                        "margin-left": "30px",
                                        "margin-right": "30px",
                                        "margin-bottom": "10px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Section(
                                            id="crash-count",
                                        ),
                                    ],
                                    style={
                                        "margin-left": "30px",
                                        "margin-right": "30px",
                                        "margin-bottom": "10px",
                                    },
                                ),
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=3,
                            className="left-col d-flex flex-column",
                            align="start",
                        ),
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dcc.Graph(
                                            id="map",
                                            figure=density_fig,
                                            responsive=True,
                                            style={"height": "65vh"},
                                        )
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        dcc.Graph(
                                            id="histogram",
                                            figure=histogram_fig,
                                            responsive=True,
                                            style={
                                                "height": "35vh",
                                            },
                                        )
                                    ],
                                ),
                            ],
                            align="end",
                            xs=12,
                            sm=12,
                            md=12,
                            lg=9,
                            className="bg-black",
                        ),
                    ],
                ),
            ],
            fluid=True,
            className="bg-black bg-opacity-50",
        ),
    ],
)


@app.callback(
    Output("map", "figure"),
    Output("histogram", "figure"),
    Output("slider-label", "children"),
    Output("crash-count", "children"),
    Input("dropdown", "value"),
    Input("slider", "value"),
)
def update_all(selected_value, slider_value):
    df = filter_dataframe_by_days(FULL_DF_INJURED, slider_value)

    if selected_value == "density":
        map_fig = create_density_fig(df, slider_value, BOROUGH_COLORS)
    else:
        map_fig = create_scatter_fig(df, slider_value)

    histogram_fig = create_histogram_fig(df, slider_value)

    label_text = f"Currently Showing {slider_value} Days Of Crashes"

    crash_count_injured = len(df)

    crash_count_display = f"In the past {slider_value} days of available data, there have been {crash_count_injured:,} total cyclist injury reports across NYC."

    return map_fig, histogram_fig, label_text, crash_count_display

