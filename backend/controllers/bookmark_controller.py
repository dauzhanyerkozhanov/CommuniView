from models import Bookmark
from database import db
from forms import BookmarkForm

# The BookmarkController class handles all operations related to bookmarks.
class BookmarkController:
    # Initialize the BookmarkController with a form for validating bookmark data.
    def __init__(self):
        self.bookmark_form = BookmarkForm()

    # Create a new bookmark with the given user and associated business.
    def create_bookmark(self, user, associated_business):
        new_bookmark = Bookmark(associated_user=user.username, associated_business=associated_business)
        try:
            # Add the new bookmark to the database session and commit it.
            db.session.add(new_bookmark)
            db.session.commit()
            return {'message': 'Bookmark created successfully.'}, 201
        except Exception as e:
            # If an error occurs, return a 500 status code and the error message.
            return {'error': str(e)}, 500

    # Edit an existing bookmark with the given bookmark ID and new associated business.
    def edit_bookmark(self, bookmark_id, new_associated_business):
        try:
            # Fetch the bookmark from the database.
            bookmark = Bookmark.query.get(bookmark_id)
            if not bookmark:
                return {'message': 'Bookmark not found.'}, 404
            # Update the associated business of the bookmark.
            bookmark.associated_business = new_associated_business
            db.session.commit()
            return {'message': 'Bookmark edited successfully.'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    # Delete a bookmark with the given bookmark ID and user.
    def delete_bookmark(self, bookmark_id, user):
        try:
            bookmark = Bookmark.query.get(bookmark_id)
            # Check if the user is authorized to delete the bookmark.
            if bookmark.associated_user != user.username:
                return {'message': 'Unauthorized.'}, 403
            # Delete the bookmark from the database session and commit it.
            db.session.delete(bookmark)
            db.session.commit()
            return {'message': 'Bookmark deleted successfully.'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    # Get the details of a bookmark with the given bookmark ID and user.
    def get_bookmark_details(self, bookmark_id, user):
        try:
            bookmark = Bookmark.query.get(bookmark_id)
            # Check if the user is authorized to view the bookmark.
            if bookmark.associated_user != user.username:
                return {'message': 'Unauthorized.'}, 403
            # Return the associated user and business of the bookmark.
            return {
                'associated_user': bookmark.associated_user,
                'associated_business': bookmark.associated_business
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500