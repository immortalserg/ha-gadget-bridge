"""HA Gadget Bridge."""
from homeassistant.const import CONF_ADDRESS
from .const import DOMAIN
from .connection import GattSession
from .history import HistoryStore


async def async_setup_entry(hass, entry):
    store = HistoryStore(hass.config.path("gadget_bridge_history.sqlite3")) if entry.options.get("record_history", True) else None
    session = GattSession(hass, entry.data[CONF_ADDRESS], entry.entry_id, store, poll_interval=entry.options.get("poll_interval", 300), reconnect_interval=entry.options.get("reconnect_interval", 30))
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = session
    await hass.config_entries.async_forward_entry_setups(entry, ("sensor",))
    session.task = entry.async_create_background_task(hass, session.run(), "gadget_bridge_gatt")
    return True


async def async_unload_entry(hass, entry):
    if not await hass.config_entries.async_unload_platforms(entry, ("sensor",)):
        return False
    session = hass.data[DOMAIN].pop(entry.entry_id)
    await session.stop()
    return True
