from flask import request, jsonify, Flask
from models import SpecialOffer, User, Business
from database import db
from forms import SpecialOfferForm
import unittest
from datetime import datetime, timedelta
from controllers.special_offer_controller import SpecialOfferController

app = Flask(__name__)
class SpecialOfferControllerTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.controller = SpecialOfferController()
        self.user = User(name='Test User', email='testuser@example.com')
        self.business = Business(name='Test Business', owner=self.user)
        db.session.add(self.user)
        db.session.add(self.business)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_special_offer(self):
        title = 'Test Offer'
        description = 'Test Description'
        expiration_date = datetime.now() + timedelta(days=30)
        response, status_code = self.controller.create_special_offer(self.user, title, description, expiration_date, self.business)
        self.assertEqual(status_code, 201)
        self.assertEqual(response['message'], 'Special offer created successfully.')

    def test_create_special_offer_unauthorized(self):
        other_user = User(name='Other User', email='otheruser@example.com')
        db.session.add(other_user)
        db.session.commit()
        title = 'Test Offer'
        description = 'Test Description'
        expiration_date = datetime.now() + timedelta(days=30)
        response, status_code = self.controller.create_special_offer(other_user, title, description, expiration_date, self.business)
        self.assertEqual(status_code, 403)
        self.assertEqual(response['message'], 'Unauthorized.')

    def test_edit_offer(self):
        offer = SpecialOffer(title='Test Offer', description='Test Description', expiration_date=datetime.now() + timedelta(days=30), associated_business=self.business)
        db.session.add(offer)
        db.session.commit()
        new_title = 'Updated Offer'
        new_description = 'Updated Description'
        new_expiration_date = datetime.now() + timedelta(days=60)
        response, status_code = self.controller.edit_offer(offer.id, self.user, new_title, new_description, new_expiration_date)
        self.assertEqual(status_code, 200)
        self.assertEqual(response['message'], 'Special offer updated successfully.')

    def test_edit_offer_unauthorized(self):
        other_user = User(name='Other User', email='otheruser@example.com')
        db.session.add(other_user)
        db.session.commit()
        offer = SpecialOffer(title='Test Offer', description='Test Description', expiration_date=datetime.now() + timedelta(days=30), associated_business=self.business)
        db.session.add(offer)
        db.session.commit()
        new_title = 'Updated Offer'
        new_description = 'Updated Description'
        new_expiration_date = datetime.now() + timedelta(days=60)
        response, status_code = self.controller.edit_offer(offer.id, other_user, new_title, new_description, new_expiration_date)
        self.assertEqual(status_code, 403)
        self.assertEqual(response['message'], 'Unauthorized.')

    def test_delete_offer(self):
        offer = SpecialOffer(title='Test Offer', description='Test Description', expiration_date=datetime.now() + timedelta(days=30), associated_business=self.business)
        db.session.add(offer)
        db.session.commit()
        response, status_code = self.controller.delete_offer(offer.id, self.user)
        self.assertEqual(status_code, 200)
        self.assertEqual(response['message'], 'Special offer deleted successfully.')

    def test_delete_offer_unauthorized(self):
        other_user = User(name='Other User', email='otheruser@example.com')
        db.session.add(other_user)
        db.session.commit()
        offer = SpecialOffer(title='Test Offer', description='Test Description', expiration_date=datetime.now() + timedelta(days=30), associated_business=self.business)
        db.session.add(offer)
        db.session.commit()
        response, status_code = self.controller.delete_offer(offer.id, other_user)
        self.assertEqual(status_code, 403)
        self.assertEqual(response['message'], 'Unauthorized.')

    def test_get_offer(self):
        offer = SpecialOffer(title='Test Offer', description='Test Description', expiration_date=datetime.now() + timedelta(days=30), associated_business=self.business)
        db.session.add(offer)
        db.session.commit()
        response, status_code = self.controller.get_offer(offer.id, self.user)
        self.assertEqual(status_code, 200)
        self.assertEqual(response['title'], 'Test Offer')
        self.assertEqual(response['description'], 'Test Description')

    def test_get_offer_not_found(self):
        response, status_code = self.controller.get_offer(999)  # Non-existent offer ID
        self.assertEqual(status_code, 404)
        self.assertEqual(response['message'], 'Special offer not found.')

    if __name__ == '__main__':
        unittest.main()
        