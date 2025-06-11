from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import math

app = Flask(__name__)
CORS(app)

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname="EV",
        user="postgres",
        password="@Ankur7753",
        host="localhost",
        port="5432"
    )

# Route 1: Fetch existing EV stations
@app.route('/api/existing_ev_stations', methods=['GET'])
def get_ev_stations():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, latitude, longitude, type FROM ev_stations")
        stations = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{ "name": row[0], "latitude": row[1], "longitude": row[2], "type": row[3] } for row in stations])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route 2: Fetch potential locations
@app.route('/api/potential_locations', methods=['GET'])
def get_potential_locations():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, latitude, longitude, type FROM potential_locations")
        locations = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{ "name": row[0], "latitude": row[1], "longitude": row[2], "type": row[3] } for row in locations])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route 3: Fetch optimal EV stations for heatmap
@app.route('/api/get_optimal_ev_stations', methods=['GET'])
def get_optimal_ev_stations():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, latitude, longitude, type FROM optimal_ev_stations")
        stations = cursor.fetchall()
        conn.close()
        return jsonify([{ "id": row[0], "name": row[1], "latitude": row[2], "longitude": row[3], "type": row[4] } for row in stations])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route 4: Find nearest EV stations using Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route('/api/nearest_ev_stations', methods=['GET'])
def nearest_ev_stations():
    try:
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        if latitude is None or longitude is None:
            return jsonify({"error": "Missing or invalid latitude/longitude parameters"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, latitude, longitude, type FROM optimal_ev_stations")
        stations = cursor.fetchall()
        conn.close()

        station_distances = [(row[0], row[1], row[2], row[3], row[4], haversine(latitude, longitude, row[2], row[3])) for row in stations]
        station_distances.sort(key=lambda x: x[5])
        nearest_stations = station_distances[:5]

        return jsonify([{ "id": s[0], "name": s[1], "latitude": s[2], "longitude": s[3], "type": s[4], "distance_km": round(s[5], 2) } for s in nearest_stations])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("\n🚀 Merged EV Stations API is running at: http://127.0.0.1:6001")
    app.run(debug=True, host="0.0.0.0", port=6001)
