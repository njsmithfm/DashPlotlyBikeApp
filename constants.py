import pandas as pd
import api
# from api import NYC_BIKE_API_LINK

from datetime import datetime, timedelta
import requests

# Calculate the date 30 days ago from today
today = datetime.now()
thirty_days_ago = today - timedelta(days=30)
thirty_days_ago_str = thirty_days_ago.strftime('%Y-%m-%d')

# Use the Socrata Query Language (SoQL) with proper URL structure
base_url = "https://data.cityofnewyork.us/resource/h9gi-nx95.json"

# Build parameters dict - this handles proper URL encoding
params = {
    "$select": "crash_date, borough, latitude, longitude, number_of_cyclist_injured, number_of_cyclist_killed, contributing_factor_vehicle_1, vehicle_type_code1, vehicle_type_code2",
    "$where": f"number_of_cyclist_injured > 0 AND crash_date >= '{thirty_days_ago_str}'",
    "$order": "crash_date DESC"
}

# Make the request
response = requests.get(base_url, params=params)

# Convert to DataFrame
NYC_BIKE_API_LINK = pd.DataFrame(response.json())

# Convert crash_date to datetime
NYC_BIKE_API_LINK["crash_date"] = pd.to_datetime(NYC_BIKE_API_LINK["crash_date"])

# Rename columns
NYC_BIKE_API_LINK = NYC_BIKE_API_LINK.rename(
    columns={
        "crash_date": "Date",
        "borough": "Borough",
        "latitude": "Latitude",
        "number_of_cyclist_killed": "Cyclists_Killed",
        "longitude": "Longitude",
        "number_of_cyclist_injured": "Cyclists_Injured",
        "vehicle_type_code1": "Vehicle_1",
        "vehicle_type_code2": "Vehicle_2",
        "contributing_factor_vehicle_1": "Contributing_Factor",
    }
)

days = 30

