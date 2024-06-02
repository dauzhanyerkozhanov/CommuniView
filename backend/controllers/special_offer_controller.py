from flask import request, jsonify
from models import SpecialOffer
from database import db
from forms import SpecialOfferForm

class SpecialOfferController:
    # Initialize the controller with a form for special offers
    def __init__(self):
        self.special_offer_form = SpecialOfferForm()

    # Create a new special offer if the user is the owner of the associated business
    def create_special_offer(self, user, title, description, expiration_date, associated_business):
        if user == associated_business.owner:
            try:
                # Create a new special offer and add it to the database
                new_offer = SpecialOffer(title=title, description=description, expiration_date=expiration_date, associated_business=associated_business)
                db.session.add(new_offer)
                db.session.commit()
                return {'message': 'Special offer created successfully.'}, 201
            except Exception as e:
                # Return an error message if the creation fails
                return {'error': str(e)}, 500
        else:
            return {'message': 'Unauthorized.'}, 403

    # Edit an existing special offer if the user is the owner of the associated business
    def edit_offer(self, offer_id, user, new_title, new_description, new_expiration_date):
        try:
            # Fetch the special offer from the database
            offer = SpecialOffer.query.get(offer_id)
            if offer.associated_business.owner != user:
                return {'message': 'Unauthorized.'}, 403
            
            # Update the special offer details and commit the changes to the database
            offer.title = new_title
            offer.description = new_description
            offer.expiration_date = new_expiration_date
            db.session.commit()
            return {'message': 'Special offer updated successfully.'}, 200
        except Exception as e:
            # Return an error message if the update fails
            return {'error': str(e)}, 500

    # Delete a special offer if the user is the owner of the associated business
    def delete_offer(self, offer_id, user):
        try:
            # Fetch the special offer from the database
            offer = SpecialOffer.query.get(offer_id)
            if offer.associated_business.owner != user:
                return {'message': 'Unauthorized.'}, 403
            
            # Delete the special offer and commit the changes to the database
            db.session.delete(offer)
            db.session.commit()
            return {'message': 'Special offer deleted successfully.'}, 200
        except Exception as e:
            # Return an error message if the deletion fails
            return {'error': str(e)}, 500

    # Fetch a special offer if the user is the owner of the associated business
    def get_offer(self, offer_id, user):
        try:
            # Fetch the special offer from the database
            offer = SpecialOffer.query.get(offer_id)
            if offer.associated_business.owner == user:
                # Return the special offer details
                offer_data = {
                    'title': offer.title,
                    'description': offer.description,
                    'expiration_date': offer.expiration_date,
                    'associated_business': offer.associated_business
                }
                return offer_data, 200
            return {'message': 'Unauthorized.'}, 403
        except Exception as e:
            # Return an error message if the fetch fails
            return {'error': str(e)}, 500