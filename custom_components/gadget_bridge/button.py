"""Native device controls."""
from homeassistant.components.button import ButtonEntity
from homeassistant.const import CONF_ADDRESS, CONF_NAME, EntityCategory
from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    session = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        GadgetButton(entry, session, "reconnect", "Reconnect"),
        GadgetButton(entry, session, "refresh", "Refresh battery"),
    ])


class GadgetButton(ButtonEntity):
    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, session, action, name):
        self.session = session
        self.action = action
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{action}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.data[CONF_ADDRESS])},
            name=entry.data[CONF_NAME],
        )

    async def async_press(self):
        if self.action == "reconnect":
            self.session.reconnect_requested.set()
        else:
            self.session.refresh_requested.set()
