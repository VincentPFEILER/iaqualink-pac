from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    api = ZodiacPacAPI(
        config_entry.data["username"],
        config_entry.data["password"]
    )
    async_add_entities([ZodiacPacSensor(api)])

class ZodiacPacSensor(SensorEntity):
    def __init__(self, api):
        self.api = api
        self._state = None

    @property
    def name(self):
        return "Zodiac PAC"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        self._state = self.api.get_pac_info().get("current_temperature")

