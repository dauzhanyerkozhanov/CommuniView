from flask import Blueprint, jsonify, request
from controllers.business_update_controller import BusinessUpdateController
from flask_login import login_required
from forms import BusinessUpdateForm

# Instantiate the BusinessUpdateController
business_update_controller = BusinessUpdateController()

# Create a Blueprint for business update routes
business_bp = Blueprint('business_bp', __name__)

# Define a route for updating business form
@business_bp.route('/update_form', methods=['POST'])
@login_required  # Ensure the user is logged in
def update_business_form():
    # Check if the request content type is JSON
    if request.content_type == 'application/json':
        # Load JSON data if content type is application/json
        form_data = request.get_json()
    else:
        # Use form data if content type is not application/json
        form_data = request.form
    # Initialize the form with the appropriate data
    form = BusinessUpdateForm(form_data)
    if form.validate():  # Validate the form
        # Pass the validated form data to the controller
        response = business_update_controller.submit_form(form.data)
        # Return the response from the controller
        return jsonify(response[0]), response[1]
    else:
        # Handle validation failure
        return jsonify({'message': 'Form validation failed.'}), 400