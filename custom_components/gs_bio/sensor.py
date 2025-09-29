from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import PERCENTAGE, UnitOfTemperature, UnitOfPressure
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import GSAPICoordinator
from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    async_add_entities([
        SepticLiquidLevelSensor(coordinator),
        SepticTemperatureSensor(coordinator),
        SepticPressureSensor(coordinator),
        SepticSedimentSensor(coordinator),
        SepticCriticalLevelSensor(coordinator),
    ])


class SepticBaseSensor(CoordinatorEntity):
    """Base class for all septic sensors."""

    def __init__(self, coordinator: GSAPICoordinator, value_key: str):
        super().__init__(coordinator)
        self._value_key = value_key
        self._attr_unique_id = f"{coordinator.entry_id}_{value_key}"
        self._attr_device_info = coordinator.device

    @property
    def state(self):
        if self.coordinator.data:
            return self.coordinator.data[0][self._value_key]
        return None


class SepticLiquidLevelSensor(SepticBaseSensor, SensorEntity):
    """Representation of a Septic Liquid Level sensor."""
    _attr_name = "Septic Liquid Level"
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(self, coordinator):
        super().__init__(
            coordinator=coordinator,
            value_key="liquid_level",
        )


class SepticTemperatureSensor(SepticBaseSensor, SensorEntity):
    """Representation of a Septic Temperature sensor."""
    _attr_name = "Septic Temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE

    def __init__(self, coordinator):
        super().__init__(
            coordinator=coordinator,
            value_key="temp",
        )


class SepticPressureSensor(SepticBaseSensor, SensorEntity):
    """Representation of a Septic Pressure sensor."""
    _attr_name = "Septic Pressure"
    _attr_native_unit_of_measurement = UnitOfPressure.MBAR
    _attr_device_class = SensorDeviceClass.PRESSURE

    def __init__(self, coordinator):
        super().__init__(
            coordinator=coordinator,
            value_key="pressure",
        )


class SepticSedimentSensor(SepticBaseSensor, SensorEntity):
    """Representation of a Septic Sediment sensor."""
    _attr_name = "Septic Sediment"
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(self, coordinator):
        super().__init__(
            coordinator=coordinator,
            value_key="sdt",
        )


class SepticCriticalLevelSensor(SepticBaseSensor, SensorEntity):
    """Representation of a Septic Critical Level sensor."""
    _attr_name = "Septic Critical Level"
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(self, coordinator):
        super().__init__(
            coordinator=coordinator,
            value_key="x_level",
        )
