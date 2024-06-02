import pytest
from database import db
from models.business_claim import BusinessClaim

def setup_module(module):
    # Setup for the tests: create a new business claim
    module.test_claim = BusinessClaim('testBusiness', 'testUser', 'pending', 'doc1, doc2')
    db.session.add(module.test_claim)
    db.session.commit()

def teardown_module(module):
    # Teardown for the tests: remove the test claim
    db.session.delete(module.test_claim)
    db.session.commit()

def test_business_claim_model(module):
    # Fetch the claim from the database
    claim = BusinessClaim.query.get(module.test_claim.claimID)
    # Check that the claim has the correct properties
    assert claim.businessID == 'testBusiness'
    assert claim.ownerID == 'testUser'
    assert claim.claimStatus == 'pending'
    assert claim.proofDocuments == 'doc1, doc2'

def test_business_claim_init():
    claim = BusinessClaim('testBusiness2', 'testUser2', 'pending', 'doc3, doc4')
    assert claim.businessID == 'testBusiness2'
    assert claim.ownerID == 'testUser2'
    assert claim.claimStatus == 'pending'
    assert claim.proofDocuments == 'doc3, doc4'

def test_business_claim_empty_claim_status():
    with pytest.raises(ValueError):
        BusinessClaim('testBusiness3', 'testUser3', '', 'doc5')

def test_business_claim_empty_proof_documents():
    claim = BusinessClaim('testBusiness4', 'testUser4', 'pending', '')
    assert claim.proofDocuments == ''

def test_business_claim_empty_business_id():
    with pytest.raises(ValueError):
        BusinessClaim('', 'testUser5', 'pending', 'doc6')

def test_business_claim_empty_owner_id():
    with pytest.raises(ValueError):
        BusinessClaim('testBusiness6', '', 'pending', 'doc7')