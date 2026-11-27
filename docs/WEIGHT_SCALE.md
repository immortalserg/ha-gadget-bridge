# Standard Bluetooth weight scales (experimental)

This is support for the Bluetooth SIG Weight Scale Service (UUID 0x181D)
and Weight Measurement characteristic (UUID 0x2A9D) **only**, not a promise
of compatibility with Gadgetbridge proprietary scale protocols.

- The scale must advertise 0x181D, be reachable over a connectable BLE
  adapter/proxy, and permit GATT indications without vendor-specific login.
- The Weight entity appears only when the characteristic is present and
  only becomes available once a valid indication arrives.
- Values are stored in the unit reported by the scale (kg or lb). Additional
  fields like BMI, user ID and height are parsed but deliberately not published:
  a shared household scale must not silently mix personal measurements.
- Some scales send an indication only when stepped on and may require bonding.
  This integration does not implement pairing/bonding workflows.
- No history syncing or per-person attribution is provided at this stage.

Hardware validation is still required before advertising specific models as
supported. Use `pytest -q` for offline decoder regression tests.
