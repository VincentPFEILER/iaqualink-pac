import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class ZodiacPacConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            username = user_input["username"]
            password = user_input["password"]

            # Testez la connexion ici (API call)
            if await self.test_credentials(username, password):
                return self.async_create_entry(title="Zodiac PAC", data=user_input)
            else:
                errors["base"] = "auth_failed"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("username"): str,
                    vol.Required("password"): str,
                }
            ),
            errors=errors,
        )

    async def test_credentials(self, username, password):
        # Remplacez par un appel réel à l'API pour vérifier les identifiants
        return username == "test" and password == "test"

