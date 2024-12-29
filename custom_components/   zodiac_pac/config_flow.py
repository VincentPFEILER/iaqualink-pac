import logging
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Zodiac PAC."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step of the configuration flow."""
        _LOGGER.debug("ConfigFlow triggered for Zodiac PAC")
        errors = {}

        if user_input is not None:
            email = user_input.get("email")
            password = user_input.get("password")

            # Simulation de validation des identifiants
            if email == "test@example.com" and password == "password":
                _LOGGER.debug("Validation réussie pour l'utilisateur : %s", email)
                return self.async_create_entry(
                    title="Zodiac PAC",
                    data=user_input,
                )
            else:
                _LOGGER.error("Échec de validation pour l'utilisateur : %s", email)
                errors["base"] = "invalid_auth"

        # Formulaire affiché si aucune donnée ou erreur
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("email"): str,
                    vol.Required("password"): str,
                }
            ),
            errors=errors,
        )
