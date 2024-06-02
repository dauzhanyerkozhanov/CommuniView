import pytest
from unittest.mock import patch
from controllers.user_registration_controller import UserRegistrationController
from forms import RegistrationForm
from models import User
from database import db

# Instantiate the controller
controller = UserRegistrationController()

def test_submit_form_success():
    """
    Test successful form submission
    """
    # Mock the form data
    controller.registration_form = RegistrationForm(data={'username': 'test', 'email': 'test@example.com', 'password': 'test'})
    # Test successful form submission
    with patch('flask_mail.Message') as mock_message:
        response, status = controller.submit_form()
        assert status == 201
        assert response == {'message': 'User registered successfully.'}
        mock_message.assert_called_once()
    # Clean up the test user
    User.query.filter_by(username='test').delete()
    db.session.commit()

def test_submit_form_validation_failure():
    """
    Test form submission with invalid data
    """
    # Mock the form data with invalid email
    controller.registration_form = RegistrationForm(data={'username': 'test', 'email': 'invalid_email', 'password': 'test'})
    # Test form submission with invalid data
    response, status = controller.submit_form()
    assert status == 400
    assert response == {'message': 'Validation failed.'}

def test_submit_form_exception():
    """
    Test form submission with an exception
    """
    # Mock the form data
    controller.registration_form = RegistrationForm(data={'username': 'test', 'email': 'test@example.com', 'password': 'test'})
    # Patch the session commit to raise an exception
    with patch.object(db.session, 'commit', side_effect=Exception('Database error')):
        response, status = controller.submit_form()
        assert status == 500
        assert response == {'error': 'Database error'}

def test_init():
    """
    Test the initialization of the UserRegistrationController
    """
    controller = UserRegistrationController()
    assert isinstance(controller.registration_form, RegistrationForm)
