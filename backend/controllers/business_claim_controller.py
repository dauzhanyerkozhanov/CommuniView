from flask import jsonify, request
from models import BusinessClaim
from database import db
from forms import BusinessClaimForm

# BusinessClaimController handles the business logic related to business claims.
class BusinessClaimController:
    # Initialize the controller with a form instance for validation.
    def __init__(self):
        self.claim_form = BusinessClaimForm()

    # submit_claim method validates the form data and creates a new business claim.
    def submit_claim(self):
        # Validate form data
        if self.claim_form.validate_on_submit():
            try:
                # Create a new business claim
                business_claim = BusinessClaim(
                    business_id=self.claim_form.business_id.data,
                    owner_id=self.claim_form.owner_id.data,
                    claim_status=self.claim_form.claim_status.data,
                    proof_documents=self.claim_form.proof_documents.data
                )
                # Add the new claim to the database session and commit it
                db.session.add(business_claim)
                db.session.commit()
                return {'message': 'Business claim submitted successfully.'}, 201
            except Exception as e:
                # Handle any exceptions that occur during the claim submission
                return {'error': str(e)}, 500
        return {'message': 'Validation failed.'}, 400

    # edit_claim method updates the status of an existing business claim.
    def edit_claim(self, claim_id, new_status):
        try:
            # Fetch the claim from the database
            claim = BusinessClaim.query.get(claim_id)
            if not claim:
                return {'message': 'Claim not found.'}, 404
            # Update the claim status
            claim.claim_status = new_status
            db.session.commit()
            return {'message': 'Claim status updated successfully.'}, 200
        except Exception as e:
            # Handle any exceptions that occur during the claim update
            return {'error': str(e)}, 500

    # delete_claim method deletes an existing business claim.
    def delete_claim(self, claim_id):
        try:
            # Fetch the claim from the database
            claim = BusinessClaim.query.get(claim_id)
            if not claim:
                return {'message': 'Claim not found.'}, 404
            # Delete the claim from the database session and commit it
            db.session.delete(claim)
            db.session.commit()
            return {'message': 'Claim deleted successfully.'}, 200
        except Exception as e:
            # Handle any exceptions that occur during the claim deletion
            return {'error': str(e)}, 500