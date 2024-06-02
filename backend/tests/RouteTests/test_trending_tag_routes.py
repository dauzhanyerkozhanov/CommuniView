import pytest
from app import create_app
from models import db, TrendingTag, Business
from controllers.trending_tag_controller import TrendingTagController

@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

def setup_module(module):
    pass

def teardown_module(module):
    pass

def test_create_trending_tag(client):
    # Test the happy scenario
    response = client.post('/tags', data={'name': 'TestTag', 'popularity_score': 5})
    assert response.status_code == 200
    assert response.json['name'] == 'TestTag'

    # Test the unhappy scenario (empty name)
    response = client.post('/tags', data={'name': '', 'popularity_score': 5})
    assert response.status_code == 400
    assert 'Form validation failed' in response.json['message']

def test_edit_trending_tag(client):
    # Setup test data: Create a tag to be edited
    tag = TrendingTag(name='InitialTag', popularity_score=1)
    db.session.add(tag)
    db.session.commit()

    # Test the happy scenario
    response = client.put(f'/tags/{tag.id}', data={'name': 'EditedTag', 'popularity_score': 10})
    assert response.status_code == 200
    assert response.json['name'] == 'EditedTag'

    # Test the unhappy scenario (invalid tag_id)
    response = client.put('/tags/999', data={'name': 'EditedTag', 'popularity_score': 10})
    assert response.status_code == 404
    assert 'Tag not found' in response.json['message']

def test_delete_trending_tag(client):
    # Setup test data: Create a tag to be deleted
    tag = TrendingTag(name='ToDeleteTag', popularity_score=2)
    db.session.add(tag)
    db.session.commit()

    # Test the happy scenario
    response = client.delete(f'/tags/{tag.id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Tag deleted successfully'

    # Test the unhappy scenario (invalid tag_id)
    response = client.delete('/tags/999')
    assert response.status_code == 404
    assert 'Tag not found' in response.json['message']

def test_get_trending_tags(client):
    # Setup test data: Create some trending tags
    tag1 = TrendingTag(name='Tag1', popularity_score=3)
    tag2 = TrendingTag(name='Tag2', popularity_score=5)
    db.session.add_all([tag1, tag2])
    db.session.commit()

    # Test the happy scenario
    response = client.get('/tags')
    assert response.status_code == 200
    assert len(response.json) == 2
    assert {'id': tag1.id, 'name': 'Tag1', 'popularity_score': 3} in response.json
    assert {'id': tag2.id, 'name': 'Tag2', 'popularity_score': 5} in response.json

def test_get_businesses_for_tag(client):
    # Setup test data: Create a tag and associate it with businesses
    tag = TrendingTag(name='TagWithBusinesses', popularity_score=4)
    business1 = Business(name='Business1')
    business2 = Business(name='Business2')
    tag.businesses.extend([business1, business2])
    db.session.add(tag)
    db.session.commit()

    # Test the happy scenario
    response = client.get(f'/tags/{tag.id}/businesses')
    assert response.status_code == 200
    assert len(response.json) == 2
    assert 'Business1' in response.json
    assert 'Business2' in response.json

    # Test the unhappy scenario (invalid tag_id)
    response = client.get('/tags/999/businesses')
    assert response.status_code == 404
    assert 'Tag not found or no businesses associated' in response.json['message']
