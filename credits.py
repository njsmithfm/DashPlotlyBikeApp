from dash import Dash, dcc, html, Input, Output, callback

html.Div(
    [
        "This app was created through the ",
        html.A(
            "Data Visualization Society's",
            href="https://datavisualizationsociety.org",
            target="_blank",
        ),
        " Spring 2025 mentorship program. It would not exist without my mentor, Adam Kulidjian, and his guidance introducing me to Plotly and Dash."
    ],
),

