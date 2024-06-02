from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from controllers.bookmark_controller import BookmarkController
from forms import BookmarkForm

# Create a Blueprint for bookmark routes
bookmark_bp = Blueprint('bookmark_bp', __name__)

# Instantiate the BookmarkController
bookmark_controller = BookmarkController()

# Route for creating a bookmark
@bookmark_bp.route('/bookmark', methods=['POST'])
@login_required  # Ensure the user is logged in
def create_bookmark():
    # Initialize the form with the request data
    form = BookmarkForm(request.form)
    if form.validate():  # Validate the form
        # Get the validated form data
        data = form.data
        # Call the create_bookmark method from the controller
        response, status_code = bookmark_controller.create_bookmark(current_user, data['associated_user'], data['associated_business'])
        return jsonify(response), status_code
    else:
        # Handle validation failure
        return jsonify({'message': 'Form validation failed.'}), 400

# Route for deleting a bookmark
@bookmark_bp.route('/bookmark/<int:bookmark_id>', methods=['DELETE'])
@login_required  # Ensure the user is logged in
def delete_bookmark(bookmark_id):
    # Call the delete_bookmark method from the controller
    response, status_code = bookmark_controller.delete_bookmark(bookmark_id, current_user)
    return jsonify(response), status_code

# Route for editing a bookmark
@bookmark_bp.route('/bookmark/<int:bookmark_id>/edit', methods=['PUT'])
@login_required  # Ensure the user is logged in
def edit_bookmark(bookmark_id):
    # Initialize the form with the request data
    form = BookmarkForm(request.form)
    if form.validate():  # Validate the form
        # Get the validated form data
        data = form.data
        # Call the edit_bookmark method from the controller
        response, status_code = bookmark_controller.edit_bookmark(bookmark_id, data['new_associated_user'], data['new_associated_business'])
        return jsonify(response), status_code
    else:
        # Handle validation failure
        return jsonify({'message': 'Form validation failed.'}), 400

# Route for getting bookmark details
@bookmark_bp.route('/bookmark', methods=['GET'])
@login_required  # Ensure the user is logged in
def get_bookmark_details():
    # Call the get_bookmark_details method from the controller
    bookmark_details = bookmark_controller.get_bookmark_details(current_user)
    if bookmark_details:
        return jsonify(bookmark_details), 200
    else:
        # Handle case where no bookmarks are found or they are not owned by the current user
        return jsonify({'message': 'Bookmarks not found or not owned by current user.'}), 404