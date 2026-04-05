# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A custom Home Assistant integration (`tuya_water_pump`) for local control of a Tuya water pump (model WIFIWP10GY, Protocol 3.5). Uses **tinytuya** as the communication layer since localtuya does not support protocol 3.5.

## Architecture

The integration follows the Home Assistant DataUpdateCoordinator pattern:

- **coordinator.py** — Wraps tinytuya.OutletDevice, polls device every 5s, runs all blocking tinytuya calls via `async_add_executor_job()`
- **config_flow.py** — UI-based setup: IP, device ID, local key, protocol version. Validates by connecting to the device.
- **switch.py** — Pump on/off (DP 1)
- **number.py** — Auto-off timer duration (DP 102)
- **sensor.py** — Countdown remaining (DP 104), pump state idle/running (DP 106)
- **binary_sensor.py** — Dry-run protection alert (DP 109)

All entities use `CoordinatorEntity` and share a single device via `entry.runtime_data`.

## DPS Map (confirmed from device)

| DP | Type | Function |
|----|------|----------|
| 1 | Boolean | Main switch |
| 102 | Integer | Auto-off timer (seconds) |
| 104 | Integer | Countdown remaining |
| 106 | String | State ("1"=idle, "3"=running) |
| 109 | Boolean | Dry-run protection |

## Development

Test connectivity to the physical device (requires tinytuya installed and device on same network):
```
pip install tinytuya
python test_pump.py
```

Deploy to Home Assistant by copying `custom_components/tuya_water_pump/` into HA's `custom_components/` directory.

## Key Constraints

- tinytuya is synchronous — all device calls must go through `hass.async_add_executor_job()`
- Protocol 3.5 uses AES-GCM encryption; persistent socket (`set_socketPersistent(True)`) is used but connections can drop and need reconnection
- The device auto-shuts-off after the timer (DP 102) expires as a safety measure
