"""Experimental Huami session using standard measurements after authentication."""
from ..connection import GattSession
from .huami_auth import authenticate, parse_key


class HuamiSession(GattSession):
    def __init__(self, *args, auth_key="", **kwargs):
        super().__init__(*args, **kwargs)
        self._auth_key = parse_key(auth_key)

    async def prepare_client(self, client):
        await authenticate(client, self._auth_key)
