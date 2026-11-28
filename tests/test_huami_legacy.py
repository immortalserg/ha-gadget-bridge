import unittest
from custom_components.gadget_bridge.drivers.huami_legacy import (
    challenge_request, challenge_response, authentication_succeeded,
)


class LegacyHuamiTest(unittest.TestCase):
    def test_challenge(self):
        key = bytes(range(16))
        challenge = bytes(range(16, 32))
        def encrypt(k, block):
            self.assertEqual(k, key)
            self.assertEqual(block, challenge)
            return bytes(16)
        self.assertEqual(challenge_request(), b"\x02\x00")
        self.assertEqual(challenge_response(b"\x10\x02\x01" + challenge, key, encrypt), b"\x03\x00" + bytes(16))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            challenge_response(b"\x10\x02\x04" + bytes(16), bytes(16), lambda k, b: b)
        self.assertTrue(authentication_succeeded(b"\x10\x03\x01"))
        self.assertFalse(authentication_succeeded(b"\x10\x03\x04"))
