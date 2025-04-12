from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Import CORS to fix frontend access
import psycopg2
import math

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for frontend requests

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname="EV",
        user="postgres",
        password="@Ankur7753",
        host="localhost",
        port="5432"
    )

# Haversine formula to calculate distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# API to fetch 5 nearest EV stations
@app.route('/api/nearest_ev_stations', methods=['GET'])
def nearest_ev_stations():
    try:
        # ✅ Print received request parameters
        print("Received Query Params:", request.args)

        # ✅ Fetch latitude & longitude safely
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)

        print("Parsed Latitude:", latitude)
        print("Parsed Longitude:", longitude)

        # ❌ If missing, return an error
        if latitude is None or longitude is None:
            return jsonify({"error": "Missing or invalid latitude/longitude parameters"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, latitude, longitude, type FROM optimal_ev_stations")
        stations = cursor.fetchall()
        conn.close()  # ✅ Close connection

        # ✅ Calculate distances
        station_distances = [
            (row[0], row[1], row[2], row[3], row[4], haversine(latitude, longitude, row[2], row[3]))
            for row in stations
        ]
        station_distances.sort(key=lambda x: x[5])
        nearest_stations = station_distances[:5]

        return jsonify([
            {"id": s[0], "name": s[1], "latitude": s[2], "longitude": s[3], "type": s[4], "distance_km": round(s[5], 2)}
            for s in nearest_stations
        ])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5506)
