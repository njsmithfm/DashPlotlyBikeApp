from dash import Dash, dcc, html, Input, Output, callback
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
crashApp = Dash(__name__, 
                external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP],
                meta_tags=[{'name': 'viewport', 
                          'content': 'width=device-width, initial-scale=1.0'}]
               )

# Load data once for all visualizations
df = pd.read_json('https://data.cityofnewyork.us/resource/h9gi-nx95.json?$query=SELECT%0A%20%20%60crash_date%60%2C%0A%20%20%60crash_time%60%2C%0A%20%20%60borough%60%2C%0A%20%20%60zip_code%60%2C%0A%20%20%60latitude%60%2C%0A%20%20%60longitude%60%2C%0A%20%20%60location%60%2C%0A%20%20%60on_street_name%60%2C%0A%20%20%60off_street_name%60%2C%0A%20%20%60cross_street_name%60%2C%0A%20%20%60number_of_persons_injured%60%2C%0A%20%20%60number_of_persons_killed%60%2C%0A%20%20%60number_of_pedestrians_injured%60%2C%0A%20%20%60number_of_pedestrians_killed%60%2C%0A%20%20%60number_of_cyclist_injured%60%2C%0A%20%20%60number_of_cyclist_killed%60%2C%0A%20%20%60number_of_motorist_injured%60%2C%0A%20%20%60number_of_motorist_killed%60%2C%0A%20%20%60contributing_factor_vehicle_1%60%2C%0A%20%20%60contributing_factor_vehicle_2%60%2C%0A%20%20%60contributing_factor_vehicle_3%60%2C%0A%20%20%60contributing_factor_vehicle_4%60%2C%0A%20%20%60contributing_factor_vehicle_5%60%2C%0A%20%20%60collision_id%60%2C%0A%20%20%60vehicle_type_code1%60%2C%0A%20%20%60vehicle_type_code2%60%2C%0A%20%20%60vehicle_type_code_3%60%2C%0A%20%20%60vehicle_type_code_4%60%2C%0A%20%20%60vehicle_type_code_5%60%0AWHERE%20%60number_of_cyclist_injured%60%20%3E%200%0AORDER%20BY%20%60crash_date%60%20DESC%20NULL%20LAST')


df['crash_date'] = pd.to_datetime(df['crash_date'])

boroughs = ['MANHATTAN', 'BROOKLYN', 'QUEENS', 'BRONX', 'STATEN ISLAND']

# color scheme
color_sequence = px.colors.qualitative.Vivid  # You can change this to any palette you prefer

