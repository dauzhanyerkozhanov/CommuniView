import pytest
from unittest.mock import patch, MagicMock

from controllers.search_controller import SearchController
from models import Business

@pytest.fixture
def search_controller():
    return SearchController()

@pytest.fixture
def mock_business_model():
    with patch('search_controller.Business') as mock_business:
        mock_business.query = MagicMock()
        yield mock_business

def test_execute_search_successful(search_controller, mock_business_model):
    # Arrange
    query = 'test'
    mock_business_model.query.filter.return_value.all.return_value = [Business(name='Test Business')]

    # Act
    result, status_code = search_controller.execute_search(query)

    # Assert
    assert status_code == 200
    assert len(result) == 1
    assert result[0].name == 'Test Business'

def test_execute_search_exception(search_controller, mock_business_model):
    # Arrange
    query = 'test'
    mock_business_model.query.filter.side_effect = Exception('Test exception')

    # Act
    result, status_code = search_controller.execute_search(query)

    # Assert
    assert status_code == 500
    assert result == {'error': 'Test exception'}

def test_display_results_successful(search_controller):
    # Arrange
    search_controller.search_results = [Business(name='Test Business')]

    # Act
    result, status_code = search_controller.display_results()

    # Assert
    assert status_code == 200
    assert len(result) == 1
    assert result[0].name == 'Test Business'

def test_display_results_no_search(search_controller):
    # Act
    result, status_code = search_controller.display_results()

    # Assert
    assert status_code == 400
    assert result == {'message': 'No search executed prior to displaying results.'}

def test_display_results_exception(search_controller):
    # Arrange
    search_controller.search_results = [Business(name='Test Business')]

    # Act
    with patch('search_controller.SearchController.display_results', side_effect=Exception('Test exception')):
        result, status_code = search_controller.display_results()

    # Assert
    assert status_code == 500
    assert result == {'error': 'Test exception'}
