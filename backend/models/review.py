from database import db

class Review(db.Model):
    reviewID = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), db.ForeignKey('user.username'))
    content = db.Column(db.String(500))
    ratingValue = db.Column(db.Integer)
    associatedBusiness = db.Column(db.String(50), db.ForeignKey('business.businessID'))

def __init__(self, reviewID, author, content, ratingValue, associatedBusiness):
    if not author or not content or ratingValue not in range(1, 6):
        raise ValueError("Invalid input for the review.")
    self.reviewID = reviewID
    self.author = author
    self.content = content
    self.ratingValue = ratingValue
    self.associatedBusiness = associatedBusiness