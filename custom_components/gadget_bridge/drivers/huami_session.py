"""Experimental Huami session using standard measurements after authentication."""
import logging
from ..connection import GattSession
from .huami_battery import BATTERY_INFO, decode_battery_info
from .huami_activity import REALTIME_STEPS, decode_steps

_LOGGER = logging.getLogger(__name__)
from .huami_auth import authenticate, parse_key


class HuamiSession(GattSession):
    supports_steps = True
    supports_charging = True

    def __init__(self, *args, auth_key="", **kwargs):
        super().__init__(*args, **kwargs)
        self._auth_key = parse_key(auth_key)
        self._steps_char = None
        self._battery_char = None

    async def prepare_client(self, client):
        await authenticate(client, self._auth_key)


    def steps_notification(self, sender, data):
        try:
            self.publish("steps", decode_steps(bytes(data)))
        except ValueError:
            _LOGGER.debug("Unsupported Huami steps packet")

    def battery_notification(self, sender, data):
        info = decode_battery_info(bytes(data))
        if info.level is not None:
            self.publish("battery", info.level)
        self.publish("charging", info.charging)
        self.publish("last_charge_level", info.last_charge_level)

    async def setup_extra(self, client):
        self._battery_char = client.services.get_characteristic(BATTERY_INFO)
        battery_supported = False
        if self._battery_char is not None:
            props = self._battery_char.properties
            if "notify" in props or "indicate" in props:
                await client.start_notify(self._battery_char, self.battery_notification)
            battery_supported = any(p in props for p in ("read", "notify", "indicate"))
        self._steps_char = client.services.get_characteristic(REALTIME_STEPS)
        if self._steps_char is None:
            return battery_supported
        properties = self._steps_char.properties
        if "notify" in properties or "indicate" in properties:
            await client.start_notify(self._steps_char, self.steps_notification)
        return battery_supported or any(p in properties for p in ("read", "notify", "indicate"))

    async def poll_extra(self, client):
        if self._battery_char is not None and "read" in self._battery_char.properties:
            try:
                self.battery_notification(None, await client.read_gatt_char(self._battery_char))
            except Exception:
                _LOGGER.debug("Huami battery read failed", exc_info=True)
        if self._steps_char is not None and "read" in self._steps_char.properties:
            try:
                self.steps_notification(None, await client.read_gatt_char(self._steps_char))
            except Exception:
                _LOGGER.debug("Huami steps read failed", exc_info=True)
