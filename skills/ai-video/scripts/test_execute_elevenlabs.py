from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("execute_elevenlabs.py")
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("execute_elevenlabs", SCRIPT)
assert SPEC and SPEC.loader
executor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(executor)


def packet(kind: str) -> dict:
    return {
        "kind": kind,
        "prompt_or_script": "Restrained instrumental pulse with a clean ending.",
        "parameters": {"model": "music_v2", "force_instrumental": True},
        "timing": {"duration_seconds": 12.5},
    }


class ElevenLabsExecutorTests(unittest.TestCase):
    def test_builds_music_v2_request(self) -> None:
        request = executor.build_request(packet("music"), "credential")
        body = json.loads(request.data)
        self.assertEqual(
            request.full_url,
            "https://api.elevenlabs.io/v1/music?output_format=mp3_48000_192",
        )
        self.assertEqual(body["model_id"], "music_v2")
        self.assertEqual(body["music_length_ms"], 12500)
        self.assertTrue(body["force_instrumental"])

    def test_music_respects_explicit_output_format_and_duration(self) -> None:
        payload = packet("music")
        payload["parameters"].update(
            {"output_format": "mp3_44100_192", "duration_seconds": 30}
        )
        request = executor.build_request(payload, "credential")
        body = json.loads(request.data)
        self.assertTrue(request.full_url.endswith("output_format=mp3_44100_192"))
        self.assertEqual(body["music_length_ms"], 30000)

    def test_music_uses_nonvoice_duration_acceptance(self) -> None:
        result = executor.acceptance(packet("music"), {"duration_seconds": 12.4})
        self.assertTrue(result["duration_pass"])
        self.assertFalse(result["accepted"])
        self.assertTrue(result["manual_creative_review_pending"])


if __name__ == "__main__":
    unittest.main()
