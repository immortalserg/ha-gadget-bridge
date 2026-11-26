"""Check adapter-contract source and initial capability declarations."""
from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1] / "custom_components" / "gadget_bridge" / "drivers"


def test_driver_sources_parse():
    for path in ROOT.rglob("*.py"):
        ast.parse(path.read_text(encoding="utf-8"))


def test_capabilities_declared():
    source = (ROOT / "base.py").read_text(encoding="utf-8")
    for capability in ("HEART_RATE", "SPO2", "STEPS", "SLEEP", "WEIGHT", "BLOOD_PRESSURE", "BATTERY"):
        assert capability in source
