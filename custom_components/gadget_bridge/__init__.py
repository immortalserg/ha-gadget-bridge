"""HA Gadget Bridge."""
from homeassistant.const import CONF_ADDRESS
from .const import DOMAIN
from .connection import GattSession


async def async_setup_entry(hass, entry):
    session = GattSession(hass, entry.data[CONF_ADDRESS], entry.entry_id)
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
