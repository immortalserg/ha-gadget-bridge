"""Experimental legacy Huami realtime activity packet format."""
from dataclasses import dataclass
import struct

REALTIME_STEPS = "00000007-0000-3512-2118-0009af100700"


@dataclass(frozen=True)
class Activity:
    steps: int
    distance_m: int
    calories: int


def decode_activity(packet: bytes) -> Activity:
    """Decode the candidate 13-byte legacy format; reject other layouts."""
    if len(packet) != 13:
        raise ValueError("Unsupported Huami activity packet length")
    steps, distance, calories = struct.unpack_from("<III", packet, 1)
    return Activity(steps, distance, calories)
