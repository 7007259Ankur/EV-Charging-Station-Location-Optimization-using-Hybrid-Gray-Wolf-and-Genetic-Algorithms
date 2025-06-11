import requests
import csv

# Google API Key
API_KEY = "AIzaSyDqC7hVN3khlGg8DiDfJJLiw_5acWS3U30"

# Location: Guwahati (Latitude, Longitude)
location = "26.080674618890548, 91.5581063516589"

# Search radius (in meters)
radius = 100000  # 100 km

# Place types to search for
place_types = {
    "universities": "university",
    "shopping_malls": "shopping_mall",
    "supermarkets": "supermarket",
    "hotels": "hotel",
    "parks": "park",
    "parking_spots": "parking",
    "petrol_pumps": "gas_station",
    "railway_stations": "train_station",
    "airports": "airport"
}

# CSV File to store results
csv_filename = "potential.csv"

# Open CSV file for writing
with open("output.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)
    writer.writerow(["name", "latitude", "longitude", "type"])  # CSV Header

    # Fetch data for each place type
    for category, place_type in place_types.items():
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={place_type}&key={API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        # Debug: Print API response
        print(f"Response for {category}: {data}")

        # If API response has results
        if "results" in data:
            for place in data["results"]:
                name = place["name"]
                lat = place["geometry"]["location"]["lat"]
                lon = place["geometry"]["location"]["lng"]
                writer.writerow([name, lat, lon, category])

print(f"✅ Data saved to {csv_filename}")
