import pytest
from controllers.api_connector import APIConnector
from unittest.mock import patch, Mock

class TestAPIConnector:
    @pytest.fixture
    def connector(self):
        # Setup: Create an instance of APIConnector with test API key and URL
        return APIConnector('test_key', 'http://testurl.com')

    @patch('requests.get')
    def test_send_request_get(self, mock_get, connector):
        # Setup: Create a mock response
        mock_response = Mock()
        mock_get.return_value = mock_response
        # Action: Call send_request with a test endpoint
        response = connector.send_request('endpoint')
        # Assert: Verify that requests.get was called with the correct arguments and that the response matches the mock response
        mock_get.assert_called_once_with('http://testurl.com/endpoint', headers={'Authorization': 'Bearer test_key'}, json=None)
        assert response == mock_response

    @patch('requests.post')
    def test_send_request_post(self, mock_post, connector):
        # Setup: Create a mock response
        mock_response = Mock()
        mock_post.return_value = mock_response
        # Action: Call send_request with a test endpoint and POST method
        response = connector.send_request('endpoint', 'POST', {'key': 'value'})
        # Assert: Verify that requests.post was called with the correct arguments and that the response matches the mock response
        mock_post.assert_called_once_with('http://testurl.com/endpoint', headers={'Authorization': 'Bearer test_key'}, json={'key': 'value'})
        assert response == mock_response

    def test_parse_response(self, connector):
        # Setup: Create a mock response with status code 200 and a json method that returns a test value
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'key': 'value'}
        # Action: Parse the mock response
        result = connector.parse_response(mock_response)
        # Assert: Verify that the parsed result matches the expected value
        assert result == {'key': 'value'}

    def test_parse_response_failure(self, connector):
        # Setup: Create a mock response with status code 404
        mock_response = Mock()
        mock_response.status_code = 404
        # Action: Parse the mock response
        result = connector.parse_response(mock_response)
        # Assert: Verify that the parsed result is None, as expected for a failure response
        assert result is None

    def test_parse_response_exception(self, connector):
        # Setup: Create a mock response that raises an exception when json() is called
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError('Invalid JSON')
        if mock_response.status_code == 200:
            try:
                return mock_response.json()
            except ValueError:
                # Handle the case where the response body cannot be parsed as JSON
                return None
        # Action: Parse the mock response
        result = connector.parse_response(mock_response)
        # Assert: Verify that the parsed result is None, as expected for an exception
        assert result is None

    def test_init(self):
        # Action: Create an instance of APIConnector with test API key and URL
        connector = APIConnector('test_key', 'http://testurl.com')
        # Assert: Verify that the API key and URL are set correctly
        assert connector.api_key == 'test_key'
        assert connector.api_url == 'http://testurl.com'