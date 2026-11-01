"""Measure live Deepgram endpointing and Luna first-token latency.

Run with the project's virtual environment. Uses a public Deepgram sample WAV
and configured API keys; never prints credentials or response text.
"""

import argparse
import asyncio
import io
import sys
import time
import wave
from array import array

import httpx

from core.provider_service import load_providers_config
from services.context_manager import PersistentContextManager
from services.llm_service import LLMManager
from services.stt_service import DeepgramManager


SAMPLE_URL = "https://static.deepgram.com/examples/voices/angus.wav"


def pcm_48k_mono(wav_bytes):
    with wave.open(io.BytesIO(wav_bytes), "rb") as sound:
        channels = sound.getnchannels()
        rate = sound.getframerate()
        if sound.getsampwidth() != 2 or channels not in (1, 2):
            raise ValueError("Sample WAV must contain 16-bit mono or stereo PCM")
        samples = array("h")
        samples.frombytes(sound.readframes(sound.getnframes()))
    mono = samples if channels == 1 else array(
        "h", ((samples[i] + samples[i + 1]) // 2 for i in range(0, len(samples), 2))
    )
    output = array("h", (mono[min(int(i * rate / 48000), len(mono) - 1)]
                         for i in range(round(len(mono) * 48000 / rate))))
    return output.tobytes(), len(output) / 48000


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm-only", action="store_true")
    parser.add_argument("--clip-seconds", type=float, default=5.0)
    parser.add_argument("--provider", choices=("OpenAI", "Gemini"), default="OpenAI")
    parser.add_argument("--reasoning-effort", choices=("none", "low"), default="low")
    args = parser.parse_args()
    question = "Hello, can you listen to me?"
    final_at = None
    first_token_at = None
    llm_started = None
    ai_task = None

    provider_config = next(p for p in load_providers_config() if p["name"] == args.provider)
    model_name = "gpt-6-luna" if args.provider == "OpenAI" else "gemini-flash-latest"
    context = PersistentContextManager()
    context.initialize_persistent_context({"name": "Latency Test", "interviewType": "general"})
    llm = LLMManager(
        provider_name=args.provider,
        base_url=provider_config["baseURL"],
        api_key=provider_config["apiKeys"][0],
        api_keys=provider_config["apiKeys"],
        model_name=model_name,
        request_params={"reasoning_effort": args.reasoning_effort} if args.provider == "OpenAI" else None,
    )
    llm.set_context_manager(context)

    async def on_chunk(chunk, chunk_type):
        nonlocal first_token_at
        if first_token_at is None and chunk:
            first_token_at = time.perf_counter()

    async def ask(text):
        nonlocal llm_started
        llm_started = time.perf_counter()
        answer, result = await llm.get_ai_answer(text, on_chunk)
        completed = time.perf_counter()
        print(f"model={model_name}")
        print(f"model_success={bool(result.get('success'))}")
        print(f"model_first_token_s={first_token_at - llm_started:.3f}" if first_token_at else "model_first_token_s=none")
        print(f"model_full_answer_s={completed - llm_started:.3f}")
        print(f"answer_chars={len(answer)}")

    if args.llm_only:
        await ask(question)
        return

    if not args.llm_only:
        response = httpx.get(SAMPLE_URL, timeout=20, follow_redirects=True)
        response.raise_for_status()
        pcm, duration = pcm_48k_mono(response.content)
        pcm = pcm[:int(args.clip_seconds * 48000) * 2]
        duration = len(pcm) / 96000
        print(f"sample_duration_s={duration:.3f}")
        endpoint = asyncio.Event()
        finals = []

        async def on_transcript(data):
            nonlocal final_at, ai_task
            if data["is_final"]:
                finals.append(data["transcript"])
                print(f"deepgram_final_speech_final={bool(data.get('speech_final'))}")
                if data.get("speech_final") and ai_task is None:
                    final_at = time.perf_counter()
                    question = " ".join(finals).strip()
                    ai_task = asyncio.create_task(ask(question))
                    endpoint.set()

        stt = DeepgramManager(on_transcript)
        await stt.start()
        if not stt.is_connected:
            raise RuntimeError("Deepgram live connection did not open")
        try:
            started = time.perf_counter()
            for offset in range(0, len(pcm), 4096):
                await stt.send_audio(pcm[offset:offset + 4096])
                await asyncio.sleep(2048 / 48000)
            for _ in range(25):
                if endpoint.is_set():
                    break
                await stt.send_audio(bytes(4096))
                await asyncio.sleep(2048 / 48000)
            await asyncio.wait_for(endpoint.wait(), 8)
            print(f"deepgram_start_to_final_s={final_at - started:.3f}")
            print(f"transcript_chars={len(' '.join(finals))}")
        finally:
            await stt.finish()
    await ai_task
    if final_at and first_token_at:
        print(f"final_to_first_token_s={first_token_at - final_at:.3f}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main())
