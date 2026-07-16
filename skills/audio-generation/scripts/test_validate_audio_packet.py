from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path

import yaml


SCRIPT = Path(__file__).with_name("validate_audio_packet.py")
SPEC = importlib.util.spec_from_file_location("validate_audio_packet", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def packet(provider: str = "fish", kind: str = "voice") -> dict:
    return {
        "kind": kind,
        "provider": provider,
        "capability": validator.CAPABILITY_LABELS[kind],
        "execution_mode": "dry_run",
        "brief_ref": "audio-direction.md",
        "prompt_or_script": "Explain the queue.",
        "profile_ref": None,
        "parameters": {"model": "s2-pro"},
        "timing": {"duration_seconds": 4, "cue_ref": "cue:scene-01.voice"},
        "output": {
            "owner": "tickets/TASK-0376/artifacts/audio",
            "path": "artifacts/audio/voice.mp3",
            "format": "mp3",
        },
        "rights_and_consent": {"status": "cleared", "basis": "library voice"},
        "acceptance_checks": ["duration matches cue"],
        "secret_source": "runtime_environment_only",
    }


class AudioPacketValidationTests(unittest.TestCase):
    def test_accepts_supported_packet(self) -> None:
        self.assertEqual(validator.validate_packet(packet()), [])

    def test_rejects_unsupported_pair(self) -> None:
        errors = validator.validate_packet(packet(provider="fish", kind="music"))
        self.assertTrue(any("unsupported provider/kind" in error for error in errors))

    def test_accepts_explicit_unsupported_blocker(self) -> None:
        blocker = {
            "result": "blocked_report", "code": "unsupported_provider_kind_pair",
            "provider": "fish", "kind": "music",
            "requested_capability": "music", "execution_mode": "dry_run",
            "brief_ref": "audio-direction.md", "reason": "Fish is voice-only",
            "silent_provider_switch": False, "next_action": "Select ElevenLabs explicitly",
            "external_call_made": False,
        }
        self.assertEqual(validator.validate_packet(blocker), [])

    def test_accepts_supported_pair_safety_blockers(self) -> None:
        missing_secret = {
            "result": "blocked_report", "code": "missing_runtime_secret",
            "provider": "fish", "kind": "voice", "requested_capability": "voice",
            "execution_mode": "authorized_execution", "brief_ref": "audio-direction.md",
            "reason": "FISH_AUDIO_API_KEY is not ready in the managed runtime",
            "silent_provider_switch": False, "next_action": "Configure the runtime secret",
            "external_call_made": False,
        }
        unresolved_consent = dict(
            missing_secret,
            code="unresolved_voice_consent",
            provider="elevenlabs",
            reason="Voice consent evidence is unresolved",
            next_action="Attach consent evidence or choose a rights-safe library voice",
        )
        self.assertEqual(validator.validate_packet(missing_secret), [])
        self.assertEqual(validator.validate_packet(unresolved_consent), [])

    def test_rejects_credential_key_and_value(self) -> None:
        keyed = packet()
        keyed["parameters"]["access_key"] = "hidden"
        self.assertTrue(any("credential-bearing" in error for error in validator.validate_packet(keyed)))
        valued = packet()
        valued["parameters"]["model"] = "sk-test-1234567890abcdef"
        self.assertTrue(any("resembles a credential" in error for error in validator.validate_packet(valued)))

    def test_requires_packet_shape(self) -> None:
        self.assertTrue(validator.validate_packet({"provider": "fish", "kind": "voice"}))

    def test_rejects_malformed_nested_packet_shape(self) -> None:
        malformed = packet()
        malformed.pop("capability")
        malformed["timing"] = {"duration_seconds": 0}
        malformed["output"] = {"path": "artifacts/audio/voice.mp3"}
        malformed["rights_and_consent"] = None
        errors = validator.validate_packet(malformed)
        for expected in (
            "missing required fields: capability",
            "timing.duration_seconds",
            "timing.cue_ref",
            "output.owner",
            "output.format",
            "rights_and_consent",
        ):
            self.assertTrue(any(expected in error for error in errors), errors)

    def test_rejects_unknown_or_malformed_blocker(self) -> None:
        blocker = {
            "result": "blocked_report",
            "provider": "unknown",
            "kind": "unknown",
            "reason": "no route",
            "silent_provider_switch": False,
        }
        errors = validator.validate_packet(blocker)
        self.assertTrue(any("missing required fields" in error for error in errors))
        self.assertTrue(any("unknown provider" in error for error in errors))
        self.assertTrue(any("unknown kind" in error for error in errors))

    def test_canonical_example_packets_validate(self) -> None:
        example = Path(__file__).parents[1] / "examples/explainer-audio-packet/example.md"
        match = re.search(r"```yaml\n(.*?)\n```", example.read_text(encoding="utf-8"), re.S)
        self.assertIsNotNone(match)
        payload = yaml.safe_load(match.group(1))
        packets = payload["audio_generation_packets"]
        self.assertEqual(len(packets), 3)
        for item in packets:
            self.assertEqual(validator.validate_packet(item), [], item)


if __name__ == "__main__":
    unittest.main()
