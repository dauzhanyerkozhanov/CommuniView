import pytest
from models import Bookmark
from controllers.bookmark_controller import BookmarkController
from database import db

# Define a fixture for the BookmarkController
@pytest.fixture
def bookmark_controller():
    return BookmarkController()

class MockUser:
    def __init__(self, username):
        self.username = username
        
# Test the creation of a bookmark
def test_create_bookmark(bookmark_controller):
    user = MockUser('testUser')
    associated_business = 'testBusiness'
    # Call the create_bookmark method and store the response and status code
    response, status_code = bookmark_controller.create_bookmark(user, associated_business)
    # Assert that the status code is 201 and the response message is as expected
    assert status_code == 201
    assert response['message'] == 'Bookmark created successfully.'

    # Test the creation of a bookmark with invalid input
    user = MockUser('testUser')
    associated_business = 'invalidBusiness'
    response, status_code = bookmark_controller.create_bookmark(user, associated_business)
    assert status_code == 500
    assert 'error' in response

# Test the editing of a bookmark
def test_edit_bookmark(bookmark_controller):
    bookmark_id = 1
    new_associated_business = 'newTestBusiness'
    # Call the edit_bookmark method and store the response and status code
    response, status_code = bookmark_controller.edit_bookmark(bookmark_id, new_associated_business)
    # Assert that the status code is 200 and the response message is as expected
    assert status_code == 200
    assert response['message'] == 'Bookmark edited successfully.'

    # Test the editing of a non-existent bookmark
    bookmark_id = 999
    new_associated_business = 'nonExistentBookmark'
    response, status_code = bookmark_controller.edit_bookmark(bookmark_id, new_associated_business)
    assert status_code == 404
    assert response['message'] == 'Bookmark not found.'

# Test the deletion of a bookmark
def test_delete_bookmark(bookmark_controller):
    bookmark_id = 1
    user = 'testUser'
    # Call the delete_bookmark method and store the response and status code
    response, status_code = bookmark_controller.delete_bookmark(bookmark_id, user)
    # Assert that the status code is 200 and the response message is as expected
    assert status_code == 200
    assert response['message'] == 'Bookmark deleted successfully.'

    # Test the deletion of a bookmark with an unauthorized user
    bookmark_id = 2
    user = 'unauthorizedUser'
    response, status_code = bookmark_controller.delete_bookmark(bookmark_id, user)
    assert status_code == 403
    assert response['message'] == 'Unauthorized.'

# Test getting the details of a bookmark
def test_get_bookmark_details(bookmark_controller):
    bookmark_id = 1
    user = MockUser('testUser')
    # Call the get_bookmark_details method and store the response and status code
    response, status_code = bookmark_controller.get_bookmark_details(bookmark_id, user)
    # Assert that the status code is 200 and the response contains the correct details
    assert status_code == 200
    assert response['associated_user'] == 'testUser'
    assert response['associated_business'] == 'testBusiness'

    # Test getting the details of a bookmark with an unauthorized user
    bookmark_id = 2
    user = 'unauthorizedUser'
    response, status_code = bookmark_controller.get_bookmark_details(bookmark_id, user)
    assert status_code == 403
    assert response['message'] == 'Unauthorized.'
