import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("extract", Path(__file__).resolve().parents[1] / "tools/extract_coordinators.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_inventory(tmp_path):
    folder = tmp_path / "app/src/main/java/example/devices/mi"
    folder.mkdir(parents=True)
    (folder / "ExampleCoordinator.java").write_text("public class ExampleCoordinator extends Base {}")
    (folder / "Other.java").write_text("class Other {}")
    rows = module.extract(tmp_path)
    assert len(rows) == 1
    assert rows[0]["family_hint"] == "mi"
    assert rows[0]["coordinator"] == "ExampleCoordinator"
    assert rows[0]["status"] == "unreviewed"
