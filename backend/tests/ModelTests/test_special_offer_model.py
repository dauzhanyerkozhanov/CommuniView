import pytest
from database import db
from models.special_offer import SpecialOffer
from datetime import datetime, timedelta
import time

def setup_module(module):
    # Setup for the tests: create a new special offer
    module.test_offer = SpecialOffer('Test Offer', 'This is a test offer', datetime(2022, 12, 31), 'testBusiness')
    db.session.add(module.test_offer)
    db.session.commit()

def teardown_module(module):
    # Teardown for the tests: remove the test offer
    db.session.delete(module.test_offer)
    db.session.commit()

def test_special_offer_model():
    # Fetch the offer from the database
    offer = SpecialOffer.query.get(1)

    # Check that the offer has the correct properties
    assert offer.title == 'Test Offer'
    assert offer.description == 'This is a test offer'
    assert offer.expirationDate == datetime(2022, 12, 31)
    assert offer.associatedBusiness == 'testBusiness'

def test_special_offer_expiration():
    # Create an expired offer
    expired_offer = SpecialOffer('Expired Offer', 'This offer has expired', datetime.now() - timedelta(days=1), 'testBusiness')
    db.session.add(expired_offer)
    db.session.commit()

    # Check that the offer is marked as expired
    assert expired_offer.is_expired() is True

    # Clean up the expired offer
    db.session.delete(expired_offer)
    db.session.commit()

def test_special_offer_invalid_inputs():
    # Test invalid title
    with pytest.raises(ValueError):
        SpecialOffer('', 'Invalid title', datetime.now(), 'testBusiness')

    # Test invalid description
    with pytest.raises(ValueError):
        SpecialOffer('Invalid Description', '', datetime.now(), 'testBusiness')

    # Test invalid expiration date
    with pytest.raises(ValueError):
        SpecialOffer('Invalid Expiration', 'Invalid expiration date', '2022-01-01', 'testBusiness')

    # Test invalid associated business
    with pytest.raises(ValueError):
        SpecialOffer('Invalid Business', 'Invalid associated business', datetime.now(), '')
