from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .const import DOMAIN

class ZodiacConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Zodiac PAC."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        # Read from secrets.yaml
        try:
            secrets = self.hass.config.as_dict().get('secrets', {})
            authorization = secrets.get("zodiac_authorization")
            serial_number = secrets.get("serial_number")
        except KeyError:
            errors["base"] = "missing_secrets"
            return self.async_show_form(step_id="user", errors=errors)

        # Example validation
        if not authorization or not serial_number:
            errors["base"] = "invalid_secrets"

        if not errors:
            return self.async_create_entry(title="Zodiac PAC", data={
                "authorization": authorization,
                "serial_number": serial_number
            })

        return self.async_show_form(step_id="user", errors=errors)
