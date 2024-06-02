from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from database import db

bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False)  # New field to distinguish user roles
    bookmarkedBusinesses = db.relationship('Bookmark', backref='user', lazy=True)

    def __init__(self, username, name, email, password, role="user"):
        self.username = username
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role  # Set the role

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.role == 'admin'