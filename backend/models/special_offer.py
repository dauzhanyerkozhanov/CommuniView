from database import db
from datetime import datetime

class SpecialOffer(db.Model):
    offerID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(500))
    expirationDate = db.Column(db.DateTime)
    associatedBusiness = db.Column(db.String(50), db.ForeignKey('business.businessID'))

def __init__(self, title, description, expirationDate, associatedBusiness):
    if not title or not description or not associatedBusiness:
        raise ValueError("Title, description, and associatedBusiness cannot be empty.")
    if not isinstance(expirationDate, datetime):
        raise TypeError("expirationDate must be a datetime object.")
    self.title = title
    self.description = description
    self.expirationDate = expirationDate
    self.associatedBusiness = associatedBusiness