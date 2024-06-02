import pytest
from database import db
from models.trending_tag import TrendingTag

def setup_module(module):
    # Setup for the tests: create a new trending tag
    module.test_tag = TrendingTag('Test Tag', 100)
    db.session.add(module.test_tag)
    db.session.commit()

def teardown_module(module):
    # Teardown for the tests: remove the test tag
    db.session.delete(module.test_tag)
    db.session.commit()

def test_trending_tag_model():
    # Fetch the tag from the database
    tag = TrendingTag.query.get(1)

    # Check that the tag has the correct properties
    assert tag.name == 'Test Tag'
    assert tag.popularityScore == 100

def test_trending_tag_init():
    # Test the __init__ method
    tag = TrendingTag('New Tag', 50)
    assert tag.name == 'New Tag'
    assert tag.popularityScore == 50
    assert tag.associatedBusinesses is None

def test_trending_tag_name_uniqueness():
    # Test that the name is unique
    with pytest.raises(Exception):
        duplicate_tag = TrendingTag('Test Tag', 200)
        db.session.add(duplicate_tag)
        db.session.commit()

def test_trending_tag_invalid_name():
    # Test with an invalid name (empty string)
    with pytest.raises(ValueError):
        invalid_tag = TrendingTag('', 100)

def test_trending_tag_invalid_popularity_score():
    # Test with an invalid popularity score (negative value)
    with pytest.raises(ValueError):
        invalid_tag = TrendingTag('Invalid Tag', -10)
