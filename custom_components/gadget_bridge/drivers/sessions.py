"""Runtime session registry, separate from upstream model inventory."""
from ..connection import GattSession

from .huami_session import HuamiSession

SESSION_FACTORIES = {"standard_gatt": GattSession, "huami_legacy": HuamiSession}


def create_session(driver_id, hass, address, entry_id, store, **options):
    factory = SESSION_FACTORIES.get(driver_id)
    if factory is None:
        raise ValueError(f"Unsupported runtime driver: {driver_id}")
    if driver_id == "standard_gatt":
        options.pop("auth_key", None)
    return factory(hass, address, entry_id, store, **options)
