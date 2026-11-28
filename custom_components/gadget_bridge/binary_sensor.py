"""Charging state for supported devices."""
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.const import CONF_ADDRESS, CONF_NAME
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    session = hass.data[DOMAIN][entry.entry_id]
    if getattr(session, "supports_charging", False):
        async_add_entities([ChargingSensor(entry, session)])


class ChargingSensor(BinarySensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Charging"
    _attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING
    _attr_should_poll = False

    def __init__(self, entry, session):
        self.session = session
        self._attr_unique_id = f"{entry.entry_id}_charging"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.data[CONF_ADDRESS])},
            name=entry.data[CONF_NAME],
        )

    @property
    def available(self):
        return self.session.connected and self.is_on is not None

    @property
    def is_on(self):
        return self.session.values.get("charging")

    async def async_added_to_hass(self):
        self.async_on_remove(async_dispatcher_connect(
            self.hass, self.session.signal, self.async_write_ha_state
        ))
