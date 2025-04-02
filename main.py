from dash import Dash, dcc, html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.io as pio
from datetime import datetime, timedelta

# Set default template
pio.templates.default = "plotly_dark"

# Initialize Dash app with Bootstrap
crashApp = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Load data once for all visualizations
df = pd.read_json('https://data.cityofnewyork.us/resource/h9gi-nx95.json?$query=SELECT%0A%20%20%60crash_date%60%2C%0A%20%20%60crash_time%60%2C%0A%20%20%60borough%60%2C%0A%20%20%60zip_code%60%2C%0A%20%20%60latitude%60%2C%0A%20%20%60longitude%60%2C%0A%20%20%60location%60%2C%0A%20%20%60on_street_name%60%2C%0A%20%20%60off_street_name%60%2C%0A%20%20%60cross_street_name%60%2C%0A%20%20%60number_of_persons_injured%60%2C%0A%20%20%60number_of_persons_killed%60%2C%0A%20%20%60number_of_pedestrians_injured%60%2C%0A%20%20%60number_of_pedestrians_killed%60%2C%0A%20%20%60number_of_cyclist_injured%60%2C%0A%20%20%60number_of_cyclist_killed%60%2C%0A%20%20%60number_of_motorist_injured%60%2C%0A%20%20%60number_of_motorist_killed%60%2C%0A%20%20%60contributing_factor_vehicle_1%60%2C%0A%20%20%60contributing_factor_vehicle_2%60%2C%0A%20%20%60contributing_factor_vehicle_3%60%2C%0A%20%20%60contributing_factor_vehicle_4%60%2C%0A%20%20%60contributing_factor_vehicle_5%60%2C%0A%20%20%60collision_id%60%2C%0A%20%20%60vehicle_type_code1%60%2C%0A%20%20%60vehicle_type_code2%60%2C%0A%20%20%60vehicle_type_code_3%60%2C%0A%20%20%60vehicle_type_code_4%60%2C%0A%20%20%60vehicle_type_code_5%60%0AWHERE%20%60number_of_cyclist_injured%60%20%3E%200%0AORDER%20BY%20%60crash_date%60%20DESC%20NULL%20LAST')

# Convert crash_date to datetime
df['crash_date'] = pd.to_datetime(df['crash_date'])

# Create density map (larger and more prominent)
map_fig = px.density_map(df, lat='latitude', lon='longitude', z='number_of_cyclist_killed', radius=10,
                        center=dict(lat=40.7128, lon=-74.0060), zoom=11,
                        map_style="open-street-map",
                        title='Cyclist Injury Heatmap')
map_fig.update_layout(
    coloraxis_colorbar_title="Deaths")

# Adjust map layout to be taller
map_fig.update_layout(
    height=800,
    margin=dict(l=0, r=0, t=50, b=0)
)

# Create borough summary data for bar chart
borough_crashSums = df.groupby('borough')['number_of_cyclist_injured'].sum().reset_index()

# Create bar chart (more compact)
bar_fig = px.bar(borough_crashSums, x='number_of_cyclist_injured', y='borough', 
             title='Total Cyclist Injuries by Borough',
             orientation='h',
             labels={'borough': ' ', 'number_of_cyclist_injured': 'Injuries'})

# Make bar chart more compact
bar_fig.update_layout(
    height=300,
    margin=dict(l=0, r=0, t=50, b=0)
)

# Create sparklines for the last 30 days by borough
# First, filter to last 30 days
today = df['crash_date'].max()
thirty_days_ago = today - timedelta(days=30)
recent_df = df[(df['crash_date'] >= thirty_days_ago) & (df['crash_date'] <= today)]

# Create a complete date range for the last 30 days
date_range = pd.date_range(start=thirty_days_ago, end=today)

# Get list of boroughs
boroughs = ['MANHATTAN', 'BROOKLYN', 'QUEENS', 'BRONX', 'STATEN ISLAND']

# Create sparklines figure (more compact)
spark_fig = make_subplots(rows=len(boroughs), cols=1, 
                        subplot_titles=boroughs,
                        vertical_spacing=0.1,
                        shared_xaxes=True)

# Create a color map for the boroughs
colors = px.colors.qualitative.Plotly
borough_colors = {borough: colors[i % len(colors)] for i, borough in enumerate(boroughs)}

# Add traces for each borough
for i, borough in enumerate(boroughs):
    # Filter data for this borough
    borough_data = recent_df[recent_df['borough'] == borough]
    
    # Group by date and sum injuries
    daily_counts = borough_data.groupby('crash_date')['number_of_cyclist_injured'].sum().reset_index()
    
    # Create a complete time series with zeros for missing dates
    full_ts = pd.DataFrame({'crash_date': date_range})
    full_ts = full_ts.merge(daily_counts, on='crash_date', how='left')
    full_ts['number_of_cyclist_injured'] = full_ts['number_of_cyclist_injured'].fillna(0)
    
    # Add line trace
    spark_fig.add_trace(
        go.Scatter(
            x=full_ts['crash_date'],
            y=full_ts['number_of_cyclist_injured'],
            mode='lines',
            name=borough,
            line=dict(width=1.5, color=borough_colors[borough]),
            showlegend=False
        ),
        row=i+1, col=1
    )
    
    # Add filled area under the lines
    color = borough_colors[borough].replace('#', '')
    r = int(color[0:2], 16) if len(color) >= 2 else 0
    g = int(color[2:4], 16) if len(color) >= 4 else 0
    b = int(color[4:6], 16) if len(color) >= 6 else 0
    
    spark_fig.add_trace(
        go.Scatter(
            x=full_ts['crash_date'],
            y=full_ts['number_of_cyclist_injured'],
            mode='none',
            fill='tozeroy',
            fillcolor=f'rgba({r},{g},{b},0.1)',
            showlegend=False
        ),
        row=i+1, col=1
    )

# Update sparklines layout to be more compact
spark_fig.update_layout(
    height=600,
    margin=dict(l=0, r=0, t=50, b=0),
    title_text="Injuries by Borough (Last 30 Days)"
)

# Make the sparklines minimal
spark_fig.update_xaxes(showticklabels=False, showgrid=False)
for i in range(len(boroughs)):
    spark_fig.update_yaxes(
        showticklabels=False,
        showgrid=False,
        row=i+1, col=1
    )

# Create layout with map on left (taller), bar chart and sparklines stacked on right
crashApp.layout = html.Div([
    dbc.Container([
        html.H1('Where In NYC Are Cyclists Getting Injured?', className='text-center my-4'),
        
        dbc.Row([
            # Left column for prominent map (wider)
            dbc.Col([
                dcc.Graph(id='map-graph', figure=map_fig, style={'height': '800px'})
            ], width=7, className="d-flex align-items-stretch"),
            
            # Right column for stacked bar chart and sparklines
            dbc.Col([
                # Bar chart on top
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='bar-graph', figure=bar_fig)
                    ])
                ], className='mb-2'),
                
                # Sparklines below
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='sparklines-graph', figure=spark_fig)
                    ])
                ])
            ], width=5)
        ])
    ], fluid=True)
])

if __name__ == '__main__':
    crashApp.run(debug=True, use_reloader=False)