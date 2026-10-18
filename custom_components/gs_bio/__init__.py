from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import GSAPICoordinator

PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR]


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up the integration from a config entry."""
    api_key = config_entry.options.get("api_key") or config_entry.data.get("api_key")
    coordinator = GSAPICoordinator(hass=hass, config_entry=config_entry, api_key=api_key)
    await coordinator.async_config_entry_first_refresh()

    config_entry.runtime_data = coordinator
    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = {
        "coordinator": coordinator,
    }

    config_entry.async_on_unload(config_entry.add_update_listener(async_reload_entry))

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS):
        if DOMAIN in hass.data:
            hass.data[DOMAIN].pop(config_entry.entry_id, None)
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Reload config entry when options change."""
    await hass.config_entries.async_reload(config_entry.entry_id)
