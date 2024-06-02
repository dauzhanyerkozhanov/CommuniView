from flask import Blueprint, request, jsonify
from controllers.search_controller import SearchController
from models import Business

# Create a Blueprint for search routes
search_bp = Blueprint('search_bp', __name__)

# Instantiate the SearchController
search_controller = SearchController()

# Define a route for executing a search
@search_bp.route('/search', methods=['GET'])
def search():
    # Get the search query from the request arguments
    query = request.args.get('query')
    
    # Validate the search query
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    # Execute the search with the provided query
    search_controller.executeSearch(query)
    # Get the results of the search
    results = search_controller.displayResults()
    # Return the names of the businesses found in the search results
    return jsonify([business.name for business in results]), 200