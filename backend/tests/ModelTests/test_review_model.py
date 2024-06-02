import pytest
from database import db
from models.review import Review

@pytest.fixture(scope="module")
def setup_teardown():
    # Setup for the tests: create a new review
    test_review = Review(1, 'testUser', 'This is a test review', 5, 'testBusiness')
    db.session.add(test_review)
    db.session.commit()
    yield
    # Teardown for the tests: remove the test review
    db.session.delete(test_review)
    db.session.commit()

def test_review_model(setup_teardown):
    # Fetch the review from the database
    review = Review.query.get(1)
    # Check that the review has the correct properties
    assert review.author == 'testUser'
    assert review.content == 'This is a test review'
    assert review.ratingValue == 5
    assert review.associatedBusiness == 'testBusiness'

def test_review_init():
    review = Review(2, 'anotherUser', 'Another test review', 3, 'anotherBusiness')
    assert review.reviewID == 2
    assert review.author == 'anotherUser'
    assert review.content == 'Another test review'
    assert review.ratingValue == 3
    assert review.associatedBusiness == 'anotherBusiness'

def test_review_init_invalid_inputs():
    with pytest.raises(ValueError):
        Review(3, '', 'Invalid review', 6, 'invalidBusiness')
    with pytest.raises(ValueError):
        Review(4, 'validUser', '', 0, 'validBusiness')
    with pytest.raises(ValueError):
        Review(5, 'validUser', 'Valid review', 10, 'validBusiness')
    with pytest.raises(ValueError):
        Review(6, 'validUser', 'Valid review', -1, 'validBusiness')
