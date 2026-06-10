#!/usr/bin/env python3
"""Tests for harness-native eval runner."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "run_evals.py"
SPEC = importlib.util.spec_from_file_location("eval_run_evals", SCRIPT_PATH)
assert SPEC is not None
runner = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["eval_run_evals"] = runner
SPEC.loader.exec_module(runner)


def write_fake_cli(path: Path) -> None:
    path.write_text(
        textwrap.dedent(
            """\
            #!/usr/bin/env python3
            from __future__ import annotations

            import argparse
            import json
            from pathlib import Path

            parser = argparse.ArgumentParser()
            parser.add_argument("--prompt-file", required=True)
            parser.add_argument("--output-file", required=True)
            args = parser.parse_args()
            prompt = Path(args.prompt_file).read_text()
            output = Path(args.output_file)
            if "Assistant answer:" in prompt:
                output.write_text(json.dumps({
                    "verdict": "A",
                    "pass": True,
                    "rubric": {
                        "groundedness": "A",
                        "completeness": "A",
                        "usefulness": "A",
                        "repeatability": "A",
                        "length_balance": "A"
                    },
                    "reference_point_results": [
                        {"reference_point": "Names proof", "met": True, "reason": "present"}
                    ],
                    "reason": "all required points covered"
                }))
            else:
                output.write_text("The answer names proof, evidence, and the next step.")
            """
        )
    )
    path.chmod(0o755)


def write_tasks(path: Path) -> None:
    path.write_text(
        json.dumps(
            [
                {
                    "id": "proof_01",
                    "title": "Proof task",
                    "query": "Explain proof discipline.",
                    "reference_points": [
                        "Names proof",
                        "Names evidence",
                    ],
                    "tags": ["proof"],
                    "notes": "synthetic task",
                }
            ]
        )
    )


class EvalRunnerTests(unittest.TestCase):
    def test_init_creates_codex_eval_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_dir = root / ".farplane" / "evals"
            code = runner.main(["init", "--harness", "codex", "--target-root", str(root)])
            self.assertEqual(code, 0)
            self.assertTrue((eval_dir / "run_evals.py").exists())
            self.assertTrue((eval_dir / "config.json").exists())
            self.assertTrue((eval_dir / "contexts" / "agi-toy-shop.md").exists())
            self.assertTrue((eval_dir / "viewer.html").exists())
            self.assertTrue((eval_dir / "viewer-react" / "package.json").exists())
            self.assertTrue((eval_dir / "viewer-react" / "src" / "App.tsx").exists())
            self.assertTrue((eval_dir / "tasks" / "harness_tasks.json").exists())
            self.assertTrue((eval_dir / "prompts" / "judge.md").exists())
            self.assertTrue((eval_dir / "README.md").exists())

    def test_load_tasks_requires_string_reference_points(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            path.write_text(
                json.dumps(
                    [
                        {
                            "id": "bad",
                            "title": "Bad",
                            "query": "Bad",
                            "reference_points": [{"match": "not allowed"}],
                        }
                    ]
                )
            )
            with self.assertRaises(runner.EvalError):
                runner.load_tasks(path)

    def test_only_a_verdict_passes(self) -> None:
        self.assertTrue(runner.normalize_judge({"verdict": "A"})["pass"])
        self.assertFalse(runner.normalize_judge({"verdict": "B"})["pass"])
        self.assertFalse(runner.normalize_judge({"verdict": "C"})["pass"])
        self.assertFalse(runner.normalize_judge({"verdict": "D"})["pass"])

    def test_context_block_renders_separately_from_query(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            write_tasks(path)
            task = runner.load_tasks(path, default_context="AGI Toy Shop fixture context.")[0]

        rendered = runner.render_template("{context_block}User request:\n{query}", task)

        self.assertIn("Context:\nAGI Toy Shop fixture context.\n\n", rendered)
        self.assertIn("User request:\nExplain proof discipline.", rendered)
        self.assertEqual(task.query, "Explain proof discipline.")

    def test_task_context_overrides_default_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            path.write_text(
                json.dumps(
                    [
                        {
                            "id": "real_repo_01",
                            "title": "Real repo task",
                            "context": "",
                            "query": "Inspect the current repo eval setup.",
                            "reference_points": ["Does not use toy context"],
                        }
                    ]
                )
            )
            task = runner.load_tasks(path, default_context="AGI Toy Shop fixture context.")[0]

        self.assertEqual(task.context, "")

    def test_eval_config_loads_default_context_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            eval_dir = Path(tmp) / ".farplane" / "evals"
            (eval_dir / "contexts").mkdir(parents=True)
            (eval_dir / "config.json").write_text(json.dumps({"default_context_file": "contexts/shop.md"}))
            (eval_dir / "contexts" / "shop.md").write_text("Shop fixture context.")

            config = runner.load_eval_config(eval_dir)

        self.assertEqual(config.default_context, "Shop fixture context.")
        self.assertEqual(config.default_context_file, "contexts/shop.md")

    def test_custom_command_runs_agent_and_judge(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_dir = root / "evals"
            fake_cli = root / "fake_cli.py"
            tasks = eval_dir / "tasks" / "harness_tasks.json"
            (eval_dir / "prompts").mkdir(parents=True)
            tasks.parent.mkdir(parents=True)
            write_fake_cli(fake_cli)
            write_tasks(tasks)
            (eval_dir / "prompts" / "agent.md").write_text("Task: {query}\n{task_json}\n")
            (eval_dir / "prompts" / "judge.md").write_text("Task: {task_json}\nAssistant answer:\n{answer}\n")

            template = f"{sys.executable} {fake_cli} --prompt-file {{prompt_file}} --output-file {{output_file}}"
            code = runner.main(
                [
                    "run",
                    "--harness",
                    "custom",
                    "--eval-dir",
                    str(eval_dir),
                    "--target-root",
                    str(root),
                    "--tasks",
                    str(tasks),
                    "--label",
                    "unit",
                    "--agent-command-template",
                    template,
                    "--judge-command-template",
                    template,
                ]
            )

            self.assertEqual(code, 0)
            run_dirs = list((eval_dir / "runs").glob("*-unit"))
            self.assertEqual(len(run_dirs), 1)
            summary = json.loads((run_dirs[0] / "summary.json").read_text())
            self.assertEqual(summary["pass_rate"], 1.0)
            self.assertEqual(summary["verdict_counts"], {"A": 1})
            self.assertTrue((run_dirs[0] / "tasks" / "proof_01.json").exists())

    def test_default_suite_loads_harness_task_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_dir = root / "evals"
            fake_cli = root / "fake_cli.py"
            (eval_dir / "prompts").mkdir(parents=True)
            (eval_dir / "tasks").mkdir(parents=True)
            write_fake_cli(fake_cli)
            write_tasks(eval_dir / "tasks" / "harness_tasks.json")
            (eval_dir / "prompts" / "agent.md").write_text("Task: {query}\n{task_json}\n")
            (eval_dir / "prompts" / "judge.md").write_text("Task: {task_json}\nAssistant answer:\n{answer}\n")

            template = f"{sys.executable} {fake_cli} --prompt-file {{prompt_file}} --output-file {{output_file}}"
            code = runner.main(
                [
                    "run",
                    "--harness",
                    "custom",
                    "--eval-dir",
                    str(eval_dir),
                    "--target-root",
                    str(root),
                    "--label",
                    "suite",
                    "--agent-command-template",
                    template,
                    "--judge-command-template",
                    template,
                ]
            )

            self.assertEqual(code, 0)
            run_dir = next((eval_dir / "runs").glob("*-suite"))
            summary = json.loads((run_dir / "summary.json").read_text())
            self.assertEqual(summary["suite"], "harness")
            self.assertEqual(summary["task_count"], 1)
            self.assertEqual(summary["verdict_counts"], {"A": 1})

    def test_skills_suite_discovers_skill_eval_task_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_dir = root / "evals"
            fake_cli = root / "fake_cli.py"
            skill_eval = root / "skills" / "advise" / "eval_task.json"
            (eval_dir / "prompts").mkdir(parents=True)
            skill_eval.parent.mkdir(parents=True)
            write_fake_cli(fake_cli)
            write_tasks(skill_eval)
            (eval_dir / "prompts" / "agent.md").write_text("Task: {query}\n{task_json}\n")
            (eval_dir / "prompts" / "judge.md").write_text("Task: {task_json}\nAssistant answer:\n{answer}\n")

            template = f"{sys.executable} {fake_cli} --prompt-file {{prompt_file}} --output-file {{output_file}}"
            code = runner.main(
                [
                    "run",
                    "--harness",
                    "custom",
                    "--eval-dir",
                    str(eval_dir),
                    "--target-root",
                    str(root),
                    "--suite",
                    "skills",
                    "--label",
                    "skill-suite",
                    "--agent-command-template",
                    template,
                    "--judge-command-template",
                    template,
                ]
            )

            self.assertEqual(code, 0)
            run_dir = next((eval_dir / "runs").glob("*-skill-suite"))
            summary = json.loads((run_dir / "summary.json").read_text())
            self.assertEqual(summary["suite"], "skills")
            self.assertEqual(summary["task_count"], 1)
            self.assertEqual([Path(path).resolve() for path in summary["task_files"]], [skill_eval.resolve()])
            self.assertEqual(summary["verdict_counts"], {"A": 1})

    def test_status_reports_missing_and_ready_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_dir = root / ".farplane" / "evals"
            missing_code = runner.main(["status", "--harness", "codex", "--target-root", str(root)])
            self.assertEqual(missing_code, 1)
            init_code = runner.main(["init", "--harness", "codex", "--target-root", str(root)])
            self.assertEqual(init_code, 0)
            ready_code = runner.main(["status", "--harness", "codex", "--target-root", str(root)])
            self.assertEqual(ready_code, 0)


if __name__ == "__main__":
    unittest.main()
