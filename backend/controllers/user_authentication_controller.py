from flask_login import logout_user, login_user
from models import User
from werkzeug.security import check_password_hash

# Controller for user authentication
class UserAuthenticationController:
    # Method to handle user login
    def login(self, username, password):
        try:
            # Fetch the user by username
            user = User.query.filter_by(username=username).first()
            # If user exists and password is correct, log the user in
            if user and check_password_hash(user.password, password):
                login_user(user)
                return {'message': 'Logged in successfully.'}, 200
            # If user doesn't exist or password is incorrect, return an error
            return {'message': 'Invalid username or password.'}, 401
        except Exception as e:
            # If any exception occurs, return an error
            return {'error': str(e)}, 500

    # Method to handle user logout
    def logout(self):
        try:
            # Log the user out
            logout_user()
            return {'message': 'Logged out successfully.'}, 200
        except Exception as e:
            # If any exception occurs, return an error
            return {'error': str(e)}, 500