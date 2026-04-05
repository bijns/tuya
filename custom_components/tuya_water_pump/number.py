"""Number platform for the Tuya Water Pump integration."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_DEVICE_ID, DP_TIMER, DOMAIN
from .coordinator import TuyaWaterPumpCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the number platform."""
    coordinator: TuyaWaterPumpCoordinator = entry.runtime_data
    async_add_entities([TuyaWaterPumpTimer(coordinator, entry)])


class TuyaWaterPumpTimer(CoordinatorEntity[TuyaWaterPumpCoordinator], NumberEntity):
    """Number entity for the auto-off timer duration."""

    _attr_has_entity_name = True
    _attr_name = "Auto-off timer"
    _attr_native_min_value = 1
    _attr_native_max_value = 3600
    _attr_native_step = 1
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS
    _attr_mode = NumberMode.BOX

    def __init__(self, coordinator: TuyaWaterPumpCoordinator, entry: ConfigEntry) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        device_id = entry.data[CONF_DEVICE_ID]
        self._attr_unique_id = f"{device_id}_timer"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
        }

    @property
    def native_value(self) -> float | None:
        """Return the current timer value."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(DP_TIMER)

    async def async_set_native_value(self, value: float) -> None:
        """Set the timer value."""
        await self.coordinator.async_set_dp(DP_TIMER, int(value))
