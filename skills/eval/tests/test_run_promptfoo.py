#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "run_promptfoo.py"
SPEC = importlib.util.spec_from_file_location("eval_run_promptfoo", SCRIPT_PATH)
runner = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["eval_run_promptfoo"] = runner
SPEC.loader.exec_module(runner)

FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "promptfoo-skill-eval"
SKILL_ROOT = FIXTURE_ROOT / "handoff-preparer"
EVAL_FILE = SKILL_ROOT / "evals" / "evals.json"
PROFILE_FILE = FIXTURE_ROOT / "profile.json"


def raw_export(candidate_pass: bool = True, baseline_pass: bool = False) -> dict:
    def row(label: str, passed: bool) -> dict:
        return {
            "provider": {"id": "openai:codex-sdk", "label": label},
            "success": passed,
            "score": 1 if passed else 0,
            "response": {
                "output": f"{label} output",
                "latencyMs": 25,
                "tokenUsage": {"total": 12},
                "metadata": {"skillCalls": [{"name": "handoff-preparer"}]} if label == "candidate" else {},
            },
            "gradingResult": {
                "pass": passed,
                "reason": f"{label} reason",
                "componentResults": [{"pass": passed, "assertion": {"type": "skill-used"}}],
            },
        }

    return {"version": 3, "results": {"results": [row("candidate", candidate_pass), row("baseline", baseline_pass)]}}


