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
            parser.add_argument("--skill-event", default="")
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
                if args.skill_event:
                    print(json.dumps({
                        "type": "item.completed",
                        "item": {"type": "skill", "name": args.skill_event}
                    }))
                output.write_text("The answer names proof, evidence, and the next step.")
            """
        )
    )
    path.chmod(0o755)


def write_behavior_cli(path: Path) -> None:
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
            parser.add_argument("--skill-event", default="")
            parser.add_argument("--output-kind", choices=["behavior", "planner-json", "text"], default="behavior")
            args = parser.parse_args()
            prompt = Path(args.prompt_file).read_text()
            output = Path(args.output_file)
            if "Assistant answer:" in prompt:
                output.write_text(json.dumps({
                    "verdict": "A",
                    "pass": True,
                    "rubric": {},
                    "reference_point_results": [],
                    "reason": "behavior evidence is complete"
                }))
            else:
                print(json.dumps({"type": "thread.started", "thread_id": "trace-thread"}))
                if args.skill_event:
                    print(json.dumps({"type": "item.completed", "item": {"type": "skill", "name": args.skill_event}}))
                print(json.dumps({
                    "type": "item.completed",
                    "item": {"type": "command_execution", "command": "printf visible", "exit_code": 0, "status": "completed"}
                }))
                print(json.dumps({"type": "turn.completed", "usage": {"input_tokens": 12, "output_tokens": 8}}))
                if args.output_kind == "planner-json":
                    output.write_text(json.dumps({"selected": ["TASK-9001"], "rationale": "highest expected value"}))
                elif args.output_kind == "text":
                    output.write_text("Selected TASK-9001 because it has the highest expected value.")
                else:
                    Path("produced.txt").write_text("visible artifact\\n")
                    output.write_text(json.dumps({
                        "target": "eval behavior trace",
                        "persona": "skill caller",
                        "checkpoints": [{"name": "created_artifact", "status": "done", "evidence": "produced.txt"}],
                        "artifacts": ["produced.txt"],
                        "deviations": [],
                        "verdict": "pass"
                    }))
            """
        )
    )
    path.chmod(0o755)


def reliability_summary(rows: list[dict[str, str]], **overrides: object) -> dict[str, object]:
    summary: dict[str, object] = {
        "harness": "codex",
        "judge_harness": "codex",
        "skill_context": "inline",
        "compare_baseline": False,
        "behavior_trace": True,
        "scopes": ["skills"],
        "task_files": ["/repo/skills/example/evals/evals.json"],
        "task_count": len(rows),
        "tasks": [
            {
                "task_id": row["task_id"],
                "title": row.get("title", row["task_id"]),
                "verdict": row["verdict"],
                "behavior_verdict": row["behavior_verdict"],
            }
            for row in rows
        ],
    }
    summary.update(overrides)
    return summary


