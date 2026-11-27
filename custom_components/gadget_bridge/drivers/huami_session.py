"""Experimental Huami session using standard measurements after authentication."""
import logging
from ..connection import GattSession
from .huami_activity import REALTIME_STEPS, decode_steps

_LOGGER = logging.getLogger(__name__)
from .huami_auth import authenticate, parse_key


class HuamiSession(GattSession):
    supports_steps = True

    def __init__(self, *args, auth_key="", **kwargs):
        super().__init__(*args, **kwargs)
        self._auth_key = parse_key(auth_key)
        self._steps_char = None

    async def prepare_client(self, client):
        await authenticate(client, self._auth_key)


    def steps_notification(self, sender, data):
        try:
            self.publish("steps", decode_steps(bytes(data)))
        except ValueError:
            _LOGGER.debug("Unsupported Huami steps packet")

    async def setup_extra(self, client):
        self._steps_char = client.services.get_characteristic(REALTIME_STEPS)
        if self._steps_char is None:
            return False
        properties = self._steps_char.properties
        if "notify" in properties or "indicate" in properties:
            await client.start_notify(self._steps_char, self.steps_notification)
        return any(p in properties for p in ("read", "notify", "indicate"))

    async def poll_extra(self, client):
        if self._steps_char is not None and "read" in self._steps_char.properties:
            try:
                self.steps_notification(None, await client.read_gatt_char(self._steps_char))
            except Exception:
                _LOGGER.debug("Huami steps read failed", exc_info=True)
