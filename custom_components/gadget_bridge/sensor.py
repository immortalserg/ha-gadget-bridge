"""Standard GATT measurement entities."""
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import CONF_ADDRESS, CONF_NAME, PERCENTAGE
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    session = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        GadgetSensor(entry, session, "heart_rate", "Heart rate", "bpm", None),
        GadgetSensor(entry, session, "battery", "Battery", PERCENTAGE, SensorDeviceClass.BATTERY),
    ])


class GadgetSensor(SensorEntity):
    _attr_should_poll = False
    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, entry, session, kind, name, unit, device_class):
        self.session = session
        self.kind = kind
        self._attr_unique_id = f"{entry.entry_id}_{kind}"
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.data[CONF_ADDRESS])},
            name=entry.data[CONF_NAME],
        )

    @property
    def available(self):
        return self.session.connected and self.kind in self.session.values

    @property
    def native_value(self):
        return self.session.values.get(self.kind)

    async def async_added_to_hass(self):
        self.async_on_remove(async_dispatcher_connect(
            self.hass, self.session.signal, self.async_write_ha_state
        ))
