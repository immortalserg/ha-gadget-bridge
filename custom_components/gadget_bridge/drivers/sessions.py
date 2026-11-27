"""Runtime session registry, separate from upstream model inventory."""
from ..connection import GattSession

SESSION_FACTORIES = {"standard_gatt": GattSession}


def create_session(driver_id, hass, address, entry_id, store, **options):
    factory = SESSION_FACTORIES.get(driver_id)
    if factory is None:
        raise ValueError(f"Unsupported runtime driver: {driver_id}")
    return factory(hass, address, entry_id, store, **options)
