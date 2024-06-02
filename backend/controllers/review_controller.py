from models import Review, Business
from database import db
from forms import ReviewForm
from werkzeug.exceptions import NotFound

class ReviewController:
    # Initialize ReviewController with a form instance
    def __init__(self):
        self.review_form = ReviewForm()

    # Create a new review and update the associated business's rating
    def create_review(self, user, content, rating_value, associated_business):
        try:
            # Create a new review instance
            new_review = Review(author=user.username, content=content, rating_value=rating_value, associated_business=associated_business)
            db.session.add(new_review)
            
            # Fetch the associated business
            business = Business.query.get(associated_business)
            if business:
                if business.review_count == 0:
                    # If there are no existing reviews, set the rating to the new review's rating
                    business.rating = rating_value
                else:
                    # Update the business's rating and review count
                    business.rating = (business.rating * business.review_count + rating_value) / (business.review_count + 1)
                business.review_count += 1
                db.session.commit()
                return {'message': 'Review created and business rating updated successfully.'}, 201
            else:
                return {'message': 'Business not found.'}, 404
            
        except Exception as e:
            return {'error': str(e)}, 500

    # Edit an existing review
    def edit_review(self, review_id, user, content, rating_value):
        try:
            # Fetch the review to be edited
            review = Review.query.get(review_id)
            if review.author != user.username:
                return {'message': 'Unauthorized.'}, 403
            
            # Update the review's content and rating
            review.content = content
            review.rating_value = rating_value
            db.session.commit()
            return {'message': 'Review updated successfully.'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    # Delete a review
    def delete_review(self, review_id, user):
        try:
            # Fetch the review to be deleted
            review = Review.query.get(review_id)
            if review.author != user.username:
                return {'message': 'Unauthorized.'}, 403
            if review is None:
                raise NotFound('Review does not exist.')
            
            # Delete the review from the database
            db.session.delete(review)
            db.session.commit()
            return {'message': 'Review deleted successfully.'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    # Fetch a review
    def get_review(self, review_id, user):
        try:
            # Fetch the requested review
            review = Review.query.get(review_id)
            if review is None:
                return {'message': 'Review not found.'}, 404
            if review.author != user.username:
                return {'message': 'Unauthorized.'}, 403
            
            # Return the review's details
            return {
                'author': review.author,
                'content': review.content,
                'rating_value': review.rating_value,
                'associated_business': review.associated_business
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500