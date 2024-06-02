import requests

# Class for connecting to an API
class APIConnector:
    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url

    def send_request(self, endpoint, method='GET', params=None):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        url = f'{self.api_url}/{endpoint}'
        request_func = getattr(requests, method.lower())
        response = request_func(url, headers=headers, json=params)
        return response

    def parse_response(self, response):
        if response.status_code == 200:
            return response.json()
        return None
