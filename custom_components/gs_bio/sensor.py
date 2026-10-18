from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfPressure, UnitOfTemperature
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
    """Set up the sensor platform."""
    coordinator: GSAPICoordinator = (
        getattr(config_entry, "runtime_data", None)
        or hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    )
    async_add_entities([
        SepticLiquidLevelSensor(coordinator),
        SepticTemperatureSensor(coordinator),
        SepticPressureSensor(coordinator),
        SepticSedimentSensor(coordinator),
        SepticCriticalLevelSensor(coordinator),
        SepticErrorSensor(coordinator),
    ])


class SepticBaseSensor(CoordinatorEntity):
    """Base class for all septic sensors."""

    def __init__(self, coordinator: GSAPICoordinator, value_key: str):
        super().__init__(coordinator)
        self._value_key = value_key
        self._attr_unique_id = f"{coordinator.entry_id}_{value_key}"
        self._attr_device_info = coordinator.device

    @property
    def native_value(self):
        if self.coordinator.data:
            return self.coordinator.data[0].get(self._value_key)
        return None


class SepticLiquidLevelSensor(SepticBaseSensor, SensorEntity):
    """Representation of a Septic Liquid Level sensor."""

    _attr_name = "Septic Liquid Level"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator):
        super().__init__(coordinator=coordinator, value_key="liquid_level")


class SepticTemperatureSensor(SepticBaseSensor, SensorEntity):
    """Representation of a Septic Temperature sensor."""

    _attr_name = "Septic Temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator):
        super().__init__(coordinator=coordinator, value_key="temp")


class SepticPressureSensor(SepticBaseSensor, SensorEntity):
    """Representation of a Septic Pressure sensor."""

    _attr_name = "Septic Pressure"
    _attr_native_unit_of_measurement = UnitOfPressure.MBAR
    _attr_device_class = SensorDeviceClass.PRESSURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator):
        super().__init__(coordinator=coordinator, value_key="pressure")


class SepticSedimentSensor(SepticBaseSensor, SensorEntity):
    """Representation of a Septic Sediment sensor."""

    _attr_name = "Septic Sediment"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator):
        super().__init__(coordinator=coordinator, value_key="sdt")


class SepticCriticalLevelSensor(SepticBaseSensor, SensorEntity):
    """Representation of a Septic Critical Level sensor."""

    _attr_name = "Septic Critical Level"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator):
        super().__init__(coordinator=coordinator, value_key="x_level")


class SepticErrorSensor(SepticBaseSensor, SensorEntity):
    """Representation of a Septic Error text sensor."""

    _attr_name = "Septic Error Message"

    def __init__(self, coordinator):
        super().__init__(coordinator=coordinator, value_key="error_name")

    @property
    def icon(self) -> str:
        """Return dynamic icon based on error state."""
        if self.coordinator.data:
            val = self.coordinator.data[0].get(self._value_key)
            if val and str(val).strip() not in ("ОК", "OK"):
                return "mdi:alert-circle"
        return "mdi:check-circle-outline"
