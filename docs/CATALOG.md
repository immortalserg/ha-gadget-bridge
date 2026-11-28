# Device inventory

The catalogue is not a compatibility claim. Import a reviewed JSON array of records with manufacturer, model, family and upstream_id using:

```sh
python tools/import_catalog.py upstream-export.json --revision UPSTREAM_COMMIT
```

The importer validates required fields, rejects duplicate upstream identifiers and records provenance. It deliberately assigns catalogued status to every imported model. Actual driver support must be tracked independently.

The initial inventory is empty. Extracting records from Gadgetbridge Java coordinators and checking upstream licensing and model aliases remain necessary. Do not infer a device protocol from a matching name alone.

## Source inventory

Clone the current upstream repository from Codeberg and run:

```sh
git clone https://codeberg.org/Freeyourgadget/Gadgetbridge.git upstream-gadgetbridge
python tools/extract_coordinators.py upstream-gadgetbridge --output upstream-coordinators.json
```

The extractor inventories Java coordinator source files and records the clean checkout revision. Family hints are package directory names, not verified shared protocols. Review model names, aliases, abstract coordinators and licensing before importing into the supported-model catalogue. The extractor does not claim completeness or runtime compatibility.
