"""Legacy Huami realtime steps, matching Gadgetbridge handleRealtimeSteps."""
REALTIME_STEPS = "00000007-0000-3512-2118-0009af100700"


def decode_steps(packet: bytes) -> int:
    if len(packet) != 13:
        raise ValueError("Unsupported Huami activity packet length")
    return int.from_bytes(packet[1:3], "little")
