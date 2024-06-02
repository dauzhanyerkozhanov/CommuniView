import pytest
from database import db
from models.user import User, bcrypt

def setup_module(module):
    # Setup for the tests: create a new user
    module.test_user = User('testuser', 'Test User', 'testuser@example.com', 'password', 'user')
    module.test_admin = User('testadmin', 'Test Admin', 'testadmin@example.com', 'adminpassword', 'admin')
    db.session.add(module.test_user)
    db.session.add(module.test_admin)
    db.session.commit()

def teardown_module(module):
    # Teardown for the tests: remove the test users
    db.session.delete(module.test_user)
    db.session.delete(module.test_admin)
    db.session.commit()

def test_user_model():
    # Fetch the user from the database
    user = User.query.get(1)
    admin = User.query.get(2)

    # Check that the user has the correct properties
    assert user.username == 'testuser'
    assert user.name == 'Test User'
    assert user.email == 'testuser@example.com'
    assert bcrypt.check_password_hash(user.password, 'password')
    assert user.role == 'user'
    assert user.is_authenticated
    assert user.is_active
    assert not user.is_anonymous
    assert not user.is_admin()

    # Check that the admin has the correct properties
    assert admin.username == 'testadmin'
    assert admin.name == 'Test Admin'
    assert admin.email == 'testadmin@example.com'
    assert bcrypt.check_password_hash(admin.password, 'adminpassword')
    assert admin.role == 'admin'
    assert admin.is_authenticated
    assert admin.is_active
    assert not admin.is_anonymous
    assert admin.is_admin()

def test_get_id():
    user = User.query.get(1)
    assert user.get_id() == 1

def test_password_hashing():
    password = 'testpassword'
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    assert bcrypt.check_password_hash(hashed_password, password)

def test_invalid_password():
    password = 'wrongpassword'
    user = User.query.get(1)
    assert not bcrypt.check_password_hash(user.password, password)
