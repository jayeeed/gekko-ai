import asyncio
import unittest
from types import SimpleNamespace

from api.session_manager import InterviewSession
from services.stt_service import DeepgramManager


class TranscriptFlowTests(unittest.IsolatedAsyncioTestCase):
    async def test_repeated_interims_are_displayed_once_and_final_keeps_endpoint(self):
        received = []

        async def callback(data):
            received.append(data)

        manager = DeepgramManager.__new__(DeepgramManager)
        manager.stop_event = asyncio.Event()
        manager.transcript_callback = callback
        manager._last_interim = None

        async def send(text, is_final=False, speech_final=False):
            result = SimpleNamespace(
                channel=SimpleNamespace(alternatives=[SimpleNamespace(transcript=text, words=[])]),
                is_final=is_final,
                speech_final=speech_final,
            )
            await manager.on_message(result=result)

        await send("Hello?")
        await send("Hello?")
        await send("Hello? Can you listen to me?")
        await send("Hello? Can you listen to me?", True, True)

        self.assertEqual(len(received), 3)
        self.assertEqual(received[-1]["transcript"], "Hello? Can you listen to me?")
        self.assertTrue(received[-1]["speech_final"])

    async def test_endpoint_dispatches_once_and_new_speech_does_not_cancel_ai(self):
        session = InterviewSession("test")
        session.websocket = object()
        started = []
        first_can_finish = asyncio.Event()

        async def send_json(kind, payload):
            if kind == "ai_processing_started":
                started.append(payload["question"])

        class FakeLLM:
            async def get_ai_answer(self, question, callback):
                if question == "First question?":
                    await first_can_finish.wait()
                return "answer", {"success": True}

        session._send_json = send_json
        session.llm_manager = FakeLLM()

        await session.on_transcript({"speaker": 0, "transcript": "First question?", "is_final": False})
        self.assertEqual(started, [])
        await session.on_transcript({"speaker": 0, "transcript": "First question?", "is_final": True, "speech_final": True})
        await asyncio.sleep(0)
        self.assertEqual(started, ["First question?"])
        await session.on_transcript({"speaker": 0, "transcript": "Second question?", "is_final": True, "speech_final": True})
        first_can_finish.set()
        await asyncio.gather(*list(session._ai_tasks))
        self.assertEqual(started, ["First question?", "Second question?"])

    async def test_final_segments_combine_until_speech_final(self):
        session = InterviewSession("test")
        processed = []

        async def capture(transcript, final_received_at):
            processed.append(transcript)

        session._process_aggregated_transcript = capture
        await session.on_transcript({"speaker": 0, "transcript": "First part", "is_final": True, "speech_final": False})
        await session.on_transcript({"speaker": 0, "transcript": "second part", "is_final": True, "speech_final": True})
        await asyncio.gather(*list(session._ai_tasks))
        self.assertEqual(processed, ["First part second part"])
        self.assertEqual(session.transcript_buffer, "")

    async def test_final_without_endpoint_uses_short_fallback(self):
        session = InterviewSession("test")
        processed = []

        async def capture(transcript, final_received_at):
            processed.append(transcript)

        session._process_aggregated_transcript = capture
        await session.on_transcript({"speaker": 0, "transcript": "Fallback question?", "is_final": True})
        await asyncio.sleep(0.85)
        await asyncio.gather(*list(session._ai_tasks))
        self.assertEqual(processed, ["Fallback question?"])


if __name__ == "__main__":
    unittest.main()
