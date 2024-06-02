import pytest
from flask import Flask, json
from routes.business_update_routes import business_bp
from forms import BusinessUpdateForm
from unittest.mock import patch

# Create a new Flask application for testing
app = Flask(__name__)
app.register_blueprint(business_bp)

@pytest.fixture
def client():
    return app.test_client()

def test_update_business_form_success(client):
    # Mock form data
    form_data = {
        'business_id': 1,
        'name': 'Test Business',
        'address': '123 Test St',
        'phone_number': '1234567890',
        'category': 'Test Category',
        'description': 'This is a test business.',
        'business_hours': '9:00 AM - 5:00 PM'
    }
    # Send a POST request to the 'update_form' route
    response = client.post('/update_form', data=json.dumps(form_data), content_type='application/json')
    # Parse the response data
    response_data = json.loads(response.data)
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    # Assert that the response data contains a success message
    assert response_data['message'] == 'Business updated successfully.'

@patch('controllers.business_update_controller.BusinessUpdateController.submit_form')
def test_update_business_form_validation_error(mock_submit_form, client):
    # Mock form data with missing fields
    form_data = {
        'business_id': 1,
        'name': '',
        'address': '123 Test St',
        'phone_number': '1234567890',
        'category': 'Test Category',
        'description': 'This is a test business.',
        'business_hours': '9:00 AM - 5:00 PM'
    }
    mock_submit_form.return_value = ({'message': 'Form validation failed.'}, 400)
    # Send a POST request to the 'update_form' route
    response = client.post('/update_form', data=json.dumps(form_data), content_type='application/json')
    # Assert that the response status code is 400 (Bad Request)
    assert response.status_code == 400
    # Parse the response data
    response_data = json.loads(response.data)
    # Assert that the response data contains a validation error message
    assert response_data['message'] == 'Form validation failed.'

@patch('controllers.business_update_controller.BusinessUpdateController.submit_form')
def test_update_business_form_controller_error(mock_submit_form, client):
    # Mock form data
    form_data = {
        'business_id': 1,
        'name': 'Test Business',
        'address': '123 Test St',
        'phone_number': '1234567890',
        'category': 'Test Category',
        'description': 'This is a test business.',
        'business_hours': '9:00 AM - 5:00 PM'
    }
    mock_submit_form.return_value = ({'message': 'Internal server error.'}, 500)
    # Send a POST request to the 'update_form' route
    response = client.post('/update_form', data=json.dumps(form_data), content_type='application/json')
    # Assert that the response status code is 500 (Internal Server Error)
    assert response.status_code == 500
    # Parse the response data
    response_data = json.loads(response.data)
    # Assert that the response data contains an error message
    assert response_data['message'] == 'Internal server error.'
