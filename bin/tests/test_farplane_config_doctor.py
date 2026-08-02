from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

import farplane_config_doctor


class FarplaneConfigDoctorTests(unittest.TestCase):
    def test_parse_doppler_names_from_table(self) -> None:
        output = "\n".join(
            [
                "┌──────────────┐",
                "│ NAME         │",
                "├──────────────┤",
                "│ REF_API_KEY  │",
                "│ NOTION_TOKEN │",
                "└──────────────┘",
            ]
        )

        self.assertEqual(
            farplane_config_doctor.parse_doppler_names(output),
            {"REF_API_KEY", "NOTION_TOKEN"},
        )

    def test_reports_doppler_as_effective_source_without_values(self) -> None:
        def runner(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
            if command == ["doppler", "configure", "get", "project", "--plain"]:
                return subprocess.CompletedProcess(command, 0, "farplane\n", "")
            if command == ["doppler", "configure", "get", "config", "--plain"]:
                return subprocess.CompletedProcess(command, 0, "dev_personal\n", "")
            if command == ["doppler", "secrets", "--only-names"]:
                return subprocess.CompletedProcess(
                    command,
                    0,
                    "\n".join(
                        [
                            "┌────────────────┐",
                            "│ NAME           │",
                            "├────────────────┤",
                            "│ REF_API_KEY    │",
                            "│ NOTION_TOKEN │",
                            "└────────────────┘",
                        ]
                    ),
                    "",
                )
            return subprocess.CompletedProcess(command, 1, "", "unexpected")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane_home = root / "farplane"
            codex_home = root / "codex"
            project_root = root / "project"
            farplane_home.mkdir()
            codex_home.mkdir()
            project_root.mkdir()
            (project_root / "doppler.yaml").write_text(
                "setup:\n  - project: farplane\n    config: dev_personal\n",
                encoding="utf-8",
            )

            payload = farplane_config_doctor.config_doctor(
                codex_home=codex_home,
                farplane_home=farplane_home,
                project_root=project_root,
                process_env={},
                doppler_runner=runner,
            )

        ref_row = next(row for row in payload["keys"] if row["key"] == "REF_API_KEY")
        notion_row = next(row for row in payload["keys"] if row["key"] == "NOTION_TOKEN")
        self.assertEqual(ref_row["effectiveSource"], "doppler")
        self.assertEqual(notion_row["effectiveSource"], "doppler")
        self.assertEqual(payload["doppler"]["project"], "farplane")
        self.assertEqual(payload["doppler"]["config"], "dev_personal")
        self.assertEqual(payload["doppler"]["secretNameCount"], 2)
        self.assertNotIn("missing_required_secret", json.dumps(payload))
        self.assertNotIn("secret-value", json.dumps(payload))

    def test_ignores_and_reports_private_toml_secrets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane_home = root / "farplane"
            codex_home = root / "codex"
            project_root = root / "project"
            farplane_home.mkdir()
            codex_home.mkdir()
            project_root.mkdir()
            (farplane_home / "config.toml").write_text(
                "[integrations]\nref_api_key = \"local-ref-secret\"\nnotion_token = \"local-notion-secret\"\n",
                encoding="utf-8",
            )
            (codex_home / "config.toml").write_text(
                "[env]\nREF_API_KEY = \"rendered-ref-secret\"\n",
                encoding="utf-8",
            )

            payload = farplane_config_doctor.config_doctor(
                codex_home=codex_home,
                farplane_home=farplane_home,
                project_root=project_root,
                process_env={"REF_API_KEY": "process-ref-secret"},
            )

        ref_row = next(row for row in payload["keys"] if row["key"] == "REF_API_KEY")
        notion_row = next(row for row in payload["keys"] if row["key"] == "NOTION_TOKEN")
        self.assertEqual(ref_row["effectiveSource"], "process_env")
        self.assertEqual(
            ref_row["sources"],
            ["process_env", "~/.codex/config.toml"],
        )
        self.assertIsNone(notion_row["effectiveSource"])
        self.assertEqual(
            payload["prohibitedPrivateSecretKeys"],
            ["NOTION_TOKEN", "REF_API_KEY"],
        )
        self.assertEqual(
            payload["prohibitedPrivateSecretFields"],
            ["integrations.notion_token", "integrations.ref_api_key"],
        )
        self.assertIn("secret_in_farplane_config:NOTION_TOKEN", payload["issues"])
        encoded = json.dumps(payload)
        self.assertNotIn("process-ref-secret", encoded)
        self.assertNotIn("local-ref-secret", encoded)
        self.assertNotIn("local-notion-secret", encoded)
        self.assertNotIn("rendered-ref-secret", encoded)

    def test_flags_open_private_config_and_tracked_secret_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane_home = root / "farplane"
            codex_home = root / "codex"
            project_root = root / "project"
            farplane_home.mkdir()
            codex_home.mkdir()
            project_root.mkdir()
            config_path = farplane_home / "config.toml"
            config_path.write_text(
                "[integrations]\nref_api_key = \"local-ref-secret\"\nnotion_token = \"local-notion-secret\"\n",
                encoding="utf-8",
            )
            config_path.chmod(0o644)
            (project_root / "leaky.toml").write_text(
                'SERVICE_API_KEY = "real-looking-secret-value"\n',
                encoding="utf-8",
            )
            (project_root / "setup.md").write_text(
                'export MESHY_API_KEY="msy_PASTE_KEY_HERE"\n',
                encoding="utf-8",
            )

            payload = farplane_config_doctor.config_doctor(
                codex_home=codex_home,
                farplane_home=farplane_home,
                project_root=project_root,
                process_env={},
            )

        self.assertFalse(payload["ok"])
        self.assertTrue(any("config_permissions_too_open" in issue for issue in payload["issues"]))
        self.assertEqual(
            payload["trackedSecretCandidates"],
            [{"path": "leaky.toml", "line": 1, "key": "SERVICE_API_KEY"}],
        )
        self.assertNotIn("real-looking-secret-value", json.dumps(payload))

    def test_reports_invalid_private_toml_without_echoing_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane_home = root / "farplane"
            codex_home = root / "codex"
            project_root = root / "project"
            farplane_home.mkdir()
            codex_home.mkdir()
            project_root.mkdir()
            (farplane_home / "config.toml").write_text(
                'env.OPENROUTER_API_KEY = null\n', encoding="utf-8"
            )

            payload = farplane_config_doctor.config_doctor(
                codex_home=codex_home,
                farplane_home=farplane_home,
                project_root=project_root,
                process_env={},
            )

        self.assertTrue(any(issue.startswith("invalid_toml:") for issue in payload["issues"]))
        self.assertNotIn("OPENROUTER_API_KEY", json.dumps(payload))


if __name__ == "__main__":
    unittest.main()
