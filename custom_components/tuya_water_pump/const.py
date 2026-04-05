"""Constants for the Tuya Water Pump integration."""

from homeassistant.const import Platform

DOMAIN = "tuya_water_pump"

PLATFORMS = [
    Platform.SWITCH,
    Platform.NUMBER,
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]

# DPS mapping (confirmed from WIFIWP10GY device)
DP_SWITCH = "1"
DP_TIMER = "102"
DP_COUNTDOWN = "104"
DP_STATE = "106"
DP_DRY_RUN = "109"

# Config keys
CONF_DEVICE_ID = "device_id"
CONF_LOCAL_KEY = "local_key"
CONF_PROTOCOL_VERSION = "protocol_version"

# Defaults
DEFAULT_PROTOCOL_VERSION = "3.5"
DEFAULT_SCAN_INTERVAL = 5
