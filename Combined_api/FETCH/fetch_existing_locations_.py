import requests
import csv

# Google API Key (Replace with your own API key)
API_KEY = "AIzaSyDqC7hVN3khlGg8DiDfJJLiw_5acWS3U30"

latitude = 26.080674618890548 
longitude = 91.5581063516589 
radius = 100000 



# Type: EV Charging Stations
place_type = "charging_station"

# Google Places API URL
url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&keyword=EV+Charging+Station&type=charging_station&key={API_KEY}"



# API Request
response = requests.get(url)
data = response.json()

# Save results to CSV
csv_filename = "ev_stations.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Latitude", "Longitude", "Address"])  # CSV Header

    # Process API Response
    if "results" in data:
        for place in data["results"]:
            name = place.get("name", "N/A")
            lat = place["geometry"]["location"]["lat"]
            lon = place["geometry"]["location"]["lng"]
            address = place.get("vicinity", "N/A")
            writer.writerow([name, lat, lon, address])
            print(f"📍 {name} - {address} ({lat}, {lon})")

print(f"✅ EV Charging Stations data saved to {csv_filename}")
