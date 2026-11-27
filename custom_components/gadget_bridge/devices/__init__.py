"""Read-only upstream device inventory, separate from driver support."""
import json
from pathlib import Path

def load_catalog():
    return json.loads(Path(__file__).with_name("catalog.json").read_text(encoding="utf-8"))

def find_models(query):
    query = query.strip().casefold()
    return [row for row in load_catalog()["devices"] if query in (row["manufacturer"]+" "+row["model"]).casefold()]
