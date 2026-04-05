"""Switch platform for the Tuya Water Pump integration."""

from __future__ import annotations

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_DEVICE_ID, DP_SWITCH, DOMAIN
from .coordinator import TuyaWaterPumpCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the switch platform."""
    coordinator: TuyaWaterPumpCoordinator = entry.runtime_data
    async_add_entities([TuyaWaterPumpSwitch(coordinator, entry)])


class TuyaWaterPumpSwitch(CoordinatorEntity[TuyaWaterPumpCoordinator], SwitchEntity):
    """Switch entity for the water pump on/off control."""

    _attr_device_class = SwitchDeviceClass.SWITCH
    _attr_has_entity_name = True
    _attr_name = "Pump"

    def __init__(self, coordinator: TuyaWaterPumpCoordinator, entry: ConfigEntry) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        device_id = entry.data[CONF_DEVICE_ID]
        self._attr_unique_id = f"{device_id}_switch"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
            "name": "Tuya Water Pump",
            "manufacturer": "Tuya",
            "model": "WIFIWP10GY",
        }

    @property
    def is_on(self) -> bool | None:
        """Return True if the pump is on."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(DP_SWITCH)

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the pump on."""
        await self.coordinator.async_set_dp(DP_SWITCH, True)

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the pump off."""
        await self.coordinator.async_set_dp(DP_SWITCH, False)
