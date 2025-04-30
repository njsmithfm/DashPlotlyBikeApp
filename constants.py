import pandas as pd
import api
from api import NYC_BIKE_API_LINK




# NYC_BIKE_API_LINK = pd.read_json(
#     "https://data.cityofnewyork.us/resource/h9gi-nx95.json?$query=SELECT%0A%20%20%60crash_date%60%2C%0A%20%20%60crash_time%60%2C%0A%20%20%60borough%60%2C%0A%20%20%60zip_code%60%2C%0A%20%20%60latitude%60%2C%0A%20%20%60longitude%60%2C%0A%20%20%60location%60%2C%0A%20%20%60on_street_name%60%2C%0A%20%20%60off_street_name%60%2C%0A%20%20%60cross_street_name%60%2C%0A%20%20%60number_of_persons_injured%60%2C%0A%20%20%60number_of_persons_killed%60%2C%0A%20%20%60number_of_pedestrians_injured%60%2C%0A%20%20%60number_of_pedestrians_killed%60%2C%0A%20%20%60number_of_cyclist_injured%60%2C%0A%20%20%60number_of_cyclist_killed%60%2C%0A%20%20%60number_of_motorist_injured%60%2C%0A%20%20%60number_of_motorist_killed%60%2C%0A%20%20%60contributing_factor_vehicle_1%60%2C%0A%20%20%60contributing_factor_vehicle_2%60%2C%0A%20%20%60contributing_factor_vehicle_3%60%2C%0A%20%20%60contributing_factor_vehicle_4%60%2C%0A%20%20%60contributing_factor_vehicle_5%60%2C%0A%20%20%60collision_id%60%2C%0A%20%20%60vehicle_type_code1%60%2C%0A%20%20%60vehicle_type_code2%60%2C%0A%20%20%60vehicle_type_code_3%60%2C%0A%20%20%60vehicle_type_code_4%60%2C%0A%20%20%60vehicle_type_code_5%60%0AWHERE%20%60number_of_cyclist_injured%60%20%3E%200%0AORDER%20BY%20%60crash_date%60%20DESC%20NULL%20LAST"
# )

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
NYC_BIKE_API_LINK = NYC_BIKE_API_LINK[
    [
        "Date",
        "Borough",
        "Latitude",
        "Longitude",
        "Cyclists_Injured",
        "Cyclists_Killed",
        "Contributing_Factor",
        "Vehicle_1",
        "Vehicle_2",
    ]
]


days = 30

