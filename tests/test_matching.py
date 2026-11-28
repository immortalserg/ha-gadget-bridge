import importlib.util
import sys
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "custom_components/gadget_bridge/drivers/matching.py"
spec = importlib.util.spec_from_file_location("gadget_matching", path)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def test_standard():
    adv = m.Advertisement("unknown", frozenset({"0000181D-0000-1000-8000-00805F9B34FB"}))
    assert m.matching_drivers(adv, m.STANDARD_RULES) == ("standard_gatt",)


def test_name_only_not_supported():
    adv = m.Advertisement("Mi Band", frozenset())
    assert m.matching_drivers(adv, m.STANDARD_RULES) == ()
    assert not m.MatchRule("vendor", frozenset(), "Mi").matches(adv)


def test_ambiguity():
    adv = m.Advertisement("Example", frozenset({"abc"}))
    rules = (m.MatchRule("a", frozenset({"abc"})), m.MatchRule("b", frozenset({"abc"}), "ex"))
    assert m.matching_drivers(adv, rules) == ("a", "b")
