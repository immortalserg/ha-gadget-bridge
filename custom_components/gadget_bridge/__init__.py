"""HA Gadget Bridge integration.

This foundation intentionally does not attempt arbitrary BLE connections.
"""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Initialize a configured device without starting unsupported transports."""
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {"status": "driver_not_implemented"}
    await hass.config_entries.async_forward_entry_setups(entry, ("sensor",))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a device cleanly."""
    if not await hass.config_entries.async_unload_platforms(entry, ("sensor",)):
        return False
    hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    return True
