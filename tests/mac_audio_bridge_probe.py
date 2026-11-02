"""Report capture levels without storing or transcribing audio.

Run with: .venv/bin/python tests/mac_audio_bridge_probe.py
"""

import asyncio
from array import array
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from services.mac_audio_bridge import MacSystemAudioBridge


async def main():
    bridge = MacSystemAudioBridge()
    if not await bridge.start():
        print("capture_ready=False")
        return
    nonzero = 0
    total = 0
    peak = 0
    try:
        for _ in range(150):
            await asyncio.sleep(0.05)
            while bridge.packets:
                samples = array("h")
                samples.frombytes(bridge.packets.popleft())
                level = max(abs(sample) for sample in samples)
                peak = max(peak, level)
                nonzero += level > 0
                total += 1
    finally:
        await bridge.stop()
    print(f"capture_ready=True packets={total} nonzero_packets={nonzero} peak_pcm={peak}")


if __name__ == "__main__":
    asyncio.run(main())
