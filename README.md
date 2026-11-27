# HA Gadget Bridge

A Home Assistant-native functional counterpart to [Gadgetbridge](https://gadgetbridge.org/), targeting local management of the complete upstream range of gadget categories and device capabilities, not just fitness sensors.

## Architecture

Home Assistant Bluetooth (BLE including connectable proxies) -> transport -> protocol-family adapter -> normalized device capabilities -> HA entities, actions, history and dashboard. Bluetooth Classic requires a separate host transport; BLE proxies cannot provide Classic.

The upstream catalogue is a target inventory, not a compatibility promise. Each model must have separately verified discovery, authentication, data and command support.

## Current implementation

Experimental standard GATT heart rate, battery and weight measurement. No proprietary device family is yet verified. Install as a custom integration for development only.

## Upstream

Gadgetbridge source: https://codeberg.org/Freeyourgadget/Gadgetbridge (AGPLv3). Preserve applicable license and attribution when porting code. See [roadmap](docs/ROADMAP.md) and [parity plan](docs/PARITY.md).