class PromptfooAdapterTests(unittest.TestCase):
    def test_manifest_normalizes_string_and_integer_ids_and_expectations(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "evals.json"
            path.write_text(
                json.dumps(
                    {
                        "skill_name": "sample-skill",
                        "evals": [
                            {"id": "case-a", "prompt": "A", "expected_output": "A out", "files": [], "assertions": ["A check"]},
                            {"id": 2, "prompt": "B", "expected_output": "B out", "files": [], "expectations": ["B check"]},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            manifest = runner.load_manifest(path)

        self.assertEqual([case["id"] for case in manifest["evals"]], ["case-a", "2"])
        self.assertEqual(manifest["evals"][1]["assertions"], ["B check"])
        self.assertNotIn("expectations", manifest["evals"][1])

    def test_manifest_rejects_ids_that_collide_after_normalization(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "evals.json"
            path.write_text(
                json.dumps(
                    {
                        "skill_name": "sample-skill",
                        "evals": [
                            {"id": 1, "prompt": "A", "expected_output": "A out"},
                            {"id": "1", "prompt": "B", "expected_output": "B out"},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(runner.AdapterError, "duplicate eval id"):
                runner.load_manifest(path)

    def test_resolve_under_rejects_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "root"
            root.mkdir()
            outside = Path(temp) / "outside.txt"
            outside.write_text("secret", encoding="utf-8")
            with self.assertRaisesRegex(runner.AdapterError, "escapes"):
                runner.resolve_under(root, "../outside.txt", label="fixture")
            with self.assertRaisesRegex(runner.AdapterError, "must be relative"):
                runner.resolve_under(root, str(outside), label="fixture")

    def test_profile_requires_streaming_skill_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "profile.json"
            path.write_text(json.dumps({"provider": "openai:codex-sdk", "config": {}}), encoding="utf-8")
            with self.assertRaisesRegex(runner.AdapterError, "enable_streaming"):
                runner.load_profile(path)

    def test_default_runs_dir_honors_office_root_override(self) -> None:
        with tempfile.TemporaryDirectory() as temp, mock.patch.dict(
            runner.os.environ, {"FARPLANE_EVALS_ROOT": temp}
        ):
            self.assertEqual(runner.default_office_runs_dir(), Path(temp) / "runs")

    def test_workspace_materialization_isolated_and_source_safe(self) -> None:
        manifest = runner.load_manifest(EVAL_FILE)
        case = manifest["evals"][0]
        source_before = runner.snapshot_tree(SKILL_ROOT)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            candidate = root / "candidate"
            baseline = root / "baseline"
            candidate_fixture = runner.materialize_workspace(
                skill_root=SKILL_ROOT,
                case=case,
                destination=candidate,
                installed_skill=SKILL_ROOT,
                skill_name=manifest["skill_name"],
            )
            baseline_fixture = runner.materialize_workspace(
                skill_root=SKILL_ROOT,
                case=case,
                destination=baseline,
                installed_skill=None,
                skill_name=manifest["skill_name"],
            )

            self.assertEqual(candidate_fixture, baseline_fixture)
            self.assertTrue((candidate / ".agents" / "skills" / "handoff-preparer" / "SKILL.md").exists())
            self.assertFalse((candidate / ".agents" / "skills" / "handoff-preparer" / "evals").exists())
            self.assertFalse((baseline / ".agents").exists())
            (candidate / "brief.txt").write_text("changed", encoding="utf-8")
            self.assertNotEqual((candidate / "brief.txt").read_text(), (baseline / "brief.txt").read_text())

        self.assertEqual(source_before, runner.snapshot_tree(SKILL_ROOT))

    def test_provider_configs_have_parity_except_working_dir_and_label(self) -> None:
        manifest = runner.load_manifest(EVAL_FILE)
        profile = runner.load_profile(PROFILE_FILE)
        config = runner.build_promptfoo_config(
            skill_name=manifest["skill_name"],
            case=manifest["evals"][0],
            profile=profile,
            candidate_dir=Path("/tmp/candidate"),
            baseline_dir=Path("/tmp/baseline"),
            grader_dir=Path("/tmp/grader"),
        )
        candidate, baseline = config["providers"]
        candidate_config = dict(candidate.pop("config"))
        baseline_config = dict(baseline.pop("config"))
        self.assertNotEqual(candidate.pop("label"), baseline.pop("label"))
        self.assertNotEqual(candidate_config.pop("working_dir"), baseline_config.pop("working_dir"))
        self.assertEqual(candidate, baseline)
        self.assertEqual(candidate_config, baseline_config)
        self.assertEqual(config["tests"][0]["assert"][0]["type"], "skill-used")
        self.assertEqual(config["tests"][0]["assert"][1]["type"], "llm-rubric")

    def test_export_normalization_preserves_rows_and_deltas(self) -> None:
        normalized = runner.normalize_export(
            raw_export(),
            candidate_delta={"created": ["handoff.txt"], "modified": [], "deleted": []},
            baseline_delta={"created": [], "modified": [], "deleted": []},
        )
        self.assertTrue(normalized["candidate"]["pass"])
        self.assertFalse(normalized["baseline"]["pass"])
        self.assertEqual(normalized["comparison"]["pass_delta"], 1)
        self.assertEqual(normalized["candidate"]["workspace_delta"]["created"], ["handoff.txt"])
        self.assertEqual(normalized["candidate"]["assertions"][0]["assertion"]["type"], "skill-used")

    def test_promptfoo_exit_100_is_a_completed_comparison(self) -> None:
        manifest = runner.load_manifest(EVAL_FILE)
        profile = runner.load_profile(PROFILE_FILE)
        source_before = runner.snapshot_tree(SKILL_ROOT)

        def fake_run(command, **_kwargs):
            raw_path = Path(command[command.index("--output") + 1])
            raw_path.write_text(json.dumps(raw_export()), encoding="utf-8")
            return subprocess.CompletedProcess(command, 100, stdout="completed", stderr="")

        with tempfile.TemporaryDirectory() as temp, mock.patch.object(runner.subprocess, "run", side_effect=fake_run):
            result = runner.run_case(
                case=manifest["evals"][0],
                skill_name=manifest["skill_name"],
                skill_root=SKILL_ROOT,
                candidate_skill=SKILL_ROOT,
                baseline_skill=None,
                profile=profile,
                task_dir=Path(temp) / "task",
                promptfoo_version="0.122.0",
                codex_sdk_version="0.148.0",
                dry_run=False,
            )

        self.assertEqual(result["promptfoo_exit_code"], 100)
        self.assertEqual(result["comparison"]["pass_delta"], 1)
        self.assertEqual(source_before, runner.snapshot_tree(SKILL_ROOT))

    def test_cli_dry_run_emits_summary_without_duplicate_suite(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            runs_dir = Path(temp) / "runs"
            exit_code = runner.main(
                [
                    "--eval-file",
                    str(EVAL_FILE),
                    "--provider-profile",
                    str(PROFILE_FILE),
                    "--runs-dir",
                    str(runs_dir),
                    "--label",
                    "unit",
                    "--dry-run",
                ]
            )
            summaries = list(runs_dir.glob("*/summary.json"))
            self.assertEqual(exit_code, 0)
            self.assertEqual(len(summaries), 1)
            summary = json.loads(summaries[0].read_text(encoding="utf-8"))
            config_path = Path(summary["results"][0]["config"])
            config = json.loads(config_path.read_text(encoding="utf-8"))
            self.assertFalse((runs_dir / "index.json").exists())

        self.assertTrue(summary["source_hashes_unchanged"])
        self.assertIsNone(summary["candidate_gate_passed"])
        self.assertEqual(summary["results"][0]["eval_id"], "handoff_ready_01")
        self.assertEqual(len(config["tests"]), 1)
        self.assertEqual(config["tests"][0]["vars"]["request"], runner.load_manifest(EVAL_FILE)["evals"][0]["prompt"])

    def test_completed_cli_run_projects_into_office_contract_and_index(self) -> None:
        def fake_run(command, **_kwargs):
            raw_path = Path(command[command.index("--output") + 1])
            raw_path.write_text(json.dumps(raw_export()), encoding="utf-8")
            return subprocess.CompletedProcess(command, 100, stdout="completed", stderr="")

        with tempfile.TemporaryDirectory() as temp, mock.patch.object(runner.subprocess, "run", side_effect=fake_run):
            runs_dir = Path(temp) / "runs"
            exit_code = runner.main(
                [
                    "--eval-file",
                    str(EVAL_FILE),
                    "--provider-profile",
                    str(PROFILE_FILE),
                    "--runs-dir",
                    str(runs_dir),
                    "--label",
                    "office-proof",
                ]
            )
            index = json.loads((runs_dir / "index.json").read_text(encoding="utf-8"))
            job_dir = runs_dir / index[0]["job_id"]
            summary = json.loads((job_dir / "summary.json").read_text(encoding="utf-8"))
            detail = json.loads((job_dir / "tasks" / "handoff_ready_01.json").read_text(encoding="utf-8"))
            comparison = json.loads((job_dir / "tasks" / "handoff_ready_01" / "comparison.json").read_text(encoding="utf-8"))
            candidate_answer = (job_dir / "tasks" / "handoff_ready_01" / "candidate" / "outputs" / "agent_answer.txt").read_text(encoding="utf-8")

        self.assertEqual(exit_code, 0)
        self.assertEqual(index[0]["label"], "office-proof")
        self.assertEqual(summary["harness"], "promptfoo")
        self.assertEqual(summary["task_count"], 1)
        self.assertEqual(summary["pass_rate"], 1.0)
        self.assertEqual(summary["tasks"][0]["verdict"], "A")
        self.assertEqual(detail["comparison"]["delta"], "candidate_wins")
        self.assertEqual(comparison, detail["comparison"])
        self.assertTrue(detail["comparison"]["skill_value"])
        self.assertEqual(detail["candidate"]["grading"]["summary"], {"failed": 0, "passed": 1, "total": 1})
        self.assertEqual(candidate_answer, "candidate output")


if __name__ == "__main__":
    unittest.main()
