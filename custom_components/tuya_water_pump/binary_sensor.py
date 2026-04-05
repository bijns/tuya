"""Binary sensor platform for the Tuya Water Pump integration."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_DEVICE_ID, DP_DRY_RUN, DOMAIN
from .coordinator import TuyaWaterPumpCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the binary sensor platform."""
    coordinator: TuyaWaterPumpCoordinator = entry.runtime_data
    async_add_entities([TuyaWaterPumpDryRun(coordinator, entry)])


class TuyaWaterPumpDryRun(CoordinatorEntity[TuyaWaterPumpCoordinator], BinarySensorEntity):
    """Binary sensor for dry-run protection."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_has_entity_name = True
    _attr_name = "Dry run"
    _attr_icon = "mdi:water-off"

    def __init__(self, coordinator: TuyaWaterPumpCoordinator, entry: ConfigEntry) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        device_id = entry.data[CONF_DEVICE_ID]
        self._attr_unique_id = f"{device_id}_dry_run"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
        }

    @property
    def is_on(self) -> bool | None:
        """Return True if dry-run is detected."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(DP_DRY_RUN)
