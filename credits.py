from dash import Dash, dcc, html, Input, Output, callback

html.Div(
    [
        "This app was created through the ",
        html.A(
            "Data Visualization Society's",
            href="https://datavisualizationsociety.org",
            target="_blank",
        ),
        " Spring 2025 mentorship program. It would not exist without the guidance of my mentor, Adam Kulidjian, and his skill helping me navigate Plotly and Dash.",
    ],
),

