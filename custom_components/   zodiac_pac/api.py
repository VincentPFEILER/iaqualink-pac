import requests
from .const import API_URL, API_KEY

class ZodiacAPI:
    """Handle communication with the Zodiac API."""

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.id_token = None

    def authenticate(self):
        """Authenticate the user and retrieve the token."""
        url = f"{API_URL}/users/v1/login"
        payload = {
            "apiKey": API_KEY,
            "email": self.email,
            "password": self.password,
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            self.id_token = data.get("IdToken")
        else:
            raise Exception("Authentication failed")
