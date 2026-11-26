# HA Gadget Bridge

Local Bluetooth device integration for Home Assistant. The long-term goal is to support the device families documented by [Gadgetbridge](https://gadgetbridge.org/), subject to protocol availability, transport constraints and hardware verification.

**Development status: experimental foundation.** No proprietary Gadgetbridge protocols have been ported yet. The initial integration supports manual setup for an explicitly identified BLE device, a device entry, and a placeholder diagnostic sensor. It does **not** claim to read measurements yet.

## Installation

Copy `custom_components/gadget_bridge` into the Home Assistant `config/custom_components` directory and restart Home Assistant. Alternatively add this repository as a custom integration repository in HACS after the initial scaffold is committed. Add **HA Gadget Bridge** under Settings → Devices & services → Add integration. Enter the BLE MAC address and a recognizable name.

## Architecture

- `drivers/base.py`: typed measurements and driver protocol
- `drivers/registry.py`: explicit driver identifiers, capability flags, and registered drivers
- `config_flow.py`: safe manual pairing entry point without pretending all BLE advertisements are supported
- `sensor.py`: initial diagnostic sensor; not medical measurement data
- `docs/ROADMAP.md`: migration plan and verification criteria

Home Assistant's built-in Bluetooth integration will be used for discovery and connections when real device drivers are introduced; do not run an independent BLE scanner in an integration.

## Relationship to Gadgetbridge

Upstream: https://codeberg.org/Freeyourgadget/Gadgetbridge/

Gadgetbridge is licensed under AGPL-3.0. This repository currently contains independently authored integration scaffolding, not copied protocol implementations. Before importing or adapting any Gadgetbridge code, review copyright, license notices and AGPL obligations. Unsupported families are not listed as compatible.

## License

AGPL-3.0-or-later is intended for this project. See `LICENSE` and source attribution when protocol code is ported.
