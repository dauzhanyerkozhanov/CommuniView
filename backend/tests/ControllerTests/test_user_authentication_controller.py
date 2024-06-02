import pytest
from controllers.user_authentication_controller import UserAuthenticationController
from models import User
from werkzeug.security import generate_password_hash
from flask_login import current_user

# Instantiate the controller
controller = UserAuthenticationController()

def setup_module(module):
    # Create a test user
    test_user = User(username='test', password=generate_password_hash('test'))
    test_user.save()

def teardown_module(module):
    # Delete the test user
    User.query.filter_by(username='test').delete()

def test_login_successful():
    # Test successful login
    response, status = controller.login('test', 'test')
    assert status == 200
    assert response == {'message': 'Logged in successfully.'}
    assert current_user.is_authenticated

def test_login_unsuccessful():
    # Test unsuccessful login
    response, status = controller.login('test', 'wrong_password')
    assert status == 401
    assert response == {'message': 'Invalid username or password.'}
    assert not current_user.is_authenticated

def test_login_nonexistent_user():
    # Test login with non-existent user
    response, status = controller.login('nonexistent', 'password')
    assert status == 401
    assert response == {'message': 'Invalid username or password.'}
    assert not current_user.is_authenticated

def test_login_exception():
    # Test login with an exception
    with pytest.raises(Exception):
        controller.login(None, 'test')

def test_logout_successful():
    # Test successful logout
    controller.login('test', 'test')  # Log in first
    response, status = controller.logout()
    assert status == 200
    assert response == {'message': 'Logged out successfully.'}
    assert not current_user.is_authenticated

def test_logout_exception():
    # Test logout with an exception
    with pytest.raises(Exception):
        controller.logout()
