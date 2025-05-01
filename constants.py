import pandas as pd
from datetime import datetime, timedelta
import requests

# Set 30 day timeframe
today = datetime.now()
thirty_days_ago = today - timedelta(days=30)
thirty_days_ago_str = thirty_days_ago.strftime('%Y-%m-%d')

base_url = "https://data.cityofnewyork.us/resource/h9gi-nx95.json"

params = {
    "$select": "crash_date, borough, latitude, longitude, number_of_cyclist_injured, number_of_cyclist_killed, contributing_factor_vehicle_1, vehicle_type_code1, vehicle_type_code2",
    "$where": f"number_of_cyclist_injured > 0 AND crash_date >= '{thirty_days_ago_str}'",
    "$order": "crash_date DESC"
}

response = requests.get(base_url, params=params)

NYC_BIKE_API_LINK = pd.DataFrame(response.json())

NYC_BIKE_API_LINK["crash_date"] = pd.to_datetime(NYC_BIKE_API_LINK["crash_date"])

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

