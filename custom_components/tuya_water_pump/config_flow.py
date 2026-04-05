"""Config flow for the Tuya Water Pump integration."""

from __future__ import annotations

import logging
from typing import Any

import tinytuya
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_HOST
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_DEVICE_ID,
    CONF_LOCAL_KEY,
    CONF_PROTOCOL_VERSION,
    DEFAULT_PROTOCOL_VERSION,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_DEVICE_ID): str,
        vol.Required(CONF_LOCAL_KEY): str,
        vol.Required(CONF_PROTOCOL_VERSION, default=DEFAULT_PROTOCOL_VERSION): vol.In(
            ["3.3", "3.4", "3.5"]
        ),
    }
)


def _test_connection(host: str, device_id: str, local_key: str, version: str) -> dict | None:
    """Test connection to the device. Returns status dict or None on failure."""
    device = tinytuya.OutletDevice(
        dev_id=device_id,
        address=host,
        local_key=local_key,
        version=float(version),
    )
    result = device.status()
    device.close()
    if isinstance(result, dict) and "dps" in result:
        return result
    return None


class TuyaWaterPumpConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tuya Water Pump."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_DEVICE_ID])
            self._abort_if_unique_id_configured()

            result = await self.hass.async_add_executor_job(
                _test_connection,
                user_input[CONF_HOST],
                user_input[CONF_DEVICE_ID],
                user_input[CONF_LOCAL_KEY],
                user_input[CONF_PROTOCOL_VERSION],
            )

            if result is not None:
                return self.async_create_entry(
                    title="Tuya Water Pump",
                    data=user_input,
                )
            errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=USER_SCHEMA,
            errors=errors,
        )
