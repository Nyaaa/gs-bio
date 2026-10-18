import asyncio
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import BASE_URL, DOMAIN, TIMEOUT


class GSBioConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for GS Bio."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            api_key = user_input["api_key"].strip()
            await self.async_set_unique_id(api_key)
            self._abort_if_unique_id_configured()

            # Test API connection
            session = async_get_clientsession(self.hass)
            try:
                async with asyncio.timeout(TIMEOUT):
                    async with session.get(BASE_URL.format(api_key=api_key)) as response:
                        if response.status == 200:
                            return self.async_create_entry(
                                title="GS Bio",
                                data={"api_key": api_key},
                            )
                        if response.status in (401, 403):
                            errors["base"] = "invalid_auth"
                        else:
                            errors["base"] = "cannot_connect"
            except (TimeoutError, asyncio.TimeoutError):
                errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("api_key"): str,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return SepticSensorOptionsFlow()


class SepticSensorOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Septic Sensor."""

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_api_key = self.config_entry.options.get(
            "api_key", self.config_entry.data.get("api_key", "")
        )
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required("api_key", default=current_api_key): str,
                }
            ),
        )
