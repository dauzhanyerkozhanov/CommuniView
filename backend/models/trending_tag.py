from database import db

class TrendingTag(db.Model):
    tagID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    popularityScore = db.Column(db.Integer)
    associatedBusinesses = db.Column(db.String(50))

def __init__(self, name, popularityScore, associatedBusinesses=None):
    self.name = name
    self.popularityScore = popularityScore
    self.associatedBusinesses = associatedBusinesses
