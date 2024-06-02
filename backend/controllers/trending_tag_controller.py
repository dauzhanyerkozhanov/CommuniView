from flask import jsonify
from models import TrendingTag, Business
from database import db
from forms import TrendingTagForm

# Controller for managing trending tags
class TrendingTagController:
    def __init__(self):
        # Initialize form for trending tag
        self.trending_tag_form = TrendingTagForm()

    # Create a new trending tag
    def create_trending_tag(self, name, popularity_score):
        try:
            # Create new tag object
            new_tag = TrendingTag(name=name, popularity_score=popularity_score)
            # Add new tag to the session
            db.session.add(new_tag)
            # Commit the session to save the tag
            db.session.commit()
            return {'message': 'Trending tag created successfully.'}, 201
        except Exception as e:
            return {'error': str(e)}, 500

    # Edit an existing trending tag
    def edit_trending_tag(self, tag_id, new_name, new_popularity_score):
        try:
            # Fetch the tag by id
            tag = TrendingTag.query.get(tag_id)
            if not tag:
                return {'message': 'Trending tag not found.'}, 404
            
            # Update tag details
            tag.name = new_name
            tag.popularity_score = new_popularity_score
            # Commit the session to save changes
            db.session.commit()
            return {'message': 'Trending tag updated successfully.'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    # Delete a trending tag
    def delete_trending_tag(self, tag_id):
        try:
            # Fetch the tag by id
            tag = TrendingTag.query.get(tag_id)
            if not tag:
                return {'message': 'Trending tag not found.'}, 404
            
            # Remove the tag from the session
            db.session.delete(tag)
            # Commit the session to delete the tag
            db.session.commit()
            return {'message': 'Trending tag deleted successfully.'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    # Get top 10 trending tags
    def get_trending_tags(self):
        try:
            # Fetch top 10 tags ordered by popularity score
            trending_tags = TrendingTag.query.order_by(TrendingTag.popularity_score.desc()).limit(10).all()
            return jsonify([tag.name for tag in trending_tags]), 200
        except Exception as e:
            return {'error': str(e)}, 500

    # Get businesses associated with a tag
    def get_businesses_for_tag(self, tag_id):
        try:
            # Fetch the tag by id
            tag = TrendingTag.query.filter_by(id=tag_id).first()
            if not tag:
                return {'message': 'Trending tag not found.'}, 404
            
            # Fetch businesses associated with the tag
            businesses = Business.query.filter(Business.tags.contains(tag)).all()
            return businesses, 200  # Assuming this returns a list of businesses and 200 for success
        except Exception as e:
            return {'error': str(e)}, 500