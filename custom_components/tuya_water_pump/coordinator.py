"""DataUpdateCoordinator for the Tuya Water Pump integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import tinytuya

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_DEVICE_ID, CONF_LOCAL_KEY, CONF_PROTOCOL_VERSION, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class TuyaWaterPumpCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator that polls the Tuya water pump via tinytuya."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self._host = entry.data[CONF_HOST]
        self._device_id = entry.data[CONF_DEVICE_ID]
        self._local_key = entry.data[CONF_LOCAL_KEY]
        self._protocol_version = float(entry.data[CONF_PROTOCOL_VERSION])
        self._device: tinytuya.OutletDevice | None = None

    def _create_device(self) -> tinytuya.OutletDevice:
        """Create and configure the tinytuya device (runs in executor)."""
        device = tinytuya.OutletDevice(
            dev_id=self._device_id,
            address=self._host,
            local_key=self._local_key,
            version=self._protocol_version,
        )
        device.set_socketPersistent(True)
        return device

    async def _async_update_data(self) -> dict[str, Any]:
        """Poll the device for current status."""
        if self._device is None:
            self._device = await self.hass.async_add_executor_job(self._create_device)

        try:
            result = await self.hass.async_add_executor_job(self._device.status)
        except (OSError, ConnectionResetError) as err:
            self._device = None
            raise UpdateFailed(f"Connection lost: {err}") from err

        if not isinstance(result, dict) or "dps" not in result:
            error = result.get("Error", "Unknown error") if isinstance(result, dict) else str(result)
            # Recreate device on auth/network errors
            if isinstance(result, dict) and result.get("Err") in ("905", "906"):
                self._device = None
            raise UpdateFailed(f"Device error: {error}")

        return result["dps"]

    async def async_set_dp(self, dp_id: str, value: Any) -> None:
        """Set a data point value on the device."""
        if self._device is None:
            self._device = await self.hass.async_add_executor_job(self._create_device)

        try:
            await self.hass.async_add_executor_job(
                self._device.set_value, int(dp_id), value
            )
        except (OSError, ConnectionResetError) as err:
            self._device = None
            raise UpdateFailed(f"Failed to set DP {dp_id}: {err}") from err

        await self.async_request_refresh()

    async def async_close(self) -> None:
        """Close the device connection."""
        if self._device is not None:
            await self.hass.async_add_executor_job(self._device.close)
            self._device = None
