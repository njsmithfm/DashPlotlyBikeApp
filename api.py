import pandas as pd
import requests

# NYC_BIKE_API_LINK is just the URL
from constants import NYC_BIKE_API_LINK

# Fetch data from the API
response = requests.get(NYC_BIKE_API_LINK)
data = response.json()

# Load into DataFrame
df = pd.DataFrame(data)

# Convert crash_date from string to datetime, then to integer format
if "crash_date" in df.columns:
    df["crash_date"] = pd.to_datetime(df["crash_date"], errors='coerce')  # Convert to datetime
    df["crash_date"] = df["crash_date"].dt.strftime('%Y%m%d').astype("Int64")  # Format as int YYYYMMDD

print(df.head())
