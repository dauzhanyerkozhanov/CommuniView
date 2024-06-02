import pytest
from flask import json, jsonify
from backend import app
from controllers.platform_management_controller import PlatformManagementController
from controllers.user_authentication_controller import UserAuthenticationController
from flask_login import current_user

# Initialize controllers
platform_management_controller = PlatformManagementController()
user_authentication_controller = UserAuthenticationController()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_monitor(client):
    # Test the monitor route (happy scenario)
    response = client.get('/monitor')
    assert response.status_code == 200
    assert 'platform_stats' in json.loads(response.data)

    # Test the monitor route (unhappy scenario: unauthorized access)
    with app.test_request_context():
        current_user.is_authenticated = False
        response = client.get('/monitor')
        assert response.status_code == 401

def test_dashboard(client):
    # Test the dashboard route (happy scenario)
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert 'dashboard' in json.loads(response.data)

    # Test the dashboard route (unhappy scenario: unauthorized access)
    with app.test_request_context():
        current_user.is_authenticated = False
        response = client.get('/dashboard')
        assert response.status_code == 401

def test_execute_tasks(client):
    # Test the execute tasks route (happy scenario)
    response = client.post('/execute')
    assert response.status_code == 200
    assert 'result' in json.loads(response.data)

    # Test the execute tasks route (unhappy scenario: unauthorized access)
    with app.test_request_context():
        current_user.is_authenticated = False
        response = client.post('/execute')
        assert response.status_code == 401

def test_logout(client):
    # Test the logout route (happy scenario)
    response = client.post('/logout')
    assert response.status_code == 200
    assert 'response' in json.loads(response.data)

    # Test the logout route (unhappy scenario: unauthorized access)
    with app.test_request_context():
        current_user.is_authenticated = False
        response = client.post('/logout')
        assert response.status_code == 401
