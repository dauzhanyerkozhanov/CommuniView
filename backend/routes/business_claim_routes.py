from flask import Blueprint, request, jsonify
from flask_login import login_required
from controllers.business_claim_controller import BusinessClaimController
from forms import BusinessClaimForm

# Instantiate the BusinessClaimController
business_claim_controller = BusinessClaimController()

# Create a Blueprint for business claim routes
business_claim_bp = Blueprint('business_claim_bp', __name__)

# Route for submitting a business claim
@business_claim_bp.route('/submit_claim', methods=['POST'])
@login_required  # Ensure the user is logged in
def submit_claim():
    # Initialize the form with the request data
    form = BusinessClaimForm(request.form)
    if form.validate():  # Validate the form
        # Call the submit_claim method from the controller
        response = business_claim_controller.submit_claim(form)
        return response
    else:
        # Handle validation failure
        return jsonify({'errors': form.errors}), 400

# Route for editing a business claim
@business_claim_bp.route('/edit_claim/<int:claim_id>', methods=['PUT'])
@login_required  # Ensure the user is logged in
def edit_claim(claim_id):
    # Initialize the form with the request data
    form = BusinessClaimForm(request.form)
    if form.validate():  # Validate the form
        # Get the new status from the request data
        new_status = request.get_json().get('new_status')
        # Call the edit_claim method from the controller
        response = business_claim_controller.edit_claim(claim_id, form, new_status)
        return response
    else:
        # Handle validation failure
        return jsonify({'errors': form.errors}), 400

# Route for deleting a business claim
@business_claim_bp.route('/delete_claim/<int:claim_id>', methods=['DELETE'])
@login_required  # Ensure the user is logged in
def delete_claim(claim_id):
    # Call the delete_claim method from the controller
    response = business_claim_controller.delete_claim(claim_id)
    return response