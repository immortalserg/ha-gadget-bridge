"""Contracts for future BLE device adapters."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol


class Capability(StrEnum):
    HEART_RATE = "heart_rate"
    SPO2 = "spo2"
    STEPS = "steps"
    SLEEP = "sleep"
    WEIGHT = "weight"
    BLOOD_PRESSURE = "blood_pressure"
    BATTERY = "battery"
    LAST_CHARGE_LEVEL = "last_charge_level"


@dataclass(frozen=True)
class Measurement:
    kind: Capability
    measured_at: datetime
    value: float
    unit: str
    device_id: str


class DeviceDriver(Protocol):
    driver_id: str
    capabilities: frozenset[Capability]

    async def async_connect(self) -> None: ...
    async def async_disconnect(self) -> None: ...
    async def async_read_history(self, since: datetime | None) -> list[Measurement]: ...
