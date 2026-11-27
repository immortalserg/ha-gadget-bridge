"""Manual configuration flow for the initial HA Gadget Bridge foundation."""

import voluptuous as vol
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak
from .drivers.matching import Advertisement, STANDARD_RULES, matching_drivers

from homeassistant import config_entries
from homeassistant.const import CONF_ADDRESS, CONF_NAME

from .const import DOMAIN


class GadgetBridgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Allow a device registration without implying functional driver support."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry):
        return GadgetBridgeOptionsFlow()

    async def async_step_bluetooth(self, discovery_info: BluetoothServiceInfoBleak):
        advertisement = Advertisement(discovery_info.name or "", frozenset(discovery_info.service_uuids))
        if matching_drivers(advertisement, STANDARD_RULES) != ("standard_gatt",):
            return self.async_abort(reason="unsupported_device")
        self._discovered = discovery_info
        await self.async_set_unique_id(discovery_info.address.upper())
        self._abort_if_unique_id_configured()
        self.context["title_placeholders"] = {"name": discovery_info.name or discovery_info.address}
        return await self.async_step_confirm()

    async def async_step_confirm(self, user_input=None):
        if user_input is not None:
            info = self._discovered
            name = info.name or info.address
            return self.async_create_entry(title=name, data={CONF_ADDRESS: info.address.upper(), CONF_NAME: name})
        return self.async_show_form(step_id="confirm", description_placeholders={"name": self._discovered.name or self._discovered.address})

    async def async_step_user(self, user_input: dict | None = None):
        """Register a candidate BLE device for later driver development."""
        errors = {}
        if user_input is not None:
            address = user_input[CONF_ADDRESS].strip().upper()
            # Currently require a conventional BLE MAC address for this manual flow.
            import re
            if not re.fullmatch(r"(?:[0-9A-F]{2}:){5}[0-9A-F]{2}", address):
                errors["base"] = "invalid_address"
            else:
                await self.async_set_unique_id(address)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_NAME].strip(),
                    data={CONF_ADDRESS: address, CONF_NAME: user_input[CONF_NAME].strip()},
                )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_ADDRESS): str,
            }),
            errors=errors,
        )


class GadgetBridgeOptionsFlow(config_entries.OptionsFlowWithReload):
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        options = self.config_entry.options
        return self.async_show_form(step_id="init", data_schema=vol.Schema({
            vol.Required("poll_interval", default=options.get("poll_interval", 300)): vol.All(vol.Coerce(int), vol.Range(min=15, max=86400)),
            vol.Required("reconnect_interval", default=options.get("reconnect_interval", 30)): vol.All(vol.Coerce(int), vol.Range(min=5, max=3600)),
            vol.Required("record_history", default=options.get("record_history", True)): bool,
        }))
