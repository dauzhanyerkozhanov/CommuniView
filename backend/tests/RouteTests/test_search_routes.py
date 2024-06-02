import pytest
from flask import json, Flask
from unittest.mock import patch
from routes.search_routes import search_bp
from controllers.search_controller import SearchController
from models import Business

# Create a new Flask application for testing
app = Flask(__name__)
app.register_blueprint(search_bp)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_search_route_happy_scenario(client):
    # Mock the SearchController and its methods
    with patch.object(SearchController, 'executeSearch', return_value=None):
        with patch.object(SearchController, 'displayResults', return_value=[Business(name='Test Business')]):
            # Send a GET request to the 'search' route with a query parameter
            response = client.get('/search', query_string={'query': 'test'})
            # Parse the response data from json
            data = json.loads(response.data)
            # Assert that the status code of the response is 200
            assert response.status_code == 200
            # Assert that the response data is a list (of business names)
            assert isinstance(data, list)
            # Assert that the list contains the expected business name
            assert data == ['Test Business']

def test_search_route_no_query(client):
    # Mock the SearchController and its methods
    with patch.object(SearchController, 'executeSearch', return_value=None):
        with patch.object(SearchController, 'displayResults', return_value=[]):
            # Send a GET request to the 'search' route without a query parameter
            response = client.get('/search')
            # Parse the response data from json
            data = json.loads(response.data)
            # Assert that the status code of the response is 200
            assert response.status_code == 200
            # Assert that the response data is an empty list
            assert data == []

def test_search_route_exception(client):
    # Mock the SearchController and its methods
    with patch.object(SearchController, 'executeSearch', side_effect=Exception('Test Exception')):
        # Send a GET request to the 'search' route with a query parameter
        response = client.get('/search', query_string={'query': 'test'})
        # Assert that the status code of the response is 500 (Internal Server Error)
        assert response.status_code == 500
