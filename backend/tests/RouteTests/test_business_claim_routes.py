import pytest
from flask import Flask, jsonify
from unittest.mock import patch
from routes.business_claim_routes import business_claim_bp
from controllers.business_claim_controller import BusinessClaimController
from forms import BusinessClaimForm

# Create a new Flask application for testing
app = Flask(__name__)
app.register_blueprint(business_claim_bp)

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Mock the BusinessClaimController
@pytest.fixture
def mock_controller():
    with patch('business_claim_routes.business_claim_controller') as mock_controller:
        yield mock_controller

def test_submit_claim(client, mock_controller):
    # Mock form data
    form_data = {
        'business_id': 1,
        'owner_id': 1,
        'claim_status': 'pending',
        'proof_documents': 'document.pdf'
    }

    # Mock the submit_claim method
    mock_controller.submit_claim.return_value = jsonify({'message': 'Claim submitted successfully'}), 200

    # Send a POST request to the 'submit_claim' route
    response = client.post('/submit_claim', data=form_data)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    assert response.json == {'message': 'Claim submitted successfully'}

    # Test for invalid form data
    invalid_form_data = {
        'business_id': 1,
        'owner_id': 1,
        'claim_status': 'invalid_status',
        'proof_documents': 'document.pdf'
    }
    form = BusinessClaimForm(invalid_form_data)
    form.validate.return_value = False
    form.errors = {'claim_status': ['Invalid claim status']}

    # Send a POST request with invalid form data
    response = client.post('/submit_claim', data=invalid_form_data)

    # Assert that the response status code is 400 (Bad Request)
    assert response.status_code == 400
    assert response.json == {'errors': {'claim_status': ['Invalid claim status']}}

def test_edit_claim(client, mock_controller):
    # Mock form data
    form_data = {
        'business_id': 1,
        'owner_id': 1,
        'claim_status': 'approved',
        'proof_documents': 'document.pdf'
    }

    # Mock the edit_claim method
    mock_controller.edit_claim.return_value = jsonify({'message': 'Claim edited successfully'}), 200

    # Send a PUT request to the 'edit_claim' route
    response = client.put('/edit_claim/1', data=form_data, json={'new_status': 'approved'})

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    assert response.json == {'message': 'Claim edited successfully'}

    # Test for invalid claim ID
    mock_controller.edit_claim.return_value = jsonify({'error': 'Claim not found'}), 404

    # Send a PUT request with an invalid claim ID
    response = client.put('/edit_claim/999', data=form_data, json={'new_status': 'approved'})

    # Assert that the response status code is 404 (Not Found)
    assert response.status_code == 404
    assert response.json == {'error': 'Claim not found'}

def test_delete_claim(client, mock_controller):
    # Mock the delete_claim method
    mock_controller.delete_claim.return_value = jsonify({'message': 'Claim deleted successfully'}), 200

    # Send a DELETE request to the 'delete_claim' route
    response = client.delete('/delete_claim/1')

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    assert response.json == {'message': 'Claim deleted successfully'}

    # Test for invalid claim ID
    mock_controller.delete_claim.return_value = jsonify({'error': 'Claim not found'}), 404

    # Send a DELETE request with an invalid claim ID
    response = client.delete('/delete_claim/999')

    # Assert that the response status code is 404 (Not Found)
    assert response.status_code == 404
    assert response.json == {'error': 'Claim not found'}