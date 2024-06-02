import pytest
from controllers.platform_management_controller import PlatformManagementController
from models import User, Business, Review
from database import db

# Create a fixture for the controller
@pytest.fixture
def controller():
    return PlatformManagementController()

# Test the monitor_platform method
def test_monitor_platform(controller):
    # Mock the data
    user = User(username='testuser', email='testuser@example.com', password='testpassword')
    business = Business(businessID='testBusiness', name='Test Business')
    review = Review(reviewID='testReview', content='This is a test review', ratingValue=5)
    db.session.add(user)
    db.session.add(business)
    db.session.add(review)
    db.session.commit()

    # Call the method and check the response
    platform_stats, status = controller.monitor_platform()
    assert status == 200
    assert platform_stats['users'] == 1
    assert platform_stats['businesses'] == 1
    assert platform_stats['reviews'] == 1

    # Test the unhappy scenario (exception)
    with pytest.raises(Exception):
        User.query.count()  # Simulate an exception

# Test the execute_tasks method
def test_execute_tasks(controller, monkeypatch):
    # Mock the monitor_platform method
    def mock_monitor_platform():
        return {'users': 1, 'businesses': 1, 'reviews': 1}, 200

    monkeypatch.setattr(controller, 'monitor_platform', mock_monitor_platform)

    # Call the method and check the response
    response, status = controller.execute_tasks()
    assert status == 200
    assert response['message'] == 'Platform metrics updated successfully.'

    # Test the unhappy scenario (exception)
    def mock_monitor_platform_error():
        raise Exception('Test exception')

    monkeypatch.setattr(controller, 'monitor_platform', mock_monitor_platform_error)

    with pytest.raises(Exception):
        controller.execute_tasks()

# Test the dashboard_data method
def test_dashboard_data(controller, monkeypatch):
    # Mock the dashboard.get_metrics method
    def mock_get_metrics():
        return {'users': 1, 'businesses': 1, 'reviews': 1}

    monkeypatch.setattr(controller.dashboard, 'get_metrics', mock_get_metrics)

    # Call the method and check the response
    dashboard_info, status = controller.dashboard_data()
    assert status == 200
    assert 'users' in dashboard_info
    assert 'businesses' in dashboard_info
    assert 'reviews' in dashboard_info

    # Test the unhappy scenario (exception)
    def mock_get_metrics_error():
        raise Exception('Test exception')

    monkeypatch.setattr(controller.dashboard, 'get_metrics', mock_get_metrics_error)

    with pytest.raises(Exception):
        controller.dashboard_data()
