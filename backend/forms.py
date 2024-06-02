# Importing necessary modules and classes for form creation and validation
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange
from models import User

# Form for user registration
class RegistrationForm(FlaskForm):
    # Fields for user input
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # Custom validation for username
    def validate_username(self, username):
        # Check if username already exists in the database
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    # Custom validation for email
    def validate_email(self, email):
        # Check if email already exists in the database
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is registered. Please choose a different one.')

# Form for user login
class LoginForm(FlaskForm):
    # Fields for user input
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Form for claiming a business
class BusinessClaimForm(FlaskForm):
    # Fields for business details
    business_name = StringField('Business Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Claim')

# Form for updating business details
class BusinessUpdateForm(FlaskForm):
    # Fields for business details
    business_name = StringField('Business Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    business_description = StringField('Business Description', validators=[DataRequired()])
    submit = SubmitField('Update')

# Form for submitting a review
class ReviewForm(FlaskForm):
    # Fields for review details
    content = StringField('Content', validators=[DataRequired()])
    rating_value = IntegerField('Rating Value', validators=[DataRequired(), NumberRange(min=1, max=5)])
    associated_business = StringField('Associated Business', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Form for creating a special offer
class SpecialOfferForm(FlaskForm):
    # Fields for offer details
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    expiration_date = DateTimeField('Expiration Date', validators=[DataRequired()])
    associated_business = StringField('Associated Business', validators=[DataRequired()])
    submit = SubmitField('Create')

# Form for creating a bookmark
class BookmarkForm(FlaskForm):
    # Fields for bookmark details
    associated_user = StringField('Associated User', validators=[DataRequired()])
    associated_business = StringField('Associated Business', validators=[DataRequired()])
    submit = SubmitField('Create')

# Form for creating a trending tag
class TrendingTagForm(FlaskForm):
    # Fields for tag details
    name = StringField('Tag Name', validators=[DataRequired()])
    popularity_score = IntegerField('Popularity Score', validators=[DataRequired()])
    submit = SubmitField('Create')