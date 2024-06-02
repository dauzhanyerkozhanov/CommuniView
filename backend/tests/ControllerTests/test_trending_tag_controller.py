import pytest
from controllers.trending_tag_controller import TrendingTagController
from models import TrendingTag, Business
from database import db

# Initialize the controller
controller = TrendingTagController()

@pytest.fixture(scope="module")
def setup_trending_tag():
    # Create a new trending tag
    name = "Test Tag"
    popularity_score = 10
    new_tag = TrendingTag(name=name, popularity_score=popularity_score)
    db.session.add(new_tag)
    db.session.commit()
    yield new_tag.id
    # Teardown
    db.session.delete(new_tag)
    db.session.commit()

def test_create_trending_tag(setup_trending_tag):
    # Test data
    name = "New Test Tag"
    popularity_score = 15

    # Test step
    response, status_code = controller.create_trending_tag(name, popularity_score)

    # Assert the response
    assert status_code == 201
    assert response['message'] == 'Trending tag created successfully.'

def test_edit_trending_tag(setup_trending_tag):
    # Test data
    tag_id = setup_trending_tag
    new_name = "Edited Tag"
    new_popularity_score = 20

    # Test step
    response, status_code = controller.edit_trending_tag(tag_id, new_name, new_popularity_score)

    # Assert the response
    assert status_code == 200
    assert response['message'] == 'Trending tag updated successfully.'

def test_delete_trending_tag(setup_trending_tag):
    # Test data
    tag_id = setup_trending_tag

    # Test step
    response, status_code = controller.delete_trending_tag(tag_id)

    # Assert the response
    assert status_code == 200
    assert response['message'] == 'Trending tag deleted successfully.'

def test_get_trending_tags():
    # Test step
    response, status_code = controller.get_trending_tags()

    # Assert the response
    assert status_code == 200
    assert isinstance(response, list)

def test_get_businesses_for_tag(setup_trending_tag):
    # Test data
    tag_id = setup_trending_tag

    # Test step
    response, status_code = controller.get_businesses_for_tag(tag_id)

    # Assert the response
    assert status_code == 200
    assert isinstance(response, list)

def test_create_trending_tag_invalid_input():
    # Test data
    name = ""  # Empty name
    popularity_score = -10  # Negative popularity score

    # Test step
    response, status_code = controller.create_trending_tag(name, popularity_score)

    # Assert the response
    assert status_code == 500
    assert 'error' in response

def test_edit_trending_tag_invalid_tag_id():
    # Test data
    tag_id = 999  # Non-existent tag ID
    new_name = "Edited Tag"
    new_popularity_score = 20

    # Test step
    response, status_code = controller.edit_trending_tag(tag_id, new_name, new_popularity_score)

    # Assert the response
    assert status_code == 404
    assert response['message'] == 'Trending tag not found.'

def test_delete_trending_tag_invalid_tag_id():
    # Test data
    tag_id = 999  # Non-existent tag ID

    # Test step
    response, status_code = controller.delete_trending_tag(tag_id)

    # Assert the response
    assert status_code == 404
    assert response['message'] == 'Trending tag not found.'

def test_get_businesses_for_tag_invalid_tag_id():
    # Test data
    tag_id = 999  # Non-existent tag ID

    # Test step
    response, status_code = controller.get_businesses_for_tag(tag_id)

    # Assert the response
    assert status_code == 404
    assert response['message'] == 'Trending tag not found.'
