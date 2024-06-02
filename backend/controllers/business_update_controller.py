from models import Business
from database import db
from forms import BusinessUpdateForm

# Controller for updating business information
class BusinessUpdateController:
    def __init__(self):
        # Initialize the form for updating business information
        self.update_form = BusinessUpdateForm()

    # Method to handle form submission
    def submit_form(self):
        # Validate the form data
        if self.update_form.validate_on_submit():
            try:
                # Fetch the business record from the database
                business = Business.query.get(self.update_form.business_id.data)
                # If the business exists, update its information
                if business:
                    business.name = self.update_form.name.data
                    business.address = self.update_form.address.data
                    business.phone_number = self.update_form.phone_number.data
                    business.category = self.update_form.category.data
                    business.description = self.update_form.description.data
                    business.business_hours = self.update_form.business_hours.data
                    # Commit the changes to the database
                    db.session.commit()
                    # Return a success message
                    return {'message': 'Business updated successfully.'}, 200
                # If the business does not exist, return an error message
                return {'message': 'Business not found.'}, 404
            # Handle any exceptions that occur during the update process
            except Exception as e:
                return {'error': str(e)}, 500
        # If form validation fails, return an error message
        return {'message': 'Validation failed.'}, 400