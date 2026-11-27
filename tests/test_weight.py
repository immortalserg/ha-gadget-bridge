"""Offline protocol fixtures; Home Assistant installation not required."""
import importlib.util
import sys
from pathlib import Path

import pytest

path = Path(__file__).resolve().parents[1] / "custom_components/gadget_bridge/drivers/weight.py"
spec = importlib.util.spec_from_file_location("gadget_weight", path)
weight = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = weight
spec.loader.exec_module(weight)


def test_metric_minimal():
    result = weight.decode_weight(bytes([0, 0x10, 0x27]))
    assert result.weight == 50.0 and result.unit == "kg"
    assert result.measured_at is None


def test_imperial():
    result = weight.decode_weight(bytes([1, 0x10, 0x27]))
    assert result.weight == 100.0 and result.unit == "lb"


def test_optional_fields():
    packet = bytes([0x0E, 0x10, 0x27, 0xE9, 0x07, 11, 27, 10, 20, 30, 7, 0xFA, 0x00, 0xD0, 0x07])
    result = weight.decode_weight(packet)
    assert result.measured_at.year == 2025
    assert result.user_id == 7
    assert result.bmi == 25.0
    assert result.height == 2.0 and result.height_unit == "m"


def test_unknown_user():
    assert weight.decode_weight(bytes([4, 0, 0, 255])).user_id is None


@pytest.mark.parametrize("packet", [
    b"", b"\x00\x01", b"\x02\x01\x00\x00",
    b"\x04\x01\x00", b"\x08\x01\x00\x00",
    b"\x00\x00\x00\x00", b"\x10\x00\x00",
    bytes([2, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
])
def test_reject_invalid_packet(packet):
    with pytest.raises(ValueError):
        weight.decode_weight(packet)
