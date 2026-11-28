import unittest
from custom_components.gadget_bridge.drivers.huami_activity import decode_steps


class ActivityTests(unittest.TestCase):
    def test_steps(self):
        self.assertEqual(decode_steps(b"\x00\x39\x30" + b"\xff" * 10), 12345)
        self.assertEqual(decode_steps(b"\x00\xff\xff" + bytes(10)), 65535)

    def test_wrong_lengths(self):
        for length in (0, 4, 12, 14, 20):
            with self.assertRaises(ValueError):
                decode_steps(bytes(length))
