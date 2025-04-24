import pandas as pd

NYC_BIKE_API_LINK = pd.read_json(
    "https://data.cityofnewyork.us/resource/h9gi-nx95.json"
)


NYC_BIKE_API_LINK["crash_date"] = pd.to_datetime(NYC_BIKE_API_LINK["crash_date"])

NYC_BIKE_API_LINK = NYC_BIKE_API_LINK.rename(columns={'crash_date': 'Date',
                                                      'borough': 'Borough',
                                                      'latitude': 'Latitude',
                                                      'longitude': 'Longitude',
                                                      'number_of_cyclist_injured': 'Cyclists_Injured',
                                                      'vehicle_type_code1': 'Vehicle_1',
                                                      'vehicle_type_code2': 'Vehicle_2',
                                                      'contributing_factor_vehicle_1': 'Contributing_Factor'
                                                      })

print(NYC_BIKE_API_LINK.head())
# print(NYC_BIKE_API_LINK.columns)