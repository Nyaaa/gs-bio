from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import GSAPICoordinator
from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
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
        super().__init__(
            coordinator=coordinator,
            value_key="exceeds_x_level",
        )

    @property
    def is_on(self) -> bool | None:
        if self.coordinator.data:
            return self.coordinator.data[0][self._value_key].encode('utf-8').decode() == 'Да'
        return None


class SepticErrorSensor(SepticBaseBinarySensor, BinarySensorEntity):
    """Representation of a Septic Error sensor."""
    _attr_name = "Septic Error"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, coordinator):
        super().__init__(
            coordinator=coordinator,
            value_key="error_name",
        )

    @property
    def is_on(self) -> bool | None:
        if self.coordinator.data:
            return self.coordinator.data[0][self._value_key].encode('utf-8').decode() != 'ОК'
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if self.coordinator.data:
            return {
                "error_name": self.coordinator.data[0]["error_name"],
            }
        return {}
