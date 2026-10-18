from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import GSAPICoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary sensor platform."""
    coordinator: GSAPICoordinator = (
        getattr(config_entry, "runtime_data", None)
        or hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    )
    async_add_entities([
        SepticCriticalLevelExceededSensor(coordinator),
        SepticErrorSensor(coordinator),
    ])


class SepticBaseBinarySensor(CoordinatorEntity):
    """Base class for all septic binary sensors."""

    def __init__(self, coordinator: GSAPICoordinator, value_key: str):
        super().__init__(coordinator)
        self._value_key = value_key
        self._attr_unique_id = f"{coordinator.entry_id}_{value_key}"
        self._attr_device_info = coordinator.device


class SepticCriticalLevelExceededSensor(SepticBaseBinarySensor, BinarySensorEntity):
    """Representation of a Septic Critical Level Exceeded sensor."""

    _attr_name = "Septic Level Critical"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, coordinator):
        super().__init__(coordinator=coordinator, value_key="exceeds_x_level")

    @property
    def is_on(self) -> bool | None:
        if self.coordinator.data:
            val = self.coordinator.data[0].get(self._value_key)
            if val is not None:
                return str(val).strip().lower() in ("да", "da", "yes", "true", "1")
            return False
        return None


class SepticErrorSensor(SepticBaseBinarySensor, BinarySensorEntity):
    """Representation of a Septic Error sensor."""

    _attr_name = "Septic Error"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, coordinator):
        super().__init__(coordinator=coordinator, value_key="error_name")

    @property
    def is_on(self) -> bool | None:
        if self.coordinator.data:
            val = self.coordinator.data[0].get(self._value_key)
            if val is not None:
                return str(val).strip() not in ("ОК", "OK")
            return False
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if self.coordinator.data:
            return {
                "error_name": self.coordinator.data[0].get("error_name"),
            }
        return {}
