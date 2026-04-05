"""Sensor platform for the Tuya Water Pump integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_DEVICE_ID, DP_COUNTDOWN, DP_STATE, DOMAIN
from .coordinator import TuyaWaterPumpCoordinator

STATE_MAP = {
    "1": "idle",
    "3": "running",
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the sensor platform."""
    coordinator: TuyaWaterPumpCoordinator = entry.runtime_data
    async_add_entities([
        TuyaWaterPumpCountdown(coordinator, entry),
        TuyaWaterPumpState(coordinator, entry),
    ])


class TuyaWaterPumpCountdown(CoordinatorEntity[TuyaWaterPumpCoordinator], SensorEntity):
    """Sensor entity for the countdown remaining."""

    _attr_has_entity_name = True
    _attr_name = "Countdown"
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:timer-outline"

    def __init__(self, coordinator: TuyaWaterPumpCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        device_id = entry.data[CONF_DEVICE_ID]
        self._attr_unique_id = f"{device_id}_countdown"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
        }

    @property
    def native_value(self) -> int | None:
        """Return the countdown remaining in seconds."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(DP_COUNTDOWN)


class TuyaWaterPumpState(CoordinatorEntity[TuyaWaterPumpCoordinator], SensorEntity):
    """Sensor entity for the pump state."""

    _attr_has_entity_name = True
    _attr_name = "State"
    _attr_icon = "mdi:water-pump"

    def __init__(self, coordinator: TuyaWaterPumpCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        device_id = entry.data[CONF_DEVICE_ID]
        self._attr_unique_id = f"{device_id}_state"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
        }

    @property
    def native_value(self) -> str | None:
        """Return the pump state as a readable string."""
        if self.coordinator.data is None:
            return None
        raw = self.coordinator.data.get(DP_STATE)
        return STATE_MAP.get(str(raw), f"unknown ({raw})")
