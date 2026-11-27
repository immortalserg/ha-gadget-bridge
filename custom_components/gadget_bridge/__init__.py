"""HA Gadget Bridge."""
from homeassistant.const import CONF_ADDRESS
from .const import DOMAIN
from .drivers.sessions import create_session, SESSION_FACTORIES
from homeassistant.exceptions import ConfigEntryError
from .history import HistoryStore


async def async_setup_entry(hass, entry):
    store = HistoryStore(hass.config.path("gadget_bridge_history.sqlite3")) if entry.options.get("record_history", True) else None
    driver_id = entry.options.get("driver_id", entry.data.get("driver_id", "standard_gatt"))
    if driver_id not in SESSION_FACTORIES:
        raise ConfigEntryError(f"Unsupported Gadget Bridge driver: {driver_id}")
    session = create_session(driver_id, hass, entry.data[CONF_ADDRESS], entry.entry_id, store, poll_interval=entry.options.get("poll_interval", 300), reconnect_interval=entry.options.get("reconnect_interval", 30))
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = session
    await hass.config_entries.async_forward_entry_setups(entry, ("sensor", "button"))
    session.task = entry.async_create_background_task(hass, session.run(), "gadget_bridge_gatt")
    return True


async def async_unload_entry(hass, entry):
    if not await hass.config_entries.async_unload_platforms(entry, ("sensor", "button")):
        return False
    session = hass.data[DOMAIN].pop(entry.entry_id)
    await session.stop()
    return True
