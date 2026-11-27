# History storage foundation

HistoryStore provides SQLite persistence, UTC normalization, scalar sample upserts, per-device stream cursors and atomic batch/cursor commits. Run synchronous methods in Home Assistant's executor. This module is not yet wired to integration setup or drivers. Future work: lifecycle, async synchronization locks, pagination, structured sleep/ECG/BIA records, retention and export. Scalar samples with identical device, metric, timestamp and unit replace earlier values; high-frequency samples need a separate sequence-aware schema.
