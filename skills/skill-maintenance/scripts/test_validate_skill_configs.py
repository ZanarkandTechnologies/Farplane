from __future__ import annotations

import tempfile
import unittest
import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_skill_configs.py")
SPEC = importlib.util.spec_from_file_location("validate_skill_configs", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class SkillConfigValidationTests(unittest.TestCase):
    def write_config(self, root: Path, skill: str, body: str) -> Path:
        path = root / "skills" / skill / "config.toml"
        path.parent.mkdir(parents=True)
        path.write_text(body, encoding="utf-8")
        return path

    def test_accepts_commit_safe_defaults_profiles_and_providers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_config(
                Path(tmp),
                "audio-generation",
                'schema_version = "0.1.0"\nskill = "audio-generation"\n'
                '[defaults]\nprovider = "fish"\n'
                '[profiles.narrator]\nvoice_alias = "neutral"\n'
                '[providers.fish]\nmodel = "s2.1-pro"\n',
            )
            self.assertEqual(validator.validate_config(path), [])

    def test_rejects_unknown_root_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_config(
                Path(tmp), "video-production",
                'schema_version = "0.1.0"\nskill = "video-production"\noutput = "tmp"\n',
            )
            self.assertTrue(any("unsupported root keys" in error for error in validator.validate_config(path)))

    def test_rejects_nested_credential_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_config(
                Path(tmp), "audio-generation",
                'schema_version = "0.1.0"\nskill = "audio-generation"\n'
                '[providers.fish]\napi_key = "do-not-store"\n',
            )
            self.assertTrue(any("credential-bearing key" in error for error in validator.validate_config(path)))

    def test_rejects_authorization_header_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_config(
                Path(tmp), "audio-generation",
                'schema_version = "0.1.0"\nskill = "audio-generation"\n'
                '[providers.fish]\nauthorization_header = "Bearer hidden"\n',
            )
            self.assertTrue(any("credential-bearing key" in error for error in validator.validate_config(path)))

    def test_rejects_access_key_and_secret_like_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_config(
                Path(tmp), "audio-generation",
                'schema_version = "0.1.0"\nskill = "audio-generation"\n'
                '[providers.fish]\naccess_key = "not-shareable"\n',
            )
            self.assertTrue(any("credential-bearing key" in error for error in validator.validate_config(path)))
            path.write_text(
                'schema_version = "0.1.0"\nskill = "audio-generation"\n'
                '[providers.fish]\nmodel = "sk-test-1234567890abcdef"\n',
                encoding="utf-8",
            )
            self.assertTrue(any("resembles a credential" in error for error in validator.validate_config(path)))

    def test_rejects_skill_directory_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_config(
                Path(tmp), "video-production",
                'schema_version = "0.1.0"\nskill = "wrong-skill"\n',
            )
            self.assertTrue(any("must match owning directory" in error for error in validator.validate_config(path)))

    def test_rejects_non_scalar_leaf(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_config(
                Path(tmp), "video-production",
                'schema_version = "0.1.0"\nskill = "video-production"\n'
                '[defaults]\ncreated_at = 2026-07-15\n',
            )
            self.assertTrue(any("values must be TOML scalars" in error for error in validator.validate_config(path)))


if __name__ == "__main__":
    unittest.main()
