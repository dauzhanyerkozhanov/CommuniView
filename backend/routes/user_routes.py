from flask import Blueprint, jsonify, request
from flask_login import login_required
from controllers.user_authentication_controller import UserAuthenticationController
from controllers.user_registration_controller import UserRegistrationController
from forms import RegistrationForm, LoginForm

# Define a Blueprint for user-related routes
user_bp = Blueprint('user_bp', __name__)

# Instantiate the controllers for user registration and authentication
user_registration_controller = UserRegistrationController()
user_authentication_controller = UserAuthenticationController()

# Define a route for user registration
@user_bp.route('/register_form', methods=['POST'])
def register_form():
    # Create a RegistrationForm instance with the JSON data from the request
    form = RegistrationForm(request.get_json())
    # Validate the form data
    if form.validate():
        # If the form data is valid, submit the form and return the response and status
        response, status = user_registration_controller.submit_form(form)
        return jsonify(response), status
    else:
        # If the form data is not valid, return the form errors
        return jsonify({'errors': form.errors}), 400

# Define a route for user login
@user_bp.route('/login', methods=['POST'])
def login():
    # Create a LoginForm instance with the JSON data from the request
    form = LoginForm(request.get_json())
    # Validate the form data
    if form.validate():
        # If the form data is valid, login the user and return the response and status
        response, status = user_authentication_controller.login(form.username.data, form.password.data)
        return jsonify(response), status
    else:
        # If the form data is not valid, return the form errors
        return jsonify({'errors': form.errors}), 400

# Define a route for user logout
@user_bp.route('/logout')
@login_required
def logout():
    # Logout the user and return the response and status
    response, status = user_authentication_controller.logout()
    return jsonify(response), status