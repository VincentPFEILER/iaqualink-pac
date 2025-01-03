from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.const import CONF_SCAN_INTERVAL
from .const import DOMAIN

import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Zodiac PAC sensor from a config entry."""
    session = async_get_clientsession(hass)
    secrets = hass.config.as_dict().get('secrets', {})
    authorization = secrets.get("zodiac_authorization")
    serial_number = secrets.get("serial_number")

    if not authorization or not serial_number:
        _LOGGER.error("Missing secrets in secrets.yaml.")
        return

    api = ZodiacAPI(session, authorization, serial_number)
    async_add_entities([ZodiacSensor(api)], True)

class ZodiacAPI:
    """Class to interact with Zodiac API."""

    def __init__(self, session, authorization, serial_number):
        self._session = session
        self._authorization = authorization
        self._serial_number = serial_number
        self._base_url = f"https://prod.zodiac-io.com/devices/v1/{self._serial_number}/shadow"

    async def fetch_data(self):
        headers = {
            "Authorization": self._authorization,
            "User-Agent": "okhttp/3.12.0",
            "Accept": "application/json",
            "Accept-Encoding": "gzip"
        }
        async with self._session.get(self._base_url, headers=headers) as response:
            if response.status != 200:
                _LOGGER.error(f"Error fetching data: {response.status}")
                return None
            return await response.json()

class ZodiacSensor(SensorEntity):
    """Define a Zodiac PAC sensor."""

    def __init__(self, api):
        self._api = api
        self._state = None

    @property
    def name(self):
        return "Zodiac PAC Status"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Fetch the latest data from the API."""
        data = await self._api.fetch_data()
        if data:
            self._state = data.get("state", {}).get("reported", {}).get("equipment", {}).get("hp_0", {}).get("state")
