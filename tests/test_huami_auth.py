import unittest

from custom_components.gadget_bridge.drivers.huami_auth import encrypt_block, parse_key, authenticate


class FakeClient:
    def __init__(self, accepted=True):
        self.accepted = accepted
        self.stopped = False
        self.writes = []

    async def start_notify(self, characteristic, callback):
        self.callback = callback

    async def write_gatt_char(self, characteristic, data, response):
        self.writes.append(data)
        if len(self.writes) == 1:
            self.callback(None, b"\x10\x02\x01" + bytes(16))
        else:
            self.callback(None, b"\x10\x03" + (b"\x01" if self.accepted else b"\x04"))

    async def stop_notify(self, characteristic):
        self.stopped = True


class AuthTests(unittest.IsolatedAsyncioTestCase):
    def test_aes_vector(self):
        key = parse_key("000102030405060708090a0b0c0d0e0f")
        block = bytes.fromhex("00112233445566778899aabbccddeeff")
        self.assertEqual(encrypt_block(key, block).hex(), "69c4e0d86a7b0430d8cdb78070b4c55a")

    async def test_success(self):
        client = FakeClient()
        await authenticate(client, bytes(16))
        self.assertTrue(client.stopped)
        self.assertEqual(len(client.writes[1]), 18)

    async def test_rejected(self):
        client = FakeClient(False)
        with self.assertRaises(PermissionError):
            await authenticate(client, bytes(16))
        self.assertTrue(client.stopped)
