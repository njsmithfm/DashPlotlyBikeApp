import pandas as pd
from datetime import datetime, timedelta
import requests

DAYS = 30

today = datetime.now()
thirty_days_ago = today - timedelta(days=30)
thirty_days_ago_str = thirty_days_ago.strftime("%Y-%m-%d")

# base API url
base_url = "https://data.cityofnewyork.us/resource/h9gi-nx95.json"

BOROUGH_COLORS = {
    "Manhattan": "rgb(208, 28, 139)",
    "Brooklyn": "rgb(49, 163, 84)",
    "Queens": "rgb(94,60,153)",
    "Bronx": "rgb(5,113,176)",
    "Staten Island": "rgb(184,225,134)",
}


# Create Injuries variable
params_injured = {
    "$select": "crash_date, borough, latitude, longitude, number_of_cyclist_injured, number_of_cyclist_killed, contributing_factor_vehicle_1, vehicle_type_code1, vehicle_type_code2",
    "$where": f"number_of_cyclist_injured > 0 AND number_of_cyclist_killed = 0 AND crash_date >= '{thirty_days_ago_str}'",
    "$order": "crash_date DESC",
}
response_injured = requests.get(base_url, params=params_injured)
NYC_BIKE_API_LINK_INJURED = pd.DataFrame(response_injured.json())
NYC_BIKE_API_LINK_INJURED["crash_date"] = pd.to_datetime(
    NYC_BIKE_API_LINK_INJURED["crash_date"]
)
NYC_BIKE_API_LINK_INJURED = NYC_BIKE_API_LINK_INJURED.rename(
    columns={
        "crash_date": "Date",
        "borough": "Borough",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "number_of_cyclist_injured": "Cyclists_Injured",
        "vehicle_type_code1": "Vehicle_1",
        "vehicle_type_code2": "Vehicle_2",
        "contributing_factor_vehicle_1": "Contributing_Factor",
    }
)

# Create Deaths variable
params_killed = {
    "$select": "crash_date, borough, latitude, longitude, number_of_cyclist_injured, number_of_cyclist_killed, contributing_factor_vehicle_1, vehicle_type_code1, vehicle_type_code2",
    "$where": f"number_of_cyclist_injured > 0 AND number_of_cyclist_killed = 0 AND crash_date >= '{thirty_days_ago_str}'",
    "$order": "crash_date DESC",
}
response_killed = requests.get(base_url, params=params_killed)
NYC_BIKE_API_LINK_KILLED = pd.DataFrame(response_killed.json())
NYC_BIKE_API_LINK_KILLED["crash_date"] = pd.to_datetime(
    NYC_BIKE_API_LINK_KILLED["crash_date"]
)
NYC_BIKE_API_LINK_KILLED = NYC_BIKE_API_LINK_KILLED.rename(
    columns={
        "crash_date": "Date",
        "borough": "Borough",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "number_of_cyclist_injured": "Cyclists_Injured",
        "vehicle_type_code1": "Vehicle_1",
        "vehicle_type_code2": "Vehicle_2",
        "contributing_factor_vehicle_1": "Contributing_Factor",
    }
)

NYC_BIKE_API_LINK_INJURED["Borough"] = NYC_BIKE_API_LINK_INJURED["Borough"].str.title()
NYC_BIKE_API_LINK_KILLED["Borough"] = NYC_BIKE_API_LINK_KILLED["Borough"].str.title()
