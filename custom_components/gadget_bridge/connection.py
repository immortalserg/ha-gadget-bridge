"""Reconnectable standard GATT session using Home Assistant Bluetooth."""
import asyncio
import logging
from contextlib import suppress
from datetime import datetime, timezone
from .drivers.base import Capability, Measurement

from bleak import BleakClient
from bleak_retry_connector import establish_connection
from homeassistant.components import bluetooth
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .drivers.gatt import HEART_RATE_MEASUREMENT, BATTERY_LEVEL, decode_heart_rate, decode_battery
from .drivers.weight import WEIGHT_MEASUREMENT, decode_weight

_LOGGER = logging.getLogger(__name__)


class GattSession:
    def __init__(self, hass, address, entry_id, store=None):
        self.hass = hass
        self.address = address
        self.signal = f"gadget_bridge_{entry_id}"
        self.values = {}
        self.connected = False
        self.task = None
        self.store = store
        self.entry_id = entry_id
        self.pending = []
        self.writer = None

    async def flush_history(self):
        while self.pending:
            batch = self.pending[:256]
            try:
                await self.hass.async_add_executor_job(self.store.save, self.entry_id, "live", batch)
            except Exception:
                _LOGGER.warning("Unable to persist gadget history", exc_info=True)
                return
            del self.pending[:len(batch)]

    def publish(self, kind, value):
        self.values[kind] = value
        if self.store is not None:
            units = {"heart_rate": "bpm", "battery": "%", "weight": "kg"}
            if kind in units:
                if len(self.pending) >= 4096:
                    self.pending.pop(0)
                    _LOGGER.warning("Gadget history buffer full; oldest sample dropped")
                self.pending.append(Measurement(Capability(kind), datetime.now(timezone.utc), value, units[kind], self.entry_id))
                if self.writer is None or self.writer.done():
                    self.writer = self.hass.async_create_task(self.flush_history())
        async_dispatcher_send(self.hass, self.signal)

    def heart_notification(self, sender, data):
        try:
            self.publish("heart_rate", decode_heart_rate(bytes(data)).bpm)
        except ValueError:
            _LOGGER.debug("Invalid heart rate notification")

    def weight_indication(self, sender, data):
        try:
            reading = decode_weight(bytes(data))
            # HA sensor provides a consistent kg state for measurements.
            kilograms = reading.weight * 0.45359237 if reading.unit == "lb" else reading.weight
            self.publish("weight", round(kilograms, 3))
        except ValueError:
            _LOGGER.debug("Invalid weight indication")

    async def run(self):
        while True:
            client = None
            disconnected = asyncio.Event()
            try:
                device = bluetooth.async_ble_device_from_address(self.hass, self.address, connectable=True)
                if device is None:
                    await asyncio.sleep(30)
                    continue
                client = await establish_connection(
                    BleakClient, device, self.address,
                    disconnected_callback=lambda _: self.hass.loop.call_soon_threadsafe(disconnected.set),
                )
                heart = client.services.get_characteristic(HEART_RATE_MEASUREMENT)
                battery = client.services.get_characteristic(BATTERY_LEVEL)
                weight = client.services.get_characteristic(WEIGHT_MEASUREMENT)
                if heart is None and battery is None and weight is None:
                    raise ValueError("No supported standard GATT characteristics")
                self.connected = True
                async_dispatcher_send(self.hass, self.signal)
                if heart is not None:
                    await client.start_notify(heart, self.heart_notification)
                if weight is not None:
                    await client.start_notify(weight, self.weight_indication)
                while client.is_connected and not disconnected.is_set():
                    if battery is not None:
                        try:
                            self.publish("battery", decode_battery(bytes(await client.read_gatt_char(battery))))
                        except Exception:
                            _LOGGER.debug("Battery read failed", exc_info=True)
                    try:
                        await asyncio.wait_for(disconnected.wait(), timeout=300)
                    except TimeoutError:
                        pass
            except asyncio.CancelledError:
                raise
            except Exception:
                _LOGGER.debug("GATT session failed for %s", self.address, exc_info=True)
            finally:
                self.connected = False
                self.values.clear()
                async_dispatcher_send(self.hass, self.signal)
                if client is not None:
                    with suppress(Exception):
                        await client.disconnect()
            await asyncio.sleep(30)

    async def stop(self):
        if self.task is not None:
            self.task.cancel()
            with suppress(asyncio.CancelledError):
                await self.task
            self.task = None
        if self.writer is not None:
            await self.writer
        if self.store is not None:
            await self.flush_history()
