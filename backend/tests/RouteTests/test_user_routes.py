import pytest
from flask import json, jsonify
from backend.app import app
from backend.models import User
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_form(client):
    # Mock the form data
    data = {'username': 'test', 'email': 'test@example.com', 'password': 'test'}
    response = client.post('/register_form', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 201
    assert response.get_json() == {'message': 'User registered successfully.'}

    # Test for invalid form data
    invalid_data = {'username': '', 'email': 'invalid_email', 'password': ''}
    response = client.post('/register_form', data=json.dumps(invalid_data), content_type='application/json')
    assert response.status_code == 400
    assert 'errors' in response.get_json()

def test_login(client):
    # Mock the form data
    data = {'username': 'test', 'password': 'test'}
    response = client.post('/login', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

    # Test for invalid form data
    invalid_data = {'username': 'invalid', 'password': 'invalid'}
    response = client.post('/login', data=json.dumps(invalid_data), content_type='application/json')
    assert response.status_code == 400
    assert 'errors' in response.get_json()

def test_logout(client):
    # Mock the form data
    data = {'username': 'test', 'password': 'test'}
    client.post('/login', data=json.dumps(data), content_type='application/json')
    response = client.get('/logout')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Logged out successfully.'}

def test_register_form_duplicate_username(client):
    # Mock the form data
    data = {'username': 'test', 'email': 'test@example.com', 'password': 'test'}
    client.post('/register_form', data=json.dumps(data), content_type='application/json')

    # Attempt to register with the same username
    response = client.post('/register_form', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    assert 'errors' in response.get_json()

def test_register_form_duplicate_email(client):
    # Mock the form data
    data = {'username': 'test', 'email': 'test@example.com', 'password': 'test'}
    client.post('/register_form', data=json.dumps(data), content_type='application/json')

    # Attempt to register with the same email
    data = {'username': 'test2', 'email': 'test@example.com', 'password': 'test'}
    response = client.post('/register_form', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    assert 'errors' in response.get_json()
