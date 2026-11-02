"""Receive macOS system audio from ScreenCaptureKit for live transcription."""

import asyncio
from collections import deque
import hashlib
import os
from pathlib import Path
import platform
import sys
import tempfile

PACKET_BYTES = 4096  # 2048 samples, mono linear16 at 48 kHz
HELPER_PATH = Path(__file__).with_name("mac_system_audio.swift")


async def _compiled_helper() -> Path:
    """Compile once and launch the capture executable directly, without a Swift driver child."""
    fingerprint = hashlib.sha256(
        HELPER_PATH.read_bytes() + platform.mac_ver()[0].encode() + platform.machine().encode()
    ).hexdigest()[:16]
    binary = Path(tempfile.gettempdir()) / f"gekko-system-audio-{fingerprint}"
    if binary.is_file() and os.access(binary, os.X_OK):
        return binary
    process = await asyncio.create_subprocess_exec(
        "swiftc", str(HELPER_PATH), "-o", str(binary),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, error = await process.communicate()
    if process.returncode != 0:
        raise RuntimeError(f"Swift audio helper compilation failed: {error.decode(errors='replace')[-800:]}")
    return binary


class MacSystemAudioBridge:
    def __init__(self, on_failure=None, on_packet=None):
        self.on_failure = on_failure
        self.on_packet = on_packet
        self.process = None
        self.packets = deque(maxlen=8)
        self.reader_task = None
        self.error_task = None
        self.packets_received = 0
        self.nonzero_packets_received = 0

    async def start(self) -> bool:
        if sys.platform != "darwin":
            return False
        try:
            binary = await _compiled_helper()
            self.process = await asyncio.create_subprocess_exec(
                str(binary), str(os.getpid()),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            async def wait_until_ready():
                while True:
                    line = await self.process.stderr.readline()
                    if not line:
                        return False
                    message = line.decode(errors="replace").strip()
                    if message == "System audio capture ready":
                        return True
                    if message.startswith("System audio capture failed:"):
                        print(message)
                        return False
                    if message:
                        print(f"macOS system audio: {message}")

            ready = await asyncio.wait_for(wait_until_ready(), timeout=20)
            if not ready:
                await self.stop()
                return False
            self.reader_task = asyncio.create_task(self._read_packets())
            self.error_task = asyncio.create_task(self._read_errors())
            return True
        except (OSError, asyncio.TimeoutError, RuntimeError) as error:
            print(f"macOS system audio unavailable: {error}")
            await self.stop()
            return False

    async def _read_packets(self):
        try:
            while True:
                packet = await self.process.stdout.readexactly(PACKET_BYTES)
                self.packets_received += 1
                self.nonzero_packets_received += bool(any(packet))
                self.packets.append(packet)
                if self.on_packet:
                    await self.on_packet(packet)
        except asyncio.IncompleteReadError:
            if self.process is not None and self.on_failure:
                await self.on_failure()
        except asyncio.CancelledError:
            pass
        except Exception as error:
            print(f"macOS system audio forwarding failed: {error}")
            if self.process is not None and self.on_failure:
                await self.on_failure()

    async def _read_errors(self):
        try:
            while line := await self.process.stderr.readline():
                message = line.decode(errors="replace").strip()
                if message:
                    print(f"macOS system audio: {message}")
        except asyncio.CancelledError:
            pass

    async def stop(self):
        process = self.process
        self.process = None
        tasks = [task for task in (self.reader_task, self.error_task) if task]
        for task in tasks:
            if task:
                task.cancel()
        if process and process.returncode is None:
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=3)
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        self.reader_task = None
        self.error_task = None
        self.packets.clear()
