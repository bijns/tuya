"""Quick test script to verify tinytuya can talk to the Tuya water pump."""

import tinytuya

DEVICE_ID = input("Device ID: ")
DEVICE_IP = input("Device IP: ")
LOCAL_KEY = input("Local Key: ")

d = tinytuya.OutletDevice(
    dev_id=DEVICE_ID,
    address=DEVICE_IP,
    local_key=LOCAL_KEY,
    version=3.5,
)

print("Querying device status...")
status = d.status()
print("Status:", status)

print("\nTurning ON...")
d.turn_on()
print("Status:", d.status())

print("\nTurning OFF...")
d.turn_off()
print("Status:", d.status())
