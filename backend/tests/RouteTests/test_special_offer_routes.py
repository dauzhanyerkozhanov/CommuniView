import pytest
from flask import json
import app, database
from models import SpecialOffer, Business
from werkzeug.exceptions import BadRequest, NotFound
from controllers.special_offer_controller import SpecialOfferController
from datetime import datetime, timedelta

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_special_offer(client):
    # Test data for successful creation
    valid_data = {
        'title': 'Test Offer',
        'description': 'This is a test offer',
        'expiration_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
        'associated_business': 'Test Business'
    }

    # Send a POST request to the 'offers' route with valid data
    response = client.post('/offers', data=json.dumps(valid_data), content_type='application/json')
    assert response.status_code == 201

    # Test data for invalid form data
    invalid_data = {
        'title': '',
        'description': 'This is a test offer',
        'expiration_date': 'invalid_date',
        'associated_business': 'Test Business'
    }

    # Send a POST request to the 'offers' route with invalid data
    response = client.post('/offers', data=json.dumps(invalid_data), content_type='application/json')
    assert response.status_code == 400

def test_update_special_offer(client):
    # Test data for successful update
    valid_data = {
        'title': 'Updated Test Offer',
        'description': 'This is an updated test offer',
        'expiration_date': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')
    }

    # Send a PUT request to the 'offers' route with an offer_id of 1 and valid data
    response = client.put('/offers/1', data=json.dumps(valid_data), content_type='application/json')
    assert response.status_code == 200

    # Test data for invalid form data
    invalid_data = {
        'title': '',
        'description': 'This is an updated test offer',
        'expiration_date': 'invalid_date'
    }

    # Send a PUT request to the 'offers' route with an offer_id of 1 and invalid data
    response = client.put('/offers/1', data=json.dumps(invalid_data), content_type='application/json')
    assert response.status_code == 400

    # Test for non-existent offer
    response = client.put('/offers/999', data=json.dumps(valid_data), content_type='application/json')
    assert response.status_code == 404

def test_delete_special_offer(client):
    # Send a DELETE request to the 'offers' route with an offer_id of 1
    response = client.delete('/offers/1')
    assert response.status_code == 204

    # Test for non-existent offer
    response = client.delete('/offers/999')
    assert response.status_code == 404

def test_get_special_offer(client):
    # Send a GET request to the 'offers' route with an offer_id of 1
    response = client.get('/offers/1')
    assert response.status_code == 200

    # Test for non-existent offer
    response = client.get('/offers/999')
    assert response.status_code == 404

def test_get_offers_for_business(client):
    # Send a GET request to the 'offers/business/1' route
    response = client.get('/offers/business/1')
    assert response.status_code == 200

    # Test for non-existent business
    response = client.get('/offers/business/999')
    assert response.status_code == 404

def test_get_expired_offers(client):
    # Send a GET request to the 'offers/expired' route
    response = client.get('/offers/expired')
    assert response.status_code == 200

def test_get_active_offers(client):
    # Send a GET request to the 'offers/active' route
    response = client.get('/offers/active')
    assert response.status_code == 200
