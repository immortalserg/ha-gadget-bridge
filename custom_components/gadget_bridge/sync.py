"""Transport-independent history synchronization."""
import asyncio
from dataclasses import dataclass
from typing import Protocol, Sequence

from .drivers.base import Measurement
from .history import HistoryStore


@dataclass(frozen=True)
class HistoryPage:
    measurements: Sequence[Measurement]
    next_cursor: str | None
    complete: bool


class HistoryDriver(Protocol):
    async def async_connect(self) -> None: ...
    async def async_disconnect(self) -> None: ...
    async def async_history_page(self, stream: str, cursor: str | None) -> HistoryPage: ...


class DeviceSync:
    """One instance per device; driver owns transport and authentication."""

    def __init__(self, device_id: str, driver: HistoryDriver, store: HistoryStore):
        self.device_id = device_id
        self.driver = driver
        self.store = store
        self.lock = asyncio.Lock()

    async def async_sync(self, stream: str, max_pages: int = 100) -> int:
        if max_pages < 1:
            raise ValueError("max_pages must be positive")
        async with self.lock:
            cursor = await asyncio.to_thread(self.store.cursor, self.device_id, stream)
            seen = {cursor}
            count = 0
            try:
                await self.driver.async_connect()
                for _ in range(max_pages):
                    page = await self.driver.async_history_page(stream, cursor)
                    if not page.complete and (page.next_cursor is None or page.next_cursor in seen):
                        raise RuntimeError("History cursor did not advance")
                    await asyncio.to_thread(self.store.save, self.device_id, stream, page.measurements, page.next_cursor)
                    count += len(page.measurements)
                    if page.complete:
                        return count
                    cursor = page.next_cursor
                    seen.add(cursor)
                raise RuntimeError("History page limit reached; committed pages retained")
            finally:
                await self.driver.async_disconnect()
