# Tuya Water Pump - Home Assistant Integration

Custom Home Assistant integration for local control of Tuya water pumps using Protocol 3.5.

Built specifically for the **WIFIWP10GY** model, but may work with other Tuya-based water pumps.

## Features

- **Pump switch** — Turn the water pump on/off
- **Auto-off timer** — Set how long the pump runs before auto-shutoff (safety feature)
- **Countdown sensor** — See remaining seconds until auto-shutoff
- **State sensor** — Idle or running status
- **Dry-run protection** — Alert when the pump detects no water flow

## Requirements

- Home Assistant 2024.1.0 or newer
- Tuya water pump on the same local network as Home Assistant
- Device credentials: **Device ID**, **IP address**, and **Local Key**

## Getting Your Device Credentials

Install [tinytuya](https://github.com/jasonacox/tinytuya) and run the wizard:

```bash
pip install tinytuya
python -m tinytuya wizard
```

This requires a [Tuya IoT Platform](https://iot.tuya.com/) developer account. The wizard will generate a `devices.json` file containing your device ID and local key.

To find the device IP:

```bash
python -m tinytuya scan
```

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to **Integrations** → **Custom repositories**
3. Add `https://github.com/bijns/tuya` with category **Integration**
4. Search for "Tuya Water Pump" and install
5. Restart Home Assistant

### Manual

1. Copy the `custom_components/tuya_water_pump/` folder into your Home Assistant `custom_components/` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services** → **Add Integration**
2. Search for **Tuya Water Pump**
3. Enter your device details:
   - **Device IP Address** — Local IP of the pump
   - **Device ID** — From tinytuya wizard
   - **Local Key** — From tinytuya wizard
   - **Protocol Version** — Select 3.5 (default)

## Entities

Once configured, the following entities are created:

| Entity | Type | Description |
|--------|------|-------------|
| Pump | Switch | Turn pump on/off |
| Auto-off timer | Number | Duration before auto-shutoff (1–3600 seconds) |
| Countdown | Sensor | Seconds remaining until shutoff |
| State | Sensor | Current state: idle or running |
| Dry run | Binary Sensor | Alerts when pump runs without water |

## Tested Device

| Property | Value |
|----------|-------|
| Model | WIFIWP10GY |
| Main Version | v3.1.17 |
| MCU Version | v4.2.9 |
| Protocol | 3.5 |

## Troubleshooting

**"Cannot connect to device"** during setup:
- Verify the device IP is correct and reachable (`ping <ip>`)
- Ensure Home Assistant and the pump are on the same network/VLAN
- Double-check the Device ID and Local Key
- If the local key changed (e.g., after re-pairing in the Tuya app), re-run the tinytuya wizard

**Entity shows "unavailable":**
- The pump may have dropped the connection — it should reconnect automatically within 5 seconds
- Check Home Assistant logs for `tuya_water_pump` errors

## License

MIT
