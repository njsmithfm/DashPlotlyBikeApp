import pandas as pd
from datetime import datetime, timedelta
import requests


BOROUGH_COLORS = {
    "Manhattan": "#58B4E9",
    "Brooklyn": "#009E74",
    "Queens": "#CD7AA7",
    "Bronx": "#F0E442",
    "Staten Island": "#E0862B",
}


DAYS = 30

today = datetime.now()
days_ago = today - timedelta(days=DAYS)
days_ago_str = days_ago.strftime("%Y-%m-%d")


def get_crash_data(days=DAYS):
    today = datetime.now()
    days_ago = today - timedelta(days=days)
    days_ago_str = days_ago.strftime("%Y-%m-%d")
    
    # base API url
    base_url = "https://data.cityofnewyork.us/resource/h9gi-nx95.json"
    
    # Create Injuries variable
    params_injured = {
        "$select": "crash_date, borough, latitude, longitude, number_of_cyclist_injured, number_of_cyclist_killed, contributing_factor_vehicle_1, vehicle_type_code1, vehicle_type_code2",
        "$where": f"number_of_cyclist_injured > 0 AND number_of_cyclist_killed = 0 AND crash_date >= '{days_ago_str}'",
        "$order": "crash_date DESC",
    }
    response_injured = requests.get(base_url, params=params_injured)
    data_injured = response_injured.json()
    

    if len(data_injured) > 0:
        NYC_BIKE_API_LINK_INJURED = pd.DataFrame(data_injured)
        # Drop NA only for columns that exist
        cols_to_check = [c for c in ['borough', 'latitude', 'longitude'] if c in NYC_BIKE_API_LINK_INJURED.columns]
        if cols_to_check:
            NYC_BIKE_API_LINK_INJURED = NYC_BIKE_API_LINK_INJURED.dropna(subset=cols_to_check).reset_index(drop=True)
    else:
 
        NYC_BIKE_API_LINK_INJURED = pd.DataFrame(columns=['crash_date', 'borough', 'latitude', 'longitude', 'number_of_cyclist_injured', 'number_of_cyclist_killed', 'contributing_factor_vehicle_1', 'vehicle_type_code1', 'vehicle_type_code2'])
    
    NYC_BIKE_API_LINK_INJURED["crash_date"] = pd.to_datetime(NYC_BIKE_API_LINK_INJURED["crash_date"])
    NYC_BIKE_API_LINK_INJURED = NYC_BIKE_API_LINK_INJURED.rename(
        columns={
            "crash_date": "Date",
            "borough": "Borough",
            "latitude": "Latitude",
            "longitude": "Longitude",
            "number_of_cyclist_injured": "Cyclists_Injured",
            "number_of_cyclist_killed": "Cyclists_Killed",
            "vehicle_type_code1": "Vehicle_1",
            "vehicle_type_code2": "Vehicle_2",
            "contributing_factor_vehicle_1": "Contributing_Factor",
        }
    )
    
    # Create Deaths variable
    params_killed = {
        "$select": "crash_date, borough, latitude, longitude, number_of_cyclist_injured, number_of_cyclist_killed, contributing_factor_vehicle_1, vehicle_type_code1, vehicle_type_code2",
        "$where": f"number_of_cyclist_killed > 0 AND crash_date >= '{days_ago_str}'",
        "$order": "crash_date DESC",
    }
    response_killed = requests.get(base_url, params=params_killed)
    data_killed = response_killed.json()
    

    # Handle empty results
    if len(data_killed) > 0:
        NYC_BIKE_API_LINK_KILLED = pd.DataFrame(data_killed)
        # Drop NA only for columns that exist
        cols_to_check = [c for c in ['borough', 'latitude', 'longitude'] if c in NYC_BIKE_API_LINK_KILLED.columns]
        if cols_to_check:
            NYC_BIKE_API_LINK_KILLED = NYC_BIKE_API_LINK_KILLED.dropna(subset=cols_to_check).reset_index(drop=True)
    else:
        # Create empty DataFrame with correct columns
        NYC_BIKE_API_LINK_KILLED = pd.DataFrame(columns=['crash_date', 'borough', 'latitude', 'longitude', 'number_of_cyclist_injured', 'number_of_cyclist_killed', 'contributing_factor_vehicle_1', 'vehicle_type_code1', 'vehicle_type_code2'])

    NYC_BIKE_API_LINK_KILLED["crash_date"] = pd.to_datetime(NYC_BIKE_API_LINK_KILLED["crash_date"])
    
    # Only rename columns that exist
    rename_map = {
        "crash_date": "Date",
        "borough": "Borough",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "number_of_cyclist_injured": "Cyclists_Injured",
        "number_of_cyclist_killed": "Cyclists_Killed",
        "vehicle_type_code1": "Vehicle_1",
        "vehicle_type_code2": "Vehicle_2",
        "contributing_factor_vehicle_1": "Contributing_Factor",
    }
    rename_map = {k: v for k, v in rename_map.items() if k in NYC_BIKE_API_LINK_KILLED.columns}
    NYC_BIKE_API_LINK_KILLED = NYC_BIKE_API_LINK_KILLED.rename(columns=rename_map)
    
    NYC_BIKE_API_LINK_INJURED["Borough"] = NYC_BIKE_API_LINK_INJURED["Borough"].str.title()
    if "Borough" in NYC_BIKE_API_LINK_KILLED.columns:
        NYC_BIKE_API_LINK_KILLED["Borough"] = NYC_BIKE_API_LINK_KILLED["Borough"].fillna("Unknown").str.title()
    else:
        NYC_BIKE_API_LINK_KILLED["Borough"] = "Unknown"
    
    return NYC_BIKE_API_LINK_INJURED, NYC_BIKE_API_LINK_KILLED
NYC_BIKE_API_LINK_INJURED, NYC_BIKE_API_LINK_KILLED = get_crash_data()


