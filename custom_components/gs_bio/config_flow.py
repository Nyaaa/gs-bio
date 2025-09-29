import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN


class GSBioConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="GS Bio", data=user_input)
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required("api_key"): str},
            ),
        )


class SepticSensorOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Septic Sensor."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="GS Bio", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required("api_key", default=self.config_entry.data.get("api_key")): str,
                }
            ),
        )
