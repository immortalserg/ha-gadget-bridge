import struct
import unittest
from custom_components.gadget_bridge.drivers.huami_activity import Activity, decode_activity


class ActivityTests(unittest.TestCase):
    def test_candidate_layout(self):
        self.assertEqual(decode_activity(b"\x00" + struct.pack("<III", 12345, 8500, 350)), Activity(12345, 8500, 350))

    def test_wrong_lengths(self):
        for length in (0, 4, 12, 14, 20):
            with self.assertRaises(ValueError):
                decode_activity(bytes(length))
