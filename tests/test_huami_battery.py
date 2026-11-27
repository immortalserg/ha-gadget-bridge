import unittest
from custom_components.gadget_bridge.drivers.huami_battery import BatteryInfo, decode_battery_info


class BatteryTests(unittest.TestCase):
    def test_fields(self):
        self.assertEqual(decode_battery_info(bytes([15, 48, 1]) + bytes(16) + bytes([100])), BatteryInfo(48, True, 100))

    def test_unknown(self):
        self.assertEqual(decode_battery_info(b""), BatteryInfo(None, None, None))
        self.assertEqual(decode_battery_info(bytes([15, 255, 3])), BatteryInfo(None, None, None))
