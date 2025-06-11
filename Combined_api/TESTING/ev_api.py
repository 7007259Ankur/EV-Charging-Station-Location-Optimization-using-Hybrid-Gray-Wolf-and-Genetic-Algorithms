from flask import Flask, jsonify, request
import math

app = Flask(__name__)

# Enhanced mock data for existing EV stations
existing_stations = [
    {"id": 1, "name": "Station A", "latitude": 28.7041, "longitude": 77.1025, "capacity": 4, "available": 2},
    {"id": 2, "name": "Station B", "latitude": 28.6141, "longitude": 77.2025, "capacity": 6, "available": 3},
    {"id": 3, "name": "Station C", "latitude": 28.6541, "longitude": 77.1525, "capacity": 8, "available": 5},
    {"id": 4, "name": "Station D", "latitude": 28.7241, "longitude": 77.0825, "capacity": 4, "available": 1},
    {"id": 5, "name": "Station E", "latitude": 28.6941, "longitude": 77.1325, "capacity": 10, "available": 7},
    {"id": 6, "name": "Station F", "latitude": 28.6341, "longitude": 77.1725, "capacity": 6, "available": 4}
]

# Enhanced mock data for potential locations
potential_locations = [
    {"id": 1, "name": "Location X", "latitude": 28.7141, "longitude": 77.1125, "demand_score": 85},
    {"id": 2, "name": "Location Y", "latitude": 28.6241, "longitude": 77.2125, "demand_score": 72},
    {"id": 3, "name": "Location Z", "latitude": 28.6641, "longitude": 77.1625, "demand_score": 91}
]

# Enhanced mock data for optimal stations
optimal_stations = [
    {"id": 1, "name": "Optimal Station 1", "latitude": 28.7141, "longitude": 77.1125, "priority": "high"},
    {"id": 2, "name": "Optimal Station 2", "latitude": 28.6641, "longitude": 77.1625, "priority": "medium"},
    {"id": 3, "name": "Optimal Station 3", "latitude": 28.6241, "longitude": 77.2125, "priority": "low"}
]

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates using Haversine formula"""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return 6371 * 2 * math.asin(math.sqrt(a))  # Earth radius in km

@app.route('/api/existing_ev_stations', methods=['GET'])
def get_existing_ev_stations():
    """Return all existing EV stations"""
    return jsonify({
        "success": True,
        "count": len(existing_stations),
        "stations": existing_stations
    })

@app.route('/api/potential_locations', methods=['GET'])
def get_potential_locations():
    """Return all potential locations"""
    return jsonify({
        "success": True,
        "count": len(potential_locations),
        "locations": potential_locations
    })

@app.route('/api/get_optimal_ev_stations', methods=['GET'])
def get_optimal_ev_stations():
    """Return optimal locations for new stations"""
    return jsonify({
        "success": True,
        "count": len(optimal_stations),
        "stations": optimal_stations
    })

@app.route('/api/nearest_ev_stations', methods=['GET'])
def get_nearest_ev_stations():
    """Return nearest EV stations to given coordinates"""
    try:
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "error": "Invalid latitude or longitude parameters"
        }), 400
    
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        return jsonify({
            "success": False,
            "error": "Coordinates out of valid range"
        }), 400
    
    # Calculate distances and sort stations
    stations_with_distances = [
        {**station, "distance": calculate_distance(latitude, longitude, station['latitude'], station['longitude'])}
        for station in existing_stations
    ]
    nearest_stations = sorted(stations_with_distances, key=lambda x: x['distance'])[:5]
    
    return jsonify({
        "success": True,
        "count": len(nearest_stations),
        "stations": nearest_stations
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001, debug=True)