# Define function for creating figures
def create_figures(days=7):
    # Filter data based on selected timeframe
    today = df['crash_date'].max()
    start_date = today - timedelta(days=days)
    filtered_df = df[(df['crash_date'] >= start_date) & (df['crash_date'] <= today)]
    
    # Create a complete date range for the selected timeframe
    date_range = pd.date_range(start=start_date, end=today)
    
    # Create density map
    map_fig = px.density_map(filtered_df, lat='latitude', lon='longitude', z='number_of_cyclist_killed', radius=10,
                            center=dict(lat=40.7128, lon=-73.9560), zoom=10,
                            map_style="open-street-map",
                            title=f'Cyclist Fatality Locations (Last {days} Days)')
    
    # Improve responsiveness of map
    map_fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=50, b=0),
        height=400
    )
    
    # Create borough summary data for bar chart
    borough_crashSums = filtered_df.groupby('borough')['number_of_cyclist_injured'].sum().reset_index()
    
    # Make sure all boroughs are represented in the data (even if zero accidents)
    for borough in boroughs:
        if borough not in borough_crashSums['borough'].values:
            borough_crashSums = pd.concat([borough_crashSums, pd.DataFrame({'borough': [borough], 'number_of_cyclist_injured': [0]})], ignore_index=True)
    
    # Sort by borough to match the order in the sparklines
    borough_crashSums = borough_crashSums.set_index('borough').loc[boroughs].reset_index()
    
    # Create bar chart with simplified color sequence
    bar_fig = px.bar(borough_crashSums, x='number_of_cyclist_injured', y='borough',
                 title=f'Total Cyclist Injuries by Borough (Last {days} Days)',
                 orientation='h',
                 labels={'borough': 'Borough', 'number_of_cyclist_injured': 'Cyclist Injuries'},
                 color='borough',
                 color_discrete_sequence=color_sequence)  # Use color sequence directly
    
    # Improve responsiveness of bar chart
    bar_fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=20, t=50, b=20),
        height=350
    )
    
    # Adjust the layout for larger time frames (reduce tick frequency)
    tick_format = "%d-%b" if days <= 30 else "%b-%Y"
    tick_angle = 45 if days <= 30 else 0
    
    # Create list to hold borough data for finding consistent y-axis range
    all_borough_data = []
    
    # Process data for each borough
    for borough in boroughs:
        # Filter data for this borough
        borough_data = filtered_df[filtered_df['borough'] == borough]
        
        # For larger timeframes, group by week or month instead of day
        if days <= 30:
            # Group by date for shorter timeframes
            grouper = 'crash_date'
            daily_counts = borough_data.groupby(grouper)['number_of_cyclist_injured'].sum().reset_index()
            
            # Create a complete time series with zeros for missing dates
            full_ts = pd.DataFrame({grouper: date_range})
            full_ts = full_ts.merge(daily_counts, on=grouper, how='left')
            
        elif days <= 180:
            # Group by week for medium timeframes
            borough_data['week'] = borough_data['crash_date'].dt.isocalendar().week
            borough_data['year'] = borough_data['crash_date'].dt.isocalendar().year
            daily_counts = borough_data.groupby(['year', 'week'])['number_of_cyclist_injured'].sum().reset_index()
            
            # Create week endpoints
            daily_counts['crash_date'] = daily_counts.apply(lambda x: 
                datetime.strptime(f"{int(x['year'])}-W{int(x['week'])}-1", "%Y-W%W-%w"), axis=1)
            
            # Create a complete series of weeks
            weeks = pd.date_range(start=start_date, end=today, freq='W')
            full_ts = pd.DataFrame({'crash_date': weeks})
            full_ts = full_ts.merge(daily_counts[['crash_date', 'number_of_cyclist_injured']], on='crash_date', how='left')
            
        else:
            # Group by month for longer timeframes
            borough_data['month'] = borough_data['crash_date'].dt.month
            borough_data['year'] = borough_data['crash_date'].dt.year
            daily_counts = borough_data.groupby(['year', 'month'])['number_of_cyclist_injured'].sum().reset_index()
            
            # Create month endpoints
            daily_counts['crash_date'] = daily_counts.apply(lambda x: 
                datetime(int(x['year']), int(x['month']), 1), axis=1)
            
            # Create a complete series of months
            months = pd.date_range(start=start_date, end=today, freq='MS')
            full_ts = pd.DataFrame({'crash_date': months})
            full_ts = full_ts.merge(daily_counts[['crash_date', 'number_of_cyclist_injured']], on='crash_date', how='left')
        
        # Fill missing values with zeros
        full_ts['number_of_cyclist_injured'] = full_ts['number_of_cyclist_injured'].fillna(0)
        
        # Add to all_borough_data list
        all_borough_data.append(full_ts)
    
    # Calculate maximum y value across all boroughs for consistent y-axis
    max_y_value = max([df['number_of_cyclist_injured'].max() for df in all_borough_data])
    
    # Create sparklines with consistent y-axes using make_subplots for desktop
    spark_fig = make_subplots(rows=1, cols=5, 
                          subplot_titles=boroughs,
                          horizontal_spacing=0.05)
    
    # Add traces for each borough with consistent y-axis - SIMPLIFIED, NO FILLS
    for i, borough in enumerate(boroughs):
        # Add line trace with simple color assignment
        spark_fig.add_trace(
            go.Scatter(
                x=all_borough_data[i]['crash_date'],
                y=all_borough_data[i]['number_of_cyclist_injured'],
                mode='lines',
                name=borough,
                line=dict(width=1.5, color=color_sequence[i % len(color_sequence)]),
                showlegend=False
            ),
            row=1, col=i+1
        )
    
    # Update sparklines layout for desktop
    time_period = "Days"
    if days > 30 and days <= 180:
        time_period = "Weeks"
    elif days > 180:
        time_period = "Months"
    
    spark_fig.update_layout(
        height=300,
        margin=dict(l=40, r=20, t=50, b=20),
        title_text=f"Cyclist Injuries by Borough (Last {days} Days, Grouped by {time_period})",
        autosize=True
    )
    
    # Set consistent y-axis range for all subplots
    for i in range(1, 6):
        spark_fig.update_yaxes(
            range=[0, max_y_value * 1.25],  # Add 25% padding
            row=1, col=i
        )
    
    # Make the sparklines minimal but keep date labels on x-axis
    spark_fig.update_xaxes(
        showticklabels=True,
        showgrid=False,
        tickformat=tick_format,
        tickangle=tick_angle,
        nticks=5 if days > 30 else 7  # Fewer ticks for longer timeframes
    )
    
    for i in range(len(boroughs)):
        spark_fig.update_yaxes(
            showticklabels=True,
            showgrid=False,
            row=1, col=i+1,
            title_text="Injuries" if i == 0 else ""
        )
    
    # Create individual sparkline figures for mobile - SIMPLIFIED, NO FILLS
    mobile_figs = []
    
    for i, borough in enumerate(boroughs):
        # Create individual figure for each borough
        borough_fig = go.Figure()
        
        # Add line trace with simple color assignment
        borough_fig.add_trace(
            go.Scatter(
                x=all_borough_data[i]['crash_date'],
                y=all_borough_data[i]['number_of_cyclist_injured'],
                mode='lines',
                name=borough,
                line=dict(width=1.5, color=color_sequence[i % len(color_sequence)])
            )
        )
        # No more fill trace!
        
        # Update layout for consistent y-axis
        borough_fig.update_layout(
            title=borough,
            margin=dict(l=20, r=20, t=50, b=20),
            height=200,
            xaxis=dict(
                showticklabels=True,
                showgrid=False,
                tickformat=tick_format,
                tickangle=tick_angle,
                nticks=5 if days > 30 else 7  # Fewer ticks for longer timeframes
            ),
            yaxis=dict(
                showticklabels=True,
                showgrid=False,
                range=[0, max_y_value * 1.1]  # Add 10% padding
            )
        )
        
        mobile_figs.append(borough_fig)
    
    return map_fig, spark_fig, mobile_figs, bar_fig

