from database import db

class Business(db.Model):
    businessID = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    address = db.Column(db.String(120))
    phoneNumber = db.Column(db.String(20))
    category = db.Column(db.String(50))
    description = db.Column(db.String(500))
    businessHours = db.Column(db.String(50))
    photos = db.Column(db.String(200))
    reviews = db.relationship('Review', backref='business', lazy=True)
    ratings = db.Column(db.Float)
    specialOffers = db.relationship('SpecialOffer', backref='business', lazy=True)
    trendingTags = db.Column(db.String(50))

def __init__(self, businessID, name, address, phoneNumber, category, description, businessHours, photos, ratings, trendingTags):
    if not businessID:
        raise ValueError("Business ID cannot be empty")
    if not name:
        raise ValueError("Name cannot be empty")
    if len(phoneNumber) != 10 or not phoneNumber.isdigit():
        raise ValueError("Invalid phone number")
    if not 0 <= ratings <= 5:
        raise ValueError("Ratings must be between 0 and 5")

    self.businessID = businessID
    self.name = name
    self.address = address
    self.phoneNumber = phoneNumber
    self.category = category
    self.description = description
    self.businessHours = businessHours
    self.photos = photos
    self.ratings = ratings
    self.trendingTags = trendingTags