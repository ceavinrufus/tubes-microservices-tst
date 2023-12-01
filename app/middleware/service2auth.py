import requests
from datetime import datetime, timedelta

class Service2AuthMiddleware:
    def __init__(self, service2_login_url, username, password):
        self.service2_login_url = service2_login_url
        self.username = username
        self.password = password
        self.token = None
        self.token_expiration = None

    def login_to_service2(self):
        data = {
            "username": self.username,
            "password": self.password
        }

        response = requests.post(self.service2_login_url, json=data)

        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data.get('token')
            self.token_expiration = datetime.utcnow() + timedelta(minutes=300)  # Adjust token expiration
            print("Token acquired successfully.")
        else:
            print("Failed to acquire token.")
            print("Response status code:", response.status_code)
            print("Response text:", response.text)
            raise Exception('Failed to login to Service 2')

    def get_token(self):
        if not self.token or datetime.utcnow() > self.token_expiration:
            self.login_to_service2()

        return self.token

    def make_authenticated_request(self, service2_endpoint_url, method='GET', params=None, data=None):
        token = self.get_token()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        if method == 'GET':
            response = requests.get(service2_endpoint_url, headers=headers, params=params)
        elif method == 'POST':
            response = requests.post(service2_endpoint_url, headers=headers, params=params, json=data)
        # Add more conditions for other HTTP methods as needed (PUT, DELETE, etc.)

        return response  # Return the response object
