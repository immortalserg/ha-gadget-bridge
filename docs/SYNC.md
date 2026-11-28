# Synchronization foundation

DeviceSync serializes history operations per device, reads a durable per-stream cursor, connects through a driver, requests bounded pages, commits each page and cursor atomically, and disconnects in a finally block. Failed pages do not advance the stored cursor. A subsequent call resumes committed progress.

Instantiate exactly one manager per device. Drivers must make disconnect safe after failed or partial connection. Driver-specific authentication belongs in connect. A non-final page must advance its cursor. The final page should supply a durable resume cursor when supported.

This is a standalone foundation, not yet wired into Home Assistant lifecycle or the existing standard GATT connection. Periodic scheduling, retries, timeouts, command arbitration and actual vendor adapters remain future work.
