import importlib.util
import sys
from pathlib import Path
import pytest

path = Path(__file__).resolve().parents[1] / "custom_components/gadget_bridge/drivers/gatt.py"
spec = importlib.util.spec_from_file_location("gatt", path)
gatt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gatt
spec.loader.exec_module(gatt)

def test_heart():
    assert gatt.decode_heart_rate(bytes([0, 72])).bpm == 72
    assert gatt.decode_heart_rate(bytes([1, 44, 1])).bpm == 300
    assert gatt.decode_heart_rate(bytes([16, 60, 0, 4])).rr_seconds == (1.0,)

def test_battery():
    assert gatt.decode_battery(bytes([100])) == 100
    with pytest.raises(ValueError):
        gatt.decode_battery(bytes([101]))

def test_truncated():
    with pytest.raises(ValueError):
        gatt.decode_heart_rate(bytes([1, 72]))
