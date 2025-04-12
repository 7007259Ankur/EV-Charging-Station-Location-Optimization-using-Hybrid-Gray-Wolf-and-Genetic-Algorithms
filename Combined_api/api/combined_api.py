from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import math

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname="EV",
        user="postgres",
        password="@Ankur7753",
        host="localhost",
        port="5432"
    )

# Root endpoint that lists all available endpoints
@app.route('/')
def index():
    endpoints = {
        "available_endpoints": {
            "potential_locations": "/api/potential_locations",
            "optimal_ev_stations": "/api/optimal_ev_stations",
            "existing_ev_stations": "/api/existing_ev_stations"
        }
    }
    return jsonify(endpoints)

# Existing EV stations
@app.route('/api/existing_ev_stations', methods=['GET'])
def get_existing_ev_stations():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, latitude, longitude, type FROM ev_stations")
        stations = cur.fetchall()
        return jsonify([{
            "name": row[0], 
            "latitude": float(row[1]), 
            "longitude": float(row[2]), 
            "type": row[3]
        } for row in stations])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Potential locations
@app.route('/api/potential_locations', methods=['GET'])
def get_potential_locations():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, latitude, longitude, type FROM potential_locations")
        locations = cur.fetchall()
        return jsonify([{
            "name": row[0], 
            "latitude": float(row[1]), 
            "longitude": float(row[2]), 
            "type": row[3]
        } for row in locations])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Optimal EV stations
@app.route('/api/optimal_ev_stations', methods=['GET'])
def get_optimal_ev_stations():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, latitude, longitude, type FROM optimal_ev_stations")
        stations = cur.fetchall()
        return jsonify([{
            "id": row[0],
            "name": row[1], 
            "latitude": float(row[2]), 
            "longitude": float(row[3]), 
            "type": row[4]
        } for row in stations])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    print("\n🚀 EV API Server running at http://127.0.0.1:5000")
    print("Available endpoints:")
    print("- /api/existing_ev_stations")
    print("- /api/potential_locations")
    print("- /api/optimal_ev_stations")
    print("- / (lists all endpoints)\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
