import pytest
from database import db
from models.business import Business

def setup_module(module):
    # Setup for the tests: create a new business
    module.test_business = Business('testBusiness', 'Test Name', '123 Test St', '1234567890', 'Test Category', 'Test Description', '9am-5pm', 'photo1,photo2', 4.5, 'tag1,tag2')
    db.session.add(module.test_business)
    db.session.commit()

def teardown_module(module):
    # Teardown for the tests: remove the test business
    db.session.delete(module.test_business)
    db.session.commit()

def test_business_model():
    # Fetch the business from the database
    business = Business.query.get('testBusiness')

    # Check that the business has the correct properties
    assert business.name == 'Test Name'
    assert business.address == '123 Test St'
    assert business.phoneNumber == '1234567890'
    assert business.category == 'Test Category'
    assert business.description == 'Test Description'
    assert business.businessHours == '9am-5pm'
    assert business.photos == 'photo1,photo2'
    assert business.ratings == 4.5
    assert business.trendingTags == 'tag1,tag2'

def test_business_model_invalid_inputs():
    # Test with an empty business ID
    with pytest.raises(ValueError):
        Business('', 'Test Name', '123 Test St', '1234567890', 'Test Category', 'Test Description', '9am-5pm', 'photo1,photo2', 4.5, 'tag1,tag2')

    # Test with an empty name
    with pytest.raises(ValueError):
        Business('testBusiness', '', '123 Test St', '1234567890', 'Test Category', 'Test Description', '9am-5pm', 'photo1,photo2', 4.5, 'tag1,tag2')

    # Test with an invalid phone number
    with pytest.raises(ValueError):
        Business('testBusiness', 'Test Name', '123 Test St', 'invalid_phone', 'Test Category', 'Test Description', '9am-5pm', 'photo1,photo2', 4.5, 'tag1,tag2')

    # Test with an invalid rating
    with pytest.raises(ValueError):
        Business('testBusiness', 'Test Name', '123 Test St', '1234567890', 'Test Category', 'Test Description', '9am-5pm', 'photo1,photo2', 10, 'tag1,tag2')

def test_business_model_unique_constraint():
    # Create a duplicate business with the same name
    duplicate_business = Business('duplicateBusiness', 'Test Name', '456 Test St', '9876543210', 'Test Category', 'Test Description', '9am-5pm', 'photo3,photo4', 4.0, 'tag3,tag4')
    db.session.add(duplicate_business)

    # Check that a ValueError is raised when trying to add a duplicate business
    with pytest.raises(ValueError):
        db.session.commit()

    # Clean up the duplicate business
    db.session.rollback()
