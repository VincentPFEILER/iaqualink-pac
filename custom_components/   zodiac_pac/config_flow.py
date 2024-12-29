import voluptuous as vol
from homeassistant import config_entries
from .api import ZodiacAPI
from .const import DOMAIN

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the configuration flow for the iAqualink integration."""

    async def async_step_user(self, user_input=None):
        """Handle the first step of the configuration."""
        errors = {}

        if user_input is not None:
            api = ZodiacAPI(user_input["email"], user_input["password"])
            try:
                await self.hass.async_add_executor_job(api.authenticate)
                return self.async_create_entry(
                    title="iAqualink",
                    data={
                        "email": user_input["email"],
                        "password": user_input["password"],
                    },
                )
            except Exception:
                errors["base"] = "auth_failed"

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
