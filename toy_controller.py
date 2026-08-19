"""
Toy Controller - Buttplug + Safety Layer
"""

import asyncio
import time
import logging
from typing import Optional, List, Callable

from buttplug import ButtplugClient, DeviceOutputCommand, OutputType

import config
from patterns import get_pattern, list_patterns, PatternStep

logger = logging.getLogger(__name__)


class ToyController:
    def __init__(self):
        self.client: Optional[ButtplugClient] = None
        self.devices = []
        self._current_task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()
        self._is_running = False
        self._last_start_time: float = 0.0
        self._watchdog_task: Optional[asyncio.Task] = None
        self.max_intensity = config.MAX_INTENSITY
        self.timeout_seconds = config.CONTINUOUS_TIMEOUT_SECONDS
        self.safewords = list(config.DEFAULT_SAFEWORDS)
        self.on_stop_callbacks: List[Callable] = []

    # -------------------- Connection --------------------
    async def connect(self, url: str = None) -> bool:
        url = url or config.INTIFACE_URL
        self.client = ButtplugClient(config.CLIENT_NAME)

        self.client.on_device_added = self._on_device_added
        self.client.on_device_removed = self._on_device_removed
        self.client.on_disconnect = self._on_disconnect

        try:
            await self.client.connect(url)
            logger.info(f"Connected to Intiface at {url}")
            await self.client.start_scanning()
            await asyncio.sleep(2.5)
            await self.client.stop_scanning()
            self.devices = list(self.client.devices.values())
            logger.info(f"Found {len(self.devices)} device(s)")
            for d in self.devices:
                logger.info(f"  - {d.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Intiface: {e}")
            self.client = None
            return False

    async def disconnect(self):
        await self.stop()
        if self.client:
            try:
                await self.client.disconnect()
            except Exception:
                pass
            self.client = None
        self.devices = []

    def _on_device_added(self, device):
        logger.info(f"[+] Device added: {device.name}")
        if device not in self.devices:
            self.devices.append(device)

    def _on_device_removed(self, device):
        logger.info(f"[-] Device removed: {device.name}")
        if device in self.devices:
            self.devices.remove(device)

    def _on_disconnect(self):
        logger.warning("[!] Disconnected from Intiface server")

    # -------------------- Safety --------------------
    def set_safewords(self, words: List[str]):
        self.safewords = [w.strip().lower() for w in words if w.strip()]
        logger.info(f"Safewords set to: {self.safewords}")

    def is_safeword(self, text: str) -> bool:
        text = text.strip().lower()
        return any(sw in text for sw in self.safewords)

    def set_max_intensity(self, value: float):
        self.max_intensity = max(0.0, min(1.0, value))
        logger.info(f"Max intensity set to {self.max_intensity}")

    # -------------------- Core Control --------------------
    async def stop(self):
        """Emergency stop - highest priority"""
        self._stop_event.set()
        self._is_running = False

        if self._current_task and not self._current_task.done():
            self._current_task.cancel()
            try:
                await self._current_task
            except (asyncio.CancelledError, Exception):
                pass
        self._current_task = None

        if self._watchdog_task and not self._watchdog_task.done():
            self._watchdog_task.cancel()
            try:
                await self._watchdog_task
            except (asyncio.CancelledError, Exception):
                pass
        self._watchdog_task = None

        # Force stop all devices
        if self.client:
            try:
                await self.client.stop_all_devices()
            except Exception as e:
                logger.warning(f"stop_all_devices error: {e}")

        for cb in self.on_stop_callbacks:
            try:
                cb()
            except Exception:
                pass

        logger.info("⏹ All devices stopped")

    async def _set_intensity(self, intensity: float):
        intensity = min(intensity, self.max_intensity)
        intensity = max(0.0, intensity)

        for device in self.devices:
            if device.has_output(OutputType.VIBRATE):
                try:
                    await device.run_output(
                        DeviceOutputCommand(OutputType.VIBRATE, intensity)
                    )
                except Exception as e:
                    logger.warning(f"Failed to set intensity on {device.name}: {e}")

    async def _run_steps(self, steps: List[PatternStep]):
        """Execute a list of (intensity, duration) steps with stop support"""
        self._stop_event.clear()
        self._is_running = True
        self._last_start_time = time.time()

        # Start watchdog
        self._watchdog_task = asyncio.create_task(self._watchdog())

        try:
            for intensity, duration in steps:
                if self._stop_event.is_set():
                    break
                await self._set_intensity(intensity)
                # Sleep in small chunks so we can react to stop quickly
                remaining = duration
                while remaining > 0 and not self._stop_event.is_set():
                    sleep_time = min(0.05, remaining)
                    await asyncio.sleep(sleep_time)
                    remaining -= sleep_time
        finally:
            await self._set_intensity(0.0)
            self._is_running = False
            if self._watchdog_task and not self._watchdog_task.done():
                self._watchdog_task.cancel()

    async def _watchdog(self):
        """Auto-stop after continuous timeout"""
        try:
            await asyncio.sleep(self.timeout_seconds)
            if self._is_running:
                logger.warning(f"⏱ Continuous vibration timeout ({self.timeout_seconds}s) - auto stop")
                await self.stop()
        except asyncio.CancelledError:
            pass

    async def vibrate(self, intensity: float = 0.5, duration: float = 5.0):
        """Simple continuous vibration"""
        intensity = min(intensity, self.max_intensity)
        steps = [(intensity, duration)]
        await self._start_pattern(steps)

    async def play_pattern(self, name: str, intensity: float = 0.6, duration: float = 6.0, **kwargs):
        """Play a named pattern"""
        intensity = min(intensity, self.max_intensity)
        steps = get_pattern(name, intensity=intensity, duration=duration, **kwargs)
        await self._start_pattern(steps)

    async def _start_pattern(self, steps: List[PatternStep]):
        # Cancel any running pattern first
        if self._current_task and not self._current_task.done():
            await self.stop()
            await asyncio.sleep(0.1)

        self._current_task = asyncio.create_task(self._run_steps(steps))
        try:
            await self._current_task
        except asyncio.CancelledError:
            pass

    def is_vibrating(self) -> bool:
        return self._is_running

    def list_available_patterns(self) -> List[str]:
        return list_patterns()

    def has_devices(self) -> bool:
        return len(self.devices) > 0