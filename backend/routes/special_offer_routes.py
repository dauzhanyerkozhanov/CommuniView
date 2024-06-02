from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import SpecialOffer, Business
from database import db
from werkzeug.exceptions import BadRequest, NotFound
from controllers.special_offer_controller import SpecialOfferController
from forms import SpecialOfferForm

# Create a Blueprint for special offer routes
special_offer_bp = Blueprint('special_offer_bp', __name__)

# Instantiate the SpecialOfferController
offer_controller = SpecialOfferController()

# Define a route for creating a special offer
@special_offer_bp.route('/offers', methods=['POST'])
@login_required
def create_special_offer():
    # Initialize the form with the request data
    form = SpecialOfferForm(request.get_json())
    # Validate the form and create a special offer if valid
    if form.validate():
        data = form.data
        response, status = offer_controller.create_special_offer(current_user, data['title'], data['description'], data['expiration_date'], data['associated_business'])
        return jsonify(response), status
    else:
        # Return an error message if form validation fails
        return jsonify({'message': 'Form validation failed.'}), 400

# Define a route for updating a special offer
@special_offer_bp.route('/offers/<int:offer_id>', methods=['PUT'])
@login_required
def update_special_offer(offer_id):
    # Initialize the form with the request data
    form = SpecialOfferForm(request.get_json())
    # Validate the form and update the special offer if valid
    if form.validate():
        data = form.data
        response, status = offer_controller.edit_offer(offer_id, current_user, data['title'], data['description'], data['expiration_date'])
        return jsonify(response), status
    else:
        # Return an error message if form validation fails
        return jsonify({'message': 'Form validation failed.'}), 400

# Define a route for deleting a special offer
@special_offer_bp.route('/offers/<int:offer_id>', methods=['DELETE'])
@login_required
def delete_special_offer(offer_id):
    # Delete the special offer and return the response
    response, status = offer_controller.delete_offer(offer_id, current_user)
    return jsonify(response), status

# Define a route for getting a special offer
@special_offer_bp.route('/offers/<int:offer_id>', methods=['GET'])
@login_required
def get_special_offer(offer_id):
    # Get the special offer and return the response
    response, status = offer_controller.get_offer(offer_id, current_user)
    return jsonify(response), status