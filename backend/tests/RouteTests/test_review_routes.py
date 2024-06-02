import pytest
from flask import json
from app import create_app
from database import db
from models import User, Review, Business
from werkzeug.exceptions import BadRequest, NotFound

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_review_routes(client):
    # Setup: Create a user and a business
    user = User(username='testuser')
    business = Business(id=1, rating=4.0, review_count=1)
    db.session.add(user)
    db.session.add(business)
    db.session.commit()

    # Test create_review route
    response = client.post('/review', json={
        'content': 'Great service!',
        'rating_value': 5,
        'associated_business': 1
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Review created and business rating updated successfully.'

    # Test create_review route with invalid data
    response = client.post('/review', json={
        'content': '',
        'rating_value': 6,
        'associated_business': 1
    })
    assert response.status_code == 400
    assert 'errors' in response.get_json()

    # Test get_review route
    response = client.get('/get?review_id=1')
    assert response.status_code == 200
    assert response.get_json()['author'] == 'testuser'
    assert response.get_json()['content'] == 'Great service!'
    assert response.get_json()['rating_value'] == 5

    # Test get_review route with non-existing review
    response = client.get('/get?review_id=2')
    assert response.status_code == 404
    assert 'message' in response.get_json()

    # Test edit_review route
    response = client.put('/edit', json={
        'review_id': 1,
        'content': 'Excellent service!',
        'rating_value': 5
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Review updated successfully.'

    # Test edit_review route with invalid data
    response = client.put('/edit', json={
        'review_id': 1,
        'content': '',
        'rating_value': 6
    })
    assert response.status_code == 400
    assert 'errors' in response.get_json()

    # Test delete_review route
    response = client.delete('/delete', json={'review_id': 1})
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Review deleted successfully.'

    # Test delete_review route with non-existing review
    response = client.delete('/delete', json={'review_id': 2})
    assert response.status_code == 404
    assert 'message' in response.get_json()
