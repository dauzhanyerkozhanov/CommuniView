from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from database import db
from werkzeug.exceptions import BadRequest, NotFound
from controllers.review_controller import ReviewController
from forms import ReviewForm

# Create a Blueprint for review routes
review_bp = Blueprint('review_bp', __name__)

# Instantiate the ReviewController
review_controller = ReviewController()

# Define a route for creating a review
@review_bp.route('/review', methods=['POST'])
@login_required
def create_review():
    # Initialize the form with the request data
    form = ReviewForm(request.get_json())
    if form.validate():
        try:
            # Pass the validated form data to the controller
            response, status_code = review_controller.create_review(
                current_user,
                form.content.data,
                form.rating_value.data,
                form.associated_business.data
            )
            # Return the response from the controller
            return jsonify(response), status_code
        except Exception as e:
            # Handle exceptions during review creation
            return jsonify({'message': str(e)}), 400
    else:
        # Handle form validation failure
        return jsonify({'errors': form.errors}), 400

# Define a route for editing a review
@review_bp.route('/edit', methods=['PUT'])
@login_required
def edit_review():
    # Initialize the form with the request data
    form = ReviewForm(request.get_json())
    if form.validate():
        try:
            # Pass the validated form data to the controller
            response, status_code = review_controller.edit_review(
                form.review_id.data,
                current_user,
                form.content.data,
                form.rating_value.data
            )
            # Return the response from the controller
            return jsonify(response), status_code
        except Exception as e:
            # Handle exceptions during review editing
            return jsonify({'message': str(e)}), 400
    else:
        # Handle form validation failure
        return jsonify({'errors': form.errors}), 400

# Define a route for deleting a review
@review_bp.route('/delete', methods=['DELETE'])
@login_required
def delete_review():
    # Get the request data
    data = request.get_json()
    try:
        # Pass the review_id and current_user to the controller
        response, status_code = review_controller.delete_review(data['review_id'], current_user)
        # Return the response from the controller
        return jsonify(response), status_code
    except Exception as e:
        # Handle exceptions during review deletion
        return jsonify({'message': 'An error occurred while deleting the review: ' + str(e)}), 500

# Define a route for getting a review
@review_bp.route('/get', methods=['GET'])
@login_required
def get_review():
    # Get the review_id from the request arguments
    review_id = request.args.get('review_id')
    try:
        # Pass the review_id and current_user to the controller
        response, status_code = review_controller.get_review(review_id, current_user)
        # Return the response from the controller
        return jsonify(response), status_code
    except Exception as e:
        # Handle exceptions during review fetching
        return jsonify({'message': 'An error occurred while fetching the review: ' + str(e)}), 500