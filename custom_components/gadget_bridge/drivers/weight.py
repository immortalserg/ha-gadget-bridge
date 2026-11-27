"""Bluetooth SIG Weight Measurement (0x2A9D) decoder.

Weight is 0.005 kg/0.01 lb per unit.  This decoder intentionally does not
attribute measurements to a person: user IDs are device-local and optional.
"""
from dataclasses import dataclass
from datetime import datetime


WEIGHT_SCALE_SERVICE = "0000181d-0000-1000-8000-00805f9b34fb"
WEIGHT_MEASUREMENT = "00002a9d-0000-1000-8000-00805f9b34fb"


@dataclass(frozen=True)
class WeightMeasurement:
    weight: float
    unit: str
    measured_at: datetime | None
    user_id: int | None
    bmi: float | None
    height: float | None
    height_unit: str | None


def decode_weight(data: bytes) -> WeightMeasurement:
    """Decode a complete standard Weight Measurement indication.

    Reject truncated packets rather than publishing a potentially wrong value.
    Optional fields follow flags in mandated order.
    """
    if len(data) < 3:
        raise ValueError("Truncated weight measurement")
    flags = data[0]
    if flags & 0xF0:
        raise ValueError("Reserved flags set")
    imperial = bool(flags & 0x01)
    raw = int.from_bytes(data[1:3], "little")
    weight = round(raw * (0.01 if imperial else 0.005), 3)
    offset = 3

    measured_at = None
    if flags & 0x02:
        if len(data) < offset + 7:
            raise ValueError("Truncated timestamp")
        year = int.from_bytes(data[offset:offset + 2], "little")
        month, day, hour, minute, second = data[offset + 2:offset + 7]
        try:
            measured_at = datetime(year, month, day, hour, minute, second)
        except ValueError as err:
            raise ValueError("Invalid timestamp") from err
        offset += 7

    user_id = None
    if flags & 0x04:
        if len(data) < offset + 1:
            raise ValueError("Truncated user ID")
        uid = data[offset]
        user_id = None if uid == 0xFF else uid
        offset += 1

    bmi = height = height_unit = None
    if flags & 0x08:
        if len(data) < offset + 4:
            raise ValueError("Truncated BMI and height")
        bmi = round(int.from_bytes(data[offset:offset + 2], "little") / 10, 1)
        height = round(
            int.from_bytes(data[offset + 2:offset + 4], "little")
            * (0.1 if imperial else 0.001), 3
        )
        height_unit = "in" if imperial else "m"
        offset += 4
    if offset != len(data):
        raise ValueError("Unexpected weight measurement bytes")
    return WeightMeasurement(weight, "lb" if imperial else "kg", measured_at, user_id, bmi, height, height_unit)
