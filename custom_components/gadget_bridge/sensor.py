"""Status of candidate devices. No fabricated medical measurements."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Add an explicitly labeled unsupported-driver status sensor."""
    async_add_entities([GadgetBridgeDriverStatus(entry)])


class GadgetBridgeDriverStatus(SensorEntity):
    """Diagnostic status; not a claim of working Bluetooth support."""

    _attr_icon = "mdi:bluetooth-off"

    def __init__(self, entry: ConfigEntry) -> None:
        self._attr_unique_id = f"{entry.entry_id}_driver_status"
        self._attr_name = f"{entry.data[CONF_NAME]} driver status"
        self._attr_native_value = "not_implemented"
        self._attr_extra_state_attributes = {"ble_address": entry.data[CONF_ADDRESS]}
