"""Standard Bluetooth SIG measurement decoders."""
from dataclasses import dataclass

HEART_RATE_SERVICE = "0000180d-0000-1000-8000-00805f9b34fb"
HEART_RATE_MEASUREMENT = "00002a37-0000-1000-8000-00805f9b34fb"
BATTERY_SERVICE = "0000180f-0000-1000-8000-00805f9b34fb"
BATTERY_LEVEL = "00002a19-0000-1000-8000-00805f9b34fb"

@dataclass(frozen=True)
class HeartRate:
    bpm: int
    contact: bool | None
    energy_kj: int | None
    rr_seconds: tuple[float, ...]

def decode_heart_rate(data: bytes) -> HeartRate:
    if not data:
        raise ValueError("Empty heart rate packet")
    flags = data[0]
    width = 2 if flags & 1 else 1
    offset = 1 + width
    if len(data) < offset:
        raise ValueError("Truncated heart rate")
    bpm = int.from_bytes(data[1:offset], "little")
    contact = bool(flags & 2) if flags & 4 else None
    energy = None
    if flags & 8:
        if len(data) < offset + 2:
            raise ValueError("Truncated energy")
        energy = int.from_bytes(data[offset:offset+2], "little")
        offset += 2
    rr = ()
    if flags & 16:
        if len(data) <= offset or (len(data)-offset) % 2:
            raise ValueError("Invalid RR intervals")
        rr = tuple(int.from_bytes(data[i:i+2], "little") / 1024 for i in range(offset, len(data), 2))
    return HeartRate(bpm, contact, energy, rr)

def decode_battery(data: bytes) -> int:
    if len(data) != 1 or data[0] > 100:
        raise ValueError("Invalid battery level")
    return data[0]
