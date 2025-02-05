import requests
import logging
import json


BASE_URL = "https://mapi.talent-monitoring.com/prod-api"
BASE_HEADERS = {"Content-type": "application/json;charset=utf-8"}

_LOGGER: logging.Logger = logging.getLogger(__name__)

class DataProvider():
    def __init__(self, username: str, password: str):
        self._url = BASE_URL
        self._username = username
        self._password = password
        self._token = None

    def login(self):
        """Log in using the given credentials."""
        login_data = {"username": self._username, "password": self._password}
        response = requests.post(f"{self._url}/login", data=json.dumps(login_data), headers=BASE_HEADERS)
        #print(response.status_code)
        response_data = response.json()
        print(response_data)

        if "token" in response_data:
            self._token = response_data["token"]
            _LOGGER.debug("Login successful - received token: %s", self._token)
        else:
            _LOGGER.error("Login failed. Token missing in response. Got status code %s", response_data.code)
            raise AuthenticationError("Authentication failed")
        
    def refresh_token(self):
        """Refresh the token."""
        _LOGGER.debug("Token expired. Refreshing token...")
        self.login()

    def get_data(self, endpoint):
        """Get data from the given endpoint."""
        if not self._token:
            self.login()
        headers = BASE_HEADERS
        headers["Authorization"] = f"Bearer {self._token}"
        response = requests.get(f"{self._url}/{endpoint}", headers=headers)
        if response.status_code == 401:  # Unauthorized, token might be expired
            self.refresh_token()
            headers["Authorization"] = f"Bearer {self._token}"
            response = requests.get(f"{self._url}/{endpoint}", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            _LOGGER.error("Failed to fetch data. Status Code: %s", response.status_code)
            return None
        
class Entity:
    """Base class for TalentMonitor entities."""

    def __init__(self, entity_id: str, name: str) -> None:
        """Initialize the entity."""
        self.entity_id = entity_id
        self.name = name
        self._data = {}

    @property
    def data(self):
        """Return the data of the entity."""
        return self._data

    @data.setter
    def data(self, data):
        """Set the data of the entity."""
        self._data = data

class AuthenticationError(Exception):
    """AuthenticationError when connecting to the Talent API."""

    pass