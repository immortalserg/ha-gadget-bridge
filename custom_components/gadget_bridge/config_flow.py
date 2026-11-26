"""Manual configuration flow for the initial HA Gadget Bridge foundation."""

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_ADDRESS, CONF_NAME

from .const import DOMAIN


class GadgetBridgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Allow a device registration without implying functional driver support."""

    VERSION = 1

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
