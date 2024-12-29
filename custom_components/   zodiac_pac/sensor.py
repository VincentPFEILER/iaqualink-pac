import logging
from homeassistant.components.sensor import SensorEntity
from .api import ZodiacAPI

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor from a config entry."""
    try:
        # Vérifiez la présence des données nécessaires
        email = config_entry.data.get("email")
        password = config_entry.data.get("password")

        if not email or not password:
            _LOGGER.error("Missing email or password in config_entry.data")
            return

        # Initialise l'API
        api = ZodiacAPI(email, password)
        await hass.async_add_executor_job(api.authenticate)

        # Ajoutez le capteur
        async_add_entities([ZodiacSensor(api)])

    except Exception as e:
        _LOGGER.error("Failed to set up the sensor: %s", e)
        return

class ZodiacSensor(SensorEntity):
    """Define a sensor for the iAqualink integration."""

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
        """Fetch the latest data."""
        # Exemple de mise à jour de l'état
        # À remplacer par un appel réel à l'API Zodiac
        try:
            self._state = "Online"  # Remplacez par des données réelles
        except Exception as e:
            _LOGGER.error("Error updating ZodiacSensor state: %s", e)
