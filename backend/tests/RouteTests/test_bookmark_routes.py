import pytest
from flask import json, jsonify
import app
from controllers.bookmark_controller import BookmarkController
from flask_login import current_user

# Instantiate the BookmarkController
bookmark_controller = BookmarkController()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_bookmark(client):
    # Test the create bookmark route (happy scenario)
    response = client.post('/bookmark', data={'associated_user': 'test_user', 'associated_business': 'test_business'})
    assert response.status_code == 200
    assert 'response' in json.loads(response.data)

    # Test the create bookmark route (unhappy scenario: form validation failure)
    response = client.post('/bookmark', data={})
    assert response.status_code == 400
    assert 'message' in json.loads(response.data)

def test_delete_bookmark(client):
    # Test the delete bookmark route (happy scenario)
    response = client.delete('/bookmark/1')
    assert response.status_code == 200
    assert 'response' in json.loads(response.data)

    # Test the delete bookmark route (unhappy scenario: bookmark not found)
    response = client.delete('/bookmark/999')
    assert response.status_code == 404
    assert 'message' in json.loads(response.data)

def test_edit_bookmark(client):
    # Test the edit bookmark route (happy scenario)
    response = client.put('/bookmark/1/edit', data={'new_associated_user': 'new_test_user', 'new_associated_business': 'new_test_business'})
    assert response.status_code == 200
    assert 'response' in json.loads(response.data)

    # Test the edit bookmark route (unhappy scenario: form validation failure)
    response = client.put('/bookmark/1/edit', data={})
    assert response.status_code == 400
    assert 'message' in json.loads(response.data)

    # Test the edit bookmark route (unhappy scenario: bookmark not found)
    response = client.put('/bookmark/999/edit', data={'new_associated_user': 'new_test_user', 'new_associated_business': 'new_test_business'})
    assert response.status_code == 404
    assert 'message' in json.loads(response.data)

def test_get_bookmark_details(client):
    # Test the get bookmark details route (happy scenario)
    response = client.get('/bookmark')
    assert response.status_code == 200
    assert 'bookmark_details' in json.loads(response.data)

    # Test the get bookmark details route (unhappy scenario: no bookmarks found or not owned by current user)
    with app.test_request_context():
        current_user.id = 999  # Set an invalid user ID
        response = client.get('/bookmark')
        assert response.status_code == 404
        assert 'message' in json.loads(response.data)
