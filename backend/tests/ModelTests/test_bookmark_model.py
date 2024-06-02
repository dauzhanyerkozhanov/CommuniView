import pytest
from models import Bookmark

def test_bookmark_model_valid_input():
    # Create a new Bookmark instance with valid input
    bookmark = Bookmark(bookmarkID=1, associatedUser='testUser', associatedBusiness='testBusiness')
    
    # Verify that the properties are set correctly
    assert bookmark.bookmarkID == 1
    assert bookmark.associatedUser == 'testUser'
    assert bookmark.associatedBusiness == 'testBusiness'

def test_bookmark_model_invalid_bookmarkID():
    # Test with an invalid bookmarkID (non-integer)
    with pytest.raises(ValueError):
        Bookmark(bookmarkID='invalid', associatedUser='testUser', associatedBusiness='testBusiness')

def test_bookmark_model_missing_associatedUser():
    # Test with a missing associatedUser
    with pytest.raises(TypeError):
        Bookmark(bookmarkID=1, associatedBusiness='testBusiness')

def test_bookmark_model_missing_associatedBusiness():
    # Test with a missing associatedBusiness
    with pytest.raises(TypeError):
        Bookmark(bookmarkID=1, associatedUser='testUser')

def test_bookmark_model_none_values():
    # Test with None values for associatedUser and associatedBusiness
    bookmark = Bookmark(bookmarkID=1, associatedUser=None, associatedBusiness=None)
    
    # Verify that the properties are set to None
    assert bookmark.associatedUser is None
    assert bookmark.associatedBusiness is None