def write_tasks(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.parts[-2:] == ("evals", "evals.json"):
        payload = {
            "skill_name": path.parents[1].name,
            "evals": [
                {
                    "id": "proof_01",
                    "prompt": "Explain proof discipline.",
                    "expected_output": "An explanation that names proof and evidence.",
                    "files": [],
                    "assertions": ["Names proof", "Names evidence"],
                    "metadata": {
                        "farplane": {
                            "title": "Proof task",
                            "tags": ["proof"],
                            "notes": "synthetic task",
                        }
                    },
                }
            ],
        }
    else:
        payload = [
            {
                "id": "proof_01",
                "title": "Proof task",
                "query": "Explain proof discipline.",
                "reference_points": ["Names proof", "Names evidence"],
                "tags": ["proof"],
                "notes": "synthetic task",
            }
        ]
    path.write_text(json.dumps(payload))


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
            self.assertFalse((eval_dir / "viewer.html").exists())
            self.assertFalse((eval_dir / "viewer-react").exists())
            self.assertTrue((eval_dir / "tasks" / "harness_tasks.json").exists())
            self.assertTrue((eval_dir / "prompts" / "judge.md").exists())
            self.assertTrue((eval_dir / "README.md").exists())
            self.assertTrue((eval_dir / "tasks" / "agents_md_tasks.json").exists())

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

    def test_load_tasks_accepts_agent_skills_eval_format(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "skills" / "qa" / "evals" / "evals.json"
            path.parent.mkdir(parents=True)
            path.write_text(
                json.dumps(
                    {
                        "skill_name": "qa",
                        "evals": [
                            {
                                "id": 1,
                                "prompt": "Check the UI.",
                                "expected_output": "A proof-backed verdict.",
                                "files": [],
                                "assertions": ["Captures evidence", "Returns a verdict"],
                                "metadata": {
                                    "farplane": {
                                        "title": "Capture proof",
                                        "context": "Toy context",
                                        "tags": ["qa"],
                                        "notes": "Representative row",
                                    }
                                },
                            }
                        ],
                    }
                )
            )

            task = runner.load_tasks(path)[0]

            self.assertEqual(task.id, "1")
            self.assertEqual(task.title, "Capture proof")
            self.assertEqual(task.query, "Check the UI.")
            self.assertEqual(task.reference_points, ("Captures evidence", "Returns a verdict"))
            self.assertEqual(task.context, "Toy context")

    def test_resolve_skill_task_paths_prefers_agent_skills_format(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_dir = root / "skills" / "qa"
            standard = skill_dir / "evals" / "evals.json"
            standard.parent.mkdir(parents=True)
            standard.write_text("{}")
            (skill_dir / "evals/evals.json").write_text("[]")

            self.assertEqual(runner.resolve_skill_task_paths(root), [standard])
            self.assertEqual(runner.normalize_skill_selector("skills/qa/evals/evals.json"), "qa")

    def test_standard_skill_eval_receives_owner_skill_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_path = root / "skills" / "qa" / "evals" / "evals.json"
            eval_path.parent.mkdir(parents=True)
            eval_path.write_text("{}")
            (root / "skills" / "qa" / "SKILL.md").write_text("# QA\n\nCapture evidence.\n")

            context = runner.skill_context_for_task_file(eval_path, root)

            self.assertIn("Skill under evaluation: qa", context)
            self.assertIn("Capture evidence.", context)

    def test_standard_skill_eval_rejects_missing_fixture_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "evals.json"
            path.write_text(
                json.dumps(
                    {
                        "skill_name": "qa",
                        "evals": [
                            {
                                "id": 1,
                                "prompt": "Check this file.",
                                "expected_output": "A result.",
                                "files": ["evals/files/input.txt"],
                            }
                        ],
                    }
                )
            )

            with self.assertRaisesRegex(runner.EvalError, "file not found"):
                runner.load_tasks(path, target_root=Path(tmp))

    def test_selected_standard_skill_eval_skips_unrelated_unstaged_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "evals.json"
            path.write_text(
                json.dumps(
                    {
                        "skill_name": "qa",
                        "evals": [
                            {
                                "id": "legacy_with_files",
                                "prompt": "Check this file.",
                                "expected_output": "A result.",
                                "files": ["evals/files/input.txt"],
                            },
                            {
                                "id": "selected_portable",
                                "prompt": "Review this scenario.",
                                "expected_output": "A portable result.",
                                "files": [],
                            },
                        ],
                    }
                )
            )

            tasks = runner.load_tasks(path, task_ids={"selected_portable"}, target_root=Path(tmp))

        self.assertEqual([task.id for task in tasks], ["selected_portable"])

    def test_selected_standard_skill_eval_still_rejects_its_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "evals.json"
            path.write_text(
                json.dumps(
                    {
                        "skill_name": "qa",
                        "evals": [
                            {
                                "id": "selected_with_files",
                                "prompt": "Check this file.",
                                "expected_output": "A result.",
                                "files": ["evals/files/input.txt"],
                            }
                        ],
                    }
                )
            )

            with self.assertRaisesRegex(runner.EvalError, "file not found"):
                runner.load_tasks(path, task_ids={"selected_with_files"}, target_root=Path(tmp))

    def test_selected_standard_skill_eval_rejects_file_escape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "root"
            root.mkdir()
            path = root / "evals.json"
            path.write_text(
                json.dumps(
                    {
                        "skill_name": "qa",
                        "evals": [
                            {
                                "id": "selected_escape",
                                "prompt": "Check the supplied input.",
                                "expected_output": "A result.",
                                "files": ["../outside.txt"],
                            }
                        ],
                    }
                )
            )

            with self.assertRaisesRegex(runner.EvalError, "escapes target root"):
                runner.load_tasks(path, task_ids={"selected_escape"}, target_root=root)

    def test_selected_standard_skill_eval_stages_read_only_file_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = root / "fixtures" / "input.txt"
            fixture.parent.mkdir()
            fixture.write_text("fixture value\n")
            path = root / "evals.json"
            path.write_text(
                json.dumps(
                    {
                        "skill_name": "qa",
                        "evals": [
                            {
                                "id": "selected_with_file",
                                "prompt": "Check the supplied input.",
                                "expected_output": "A result.",
                                "files": ["fixtures/input.txt"],
                            }
                        ],
                    }
                )
            )
            task = runner.load_tasks(path, task_ids={"selected_with_file"}, target_root=root)[0]
            task_dir = root / "run" / task.id

            staged_task = runner.stage_task_files(task, root, task_dir)

            staged = task_dir / "fixtures" / "fixtures" / "input.txt"
            self.assertEqual(staged.read_text(), "fixture value\n")
            self.assertEqual(staged.stat().st_mode & 0o222, 0)
            self.assertIn(str(staged.resolve()), staged_task.context)

    def test_only_a_verdict_passes(self) -> None:
        self.assertTrue(runner.normalize_judge({"verdict": "A"})["pass"])
        self.assertFalse(runner.normalize_judge({"verdict": "B"})["pass"])
        self.assertFalse(runner.normalize_judge({"verdict": "C"})["pass"])
        self.assertFalse(runner.normalize_judge({"verdict": "D"})["pass"])

    def test_codex_profile_args_are_first_class(self) -> None:
        args = runner.codex_extra_args(["--model", "gpt-5.5"], "skill-eval")
        self.assertEqual(
            args,
            [
                "--profile",
                "skill-eval",
                "--model",
                "gpt-5.5",
                "--ephemeral",
                "--disable",
                "hooks",
                "-c",
                "notify=[]",
            ],
        )

    def test_codex_runs_are_isolated_without_a_profile(self) -> None:
        self.assertEqual(
            runner.codex_extra_args([], None),
            ["--ephemeral", "--disable", "hooks", "-c", "notify=[]"],
        )

    def test_codex_eval_isolation_tail_wins_over_user_overrides(self) -> None:
        args = runner.codex_extra_args(
            ["--enable", "hooks", "-c", 'notify=["custom"]'],
            "skill-eval",
        )

        self.assertEqual(args[-5:], ["--ephemeral", "--disable", "hooks", "-c", "notify=[]"])

    def test_codex_profile_rejects_path_like_names(self) -> None:
        with self.assertRaises(runner.EvalError):
            runner.codex_extra_args([], "../skill-eval")

    def test_codex_profile_runs_use_native_skill_context(self) -> None:
        self.assertTrue(runner.uses_native_skill_context("codex", "skill-eval"))
        self.assertFalse(runner.uses_native_skill_context("codex", None))
        self.assertFalse(runner.uses_native_skill_context("claude", "ignored"))

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
            self.assertEqual(summary["scopes"], ["custom"])
            self.assertEqual(summary["pass_rate"], 1.0)
            self.assertEqual(summary["verdict_counts"], {"A": 1})
            self.assertEqual(summary["comparison_metadata"]["max_parallel_tasks"], 2)
            self.assertEqual(len(summary["comparison_metadata"]["agent_prompt_sha256"]), 64)
            self.assertEqual(len(summary["comparison_metadata"]["task_file_sha256"][str(tasks)]), 64)
            self.assertTrue((run_dirs[0] / "tasks" / "proof_01.json").exists())

    def test_behavior_trace_preserves_and_scores_unique_behavior_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_dir = root / "evals"
            fake_cli = root / "behavior_cli.py"
            tasks = eval_dir / "tasks" / "harness_tasks.json"
            schema = root / "behavior-schema.json"
            (eval_dir / "prompts").mkdir(parents=True)
            tasks.parent.mkdir(parents=True)
            write_behavior_cli(fake_cli)
            write_tasks(tasks)
            schema.write_text(
                json.dumps(
                    {
                        "type": "object",
                        "required": ["target", "persona", "checkpoints", "artifacts", "deviations", "verdict"],
                        "properties": {
                            "target": {"type": "string"},
                            "persona": {"type": "string"},
                            "checkpoints": {"type": "array", "minItems": 1},
                            "artifacts": {"type": "array", "items": {"type": "string"}},
                            "deviations": {"type": "array"},
                            "verdict": {"type": "string", "enum": ["pass", "fail", "blocked"]},
                        },
                    }
                )
            )
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
                    "behavior",
                    "--max-parallel-tasks",
                    "1",
                    "--behavior-trace",
                    "--behavior-output-schema",
                    str(schema),
                    "--agent-command-template",
                    template,
                    "--judge-command-template",
                    template,
                ]
            )

            self.assertEqual(code, 0)
            run_dir = next((eval_dir / "runs").glob("*-behavior"))
            summary = json.loads((run_dir / "summary.json").read_text())
            detail = json.loads((run_dir / "tasks" / "proof_01.json").read_text())
            trace = detail["behavior_trace"]
            task_dir = run_dir / "tasks" / "proof_01"
            self.assertTrue(summary["behavior_trace"])
            self.assertEqual(summary["behavior_verdict_counts"], {"pass": 1})
            self.assertEqual(trace["verdict"], "pass")
            self.assertEqual(trace["event_summary"]["thread_id"], "trace-thread")
            self.assertEqual(trace["event_summary"]["command_count"], 1)
            self.assertEqual(trace["event_summary"]["usage"]["input_tokens"], 12)
            self.assertEqual(trace["checkpoint_score"]["done"], 1)
            self.assertIn("produced.txt", trace["artifact_inventory"]["present"])
            self.assertIn("produced.txt", trace["artifact_inventory"]["observed_file_delta"]["created"])
            self.assertTrue(trace["schema_validation"]["pass"])
            self.assertTrue((task_dir / "agent_prompt.md").exists())
            self.assertTrue((task_dir / "events.jsonl").exists())
            self.assertTrue((task_dir / "agent_stdout.log").exists())
            self.assertTrue((task_dir / "agent_stderr.log").exists())
            self.assertTrue((task_dir / "agent_answer.txt").exists())
            self.assertTrue((task_dir / "behavior_trace.json").exists())
            self.assertTrue((task_dir / "output_schema.json").exists())

    def test_behavior_trace_keeps_baseline_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_dir = root / "evals"
            fake_cli = root / "behavior_cli.py"
            qa_eval = root / "skills" / "qa" / "evals/evals.json"
            (eval_dir / "prompts").mkdir(parents=True)
            qa_eval.parent.mkdir(parents=True)
            write_behavior_cli(fake_cli)
            write_tasks(qa_eval)
            (eval_dir / "prompts" / "agent.md").write_text("Task: {query}\n{task_json}\n")
            (eval_dir / "prompts" / "judge.md").write_text("Task: {task_json}\nAssistant answer:\n{answer}\n")
            template = f"{sys.executable} {fake_cli} --skill-event qa --prompt-file {{prompt_file}} --output-file {{output_file}}"

            code = runner.main(
                [
                    "run",
                    "--harness",
                    "custom",
                    "--eval-dir",
                    str(eval_dir),
                    "--target-root",
                    str(root),
                    "--skill",
                    "qa",
                    "--label",
                    "behavior-compare",
                    "--compare-baseline",
                    "--behavior-trace",
                    "--max-parallel-tasks",
                    "1",
                    "--agent-command-template",
                    template,
                    "--judge-command-template",
                    template,
                ]
            )

            self.assertEqual(code, 0)
            run_dir = next((eval_dir / "runs").glob("*-behavior-compare"))
            detail = json.loads((run_dir / "tasks" / "proof_01.json").read_text())
            self.assertEqual(detail["comparison"]["delta"], "tie")
            self.assertEqual(detail["candidate"]["behavior_trace"]["verdict"], "pass")
            self.assertEqual(detail["baseline"]["behavior_trace"]["verdict"], "pass")

    def test_behavior_trace_without_schema_accepts_arbitrary_json_and_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_dir = root / "evals"
            fake_cli = root / "behavior_cli.py"
            tasks = eval_dir / "tasks" / "harness_tasks.json"
            (eval_dir / "prompts").mkdir(parents=True)
            tasks.parent.mkdir(parents=True)
            write_behavior_cli(fake_cli)
            write_tasks(tasks)
            task_rows = json.loads(tasks.read_text())
            task_rows[0]["behavior_requirements"] = {
                "required_successful_command_regexes": [r"printf\s+visible"]
            }
            tasks.write_text(json.dumps(task_rows))
            (eval_dir / "prompts" / "agent.md").write_text("Task: {query}\n{task_json}\n")
            (eval_dir / "prompts" / "judge.md").write_text("Task: {task_json}\nAssistant answer:\n{answer}\n")

            for output_kind in ("planner-json", "text"):
                with self.subTest(output_kind=output_kind):
                    template = (
                        f"{sys.executable} {fake_cli} --output-kind {output_kind} "
                        "--prompt-file {prompt_file} --output-file {output_file}"
                    )
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
                            f"trace-{output_kind}",
                            "--max-parallel-tasks",
                            "1",
                            "--behavior-trace",
                            "--agent-command-template",
                            template,
                            "--judge-command-template",
                            template,
                        ]
                    )

                    self.assertEqual(code, 0)
                    run_dir = next((eval_dir / "runs").glob(f"*-trace-{output_kind}"))
                    detail = json.loads((run_dir / "tasks" / "proof_01.json").read_text())
                    trace = detail["behavior_trace"]
                    self.assertEqual(trace["verdict"], "pass")
                    self.assertEqual(trace["command_requirement_score"]["matched"], 1)
                    self.assertNotIn(
                        "required_successful_command_regexes",
                        (run_dir / "tasks" / "proof_01" / "agent_prompt.md").read_text(),
                    )
                    self.assertFalse(trace["behavior_report_detected"])
                    self.assertFalse(trace["schema_validation"]["requested"])
                    self.assertEqual(trace["failures"], [])
                    if output_kind == "planner-json":
                        self.assertEqual(trace["final_report"]["selected"], ["TASK-9001"])
                    else:
                        self.assertIsNone(trace["final_report"])

    def test_behavior_trace_fails_when_required_successful_command_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_dir = root / "evals"
            fake_cli = root / "behavior_cli.py"
            tasks = eval_dir / "tasks" / "harness_tasks.json"
            (eval_dir / "prompts").mkdir(parents=True)
            tasks.parent.mkdir(parents=True)
            write_behavior_cli(fake_cli)
            write_tasks(tasks)
            task_rows = json.loads(tasks.read_text())
            task_rows[0]["behavior_requirements"] = {
                "required_successful_command_regexes": [r"validate_missing\.py"]
            }
            tasks.write_text(json.dumps(task_rows))
            (eval_dir / "prompts" / "agent.md").write_text("Task: {query}\n{task_json}\n")
            (eval_dir / "prompts" / "judge.md").write_text(
                "Task: {task_json}\nAssistant answer:\n{answer}\n"
            )
            template = (
                f"{sys.executable} {fake_cli} --output-kind planner-json "
                "--prompt-file {prompt_file} --output-file {output_file}"
            )

            code = runner.main(
                [
                    "run", "--harness", "custom", "--eval-dir", str(eval_dir),
                    "--target-root", str(root), "--tasks", str(tasks),
                    "--label", "missing-required-command", "--behavior-trace",
                    "--max-parallel-tasks", "1", "--agent-command-template", template,
                    "--judge-command-template", template,
                ]
            )

            self.assertEqual(code, 1)
            run_dir = next((eval_dir / "runs").glob("*-missing-required-command"))
            summary = json.loads((run_dir / "summary.json").read_text())
            detail = json.loads((run_dir / "tasks" / "proof_01.json").read_text())
            trace = detail["behavior_trace"]
            self.assertFalse(summary["tasks"][0]["pass"])
            self.assertEqual(trace["verdict"], "fail")
            self.assertEqual(trace["command_requirement_score"]["matched"], 0)
            self.assertIn("required successful command evidence missing", trace["failures"][0])

    def test_harness_scope_loads_harness_task_file(self) -> None:
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
                    "--harness-evals",
                    "--label",
                    "harness-scope",
                    "--agent-command-template",
                    template,
                    "--judge-command-template",
                    template,
                ]
            )

            self.assertEqual(code, 0)
            run_dir = next((eval_dir / "runs").glob("*-harness-scope"))
            summary = json.loads((run_dir / "summary.json").read_text())
            self.assertNotIn("suite", summary)
            self.assertEqual(summary["scopes"], ["harness"])
            self.assertEqual(summary["task_count"], 1)
            self.assertEqual(summary["verdict_counts"], {"A": 1})

    def test_default_scope_loads_all_known_eval_families(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_dir = root / "evals"
            fake_cli = root / "fake_cli.py"
            skill_eval = root / "skills" / "qa" / "evals/evals.json"
            (eval_dir / "prompts").mkdir(parents=True)
            (eval_dir / "tasks").mkdir(parents=True)
            skill_eval.parent.mkdir(parents=True)
            write_fake_cli(fake_cli)
            write_tasks(eval_dir / "tasks" / "harness_tasks.json")
            write_tasks(eval_dir / "tasks" / "agents_md_tasks.json")
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
                    "--label",
                    "all-families",
                    "--agent-command-template",
                    template,
                    "--judge-command-template",
                    template,
                ]
            )

            self.assertEqual(code, 0)
            run_dir = next((eval_dir / "runs").glob("*-all-families"))
            summary = json.loads((run_dir / "summary.json").read_text())
            self.assertNotIn("suite", summary)
            self.assertEqual(summary["scopes"], ["harness", "agents-md", "skills"])
            self.assertEqual(summary["task_count"], 3)

    def test_agents_md_scope_loads_agents_md_task_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_dir = root / "evals"
            fake_cli = root / "fake_cli.py"
            (eval_dir / "prompts").mkdir(parents=True)
            (eval_dir / "tasks").mkdir(parents=True)
            write_fake_cli(fake_cli)
            write_tasks(eval_dir / "tasks" / "harness_tasks.json")
            write_tasks(eval_dir / "tasks" / "agents_md_tasks.json")
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
                    "--agents-md",
                    "--label",
                    "agents-md",
                    "--agent-command-template",
                    template,
                    "--judge-command-template",
                    template,
                ]
            )

            self.assertEqual(code, 0)
            run_dir = next((eval_dir / "runs").glob("*-agents-md"))
            summary = json.loads((run_dir / "summary.json").read_text())
            self.assertNotIn("suite", summary)
            self.assertEqual(summary["scopes"], ["agents-md"])
            self.assertEqual([Path(path).resolve() for path in summary["task_files"]], [(eval_dir / "tasks" / "agents_md_tasks.json").resolve()])

    def test_skills_scope_discovers_skill_eval_task_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_dir = root / "evals"
            fake_cli = root / "fake_cli.py"
            skill_eval = root / "skills" / "advise" / "evals/evals.json"
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
                    "--skills",
                    "--label",
                    "skill-scope",
                    "--agent-command-template",
                    template,
                    "--judge-command-template",
                    template,
                ]
            )

            self.assertEqual(code, 0)
            run_dir = next((eval_dir / "runs").glob("*-skill-scope"))
            summary = json.loads((run_dir / "summary.json").read_text())
            self.assertNotIn("suite", summary)
            self.assertEqual(summary["scopes"], ["skills"])
            self.assertEqual(summary["task_count"], 1)
            self.assertEqual([Path(path).resolve() for path in summary["task_files"]], [skill_eval.resolve()])
            self.assertEqual(summary["verdict_counts"], {"A": 1})

    def test_skill_eval_loads_owner_skill_context_without_query_spoiling(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_dir = root / "skills" / "qa"
            skill_eval = skill_dir / "evals/evals.json"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("# QA\n\nThe QA skill requires best_evidence for UI proof.\n")
            write_tasks(skill_eval)

            tasks = runner.load_task_suite(
                [skill_eval],
                default_context="AGI Toy Shop fixture context.",
                target_root=root,
            )

        self.assertEqual(tasks[0].query, "Explain proof discipline.")
        self.assertIn("AGI Toy Shop fixture context.", tasks[0].context)
        self.assertIn("Skill under evaluation: qa", tasks[0].context)
        self.assertIn("The QA skill requires best_evidence", tasks[0].context)
        self.assertIn("Skill context:", tasks[0].context)

    def test_native_skill_context_does_not_inline_skill_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_dir = root / "skills" / "qa"
            skill_eval = skill_dir / "evals/evals.json"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("# QA\n\nThe QA skill requires best_evidence for UI proof.\n")
            write_tasks(skill_eval)

            tasks = runner.load_task_suite(
                [skill_eval],
                default_context="AGI Toy Shop fixture context.",
                target_root=root,
                native_skill_context=True,
            )

        self.assertEqual(tasks[0].query, "Explain proof discipline.")
        self.assertIn("AGI Toy Shop fixture context.", tasks[0].context)
        self.assertNotIn("Skill under evaluation: qa", tasks[0].context)
        self.assertNotIn("The QA skill requires best_evidence", tasks[0].context)

    def test_skills_scope_filters_selected_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_dir = root / "evals"
            fake_cli = root / "fake_cli.py"
            qa_eval = root / "skills" / "qa" / "evals/evals.json"
            advise_eval = root / "skills" / "advise" / "evals/evals.json"
            (eval_dir / "prompts").mkdir(parents=True)
            qa_eval.parent.mkdir(parents=True)
            advise_eval.parent.mkdir(parents=True)
            write_fake_cli(fake_cli)
            write_tasks(qa_eval)
            advise_eval.write_text(
                json.dumps(
                    [
                        {
                            "id": "advise_01",
                            "title": "Advise task",
                            "query": "Give advice.",
                            "reference_points": ["Gives advice"],
                        }
                    ]
                )
            )
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
                    "--skill",
                    "qa",
                    "--label",
                    "selected-skill",
                    "--agent-command-template",
                    template,
                    "--judge-command-template",
                    template,
                ]
            )

            self.assertEqual(code, 0)
            run_dir = next((eval_dir / "runs").glob("*-selected-skill"))
            summary = json.loads((run_dir / "summary.json").read_text())
            self.assertNotIn("suite", summary)
            self.assertEqual(summary["scopes"], ["skills"])
            self.assertEqual(summary["task_count"], 1)
            self.assertEqual([Path(path).resolve() for path in summary["task_files"]], [qa_eval.resolve()])
            self.assertEqual(summary["tasks"][0]["task_id"], "proof_01")

    def test_skill_flag_implies_skills_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_dir = root / "evals"
            fake_cli = root / "fake_cli.py"
            qa_eval = root / "skills" / "qa" / "evals/evals.json"
            (eval_dir / "prompts").mkdir(parents=True)
            qa_eval.parent.mkdir(parents=True)
            write_fake_cli(fake_cli)
            write_tasks(qa_eval)
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
                    "--skill",
                    "qa",
                    "--label",
                    "skill-implied",
                    "--agent-command-template",
                    template,
                    "--judge-command-template",
                    template,
                ]
            )

            self.assertEqual(code, 0)
            run_dir = next((eval_dir / "runs").glob("*-skill-implied"))
            summary = json.loads((run_dir / "summary.json").read_text())
            self.assertNotIn("suite", summary)
            self.assertEqual(summary["scopes"], ["skills"])
            self.assertEqual([Path(path).resolve() for path in summary["task_files"]], [qa_eval.resolve()])

    def test_compare_baseline_records_trigger_and_runs_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_dir = root / "evals"
            fake_cli = root / "fake_cli.py"
            qa_eval = root / "skills" / "qa" / "evals/evals.json"
            skill_md = root / "skills" / "qa" / "SKILL.md"
            (eval_dir / "prompts").mkdir(parents=True)
            qa_eval.parent.mkdir(parents=True)
            write_fake_cli(fake_cli)
            write_tasks(qa_eval)
            skill_md.write_text("# QA\n\nShould not be inlined in compare mode.\n")
            (eval_dir / "prompts" / "agent.md").write_text("Task: {query}\n{task_json}\n")
            (eval_dir / "prompts" / "judge.md").write_text("Task: {task_json}\nAssistant answer:\n{answer}\n")

            template = f"{sys.executable} {fake_cli} --skill-event qa --prompt-file {{prompt_file}} --output-file {{output_file}}"
            code = runner.main(
                [
                    "run",
                    "--harness",
                    "custom",
                    "--eval-dir",
                    str(eval_dir),
                    "--target-root",
                    str(root),
                    "--skill",
                    "qa",
                    "--label",
                    "compare",
                    "--compare-baseline",
                    "--agent-command-template",
                    template,
                    "--judge-command-template",
                    template,
                ]
            )

            self.assertEqual(code, 0)
            run_dir = next((eval_dir / "runs").glob("*-compare"))
            summary = json.loads((run_dir / "summary.json").read_text())
            detail = json.loads((run_dir / "tasks" / "proof_01.json").read_text())
            benchmark = json.loads((run_dir / "benchmark.json").read_text())
            candidate_prompt = (run_dir / "tasks" / "proof_01" / "candidate_agent_prompt.md").read_text()

            self.assertTrue(summary["compare_baseline"])
            self.assertEqual(summary["skill_context"], "native")
            self.assertEqual(summary["skill_trigger_counts"], {"true": 1})
            self.assertEqual(summary["comparison_counts"], {"tie": 1})
            self.assertEqual(summary["schema_version"], 2)
            self.assertEqual(detail["schema_version"], 2)
            self.assertTrue(detail["candidate"]["skill_triggered"])
            self.assertFalse(detail["baseline"]["skipped"] if "skipped" in detail["baseline"] else False)
            self.assertTrue((run_dir / "tasks" / "proof_01" / "candidate" / "timing.json").exists())
            self.assertTrue((run_dir / "tasks" / "proof_01" / "candidate" / "grading.json").exists())
            self.assertTrue((run_dir / "tasks" / "proof_01" / "baseline" / "timing.json").exists())
            self.assertTrue((run_dir / "tasks" / "proof_01" / "comparison.json").exists())
            self.assertIn("candidate", benchmark["run_summary"])
            self.assertIn("baseline", benchmark["run_summary"])
            self.assertEqual(benchmark["repetitions"], 1)
            self.assertFalse((eval_dir / "campaigns").exists())
            self.assertNotIn("Should not be inlined", candidate_prompt)

    def test_detect_skill_triggered_matches_real_codex_skill_file_read(self) -> None:
        raw_stdout = "\n".join(
            [
                json.dumps({"type": "thread.started", "thread_id": "example"}),
                json.dumps(
                    {
                        "type": "item.completed",
                        "item": {
                            "type": "agent_message",
                            "text": "I’ll use the `eval` skill for this evaluation task.",
                        },
                    }
                ),
                json.dumps(
                    {
                        "type": "item.started",
                        "item": {
                            "type": "command_execution",
                            "command": "/bin/zsh -lc \"sed -n '1,240p' /Users/test/.codex/skills/eval/SKILL.md\"",
                        },
                    }
                ),
            ]
        )

        self.assertTrue(runner.detect_skill_triggered(raw_stdout, "eval"))

    def test_compare_baseline_skips_baseline_when_skill_does_not_trigger(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eval_dir = root / "evals"
            fake_cli = root / "fake_cli.py"
            qa_eval = root / "skills" / "qa" / "evals/evals.json"
            (eval_dir / "prompts").mkdir(parents=True)
            qa_eval.parent.mkdir(parents=True)
            write_fake_cli(fake_cli)
            write_tasks(qa_eval)
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
                    "--skill",
                    "qa",
                    "--label",
                    "compare-no-trigger",
                    "--compare-baseline",
                    "--agent-command-template",
                    template,
                    "--judge-command-template",
                    template,
                ]
            )

            self.assertEqual(code, 0)
            run_dir = next((eval_dir / "runs").glob("*-compare-no-trigger"))
            summary = json.loads((run_dir / "summary.json").read_text())
            detail = json.loads((run_dir / "tasks" / "proof_01.json").read_text())

            self.assertEqual(summary["skill_trigger_counts"], {"unknown": 1})
            self.assertEqual(summary["comparison_counts"], {"baseline_skipped": 1})
            self.assertIsNone(detail["candidate"]["skill_triggered"])
            self.assertTrue(detail["baseline"]["skipped"])

    def test_load_task_suite_filters_task_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "tasks.json"
            path.write_text(
                json.dumps(
                    [
                        {
                            "id": "keep_01",
                            "title": "Keep",
                            "query": "Keep this.",
                            "reference_points": ["Kept"],
                        },
                        {
                            "id": "drop_01",
                            "title": "Drop",
                            "query": "Drop this.",
                            "reference_points": ["Dropped"],
                        },
                    ]
                )
            )

            tasks = runner.load_task_suite([path], target_root=root, task_ids={"keep_01"})

        self.assertEqual([task.id for task in tasks], ["keep_01"])

    def test_reliability_report_distinguishes_stable_unstable_and_behavior_failure(self) -> None:
        stable_rows = [
            {"task_id": "one", "verdict": "A", "behavior_verdict": "pass"},
            {"task_id": "two", "verdict": "A", "behavior_verdict": "pass"},
        ]
        stable = runner.build_reliability_report(
            [(Path("run-1"), reliability_summary(stable_rows)), (Path("run-2"), reliability_summary(stable_rows))]
        )
        self.assertEqual(stable["promotion_verdict"], "stable_pass")
        self.assertEqual(stable["strict_grade"]["a_count"], 4)
        self.assertEqual(stable["exact_suite"]["strict_a_pass_count"], 2)

        varied_rows = [
            {"task_id": "one", "verdict": "B", "behavior_verdict": "pass"},
            {"task_id": "two", "verdict": "A", "behavior_verdict": "pass"},
        ]
        unstable = runner.build_reliability_report(
            [(Path("run-1"), reliability_summary(stable_rows)), (Path("run-2"), reliability_summary(varied_rows))]
        )
        self.assertEqual(unstable["promotion_verdict"], "unstable")
        self.assertEqual(unstable["strict_grade"]["a_count"], 3)
        self.assertEqual(unstable["behavior"]["pass_count"], 4)
        self.assertEqual(unstable["exact_suite"]["strict_a_pass_count"], 1)
        self.assertEqual(unstable["disagreement_flags"][0]["task_id"], "one")

        failed_rows = [
            {"task_id": "one", "verdict": "A", "behavior_verdict": "fail"},
            {"task_id": "two", "verdict": "A", "behavior_verdict": "pass"},
        ]
        failed = runner.build_reliability_report(
            [(Path("run-1"), reliability_summary(stable_rows)), (Path("run-2"), reliability_summary(failed_rows))]
        )
        self.assertEqual(failed["promotion_verdict"], "fail")

    def test_reliability_report_fails_closed_on_incompatible_or_malformed_summaries(self) -> None:
        rows = [{"task_id": "one", "verdict": "A", "behavior_verdict": "pass"}]
        incompatible = reliability_summary(rows, harness="claude")
        with self.assertRaisesRegex(runner.EvalError, "incompatible comparison metadata"):
            runner.build_reliability_report(
                [(Path("run-1"), reliability_summary(rows)), (Path("run-2"), incompatible)]
            )

        changed_task = [{"task_id": "different", "verdict": "A", "behavior_verdict": "pass"}]
        with self.assertRaisesRegex(runner.EvalError, "incompatible task id/title set"):
            runner.build_reliability_report(
                [(Path("run-1"), reliability_summary(rows)), (Path("run-2"), reliability_summary(changed_task))]
            )

        with tempfile.TemporaryDirectory() as tmp:
            malformed = Path(tmp) / "summary.json"
            malformed.write_text("{not json")
            with self.assertRaisesRegex(runner.EvalError, "invalid JSON"):
                runner.load_reliability_summary(malformed)

            duplicate = Path(tmp) / "duplicate.json"
            duplicate.write_text(json.dumps(reliability_summary(rows + rows)))
            with self.assertRaisesRegex(runner.EvalError, "duplicate task_id"):
                runner.load_reliability_summary(duplicate)

            missing_field = Path(tmp) / "missing-field.json"
            missing = reliability_summary(rows)
            del missing["behavior_trace"]
            missing_field.write_text(json.dumps(missing))
            with self.assertRaisesRegex(runner.EvalError, "missing comparison metadata field behavior_trace"):
                runner.load_reliability_summary(missing_field)

    def test_fixture_evidence_inspection_separates_controls_from_tension(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "fixtures" / "screen.png"
            image.parent.mkdir(parents=True)
            image.write_bytes(b"png")
            eval_file = root / "evals.json"
            eval_file.write_text(
                json.dumps(
                    {
                        "skill_name": "fixture",
                        "evals": [
                            {
                                "id": "missing-control",
                                "prompt": "Review this state with no screenshot.",
                                "expected_output": "Refuses to pass without screenshot evidence.",
                                "files": [],
                                "assertions": ["Names the missing image"],
                            },
                            {
                                "id": "facts-only",
                                "prompt": "Review the evidence.",
                                "expected_output": "Uses screenshot facts as the verdict basis.",
                                "files": ["fixtures/state.facts.json"],
                                "assertions": ["Names the screenshot as best evidence"],
                            },
                            {
                                "id": "pixels",
                                "prompt": "Review the screenshot.",
                                "expected_output": "Names the best image evidence.",
                                "files": ["fixtures/screen.png"],
                                "assertions": ["Uses screenshot evidence"],
                            },
                        ],
                    }
                )
            )
            (root / "fixtures" / "state.facts.json").write_text("{}")
            report = runner.inspect_fixture_evidence(eval_file, root)

        self.assertEqual(
            report["classification_counts"],
            {
                "intentional_missing_evidence_control": 1,
                "potential_fixture_evaluator_tension": 1,
                "supported": 1,
            },
        )

    def test_reliability_cli_writes_unstable_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "first.json"
            second = root / "second.json"
            output = root / "report.json"
            first.write_text(
                json.dumps(reliability_summary([{"task_id": "one", "verdict": "A", "behavior_verdict": "pass"}]))
            )
            second.write_text(
                json.dumps(reliability_summary([{"task_id": "one", "verdict": "B", "behavior_verdict": "pass"}]))
            )
            code = runner.main(["reliability", str(first), str(second), "--output", str(output)])
            report = json.loads(output.read_text())

        self.assertEqual(code, 1)
        self.assertEqual(report["promotion_verdict"], "unstable")

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
