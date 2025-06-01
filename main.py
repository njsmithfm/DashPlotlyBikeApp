from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.io as pio
from datetime import datetime, timedelta
import constants
from constants import DAYS, BOROUGH_COLORS, NYC_BIKE_API_LINK_INJURED, NYC_BIKE_API_LINK_KILLED


pio.templates.default = "plotly_dark"
app = Dash(
    __name__,
    title="NYC Bike Crashes",
    update_title="workin on it...",
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

df = constants.NYC_BIKE_API_LINK_INJURED
df["crash_date"] = pd.to_datetime(df["Date"])


# Density fig is actually a scatter map with invisible markers and Go density traces added on top
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
                "size": 24,
                "color": "powderblue",
                "family": "verdana",
                "weight": "bold",
                "variant": "small-caps",
            },
            "x": 0.5,
            "y": 0.9,
            "xanchor": "center",
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
            b=30,
        ),
        title={
            "text": "Cyclist Injuries By Location",
            "font": {
                "size": 24,
                "color": "powderblue",
                "family": "verdana",
                "weight": "bold",
                "variant": "small-caps",
            },
            "x": 0.5,
            "y": 0.9,
            "xanchor": "center",
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
                font=dict(
                    size=10,
                    color="rgba(255,255,255)"
                    ),
                bgcolor="rgba(0,0,0,0.75)",
                bordercolor="rgba(255,255,255,0.2)",
                borderwidth=1,
            )
        ],
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
        title="Cyclist Injuries By Day",
        height=400,
    )
    histogram_fig.update_layout(
        margin=dict(l=80, r=20, t=30, b=5),
        bargap=0.1,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title={
            "text": "Cyclist Injuries By Day",
            "font": {
                "size": 24,
                "color": "powderblue",
                "family": "verdana",
                "weight": "bold",
                "variant": "small-caps",
            },
            "x": 0.5,
            "y": 0.975,
            "xanchor": "center",
            "yanchor": "top",
        },
        legend=dict(title_text=" ")
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
                                    "This map displays traffic crash events in NYC wherein at least one cyclist was injured. Adjust the options below to explore different views of crash data. Vehicle information and a contributing factor are provided where available."
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
                                            dcc.Slider(7, 60, 1,
                                                       value=constants.DAYS,
                                                       marks={
                                                       7: 'Week', 
                                                       30: 'Month', 
                                                       60: '2 Months'},
                                                       id='slider',
                                                       updatemode='drag')
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
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=3,
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
    Input("dropdown", "value"),
    Input("slider", "value")
)
def update_all(selected_value, slider_value):
    # Get fresh data when slider changes
    if slider_value != constants.DAYS:
        constants.DAYS = slider_value
        constants.NYC_BIKE_API_LINK_INJURED, constants.NYC_BIKE_API_LINK_KILLED = constants.get_crash_data(slider_value)
    
    df = constants.NYC_BIKE_API_LINK_INJURED
    
    if selected_value == "density":
        map_fig = create_density_fig(df, constants.DAYS, BOROUGH_COLORS)
    else:
        map_fig = create_scatter_fig(df, constants.DAYS)
    
    histogram_fig = create_histogram_fig(df, constants.DAYS)
    
    label_text = f"Currently Showing {slider_value} Days Of Crashes"
    
    return map_fig, histogram_fig, label_text

if __name__ == "__main__":
    app.run(debug=True)