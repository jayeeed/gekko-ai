import unittest
from array import array

from api.session_manager import InterviewSession
from services.mac_audio_bridge import PACKET_BYTES


def packet(value):
    return array("h", [value] * (PACKET_BYTES // 2)).tobytes()


class MacAudioBridgeTests(unittest.IsolatedAsyncioTestCase):
    async def test_microphone_packets_use_microphone_stream(self):
        class FakeSTT:
            def __init__(self):
                self.received = []

            async def send_audio(self, audio):
                self.received.append(audio)

        session = InterviewSession("audio-test")
        session.stt_manager = FakeSTT()
        await session.handle_audio_chunk({"audio": list(packet(1000)), "is_muted": False})

        self.assertEqual(session.stt_manager.received, [packet(1000)])

    async def test_system_audio_has_its_own_transcription_stream(self):
        class FakeSTT:
            is_connected = True

            def __init__(self):
                self.received = []

            async def send_audio(self, audio, source="unknown"):
                self.received.append((audio, source))

        session = InterviewSession("system-audio-test")
        session.system_stt_manager = FakeSTT()
        audio = packet(500)
        await session._send_system_audio(audio)
        self.assertEqual(session.system_stt_manager.received, [(audio, "system")])

        session.state["is_universally_muted"] = True
        await session._send_system_audio(audio)
        self.assertEqual(len(session.system_stt_manager.received), 1)


if __name__ == "__main__":
    unittest.main()
