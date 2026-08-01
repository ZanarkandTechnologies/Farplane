from __future__ import annotations

import importlib.util
import json
import sys
import tomllib
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("execute_fish_audio.py")
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("execute_fish_audio", SCRIPT)
assert SPEC and SPEC.loader
executor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(executor)


def packet() -> dict:
    return {
        "kind": "voice",
        "provider": "fish",
        "prompt_or_script": "A short test.",
        "parameters": {
            "model": "s2.1-pro-free",
            "reference_id_source": "FISH_AUDIO_REFERENCE_ID",
            "format": "mp3",
            "prosody": {"speed": 1.25},
        },
        "timing": {"duration_seconds": 2.0},
    }


class FishAudioExecutorTests(unittest.TestCase):
    def test_tracked_default_uses_current_free_engine(self) -> None:
        config_path = SCRIPT.parents[1] / "config.toml"
        config = tomllib.loads(config_path.read_text(encoding="utf-8"))
        self.assertEqual(config["providers"]["fish"]["model"], "s2.1-pro-free")

    def test_request_keeps_reference_out_of_url_and_uses_free_model(self) -> None:
        request = executor.build_tts_request(packet(), "credential", "private-reference")
        body = json.loads(request.data)
        self.assertEqual(request.full_url, "https://api.fish.audio/v1/tts")
        self.assertEqual(request.headers["Model"], "s2.1-pro-free")
        self.assertEqual(body["reference_id"], "private-reference")
        self.assertEqual(body["prosody"]["speed"], 1.25)

    def test_requires_runtime_reference_marker(self) -> None:
        malformed = packet()
        malformed["parameters"].pop("reference_id_source")
        with self.assertRaisesRegex(ValueError, "reference_id_source"):
            executor.require_runtime_reference(malformed, "private-reference")

    def test_rejects_non_public_or_untrained_voice(self) -> None:
        with self.assertRaisesRegex(ValueError, "public, trained TTS"):
            executor.public_voice_metadata(
                {"visibility": "private", "state": "trained", "type": "tts"}
            )

    def test_receipt_metadata_omits_private_identity(self) -> None:
        metadata = executor.public_voice_metadata(
            {
                "id": "private-reference",
                "title": "private-title",
                "visibility": "public",
                "state": "trained",
                "type": "tts",
                "languages": ["en"],
                "tags": ["storytelling"],
            }
        )
        self.assertNotIn("id", metadata)
        self.assertNotIn("title", metadata)
        self.assertEqual(metadata["visibility"], "public")

    def test_duration_gate_is_closed_until_review(self) -> None:
        passed = executor.acceptance(packet(), {"duration_seconds": 1.75})
        failed = executor.acceptance(packet(), {"duration_seconds": 1.2})
        self.assertTrue(passed["duration_pass"])
        self.assertFalse(failed["duration_pass"])
        self.assertFalse(passed["accepted"])
        self.assertTrue(passed["manual_creative_review_pending"])


if __name__ == "__main__":
    unittest.main()
