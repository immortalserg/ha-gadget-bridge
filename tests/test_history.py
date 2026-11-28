import importlib.util
from datetime import datetime, timezone, timedelta
from pathlib import Path
from types import SimpleNamespace

spec = importlib.util.spec_from_file_location("history", Path(__file__).resolve().parents[1] / "custom_components/gadget_bridge/history.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def test_persistence_and_deduplication(tmp_path):
    path = tmp_path / "history.sqlite"
    store = m.HistoryStore(path)
    now = datetime.now(timezone.utc)
    item = SimpleNamespace(device_id="a", kind="steps", measured_at=now, value=10, unit="steps")
    store.save("a", "activity", [item], "first")
    item.measured_at = now.astimezone(timezone(timedelta(hours=2)))
    item.value = 12
    store.save("a", "activity", [item], "second")
    reopened = m.HistoryStore(path)
    assert reopened.cursor("a", "activity") == "second"
    assert len(reopened.read("a", "steps")) == 1
    assert reopened.read("a", "steps")[0][1] == 12
    assert reopened.read("b", "steps") == []


def test_invalid_batch_keeps_cursor(tmp_path):
    import pytest
    store = m.HistoryStore(tmp_path / "history.sqlite")
    store.save("a", "activity", [], "first")
    item = SimpleNamespace(device_id="b", kind="steps", measured_at=datetime.now(timezone.utc), value=10, unit="steps")
    with pytest.raises(ValueError):
        store.save("a", "activity", [item], "second")
    assert store.cursor("a", "activity") == "first"
