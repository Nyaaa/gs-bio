import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import BASE_URL, DOMAIN, SCAN_INTERVAL, TIMEOUT

_LOGGER = logging.getLogger(__name__)


class GSAPICoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data from GS Septik API."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry, api_key: str = ""):
        super().__init__(
            hass,
            _LOGGER,
            name="GS Bio sensor",
            config_entry=config_entry,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
            always_update=True,
        )
        self._hass = hass
        self._api_url = BASE_URL.format(api_key=api_key)
        self.entry_id = config_entry.entry_id
        self.device = DeviceInfo(
            identifiers={(DOMAIN, self.entry_id)},
            name="GS Bio sensor",
            manufacturer="GS-House",
            model="GS Bio",
            configuration_url="https://web.gseptik.ru/",
        )

    async def _async_update_data(self):
        """Fetch data from the API."""
        try:
            data = await self.async_get_data()
            if not data:
                raise UpdateFailed("Failed to fetch data from API")
            return data
        except UpdateFailed:
            raise
        except Exception as err:
            raise UpdateFailed(f"Error updating data: {err}") from err

    async def async_get_data(self):
        """Fetch data from the API using Home Assistant's shared aiohttp session."""
        session = async_get_clientsession(self._hass)
        try:
            async with asyncio.timeout(TIMEOUT):
                _LOGGER.debug("Calling API...")
                async with session.get(self._api_url) as response:
                    if response.status == 200:
                        return await response.json(content_type=None)
                    _LOGGER.error("API request failed with status %s", response.status)
                    return None
        except (TimeoutError, asyncio.TimeoutError):
            _LOGGER.error("Timeout fetching data from GS Bio API")
            return None
        except Exception as err:
            _LOGGER.error("Error fetching data: %s", err)
            return None
