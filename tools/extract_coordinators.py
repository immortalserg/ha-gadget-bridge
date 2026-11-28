"""Inventory Java device coordinators from a local Gadgetbridge checkout.

This is a source inventory, not a verified model catalogue.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess


def extract(root):
    rows = []
    for path in sorted(root.rglob("*Coordinator.java")):
        relative = path.relative_to(root).as_posix()
        if "/devices/" not in relative:
            continue
        source = path.read_text(encoding="utf-8")
        match = re.search(r"\bclass\s+(\w+Coordinator)\b", source)
        if not match:
            continue
        rows.append({
            "coordinator": match.group(1),
            "family_hint": path.parent.name,
            "source_path": relative,
            "status": "unreviewed",
        })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("checkout", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    revision = subprocess.check_output(["git", "-C", str(args.checkout), "rev-parse", "HEAD"], text=True).strip()
    if subprocess.check_output(["git", "-C", str(args.checkout), "status", "--porcelain"], text=True).strip():
        parser.error("Upstream checkout must be clean")
    rows = extract(args.checkout)
    if not rows:
        parser.error("No device coordinators found")
    args.output.write_text(json.dumps({"revision": revision, "coordinators": rows}, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
