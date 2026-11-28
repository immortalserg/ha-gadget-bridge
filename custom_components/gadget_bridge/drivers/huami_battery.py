"""Legacy Huami battery fields; reference HuamiBatteryInfo.java, blob 43af0266bb4292eba7156357c2ceff017df1905e."""
from dataclasses import dataclass

BATTERY_INFO = "00000006-0000-3512-2118-0009af100700"


@dataclass(frozen=True)
class BatteryInfo:
    level: int | None
    charging: bool | None
    last_charge_level: int | None


def decode_battery_info(packet: bytes) -> BatteryInfo:
    def percent(index):
        return packet[index] if len(packet) > index and packet[index] <= 100 else None
    charging = bool(packet[2]) if len(packet) >= 3 and packet[2] in (0, 1) else None
    return BatteryInfo(percent(1), charging, percent(19))
