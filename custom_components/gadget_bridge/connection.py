"""Reconnectable standard GATT session using Home Assistant Bluetooth."""
import asyncio
import logging
from contextlib import suppress

from bleak import BleakClient
from bleak_retry_connector import establish_connection
from homeassistant.components import bluetooth
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .drivers.gatt import HEART_RATE_MEASUREMENT, BATTERY_LEVEL, decode_heart_rate, decode_battery

_LOGGER = logging.getLogger(__name__)


class GattSession:
    def __init__(self, hass, address, entry_id):
        self.hass = hass
        self.address = address
        self.signal = f"gadget_bridge_{entry_id}"
        self.values = {}
        self.connected = False
        self.task = None

    def publish(self, kind, value):
        self.values[kind] = value
        async_dispatcher_send(self.hass, self.signal)

    def heart_notification(self, sender, data):
        try:
            self.publish("heart_rate", decode_heart_rate(bytes(data)).bpm)
        except ValueError:
            _LOGGER.debug("Invalid heart rate notification")

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
                if heart is None and battery is None:
                    raise ValueError("No supported standard GATT characteristics")
                self.connected = True
                async_dispatcher_send(self.hass, self.signal)
                if heart is not None:
                    await client.start_notify(heart, self.heart_notification)
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
