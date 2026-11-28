"""Local durable measurement storage. Call synchronous methods in an executor."""
from contextlib import closing
from datetime import datetime, timezone
import math
import sqlite3


def utc_key(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Timezone-aware timestamp required")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds")


class HistoryStore:
    def __init__(self, path):
        self.path = path

    def _connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("CREATE TABLE IF NOT EXISTS measurements (device TEXT NOT NULL, kind TEXT NOT NULL, measured_at TEXT NOT NULL, value REAL NOT NULL, unit TEXT NOT NULL, PRIMARY KEY(device, kind, measured_at, unit))")
        db.execute("CREATE TABLE IF NOT EXISTS cursors (device TEXT NOT NULL, stream TEXT NOT NULL, cursor TEXT NOT NULL, PRIMARY KEY(device, stream))")
        return db

    def save(self, device, stream, measurements, cursor=None):
        """Commit a complete batch and its optional opaque cursor atomically."""
        rows = []
        for item in measurements:
            if item.device_id != device or not math.isfinite(item.value):
                raise ValueError("Invalid measurement")
            rows.append((device, str(item.kind), utc_key(item.measured_at), item.value, item.unit))
        with closing(self._connect()) as db, db:
            db.executemany("INSERT INTO measurements VALUES (?, ?, ?, ?, ?) ON CONFLICT(device, kind, measured_at, unit) DO UPDATE SET value=excluded.value", rows)
            if cursor is not None:
                db.execute("INSERT INTO cursors VALUES (?, ?, ?) ON CONFLICT(device, stream) DO UPDATE SET cursor=excluded.cursor", (device, stream, cursor))

    def cursor(self, device, stream):
        with closing(self._connect()) as db:
            row = db.execute("SELECT cursor FROM cursors WHERE device=? AND stream=?", (device, stream)).fetchone()
            return row[0] if row else None

    def read(self, device, kind, since=None, limit=1000):
        if not 1 <= limit <= 10000:
            raise ValueError("Invalid limit")
        with closing(self._connect()) as db:
            return db.execute("SELECT measured_at, value, unit FROM measurements WHERE device=? AND kind=? AND measured_at>=? ORDER BY measured_at, unit LIMIT ?", (device, str(kind), utc_key(since) if since is not None else "", limit)).fetchall()
