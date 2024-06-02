import pytest
from controllers.business_claim_controller import BusinessClaimController
from models import BusinessClaim
from database import db
from unittest import mock

# Create a fixture for the controller
@pytest.fixture
def controller():
    return BusinessClaimController()

# Test the submit_claim method
def test_submit_claim(controller):
    # Mock the form data
    controller.claim_form.business_id.data = 1
    controller.claim_form.owner_id.data = 1
    controller.claim_form.claim_status.data = 'pending'
    controller.claim_form.proof_documents.data = 'document.pdf'

    # Call the method and check the response for successful submission
    response, status_code = controller.submit_claim()
    assert status_code == 201
    assert response['message'] == 'Business claim submitted successfully.'

    # Test for validation failure
    controller.claim_form.business_id.data = None
    response, status_code = controller.submit_claim()
    assert status_code == 400
    assert response['message'] == 'Validation failed.'

    # Test for exception handling
    controller.claim_form.business_id.data = 1
    with pytest.raises(Exception):
        controller.submit_claim()

# Test the edit_claim method
def test_edit_claim(controller):
    # Create a claim for testing
    claim = BusinessClaim(business_id=1, owner_id=1, claim_status='pending', proof_documents='document.pdf')
    db.session.add(claim)
    db.session.commit()

    # Call the method and check the response for successful update
    response, status_code = controller.edit_claim(claim.id, 'approved')
    assert status_code == 200
    assert response['message'] == 'Claim status updated successfully.'

    # Test for claim not found
    response, status_code = controller.edit_claim(0, 'approved')
    assert status_code == 404
    assert response['message'] == 'Claim not found.'

    # Test for exception handling
    with pytest.raises(Exception):
        controller.edit_claim(claim.id, 'invalid_status')
        
    # Mock an exception during the claim update
    with mock.patch('models.BusinessClaim.query') as mock_query:
        mock_query.get.side_effect = Exception('Database error')
        response, status_code = controller.edit_claim(claim.id, 'invalid_status')
        assert status_code == 500
        assert response['error'] == 'Database error'

# Test the delete_claim method
def test_delete_claim(controller):
    # Create a claim for testing
    claim = BusinessClaim(business_id=1, owner_id=1, claim_status='pending', proof_documents='document.pdf')
    db.session.add(claim)
    db.session.commit()

    # Call the method and check the response for successful deletion
    response, status_code = controller.delete_claim(claim.id)
    assert status_code == 200
    assert response['message'] == 'Claim deleted successfully.'

    # Test for claim not found
    response, status_code = controller.delete_claim(0)
    assert status_code == 404
    assert response['message'] == 'Claim not found.'

    # Test for exception handling
    with pytest.raises(Exception):
        controller.delete_claim(claim.id)
        
    # Mock an exception during the claim deletion
    with mock.patch('models.BusinessClaim.query') as mock_query:
        mock_query.get.side_effect = Exception('Database error')
        response, status_code = controller.delete_claim(claim.id)
        assert status_code == 500
        assert response['error'] == 'Database error'
