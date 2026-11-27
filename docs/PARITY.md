# Functional parity target

Upstream reference: https://gadgetbridge.org/ and https://codeberg.org/Freeyourgadget/Gadgetbridge.

| Area | HA equivalent |
|---|---|
| Discovery, pairing and authentication | Config flow, protocol-specific authentication, secret storage |
| Activity, sleep, health and sports | Sensors, timestamped history, export, dashboard |
| Alarms, reminders and device preferences | HA actions, number/select/switch entities |
| Notifications, calls, contacts | Explicit opt-in services and mobile companion integration where required |
| Music, navigation, weather | HA media, weather and action adapters |
| Firmware and watchfaces | Explicit model-validated installation with user confirmation |
| Headphones, speakers, appliances, vehicles and other gadgets | Category-specific HA platforms |
| Bluetooth Classic | Separate host/BlueZ transport, not BLE proxy |

## Implementation order

1. Build revision-pinned upstream catalogue with model aliases and provenance.
2. Implement transport-independent adapter lifecycle and capability registry.
3. Implement durable per-device history, deduplication, cursors and export.
4. Port upstream protocol families, prioritizing shared implementations rather than individual model names.
5. Map device settings and commands to native HA platforms.
6. Add dashboards, diagnostics and hardware validation matrix.

No catalogue entry alone implies working connectivity or support. Features requiring phone telephony or Android-specific services need a separate HA-compatible bridge. Do not copy credentials or personal measurements into logs.
