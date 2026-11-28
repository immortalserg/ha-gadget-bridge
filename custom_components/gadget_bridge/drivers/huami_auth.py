"""Experimental legacy Huami authentication over an existing BLE connection."""
import asyncio

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from .huami_legacy import (
    AUTH_CHARACTERISTIC, challenge_request, challenge_response,
    authentication_succeeded,
)


def parse_key(value: str) -> bytes:
    if len(value) != 32:
        raise ValueError("Expected 32 hexadecimal characters")
    key = bytes.fromhex(value)
    if len(key) != 16:
        raise ValueError("Expected a 16-byte key")
    return key


def encrypt_block(key: bytes, block: bytes) -> bytes:
    if len(key) != 16 or len(block) != 16:
        raise ValueError("Expected AES-128 key and one block")
    encryptor = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    return encryptor.update(block) + encryptor.finalize()


async def authenticate(client, key: bytes, timeout: float = 15) -> None:
    """Authenticate an already connected client with a provisioned key."""
    if len(key) != 16:
        raise ValueError("Expected a 16-byte key")
    packets = asyncio.Queue(maxsize=32)

    def receive(_sender, data):
        if not packets.full():
            packets.put_nowait(bytes(data))

    await client.start_notify(AUTH_CHARACTERISTIC, receive)
    try:
        async with asyncio.timeout(timeout):
            await client.write_gatt_char(AUTH_CHARACTERISTIC, challenge_request(), response=True)
            packet = await packets.get()
            reply = challenge_response(packet, key, encrypt_block)
            await client.write_gatt_char(AUTH_CHARACTERISTIC, reply, response=True)
            if not authentication_succeeded(await packets.get()):
                raise PermissionError("Device rejected authentication")
    finally:
        await client.stop_notify(AUTH_CHARACTERISTIC)
