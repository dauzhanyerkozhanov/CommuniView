from database import db

class BusinessClaim(db.Model):
    claimID = db.Column(db.Integer, primary_key=True)
    businessID = db.Column(db.String(50), db.ForeignKey('business.businessID'))
    ownerID = db.Column(db.String(50))
    claimStatus = db.Column(db.String(50))
    proofDocuments = db.Column(db.String(200))

def __init__(self, businessID, ownerID, claimStatus, proofDocuments):
    if not businessID.strip():
        raise ValueError("businessID cannot be empty.")
    if not ownerID.strip():
        raise ValueError("ownerID cannot be empty.")
    if not claimStatus.strip():
        raise ValueError("claimStatus cannot be empty.")
    self.businessID = businessID
    self.ownerID = ownerID
    self.claimStatus = claimStatus
    self.proofDocuments = proofDocuments

