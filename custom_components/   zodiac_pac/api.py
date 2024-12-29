import requests

BASE_URL = "https://prod.zodiac-io.com"

class ZodiacPacAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None

    def authenticate(self):
        url = f"{BASE_URL}/login"
        payload = {"username": self.username, "password": self.password}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            self.token = response.json().get("token")
        else:
            raise Exception("Authentication failed")

    def get_pac_info(self):
        if not self.token:
            self.authenticate()
        url = f"{BASE_URL}/api/v1/pac"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch PAC info")

