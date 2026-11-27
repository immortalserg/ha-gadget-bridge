"""Import a normalized device inventory from a reviewed upstream export."""
import argparse
import json
from pathlib import Path

def normalize(rows):
    result = {}
    for row in rows:
        item = {key: str(row[key]).strip() for key in ("manufacturer", "model", "family", "upstream_id")}
        if not all(item.values()):
            raise ValueError("Empty required field")
        key = item["upstream_id"]
        if key in result:
            raise ValueError(f"Duplicate upstream ID: {key}")
        item["status"] = "catalogued"
        result[key] = item
    return sorted(result.values(), key=lambda x: (x["manufacturer"].casefold(), x["model"].casefold(), x["upstream_id"]))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--output", type=Path, default=Path("custom_components/gadget_bridge/devices/catalog.json"))
    args = parser.parse_args()
    rows = normalize(json.loads(args.source.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"source": "https://codeberg.org/Freeyourgadget/Gadgetbridge", "revision": args.revision, "devices": rows}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

if __name__ == "__main__":
    main()
