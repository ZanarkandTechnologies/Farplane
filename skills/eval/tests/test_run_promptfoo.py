#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import shutil
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
    def test_manifest_rejects_legacy_integer_ids_and_expectations_alias(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample-skill" / "evals" / "evals.json"
            path.parent.mkdir(parents=True)
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
            with self.assertRaisesRegex(runner.AdapterError, "eval contract invalid"):
                runner.load_manifest(path)

    def test_manifest_rejects_duplicate_string_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample-skill" / "evals" / "evals.json"
            path.parent.mkdir(parents=True)
            path.write_text(
                json.dumps(
                    {
                        "skill_name": "sample-skill",
                        "evals": [
                            {"id": "case-a", "prompt": "A", "expected_output": "A out"},
                            {"id": "case-a", "prompt": "B", "expected_output": "B out"},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(runner.AdapterError, "eval IDs must be unique"):
                runner.load_manifest(path)

    def test_manifest_preflight_rejects_invalid_metadata_before_workspace_creation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample-skill" / "evals" / "evals.json"
            path.parent.mkdir(parents=True)
            path.write_text(
                json.dumps(
                    {
                        "skill_name": "sample-skill",
                        "evals": [
                            {
                                "id": "case-a",
                                "prompt": "A",
                                "expected_output": "A out",
                                "metadata": {"farplane": {"workspace_fixture": "../escape"}},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(runner.AdapterError, "workspace paths must stay relative"):
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

    def test_workspace_setup_builds_a_committable_repo(self) -> None:
        manifest = runner.load_manifest(EVAL_FILE)
        case = json.loads(json.dumps(manifest["evals"][0]))
        case["metadata"] = {"farplane": {"workspace_setup": "setup.py"}}
        with tempfile.TemporaryDirectory() as temp:
            skill_root = Path(temp) / "skill"
            shutil.copytree(SKILL_ROOT, skill_root)
            (skill_root / "setup.py").write_text(
                "import subprocess, sys\n"
                "subprocess.run(['git', 'init', '-q'], check=True)\n"
                "open('case.txt', 'w').write(sys.argv[1])\n",
                encoding="utf-8",
            )
            workspaces = {label: Path(temp) / label for label in ("candidate", "baseline", "grader")}
            fixtures = [
                runner.materialize_workspace(skill_root=skill_root, case=case, destination=workspaces[label],
                                             installed_skill=None, skill_name=manifest["skill_name"])
                for label in ("candidate", "baseline")
            ]
            config = runner.build_promptfoo_config(
                skill_name=manifest["skill_name"], case=case, profile=runner.load_profile(PROFILE_FILE),
                candidate_dir=workspaces["candidate"], baseline_dir=workspaces["baseline"], grader_dir=workspaces["grader"],
            )

            self.assertEqual(fixtures[0], fixtures[1])
            self.assertEqual((workspaces["candidate"] / "case.txt").read_text(), case["id"])
            for provider in config["providers"]:
                git_dir = (workspaces[provider["label"]] / ".git").resolve()
                self.assertEqual(provider["config"]["additional_directories"], [str(git_dir)])

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
        candidate_env = candidate_config.pop("cli_env")
        baseline_env = baseline_config.pop("cli_env")
        self.assertEqual(candidate_env.keys(), baseline_env.keys())
        self.assertNotEqual(candidate_env["HOME"], baseline_env["HOME"])
        self.assertEqual(candidate, baseline)
        self.assertEqual(candidate_config, baseline_config)
        self.assertEqual(config["tests"][0]["assert"][0]["type"], "skill-used")
        self.assertEqual(config["tests"][0]["assert"][1]["type"], "llm-rubric")

    def test_claude_route_runs_on_the_subscription_with_project_settings_only(self) -> None:
        manifest = runner.load_manifest(EVAL_FILE)
        claude = Path(__file__).resolve().parents[1] / "templates" / "promptfoo-profile.claude.json"
        profile = runner.load_profile(claude)
        self.assertEqual(runner.skills_dir(profile), ".claude/skills")
        config = runner.build_promptfoo_config(
            skill_name=manifest["skill_name"], case=manifest["evals"][0], profile=profile,
            candidate_dir=Path("/tmp/candidate"), baseline_dir=Path("/tmp/baseline"),
            grader_dir=Path("/tmp/grader"),
        )
        candidate, baseline = (dict(provider["config"]) for provider in config["providers"])
        self.assertNotEqual(candidate.pop("working_dir"), baseline.pop("working_dir"))
        self.assertEqual(candidate, baseline)
        self.assertEqual(candidate["setting_sources"], ["project"])
        self.assertIs(candidate["apiKeyRequired"], False)
        grader = config["tests"][0]["assert"][1]["provider"]["config"]
        self.assertEqual((grader["setting_sources"], grader["custom_allowed_tools"]), ([], []))
        env = runner.subscription_env({"ANTHROPIC_API_KEY": "paid", "PATH": "/bin"})
        self.assertEqual(env, {"PATH": "/bin"})
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "profile.json"
            path.write_text(json.dumps({"provider": runner.CLAUDE_PROVIDER, "config": {}}), encoding="utf-8")
            with self.assertRaises(runner.AdapterError):
                runner.load_profile(path)

    def test_every_agent_runs_with_its_own_home_not_the_operators(self) -> None:
        manifest = runner.load_manifest(EVAL_FILE)
        profile = runner.load_profile(PROFILE_FILE)
        profile["config"]["cli_env"] = {"CODEX_HOME": str(Path.home() / ".codex"), "HTTPS_PROXY": "http://proxy"}
        root = Path("/tmp/eval-root")
        config = runner.build_promptfoo_config(
            skill_name=manifest["skill_name"],
            case=manifest["evals"][0],
            profile=profile,
            candidate_dir=root / "candidate",
            baseline_dir=root / "baseline",
            grader_dir=root / "grader",
        )
        grader = config["tests"][0]["assert"][1]["provider"]["config"]
        agents = {provider["label"]: provider["config"] for provider in config["providers"]} | {"grader": grader}
        for label, agent in agents.items():
            home = Path(agent["cli_env"]["HOME"])
            self.assertEqual(home, root.resolve() / f"{label}-home")
            self.assertEqual(agent["cli_env"]["CODEX_HOME"], str(home / ".codex"))
            self.assertEqual(agent["cli_env"]["HTTPS_PROXY"], "http://proxy")
            self.assertNotIn(str(Path.home()), agent["cli_env"]["HOME"])

    def test_agent_home_is_empty_but_keeps_credentials_in_place(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            real = Path(temp) / "real-codex"
            real.mkdir()
            (real / "auth.json").write_text("{}", encoding="utf-8")
            (real / "AGENTS.md").write_text("operator rules", encoding="utf-8")
            workspace = Path(temp) / "candidate"
            workspace.mkdir()
            with mock.patch.dict(runner.os.environ, {"CODEX_HOME": str(real)}):
                home = runner.make_agent_home(workspace)
            codex_home = home / ".codex"
            self.assertEqual(sorted(path.name for path in codex_home.iterdir()), ["auth.json"])
            self.assertEqual((codex_home / "auth.json").resolve(), (real / "auth.json").resolve())
            self.assertEqual(home, runner.agent_home(workspace))

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

    def skill_read_row(self, aggregated_output: str) -> dict:
        command = "/bin/zsh -lc \"sed -n '1,240p' .agents/skills/handoff-preparer/SKILL.md && sed -n 1p notes.md\""
        return {
            "provider": {"id": "openai:codex-sdk", "label": "candidate"},
            "success": False,
            "score": 0.4,
            "response": {
                "output": "candidate output",
                "metadata": {"attemptedSkillCalls": [{"name": "handoff-preparer"}]},
                "raw": json.dumps(
                    {
                        "items": [
                            {
                                "type": "command_execution",
                                "command": command,
                                "aggregated_output": aggregated_output,
                                "exit_code": 1,
                                "status": "failed",
                            }
                        ]
                    }
                ),
            },
            "gradingResult": {
                "pass": False,
                "componentResults": [
                    {
                        "pass": False,
                        "score": 0,
                        "reason": "Missing required skill(s): handoff-preparer.",
                        "assertion": {"type": "skill-used", "value": "handoff-preparer"},
                    },
                    {"pass": False, "score": 0.8, "assertion": {"type": "llm-rubric"}},
                ],
            },
        }

    def test_skill_read_printed_by_a_failed_chained_command_counts_as_used(self) -> None:
        row = self.skill_read_row("---\nname: handoff-preparer\ndescription: x\n---\nsed: notes.md: No such file\n")
        normalized = runner.normalize_row(row, workspace_delta={})
        skill_used = normalized["assertions"][0]
        self.assertTrue(skill_used["pass"])
        self.assertIn("exit code 1", skill_used["reason"])
        self.assertAlmostEqual(normalized["score"], 0.9)
        self.assertFalse(normalized["pass"])
        self.assertEqual(normalized["skill_used_override"]["skill"], "handoff-preparer")
        self.assertEqual(normalized["metadata"]["skillCalls"][0]["source"], "output-confirmed")
        self.assertFalse(row["gradingResult"]["componentResults"][0]["pass"])

    def test_failed_skill_read_without_printed_frontmatter_stays_failed(self) -> None:
        row = self.skill_read_row("sed: .agents/skills/handoff-preparer/SKILL.md: No such file or directory\n")
        normalized = runner.normalize_row(row, workspace_delta={})
        self.assertFalse(normalized["assertions"][0]["pass"])
        self.assertEqual(normalized["score"], 0.4)
        self.assertNotIn("skill_used_override", normalized)

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