# Generate initial figures with default 7-day timeframe
initial_map_fig, initial_spark_fig, initial_mobile_figs, initial_bar_fig = create_figures(7)

# Create layout with dropdown for timeframe selection
crashApp.layout = html.Div([
    dbc.Container([
        html.H1('Where In NYC Are Cyclists Getting Injured?', className='text-center my-4'),
        
        html.P("This map shows geospatial data of traffic collisions in NYC in which at least one cyclist was injured. Use the dropdown to select a time range from today's date. The thermal map shows densities, to suggest areas that are comparatively more dangerous for cyclists. Vehicle data and a primary contributing factor are provided where available."),

        # Add dropdown for timeframe selection
        dbc.Row([
            dbc.Col([
                html.Label("Select Timeframe", className="fw-bold me-2"),
                dcc.Dropdown(
                    id='timeframe-dropdown',
                    options=[
                        {'label': 'Previous 7 Days', 'value': 7},
                        {'label': 'Previous 2 Weeks', 'value': 14},
                        {'label': 'Previous 30 Days', 'value': 30},
                        {'label': 'Previous 6 Months', 'value': 180},
                        {'label': 'Previous Year', 'value': 365}
                    ],
                    value=7,
                    clearable=False,
                    style={'backgroundColor': '#fcfcfc', 'color': 'black'}
                )
            ], xs=12, sm=12, md=6, lg=4, xl=3, className="mb-4")
        ], justify="left"),
        
        # First row: Map
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='map-graph', figure=initial_map_fig, responsive=True)
            ], width=12, className="mb-4")
        ]),
        
        # Second row: Desktop sparklines (single row with 5 columns)
        dbc.Row([
            dbc.Col([
                html.Div(id='desktop-sparklines', children=[
                    dcc.Graph(id='sparklines-graph', figure=initial_spark_fig, responsive=True)
                ], className="d-none d-md-block")  # Hide on mobile screens
            ], width=12, className="mb-4")
        ]),
        
        # Mobile sparklines (stack vertically)
        dbc.Row([
            dbc.Col([
                html.Div(id='mobile-sparklines', children=[
                    dcc.Graph(
                        id=f'mobile-sparkline-{i}',
                        figure=fig,
                        responsive=True
                    ) for i, fig in enumerate(initial_mobile_figs)
                ], className="d-md-none")  # Show only on mobile screens
            ], width=12, className="mb-4")
        ]),
        
        # Third row: Bar Chart
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='bar-graph', figure=initial_bar_fig, responsive=True)
            ], width=12, className="mb-4")
        ]),
        
        # Footer with info
        dbc.Row([
            dbc.Col([
                html.P("Built by NJ Smith with Plotly + Dash. Accessed through NYC Open Data.",
                      className="text-center text-muted small")
            ], width=12)
        ])
    ], fluid=True, className="px-4")
])

# Create callback to update all graphs based on dropdown selection
@callback(
    [Output('map-graph', 'figure'),
     Output('desktop-sparklines', 'children'),
     Output('mobile-sparklines', 'children'),
     Output('bar-graph', 'figure')],
    [Input('timeframe-dropdown', 'value')]
)
def update_graphs(days):
    map_fig, spark_fig, mobile_figs, bar_fig = create_figures(days)
    
    # Desktop sparklines (single row)
    desktop_sparklines = dcc.Graph(
        id='sparklines-graph',
        figure=spark_fig,
        responsive=True
    )
    
    # Mobile sparklines (stack vertically)
    mobile_sparklines = [
        dcc.Graph(
            id=f'mobile-sparkline-{i}',
            figure=fig,
            responsive=True
        ) for i, fig in enumerate(mobile_figs)
    ]
    
    return map_fig, desktop_sparklines, mobile_sparklines, bar_fig

if __name__ == '__main__':
    crashApp.run(debug=True, use_reloader=False)