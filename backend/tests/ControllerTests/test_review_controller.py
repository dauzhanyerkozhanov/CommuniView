import pytest
from controllers.review_controller import ReviewController
from models import Review, Business, User
from database import db

# Create a fixture for the ReviewController
@pytest.fixture
def review_controller():
    return ReviewController()

# Test the create_review method
def test_create_review(review_controller):
    # Setup: Create a user and a business
    user = User(username='testuser')
    business = Business(id=1, rating=4.0, review_count=1)
    db.session.add(user)
    db.session.add(business)
    db.session.commit()

    # Happy scenario: Create a new review
    response, status_code = review_controller.create_review(user, 'Great service!', 5, 1)
    assert status_code == 201
    assert response['message'] == 'Review created and business rating updated successfully.'
    assert Business.query.get(1).rating == 4.5

    # Unhappy scenario: Business not found
    response, status_code = review_controller.create_review(user, 'Great service!', 5, 2)
    assert status_code == 404
    assert response['message'] == 'Business not found.'

# Test the edit_review method
def test_edit_review(review_controller):
    # Setup: Create a user and a review
    user = User(username='testuser')
    review = Review(id=1, author='testuser', content='Great service!', rating_value=5)
    db.session.add(user)
    db.session.add(review)
    db.session.commit()

    # Happy scenario: Edit an existing review
    response, status_code = review_controller.edit_review(1, user, 'Excellent service!', 5)
    assert status_code == 200
    assert response['message'] == 'Review updated successfully.'
    assert Review.query.get(1).content == 'Excellent service!'

    # Unhappy scenario: Unauthorized user
    unauthorized_user = User(username='otheruser')
    response, status_code = review_controller.edit_review(1, unauthorized_user, 'Bad service!', 1)
    assert status_code == 403
    assert response['message'] == 'Unauthorized.'

# Test the delete_review method
def test_delete_review(review_controller):
    # Setup: Create a user and a review
    user = User(username='testuser')
    review = Review(id=1, author='testuser')
    db.session.add(user)
    db.session.add(review)
    db.session.commit()

    # Happy scenario: Delete an existing review
    response, status_code = review_controller.delete_review(1, user)
    assert status_code == 200
    assert response['message'] == 'Review deleted successfully.'
    assert Review.query.get(1) is None

    # Unhappy scenario: Unauthorized user
    unauthorized_user = User(username='otheruser')
    response, status_code = review_controller.delete_review(1, unauthorized_user)
    assert status_code == 403
    assert response['message'] == 'Unauthorized.'

# Test the get_review method
def test_get_review(review_controller):
    # Setup: Create a user and a review
    user = User(username='testuser')
    review = Review(id=1, author='testuser', content='Great service!', rating_value=5)
    db.session.add(user)
    db.session.add(review)
    db.session.commit()

    # Happy scenario: Get an existing review
    response, status_code = review_controller.get_review(1, user)
    assert status_code == 200
    assert response['author'] == 'testuser'
    assert response['content'] == 'Great service!'
    assert response['rating_value'] == 5

    # Unhappy scenario: Unauthorized user
    unauthorized_user = User(username='otheruser')
    response, status_code = review_controller.get_review(1, unauthorized_user)
    assert status_code == 403
    assert response['message'] == 'Unauthorized.'

    # Unhappy scenario: Review not found
    response, status_code = review_controller.get_review(2, user)
    assert status_code == 404
    assert response['message'] == 'Review not found.'

# Test the get_reviews_for_business method
def test_get_reviews_for_business(review_controller):
    # Setup: Create a user, a business, and some reviews
    user = User(username='testuser')
    business = Business(id=1, name='Test Business')
    review1 = Review(id=1, author='testuser', content='Great service!', rating_value=5, business=business)
    review2 = Review(id=2, author='testuser', content='Excellent service!', rating_value=4, business=business)
    db.session.add(user)
    db.session.add(business)
    db.session.add(review1)
    db.session.add(review2)
    db.session.commit()

    # Happy scenario: Get reviews for an existing business
    response, status_code = review_controller.get_reviews_for_business(1)
    assert status_code == 200
    assert len(response) == 2
    assert response[0]['author'] == 'testuser'
    assert response[0]['content'] == 'Great service!'
    assert response[0]['rating_value'] == 5
    assert response[1]['author'] == 'testuser'
    assert response[1]['content'] == 'Excellent service!'
    assert response[1]['rating_value'] == 4

    # Unhappy scenario: Business not found
    response, status_code = review_controller.get_reviews_for_business(2)
    assert status_code == 404
    assert response['message'] == 'Business not found.'