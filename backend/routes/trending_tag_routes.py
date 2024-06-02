from flask import Blueprint, jsonify, request
from controllers.trending_tag_controller import TrendingTagController
from flask_login import login_required
from forms import TrendingTagForm

# Create a Blueprint for the trending tag routes
trending_tag_bp = Blueprint('trending_tag_bp', __name__)

# Instantiate the TrendingTagController
trending_tag_controller = TrendingTagController()

# Route to create a new trending tag
@trending_tag_bp.route('/tags', methods=['POST'])
@login_required
def create_trending_tag():
    # Initialize and validate the form
    form = TrendingTagForm(request.form)
    if form.validate():
        # If the form is valid, create a new trending tag
        data = form.data
        result, status = trending_tag_controller.create_trending_tag(data['name'], data['popularity_score'])
        return jsonify({'name': result['name'], 'popularity_score': result['popularity_score']}), status
    else:
        # If the form is not valid, return an error message
        return jsonify({'message': 'Form validation failed.'}), 400

# Route to edit an existing trending tag
@trending_tag_bp.route('/tags/<int:tag_id>', methods=['PUT'])
@login_required
def edit_trending_tag(tag_id):
    # Initialize and validate the form
    form = TrendingTagForm(request.form)
    if form.validate():
        # If the form is valid, edit the trending tag
        data = form.data
        result, status = trending_tag_controller.edit_trending_tag(tag_id, data['name'], data['popularity_score'])
        return jsonify({'name': result['name'], 'popularity_score': result['popularity_score']}), status
    else:
        # If the form is not valid, return an error message
        return jsonify({'message': 'Form validation failed.'}), 400

# Route to delete a trending tag
@trending_tag_bp.route('/tags/<int:tag_id>', methods=['DELETE'])
@login_required
def delete_trending_tag(tag_id):
    # Delete the trending tag and return the result
    result, status = trending_tag_controller.delete_trending_tag(tag_id)
    return jsonify(result), status

# Route to get all trending tags
@trending_tag_bp.route('/tags', methods=['GET'])
def get_trending_tags():
    # Get all trending tags and return them
    tags, status = trending_tag_controller.get_trending_tags()
    return jsonify(tags), status

# Route to get all businesses associated with a specific tag
@trending_tag_bp.route('/tags/<int:tag_id>/businesses', methods=['GET'])
def get_businesses_for_tag(tag_id):
    # Get all businesses associated with the tag and return them
    businesses, status = trending_tag_controller.get_businesses_for_tag(tag_id)
    if businesses:
        business_names = [business.name for business in businesses]
        return jsonify(business_names), 200
    else:
        # If no businesses are associated with the tag, return an error message
        return jsonify({'message': 'Tag not found or no businesses associated.'}), 404