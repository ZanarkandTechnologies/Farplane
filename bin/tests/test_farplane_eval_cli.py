from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "bin" / "farplane.py"
FIXTURE_ROOT = ROOT / "skills" / "eval" / "tests" / "fixtures" / "promptfoo-skill-eval"


class FarplaneEvalCliTests(unittest.TestCase):
    def run_cli(self, *args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_init_writes_non_secret_project_profile(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project_root = Path(temp)
            profile = project_root / ".farplane" / "evals" / "promptfoo-profile.json"
            result = self.run_cli("eval", "init", cwd=project_root)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(str(profile), result.stdout)
            payload = json.loads(profile.read_text(encoding="utf-8"))
            self.assertEqual(payload["provider"], "openai:codex-sdk")
            self.assertTrue(payload["config"]["enable_streaming"])
            self.assertNotIn("api_key", payload["config"])

    def test_promptfoo_skill_dry_run_uses_project_profile_and_office_runs(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project_root = Path(temp)
            skill_root = project_root / "skills" / "handoff-preparer"
            shutil.copytree(FIXTURE_ROOT / "handoff-preparer", skill_root)
            init = self.run_cli("eval", "init", cwd=project_root)
            self.assertEqual(init.returncode, 0, init.stderr)

            result = self.run_cli(
                "eval",
                "promptfoo",
                "--skill",
                "handoff-preparer",
                "--label",
                "cli-dry-run",
                "--dry-run",
                cwd=project_root,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            summaries = list((project_root / ".farplane" / "evals" / "runs").glob("*/summary.json"))
            self.assertEqual(len(summaries), 1)
            summary = json.loads(summaries[0].read_text(encoding="utf-8"))
            self.assertEqual(summary["runner"], "promptfoo")
            self.assertTrue(summary["dry_run"])
            self.assertEqual(summary["source_eval_file"], str((skill_root / "evals" / "evals.json").resolve()))

    def test_promptfoo_requires_an_initialized_profile(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project_root = Path(temp)
            skill_root = project_root / "skills" / "handoff-preparer"
            shutil.copytree(FIXTURE_ROOT / "handoff-preparer", skill_root)

            result = self.run_cli(
                "eval",
                "promptfoo",
                "--skill",
                "handoff-preparer",
                "--label",
                "missing-profile",
                cwd=project_root,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("farplane eval init", result.stderr)


if __name__ == "__main__":
    unittest.main()
