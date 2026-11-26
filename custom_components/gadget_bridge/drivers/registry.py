"""Explicit registry: do not advertise unimplemented Gadgetbridge devices."""

from .base import DeviceDriver

DRIVERS: dict[str, type[DeviceDriver]] = {}


def register_driver(driver: type[DeviceDriver]) -> None:
    """Register a tested driver by its unique ID."""
    if driver.driver_id in DRIVERS:
        raise ValueError(f"Duplicate driver ID: {driver.driver_id}")
    DRIVERS[driver.driver_id] = driver
