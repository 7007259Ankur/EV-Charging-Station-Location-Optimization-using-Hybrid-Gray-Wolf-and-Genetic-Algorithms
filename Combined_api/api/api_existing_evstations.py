from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS globally

def get_db_connection():
    return psycopg2.connect(
        dbname="EV",
        user="postgres",
        password="@Ankur7753",
        host="localhost",
        port="5432"
    )

@app.route('/', methods=['GET'])  # Root endpoint now returns EV stations data
def get_ev_stations():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, latitude, longitude, type FROM ev_stations")
        stations = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{"name": row[0], "latitude": row[1], "longitude": row[2], "type": row[3]} for row in stations])
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error response if DB fails

if __name__ == '__main__':
    print("\n🚀 EV Stations API is running at: http://127.0.0.1:5001\n")
    app.run(debug=True, host="0.0.0.0", port=5001)  # Runs on all network interfaces
