import pytest
import requests
import math

BASE_URL = "http://127.0.0.1:6001"

def calculate_distance(lat1, lon1, lat2, lon2):
    """Test implementation of distance calculation"""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return 6371 * 2 * math.asin(math.sqrt(a))

def test_existing_ev_stations():
    """Test existing EV stations endpoint"""
    response = requests.get(f"{BASE_URL}/api/existing_ev_stations")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['count'], int)
    assert isinstance(data['stations'], list)
    assert len(data['stations']) == data['count']
    assert all('id' in station and 'name' in station for station in data['stations'])

def test_potential_locations():
    """Test potential locations endpoint"""
    response = requests.get(f"{BASE_URL}/api/potential_locations")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['count'], int)
    assert isinstance(data['locations'], list)
    assert len(data['locations']) == data['count']
    assert all('demand_score' in loc for loc in data['locations'])

def test_optimal_ev_stations():
    """Test optimal EV stations endpoint"""
    response = requests.get(f"{BASE_URL}/api/get_optimal_ev_stations")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['count'], int)
    assert isinstance(data['stations'], list)
    assert len(data['stations']) == data['count']
    assert all(station['priority'] in ['high', 'medium', 'low'] for station in data['stations'])

def test_nearest_ev_stations():
    """Test nearest EV stations with valid parameters"""
    test_coords = (28.7041, 77.1025)
    response = requests.get(
        f"{BASE_URL}/api/nearest_ev_stations",
        params={'latitude': test_coords[0], 'longitude': test_coords[1]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['count'], int)
    assert data['count'] <= 5
    assert isinstance(data['stations'], list)
    
    if data['count'] > 1:
        distances = [s['distance'] for s in data['stations']]
        assert all(distances[i] <= distances[i+1] for i in range(len(distances)-1))

def test_nearest_ev_stations_no_params():
    """Test nearest EV stations without parameters"""
    response = requests.get(f"{BASE_URL}/api/nearest_ev_stations")
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert 'error' in data

def test_nearest_ev_stations_invalid_coords():
    """Test nearest EV stations with invalid coordinates"""
    invalid_tests = [
        {'latitude': 'abc', 'longitude': 77.1025},
        {'latitude': 28.7041, 'longitude': 'xyz'},
        {'latitude': 91, 'longitude': 77.1025},
        {'latitude': 28.7041, 'longitude': 181}
    ]
    
    for params in invalid_tests:
        response = requests.get(f"{BASE_URL}/api/nearest_ev_stations", params=params)
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert 'error' in data

if __name__ == "__main__":
    pytest.main(["-v", "--cov=.", "--cov-report=term-missing"])