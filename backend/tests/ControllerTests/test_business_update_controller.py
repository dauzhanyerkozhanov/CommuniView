import pytest
from controllers.business_update_controller import BusinessUpdateController
from models import Business
from database import db

# Create a fixture for the controller
@pytest.fixture
def controller():
    return BusinessUpdateController()

# Test the submit_form method
def test_submit_form(controller, mocker):
    # Mock the form data
    controller.update_form.business_id.data = 'testBusiness'
    controller.update_form.name.data = 'Updated Business'
    controller.update_form.address.data = '123 Test St'
    controller.update_form.phone_number.data = '123-456-7890'
    controller.update_form.category.data = 'Test Category'
    controller.update_form.description.data = 'This is a test business'
    controller.update_form.business_hours.data = '9-5'

    # Mock the database query
    mock_business = mocker.Mock(spec=Business)
    mocker.patch('controllers.business_update_controller.Business.query.get', return_value=mock_business)

    # Call the method and check the response
    response, status_code = controller.submit_form()
    assert status_code == 200
    assert response['message'] == 'Business updated successfully.'

    # Test the case where the business does not exist
    mocker.patch('controllers.business_update_controller.Business.query.get', return_value=None)
    response, status_code = controller.submit_form()
    assert status_code == 404
    assert response['message'] == 'Business not found.'

    # Test the case where an exception occurs
    mocker.patch('controllers.business_update_controller.Business.query.get', side_effect=Exception('Test exception'))
    response, status_code = controller.submit_form()
    assert status_code == 500
    assert response['error'] == 'Test exception'

    # Test the case where form validation fails
    mocker.patch('controllers.business_update_controller.BusinessUpdateForm.validate_on_submit', return_value=False)
    response, status_code = controller.submit_form()
    assert status_code == 400
    assert response['message'] == 'Validation failed.'
