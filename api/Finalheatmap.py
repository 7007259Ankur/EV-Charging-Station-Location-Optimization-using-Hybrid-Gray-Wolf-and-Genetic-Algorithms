from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS globally

# Function to connect to PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        dbname="EV",  # Update if your database name is different
        user="postgres",       # Your PostgreSQL username
        password="@Ankur7753", # Your PostgreSQL password
        host="localhost",      # Change to your DB server IP if not running locally
        port="5432"            # Default PostgreSQL port
    )

# API endpoint to fetch optimal EV stations
@app.route('/api/get_optimal_ev_stations', methods=['GET'])
def get_ev_stations():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, latitude, longitude, type FROM optimal_ev_stations")
        stations = cursor.fetchall()
        conn.close()

        # Convert result to JSON format
        return jsonify([
            {"id": row[0], "name": row[1], "latitude": row[2], "longitude": row[3], "type": row[4]}
            for row in stations
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error response if DB connection fails

if __name__ == '__main__':
    print("\n🚀 EV Stations API is running at: http://127.0.0.1:5002/api/get_optimal_ev_stations\n")
    app.run(debug=True, host="0.0.0.0", port=5002)  # Running on port 5002
