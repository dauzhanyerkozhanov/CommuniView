from models import User
from database import db
from forms import RegistrationForm
from flask_mail import Mail, Message

# Initialize Flask-Mail
mail = Mail()

# Controller for user registration
class UserRegistrationController:
    def __init__(self):
        # Initialize the registration form
        self.registration_form = RegistrationForm()

    # Method to handle form submission
    def submit_form(self):
        # Validate the form data
        if self.registration_form.validate_on_submit():
            try:
                # Create a new user with the form data
                new_user = User(username=self.registration_form.username.data, email=self.registration_form.email.data, password=self.registration_form.password.data)
                # Add the new user to the database session
                db.session.add(new_user)
                # Commit the session to save the new user
                db.session.commit()

                # Create a welcome message
                msg = Message('Welcome!', sender='your_email@example.com', recipients=[new_user.email])
                msg.body = 'Thank you for registering at our site!'
                # Send the welcome message
                mail.send(msg)

                # Return a success response
                return {'message': 'User registered successfully.'}, 201
            except Exception as e:
                # Return an error response in case of an exception
                return {'error': str(e)}, 500
        # Return a validation failure response
        return {'message': 'Validation failed.'}, 400