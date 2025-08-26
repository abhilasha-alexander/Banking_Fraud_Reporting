import pandas as pd
import requests
from openpyxl import Workbook
import time

# Load the CSV file
df = pd.read_csv("Location_data.csv")  # replace with your actual file name
df["Location"] = ""

# Function to get location from latitude and longitude using Nominatim
def reverse_geocode(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse"
        params = {
            'format': 'jsonv2',
            'lat': lat,
            'lon': lon,
            'zoom': 10,
            'addressdetails': 1
        }
        headers = {
            'User-Agent': 'GeoLocator/1.0'  # Nominatim requires a User-Agent header
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("display_name", "Unknown")
        else:
            return "Not Found"
    except Exception as e:
        return "Error"

# Iterate through rows and apply reverse geocoding
for i, row in df.iterrows():
    lat = row["Latitude"]
    lon = row["Longitude"]
    location = reverse_geocode(lat, lon)
    df.at[i, "Location"] = location
    time.sleep(1)  # Be polite and avoid hitting rate limits

# Save the result to Excel
df.to_excel("locations_from_coordinates.xlsx", index=False)
print("Done! File saved as locations_from_coordinates.xlsx")