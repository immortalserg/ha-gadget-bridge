# Porting Gadgetbridge device families

## Definition of support

A model is **catalogued** when upstream metadata has been mapped. **Recognized** when its BLE/Classic advertisements are verified. **Connected** when pairing/authentication and transport have passed hardware tests. **Supported** when at least one actual capability has a tested decoder, stable entity and history synchronization where applicable.

## Architecture milestones

1. Read-only upstream model inventory, provenance and license tracking.
2. Driver registry with verified matching rules and safe opt-in discovery.
3. Bluetooth GATT transport using Home Assistant's built-in Bluetooth stack and connection slots; Classic Bluetooth handled separately.
4. Common models for measurements, timestamp normalization, history cursors, retention, privacy and per-device deduplication.
5. Family adapters, protocol fixtures and real-device test evidence.
6. UI for linking devices, configuring capabilities and diagnostics.

## Initial protocol priority

BLE GATT standard services (Heart Rate, Battery, Weight Scale decoder and live indications added; hardware testing pending; Blood Pressure next), followed by manufacturers represented upstream: Xiaomi, Huami/Amazfit, Huawei/Honor, Garmin, FitPro / Da Fit / GloryFit / FitCloud and remaining device categories.

## License and attribution

Upstream Gadgetbridge: https://codeberg.org/Freeyourgadget/Gadgetbridge/ — AGPLv3. Keep copyright headers and upstream attribution when copying or porting any implementation. An upstream model catalogue alone does not mean direct-HA support.
