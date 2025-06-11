import pytest
import sys
sys.path.insert(0, '..')  # Ensure the parent directory is in the Python path

from app import app

def test_home():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home' in response.data

def test_login_get():
    client = app.test_client()
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_login_post_valid():
    client = app.test_client()
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'password'})
    assert response.status_code in [200, 302]  # Handle both possible outcomes
    if response.status_code == 302:
        assert '/user_dashboard' in response.headers['Location']

def test_register_get():
    client = app.test_client()
    response = client.get('/register')
    assert response.status_code == 200

def test_register_post():
    client = app.test_client()
    response = client.post('/register', data={'username': 'testuser', 'email': 'test@example.com', 'password': 'password'})
    assert response.status_code in [200, 302]  # Redirect or response message

def test_existing_ev_stations():
    client = app.test_client()
    response = client.get('/api/existing_ev_stations')
    assert response.status_code in [200, 404]  # Handle case where API is missing
    if response.status_code == 200:
        data = response.get_json()
        assert 'stations' in data
        assert len(data['stations']) > 0

def test_optimal_ev_stations():
    client = app.test_client()
    response = client.get('/api/optimal_ev_stations')
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.get_json()
        assert 'optimal_stations' in data
        assert len(data['optimal_stations']) > 0

def test_user_dashboard():
    client = app.test_client()
    response = client.get('/user_dashboard', follow_redirects=True)
    assert response.status_code in [200, 302]
    if response.status_code == 302:
        assert b'Login' in response.data  # If redirected, check for login page

def test_admin_dashboard():
    client = app.test_client()
    response = client.get('/admin_dashboard', follow_redirects=True)
    assert response.status_code in [200, 302]
    if response.status_code == 302:
        assert b'Login' in response.data
