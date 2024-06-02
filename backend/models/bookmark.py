from database import db

class Bookmark(db.Model):
    bookmarkID = db.Column(db.Integer, primary_key=True)
    associatedUser = db.Column(db.String(50), db.ForeignKey('user.username'))
    associatedBusiness = db.Column(db.String(50), db.ForeignKey('business.businessID'))

def __init__(self, bookmarkID, associatedUser, associatedBusiness):
    if not isinstance(bookmarkID, int):
        raise ValueError("bookmarkID must be an integer")
    if associatedUser is None or associatedBusiness is None:
        raise ValueError("associatedUser and associatedBusiness cannot be None")
    self.bookmarkID = bookmarkID
    self.associatedUser = associatedUser
    self.associatedBusiness = associatedBusiness
