#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parent.parent
STOP_HOOK_PATH = ROOT / "bin" / "stop_hook.py"
SELF_IMPROVE_PROBE_PATH = ROOT / "bin" / "self_improve_hook_probe.py"


def load_stop_hook_module():
    bin_dir = str(STOP_HOOK_PATH.parent)
    if bin_dir not in sys.path:
        sys.path.insert(0, bin_dir)
    spec = importlib.util.spec_from_file_location("codexter_stop_hook_test", STOP_HOOK_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load stop hook module from {STOP_HOOK_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_self_improve_probe_module():
    bin_dir = str(SELF_IMPROVE_PROBE_PATH.parent)
    if bin_dir not in sys.path:
        sys.path.insert(0, bin_dir)
    spec = importlib.util.spec_from_file_location("codexter_self_improve_probe_test", SELF_IMPROVE_PROBE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load self-improve probe module from {SELF_IMPROVE_PROBE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StopHookRoleConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()

    def test_load_role_config_reads_toml_fields(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-role-") as td:
            base = Path(td)
            agents = base / "agents"
            agents.mkdir(parents=True)
            (agents / "completion-reviewer.toml").write_text(
                '\n'.join(
                    [
                        'model = "gpt-5.4"',
                        'model_reasoning_effort = "high"',
                        'developer_instructions = """',
                        'You are the completion reviewer.',
                        '"""',
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            parsed = self.stop_hook.load_role_config(base, "completion-reviewer")

            self.assertEqual(
                parsed,
                {
                    "developer_instructions": "You are the completion reviewer.",
                    "model": "gpt-5.4",
                    "model_reasoning_effort": "high",
                },
            )

    def test_load_role_config_rejects_missing_instructions(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-role-") as td:
            base = Path(td)
            agents = base / "agents"
            agents.mkdir(parents=True)
            (agents / "completion-reviewer.toml").write_text('model = "gpt-5.4"\n', encoding="utf-8")

            parsed = self.stop_hook.load_role_config(base, "completion-reviewer")

            self.assertIsNone(parsed)

    def test_role_command_injects_model_and_instructions(self) -> None:
        cmd = self.stop_hook.role_command(
            Path("/tmp/codexter"),
            Path("/tmp/out.json"),
            {
                "developer_instructions": "Line one\nLine two",
                "model": "gpt-5.4",
                "model_reasoning_effort": "high",
            },
        )

        self.assertIn("-m", cmd)
        self.assertIn("gpt-5.4", cmd)
        self.assertIn('model_reasoning_effort="high"', cmd)
        injected = next(part for part in cmd if part.startswith("developer_instructions="))
        self.assertIn("\\n", injected)
        self.assertIn("Line one", injected)

    def test_parse_role_output_preserves_user_intent_gate_fields(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-output-") as td:
            output_path = Path(td) / "review.json"
            output_path.write_text(
                """{
  "action": "continue_same_ticket",
  "reason": "user intent impression failed",
  "continuation_message": "continue the same ticket and address the mismatch",
  "speak": "continuing same ticket",
  "next_ticket_id": "",
  "next_phase": "",
  "overall_score": 4.2,
  "evidence_quality": "pass",
  "integration_readiness": "pass",
  "traceability": "pass",
  "freshness": "pass",
  "qa_quality": "pass",
  "demo_quality": "fail",
  "stakeholder_readiness": "fail",
  "stakeholder_readiness_reason": "demo does not yet tell a convincing story",
  "best_demo_artifact": "",
  "storyline_gaps": ["missing the key before/after proof frame"],
  "user_intent_impression": "fail",
  "user_intent_mismatch_reason": "result undershoots the saved user ask",
  "obvious_next_step_exists": true,
  "next_step_safe": true,
  "obvious_next_step": "update the active ticket with the missing proof and rerun review",
  "user_would_expect_more": true,
  "rerun_required": false,
  "blocking_findings": []
}""",
                encoding="utf-8",
            )

            parsed = self.stop_hook.parse_role_output(output_path)

        assert parsed is not None
        self.assertEqual(parsed["qa_quality"], "pass")
        self.assertEqual(parsed["demo_quality"], "fail")
        self.assertEqual(parsed["stakeholder_readiness"], "fail")
        self.assertEqual(parsed["user_intent_impression"], "fail")
        self.assertEqual(parsed["user_intent_mismatch_reason"], "result undershoots the saved user ask")
        self.assertTrue(parsed["obvious_next_step_exists"])
        self.assertEqual(parsed["obvious_next_step"], "update the active ticket with the missing proof and rerun review")
        self.assertTrue(parsed["user_would_expect_more"])


class StopHookPayloadTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()

    def test_emit_stop_passthrough_emits_explicit_continue_json(self) -> None:
        stdout_buffer = io.StringIO()

        with redirect_stdout(stdout_buffer):
            result = self.stop_hook.emit_stop_passthrough(system_message="Stop hook: allowing stop.")

        self.assertEqual(result, 0)
        self.assertEqual(
            json.loads(stdout_buffer.getvalue()),
            {
                "systemMessage": "Stop hook: allowing stop.",
                "continue": True,
            },
        )


class StopHookMainOutputTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()

    def run_main_with_payload(self, payload: dict[str, object]) -> tuple[int, dict[str, object], str]:
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        stdin_buffer = io.StringIO(json.dumps(payload))

        with (
            patch.object(sys, "argv", ["stop_hook.py"]),
            patch.object(sys, "stdin", stdin_buffer),
            redirect_stdout(stdout_buffer),
            redirect_stderr(stderr_buffer),
        ):
            result = self.stop_hook.main()

        return result, json.loads(stdout_buffer.getvalue()), stderr_buffer.getvalue()

    def test_main_emits_continue_json_when_stop_message_is_missing(self) -> None:
        with patch.object(self.stop_hook, "hook_enabled_for_context", return_value=True):
            result, payload, stderr_output = self.run_main_with_payload({"hook_event_name": "Stop"})

        self.assertEqual(result, 0)
        self.assertTrue(payload["continue"])
        self.assertIn("missing assistant message", payload["systemMessage"])
        self.assertEqual(stderr_output, "")

    def test_main_emits_continue_json_when_stop_has_no_runtime_context(self) -> None:
        with patch.object(self.stop_hook, "hook_enabled_for_context", return_value=False):
            result, payload, stderr_output = self.run_main_with_payload({"hook_event_name": "Stop"})

        self.assertEqual(result, 0)
        self.assertTrue(payload["continue"])
        self.assertIn("no Codexter runtime context", payload["systemMessage"])
        self.assertEqual(stderr_output, "")

    def test_main_emits_continue_json_when_ticket_is_unresolved(self) -> None:
        with patch.object(self.stop_hook, "hook_enabled_for_context", return_value=True):
            result, payload, stderr_output = self.run_main_with_payload(
                {
                    "hook_event_name": "Stop",
                    "last_assistant_message": "work finished without a task reference",
                }
            )

        self.assertEqual(result, 0)
        self.assertTrue(payload["continue"])
        self.assertIn("no active ticket resolved", payload["systemMessage"])
        self.assertEqual(stderr_output, "")

    def test_main_emits_continue_json_when_impl_runtime_is_inactive(self) -> None:
        with (
            patch.object(self.stop_hook, "hook_enabled_for_context", return_value=True),
            patch.object(
                self.stop_hook,
                "resolve_ticket",
                return_value={
                    "ticket_id": "TASK-9999",
                    "phase": "documenting",
                    "status": "building",
                },
            ),
            patch.object(self.stop_hook, "impl_loop_flag_active", return_value=False),
            patch.object(self.stop_hook, "has_explicit_ticket_selector", return_value=False),
        ):
            result, payload, stderr_output = self.run_main_with_payload(
                {
                    "hook_event_name": "Stop",
                    "last_assistant_message": "Finished TASK-9999 without impl loop metadata.",
                }
            )

        self.assertEqual(result, 0)
        self.assertTrue(payload["continue"])
        self.assertIn("impl runtime inactive", payload["systemMessage"])
        self.assertEqual(stderr_output, "")


class StopHookSkillOpportunityReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()

    def test_maybe_launch_skill_opportunity_review_respects_explicit_disable(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skill-opportunity-") as td:
            project_root = Path(td)
            window = {"turn_count": 10, "last_review_turn_count": 0, "rolling_exchanges": []}

            with patch.dict(os.environ, {"CODEXTER_SKILL_OPPORTUNITY_APPLY": "0"}, clear=True):
                result = self.stop_hook.maybe_launch_skill_opportunity_review(
                    base=project_root,
                    project_root=project_root,
                    session_id="sess-123",
                    window=window,
                    payload={"hook_event_name": "Stop"},
                )

        self.assertEqual(result["status"], "skipped")
        self.assertEqual(result["reason"], "skill opportunity review disabled")
        self.assertEqual(result["name"], "skill-opportunity-review")
        self.assertEqual(result["readiness"], "ready")
        self.assertTrue(result["trigger"]["due"])
        self.assertEqual(result["artifacts"]["review_run_path"], "")

    def test_maybe_launch_skill_opportunity_review_reports_not_ready_hooklet(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skill-opportunity-") as td:
            project_root = Path(td)
            window = {"turn_count": 9, "last_review_turn_count": 0, "rolling_exchanges": []}

            with patch.dict(os.environ, {}, clear=True):
                result = self.stop_hook.maybe_launch_skill_opportunity_review(
                    base=project_root,
                    project_root=project_root,
                    session_id="sess-123",
                    window=window,
                    payload={"hook_event_name": "Stop"},
                )

        self.assertEqual(result["name"], "skill-opportunity-review")
        self.assertEqual(result["status"], "skipped")
        self.assertEqual(result["readiness"], "not_ready")
        self.assertFalse(result["trigger"]["due"])
        self.assertIn("waiting for 10", result["reason"])
        self.assertEqual(result["artifacts"], {"review_run_path": "", "pid": ""})

    def test_maybe_launch_skill_opportunity_review_dry_run_writes_report_and_marks_window(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skill-opportunity-") as td:
            project_root = Path(td)
            (project_root / ".harness" / "state").mkdir(parents=True)
            (project_root / ".harness" / "state" / "notion-context").mkdir(parents=True)
            (project_root / ".harness" / "state" / "notion-context" / "latest-status-context.md").write_text(
                "# status\n",
                encoding="utf-8",
            )
            cwd = project_root / "packages" / "app"
            cwd.mkdir(parents=True)
            window = {
                "schema_version": 1,
                "session_id": "sess-123",
                "turn_count": 10,
                "last_review_turn_count": 0,
                "rolling_exchanges": [{"user_text": "$impl-plan", "assistant_text": "done"}],
                "pending_user_turn": {},
            }

            with patch.dict(
                os.environ,
                {
                    "CODEXTER_SKILL_OPPORTUNITY_APPLY_DRY_RUN": "1",
                },
                clear=True,
            ):
                result = self.stop_hook.maybe_launch_skill_opportunity_review(
                    base=project_root,
                    project_root=project_root,
                    session_id="sess-123",
                    window=window,
                    payload={"hook_event_name": "Stop", "cwd": str(cwd)},
                )

            run_path = project_root / str(result["review_run_path"])
            report = json.loads((run_path / "report.json").read_text(encoding="utf-8"))
            input_payload = json.loads((run_path / "input.json").read_text(encoding="utf-8"))
            saved_window = json.loads(
                (project_root / ".harness" / "state" / "self-improve" / "windows" / "sess-123.json").read_text(
                    encoding="utf-8"
                )
            )

        self.assertEqual(result["status"], "launched")
        self.assertEqual(result["name"], "skill-opportunity-review")
        self.assertEqual(result["readiness"], "ready")
        self.assertEqual(result["pid"], "dry-run")
        self.assertEqual(result["artifacts"]["pid"], "dry-run")
        self.assertEqual(result["artifacts"]["review_run_path"], result["review_run_path"])
        self.assertEqual(report["status"], "dry_run")
        self.assertEqual(
            [hop["name"] for hop in report["proof_hops"]],
            [
                "user_capture",
                "assistant_capture",
                "rolling_window_write",
                "background_codex_launch",
                "notion_task_creation",
            ],
        )
        self.assertTrue(all(hop["status"] in {"present", "missing"} for hop in report["proof_hops"]))
        self.assertEqual(report["proof_hops"][-1]["status"], "missing")
        self.assertIn("dry-run", report["proof_hops"][-1]["evidence"])
        self.assertIn(
            "Include proof_hops with exactly user_capture, assistant_capture, rolling_window_write, "
            "background_codex_launch, and notion_task_creation in that order.",
            input_payload["instructions"],
        )
        self.assertEqual(input_payload["recent_windows"][0]["session_id"], "sess-123")
        self.assertEqual(input_payload["workflow_refs"]["source_to_feature"], "skills/harness-scout/SKILL.md")
        self.assertEqual(input_payload["workflow_refs"]["feature_options"], "skills/advise/SKILL.md")
        self.assertEqual(input_payload["workflow_refs"]["placement"], "skills/harness-advisor/SKILL.md")
        self.assertEqual(input_payload["workspace_context"]["current_project_name"], project_root.name)
        self.assertEqual(input_payload["workspace_context"]["current_project_root"], str(project_root))
        self.assertEqual(input_payload["workspace_context"]["hook_invocation_cwd"], str(cwd))
        self.assertEqual(
            input_payload["workspace_context"]["status_context_cache"],
            str(project_root / ".harness" / "state" / "notion-context" / "latest-status-context.md"),
        )
        self.assertTrue(input_payload["workspace_context"]["status_context_cache_exists"])
        self.assertEqual(input_payload["workspace_context"]["task_scope_default"], "harness_self_improvement")
        self.assertEqual(saved_window["last_review_turn_count"], 10)

    def test_skill_opportunity_review_uses_codexter_refs_for_cross_project_dedupe(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skill-opportunity-base-") as base_dir:
            with tempfile.TemporaryDirectory(prefix="skill-opportunity-project-") as project_dir:
                base = Path(base_dir)
                project_root = Path(project_dir)
                (base / "skills" / "harness-advisor").mkdir(parents=True)
                (base / "skills" / "harness-advisor" / "SKILL.md").write_text("# Harness Advisor\n", encoding="utf-8")
                (base / "tickets" / "TASK-0001").mkdir(parents=True)
                (base / "tickets" / "TASK-0001" / "ticket.md").write_text("# TASK-0001\n", encoding="utf-8")
                (project_root / ".harness" / "state" / "notion-context").mkdir(parents=True)
                project_status_context = (
                    project_root / ".harness" / "state" / "notion-context" / "latest-status-context.md"
                )
                project_status_context.write_text("# Project status\n", encoding="utf-8")
                window = {
                    "schema_version": 1,
                    "session_id": "sess-123",
                    "turn_count": 10,
                    "last_review_turn_count": 0,
                    "rolling_exchanges": [{"user_text": "project complaint", "assistant_text": "done"}],
                    "pending_user_turn": {},
                }

                with patch.dict(os.environ, {"CODEXTER_SKILL_OPPORTUNITY_APPLY_DRY_RUN": "1"}, clear=True):
                    result = self.stop_hook.maybe_launch_skill_opportunity_review(
                        base=base,
                        project_root=project_root,
                        session_id="sess-123",
                        window=window,
                        payload={"hook_event_name": "Stop", "cwd": str(project_root)},
                    )

                input_payload = json.loads(
                    (project_root / str(result["review_run_path"]) / "input.json").read_text(encoding="utf-8")
                )

        self.assertEqual(input_payload["dedupe_refs"]["skills"], ["skills/harness-advisor/SKILL.md"])
        self.assertEqual(input_payload["dedupe_refs"]["recent_tickets"], ["tickets/TASK-0001/ticket.md"])
        self.assertEqual(input_payload["workspace_context"]["current_project_root"], str(project_root))
        self.assertEqual(input_payload["workspace_context"]["codexter_home"], str(base))
        self.assertEqual(input_payload["workspace_context"]["status_context_cache"], str(project_status_context))
        self.assertTrue(input_payload["workspace_context"]["status_context_cache_exists"])

    def test_maybe_launch_skill_opportunity_review_reports_missing_role_config(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skill-opportunity-") as td:
            project_root = Path(td)
            window = {
                "schema_version": 1,
                "session_id": "sess-123",
                "turn_count": 10,
                "last_review_turn_count": 0,
                "rolling_exchanges": [{"user_text": "$impl-plan", "assistant_text": "done"}],
                "pending_user_turn": {},
            }

            with patch.dict(os.environ, {}, clear=True):
                result = self.stop_hook.maybe_launch_skill_opportunity_review(
                    base=project_root,
                    project_root=project_root,
                    session_id="sess-123",
                    window=window,
                    payload={"hook_event_name": "Stop"},
                )

        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["name"], "skill-opportunity-review")
        self.assertEqual(result["readiness"], "ready")
        self.assertEqual(result["reason"], "missing skill-opportunity-applier role config")

    def test_log_hooklet_result_writes_named_stop_hook_row(self) -> None:
        with tempfile.TemporaryDirectory(prefix="hooklet-log-") as td:
            base = Path(td)
            hooklet = self.stop_hook.skill_opportunity_hooklet_result(
                status="skipped",
                reason="9 captured user turns since last review; waiting for 10",
                project_root=base,
                session_id="sess-123",
                trigger={
                    "due": False,
                    "turn_count": 9,
                    "last_review_turn_count": 0,
                    "cadence": 10,
                    "reason": "9 captured user turns since last review; waiting for 10",
                },
            )
            self.stop_hook.log_hooklet_result(base, hooklet)
            rows = [
                json.loads(line)
                for line in (base / ".harness" / "logs" / "stop-hook.jsonl").read_text(encoding="utf-8").splitlines()
            ]

        self.assertEqual(rows[0]["mode"], "hooklet")
        self.assertEqual(rows[0]["hooklet"], "skill-opportunity-review")
        self.assertEqual(rows[0]["status"], "skipped")
        self.assertEqual(rows[0]["readiness"], "not_ready")
        self.assertEqual(rows[0]["trigger"]["turn_count"], 9)

    def test_stop_hook_launches_learning_review_without_persisted_runtime_turn(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-learning-main-") as td:
            project_root = Path(td)
            (project_root / ".harness" / "state" / "self-improve" / "windows").mkdir(parents=True)
            (project_root / "tickets").mkdir(parents=True)
            window_path = project_root / ".harness" / "state" / "self-improve" / "windows" / "sess-main.json"
            window_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "session_id": "sess-main",
                        "turn_count": 1,
                        "last_review_turn_count": 0,
                        "last_review_at": "",
                        "last_review_run_path": "",
                        "rolling_exchanges": [],
                        "pending_user_turn": {
                            "exchange_id": "sess-main-1",
                            "user_turn_id": "turn-1",
                            "user_captured_at": "2026-05-27T00:00:00Z",
                            "user_text": "ordinary message without a control surface",
                            "user_summary": "ordinary message without a control surface",
                            "intent_mode": "unknown",
                            "control_surface": "",
                            "source": "user_prompt_submit_hook",
                        },
                        "updated_at": "2026-05-27T00:00:00Z",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            stdout_buffer = io.StringIO()
            stdin_buffer = io.StringIO(
                json.dumps(
                    {
                        "hook_event_name": "Stop",
                        "session_id": "sess-main",
                        "cwd": str(project_root),
                        "last_assistant_message": "ordinary assistant response",
                    }
                )
            )

            with (
                patch.object(sys, "argv", ["stop_hook.py"]),
                patch.object(sys, "stdin", stdin_buffer),
                redirect_stdout(stdout_buffer),
                patch.dict(
                    os.environ,
                    {
                        "CODEXTER_HOME": str(project_root),
                        "CODEXTER_SKILL_OPPORTUNITY_APPLY_DRY_RUN": "1",
                        "CODEXTER_SKILL_OPPORTUNITY_APPLY_INTERVAL": "1",
                    },
                    clear=True,
                ),
                patch.object(self.stop_hook, "hook_enabled_for_context", return_value=True),
                patch.object(self.stop_hook, "load_current_run", return_value=None),
                patch.object(self.stop_hook, "load_persisted_runtime_claim", return_value=None),
                patch.object(self.stop_hook, "load_persisted_last_user_turn", return_value=None),
                patch.object(self.stop_hook, "resolve_ticket", return_value=None),
            ):
                result = self.stop_hook.main()

            saved_window = json.loads(window_path.read_text(encoding="utf-8"))
            reports = sorted((project_root / ".harness" / "state" / "self-improve" / "applications").glob("*/report.json"))

        self.assertEqual(result, 0)
        self.assertTrue(json.loads(stdout_buffer.getvalue())["continue"])
        self.assertEqual(saved_window["last_review_turn_count"], 1)
        self.assertEqual(saved_window["rolling_exchanges"][0]["assistant_text"], "ordinary assistant response")
        self.assertEqual(len(reports), 1)

    def test_skill_opportunity_apply_command_is_read_only_and_disables_hooks(self) -> None:
        cmd = self.stop_hook.skill_opportunity_apply_command(
            Path("/tmp/codexter"),
            Path("/tmp/report.json"),
            {
                "developer_instructions": "Return JSON only.",
                "model": "gpt-5.4",
                "model_reasoning_effort": "medium",
            },
        )

        self.assertIn("--sandbox", cmd)
        self.assertIn("read-only", cmd)
        self.assertIn("--disable", cmd)
        self.assertIn("codex_hooks", cmd)
        self.assertIn("--output-last-message", cmd)

    def test_self_improve_hook_probe_simulate_dry_run_emits_report_path(self) -> None:
        probe = load_self_improve_probe_module()
        with tempfile.TemporaryDirectory(prefix="skill-opportunity-probe-") as td:
            project_root = Path(td)
            (project_root / ".harness" / "state").mkdir(parents=True)
            (project_root / "tickets").mkdir(parents=True)
            stdout_buffer = io.StringIO()

            with redirect_stdout(stdout_buffer):
                result = probe.main(
                    [
                        "--project-root",
                        str(project_root),
                        "--session-id",
                        "probe-session",
                        "simulate",
                        "--turns",
                        "10",
                        "--dry-run",
                    ]
                )

            payload = json.loads(stdout_buffer.getvalue())

        self.assertEqual(result, 0)
        self.assertEqual(payload["command"], "simulate")
        self.assertEqual(payload["window_turn_count"], 10)
        self.assertEqual(payload["launch_result"]["status"], "launched")
        self.assertEqual(payload["hooklet_result"]["name"], "skill-opportunity-review")
        self.assertEqual(payload["hooklet_result"]["readiness"], "ready")
        self.assertEqual(payload["launch_result"]["pid"], "dry-run")
        self.assertTrue(payload["recent_application_runs"][0]["report_path"].endswith("report.json"))
        self.assertFalse((project_root / ".harness" / "state" / "current-run.json").exists())
        self.assertFalse((project_root / ".harness" / "state" / "sessions" / "probe-session.json").exists())

    def test_self_improve_hook_probe_honors_custom_interval(self) -> None:
        probe = load_self_improve_probe_module()
        with tempfile.TemporaryDirectory(prefix="skill-opportunity-probe-") as td:
            project_root = Path(td)
            (project_root / ".harness" / "state").mkdir(parents=True)
            (project_root / "tickets").mkdir(parents=True)
            stdout_buffer = io.StringIO()

            with redirect_stdout(stdout_buffer):
                result = probe.main(
                    [
                        "--project-root",
                        str(project_root),
                        "--session-id",
                        "probe-short",
                        "--interval",
                        "3",
                        "simulate",
                        "--turns",
                        "3",
                    ]
                )

            payload = json.loads(stdout_buffer.getvalue())

        self.assertEqual(result, 0)
        self.assertEqual(payload["trigger"]["cadence"], 3)
        self.assertTrue(payload["trigger"]["due"])
        self.assertEqual(payload["launch_result"]["status"], "launched")
        self.assertEqual(payload["launch_result"]["pid"], "dry-run")

    def test_self_improve_hook_probe_tolerates_literal_braces_in_templates(self) -> None:
        probe = load_self_improve_probe_module()
        with tempfile.TemporaryDirectory(prefix="skill-opportunity-probe-") as td:
            project_root = Path(td)
            (project_root / ".harness" / "state").mkdir(parents=True)
            (project_root / "tickets").mkdir(parents=True)
            stdout_buffer = io.StringIO()

            with redirect_stdout(stdout_buffer):
                result = probe.main(
                    [
                        "--project-root",
                        str(project_root),
                        "--session-id",
                        "probe-braces",
                        "--interval",
                        "1",
                        "simulate",
                        "--turns",
                        "1",
                        "--prompt",
                        'please $impl-plan TASK-0174 with {"problem": "literal braces"} {index}',
                        "--response",
                        'response with function x() { return { ok: true }; } {index}',
                    ]
                )

            payload = json.loads(stdout_buffer.getvalue())
            window_path = project_root / payload["window_path"]
            window = json.loads(window_path.read_text(encoding="utf-8"))

        self.assertEqual(result, 0)
        self.assertEqual(payload["launch_result"]["status"], "launched")
        self.assertIn('{"problem": "literal braces"} 1', window["rolling_exchanges"][0]["user_text"])
        self.assertIn("return { ok: true }; } 1", window["rolling_exchanges"][0]["assistant_text"])


class StopHookReviewerPromptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()
        self.ticket = {
            "ticket_id": "TASK-0038",
            "title": "normalize stop-hook role configs",
            "phase": "building",
            "status": "building",
            "next_action": "test",
            "acceptance_gaps": [],
            "evidence_gaps": [],
            "blockers": [],
            "requires_qa": True,
            "requires_demo": False,
            "artifact_root": ROOT / "tickets" / "TASK-0038" / "artifacts",
            "linked_artifacts": [str(ROOT / "tickets" / "TASK-0038" / "artifacts" / "qa" / "report.md")],
            "missing_artifacts": [],
            "artifact_files": [str(ROOT / "tickets" / "TASK-0038" / "artifacts" / "qa" / "report.md")],
        }
        self.current_run = {
            "claim": {"status": "build_complete"},
            "last_user_turn": {"summary": "ship the change"},
            "last_intent_alignment": "aligned",
            "last_intent_alignment_reason": "matches current turn",
            "last_intent_turn_id": "turn-123",
        }

    def test_reviewer_prompt_completion_gate_includes_artifact_state(self) -> None:
        prompt = self.stop_hook.reviewer_prompt(
            "latest response",
            self.ticket,
            self.current_run,
            {"decision": "complete_ticket"},
            mode="completion_gate",
        )

        self.assertIn('"mode": "completion_gate"', prompt)
        self.assertIn('"completion_claim_is_candidate_only": true', prompt)
        self.assertIn('"artifact_root"', prompt)
        self.assertIn('"linked_artifacts"', prompt)
        self.assertIn('"claim"', prompt)
        self.assertIn('"last_intent_alignment"', prompt)

    def test_reviewer_prompt_missing_result_review_excludes_artifact_state(self) -> None:
        prompt = self.stop_hook.reviewer_prompt(
            "latest response",
            self.ticket,
            self.current_run,
            None,
            mode="missing_result_review",
        )

        self.assertIn('"mode": "missing_result_review"', prompt)
        self.assertNotIn('"artifact_root"', prompt)

    def test_validate_reviewer_gate_requires_completion_fields(self) -> None:
        ok, reason, failures = self.stop_hook.validate_reviewer_gate({"action": "continue_same_ticket"})

        self.assertFalse(ok)
        self.assertIn("completion-gate fields", reason)
        self.assertIn("missing gate field: overall_score", failures)

    def test_validate_reviewer_gate_passes_with_clean_gate(self) -> None:
        ok, reason, failures = self.stop_hook.validate_reviewer_gate(
            {
                "overall_score": 4.6,
                "evidence_quality": "pass",
                "integration_readiness": "pass",
                "traceability": "pass",
                "freshness": "pass",
                "qa_quality": "pass",
                "demo_quality": "pass",
                "stakeholder_readiness": "pass",
                "stakeholder_readiness_reason": "",
                "best_demo_artifact": "tickets/TASK-0038/artifacts/demo/demo.html",
                "storyline_gaps": [],
                "user_intent_impression": "pass",
                "user_intent_mismatch_reason": "",
                "obvious_next_step_exists": False,
                "next_step_safe": False,
                "obvious_next_step": "",
                "user_would_expect_more": False,
                "rerun_required": False,
                "blocking_findings": [],
            }
        )

        self.assertTrue(ok)
        self.assertEqual(reason, "")
        self.assertEqual(failures, [])

    def test_validate_reviewer_gate_fails_when_user_intent_impression_fails(self) -> None:
        ok, reason, failures = self.stop_hook.validate_reviewer_gate(
            {
                "overall_score": 4.6,
                "evidence_quality": "pass",
                "integration_readiness": "pass",
                "traceability": "pass",
                "freshness": "pass",
                "qa_quality": "pass",
                "demo_quality": "pass",
                "stakeholder_readiness": "pass",
                "stakeholder_readiness_reason": "",
                "best_demo_artifact": "tickets/TASK-0038/artifacts/demo/demo.html",
                "storyline_gaps": [],
                "user_intent_impression": "fail",
                "user_intent_mismatch_reason": "result is technically valid but undershoots the saved user ask",
                "obvious_next_step_exists": False,
                "next_step_safe": False,
                "obvious_next_step": "",
                "user_would_expect_more": False,
                "rerun_required": False,
                "blocking_findings": [],
            }
        )

        self.assertFalse(ok)
        self.assertEqual(reason, "completion-reviewer completion gates are not passing")
        self.assertIn("user_intent_impression=fail", failures)
        self.assertIn(
            "user_intent_mismatch_reason=result is technically valid but undershoots the saved user ask",
            failures,
        )

    def test_validate_reviewer_gate_fails_when_obvious_next_step_exists(self) -> None:
        ok, reason, failures = self.stop_hook.validate_reviewer_gate(
            {
                "overall_score": 4.6,
                "evidence_quality": "pass",
                "integration_readiness": "pass",
                "traceability": "pass",
                "freshness": "pass",
                "qa_quality": "pass",
                "demo_quality": "pass",
                "stakeholder_readiness": "pass",
                "stakeholder_readiness_reason": "",
                "best_demo_artifact": "tickets/TASK-0038/artifacts/demo/demo.html",
                "storyline_gaps": [],
                "user_intent_impression": "pass",
                "user_intent_mismatch_reason": "",
                "obvious_next_step_exists": True,
                "next_step_safe": True,
                "obvious_next_step": "run one more same-ticket pass to attach the missing proof",
                "user_would_expect_more": True,
                "rerun_required": False,
                "blocking_findings": [],
            }
        )

        self.assertFalse(ok)
        self.assertEqual(reason, "completion-reviewer completion gates are not passing")
        self.assertIn("obvious_next_step=run one more same-ticket pass to attach the missing proof", failures)
        self.assertIn("user_would_expect_more=true", failures)

    def test_validate_reviewer_gate_fails_when_stakeholder_readiness_fails(self) -> None:
        ok, reason, failures = self.stop_hook.validate_reviewer_gate(
            {
                "overall_score": 4.4,
                "evidence_quality": "pass",
                "integration_readiness": "pass",
                "traceability": "pass",
                "freshness": "pass",
                "qa_quality": "pass",
                "demo_quality": "fail",
                "stakeholder_readiness": "fail",
                "stakeholder_readiness_reason": "demo is technically correct but not yet fit to show to leadership",
                "best_demo_artifact": "",
                "storyline_gaps": ["missing a clear wow moment"],
                "user_intent_impression": "pass",
                "user_intent_mismatch_reason": "",
                "obvious_next_step_exists": False,
                "next_step_safe": False,
                "obvious_next_step": "",
                "user_would_expect_more": False,
                "rerun_required": False,
                "blocking_findings": [],
            }
        )

        self.assertFalse(ok)
        self.assertEqual(reason, "completion-reviewer completion gates are not passing")
        self.assertIn("demo_quality=fail", failures)
        self.assertIn("stakeholder_readiness=fail", failures)
        self.assertIn("stakeholder_readiness_reason=demo is technically correct but not yet fit to show to leadership", failures)
        self.assertIn("storyline_gap=missing a clear wow moment", failures)


class StopHookExecutionPhaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()

    def test_build_live_followup_reason_for_qa_requires_delegated_qa_tester(self) -> None:
        prompt = self.stop_hook.build_live_followup_reason(
            "building",
            "continue TASK-0042 in qa and produce ticket-scoped proof artifacts",
            {"ticket_id": "TASK-0042"},
            "qa",
        )

        self.assertIn("Run the `qa` skill on ticket `TASK-0042`.", prompt)
        self.assertIn("Spawn the `qa-tester` subagent or lane", prompt)
        self.assertIn("do not use `agent-browser` directly", prompt)

    def test_decide_impl_transition_advances_impl_to_qa_when_required(self) -> None:
        verdict = self.stop_hook.decide_impl_transition(
            "building",
            {
                "ticket_id": "TASK-0042",
                "blockers": [],
                "acceptance_gaps": [],
                "evidence_gaps": [],
                "requires_qa": True,
                "requires_demo": False,
                "artifact_root": ROOT / "tickets" / "TASK-0042" / "artifacts",
                "linked_artifacts": [],
                "missing_artifacts": [],
                "artifact_files": [],
            },
            {"status": "build_complete", "next": "building", "reason": "builder finished"},
            {"execution_phase": "impl", "requires_qa": True, "requires_demo": False},
        )

        self.assertEqual(verdict["decision"], "advance_execution_phase")
        self.assertEqual(verdict["next_execution_phase"], "qa")

    def test_phase_result_gate_accepts_passing_linked_qa_result(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-qa-") as td:
            root = Path(td)
            result_path = root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "2026-04-24T210000Z" / "result.json"
            result_path.parent.mkdir(parents=True, exist_ok=True)
            result_path.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0042",
                        "phase": "qa",
                        "verdict": "pass",
                        "summary": "qa passed",
                        "artifacts": [str(result_path.parent / "report.md")],
                    }
                ),
                encoding="utf-8",
            )
            (result_path.parent / "report.md").write_text("report", encoding="utf-8")
            ticket = {
                "ticket_id": "TASK-0042",
                "updated_at": "2026-04-24T00:00:00Z",
                "artifact_root": (root / "tickets" / "TASK-0042" / "artifacts").resolve(),
                "linked_artifacts": [str(result_path.resolve())],
                "missing_artifacts": [],
                "artifact_files": [str(result_path.resolve())],
                "requires_qa": True,
                "requires_demo": False,
            }
            current_run = {
                "execution_phase": "qa",
                "phase_requirements": {
                    "impl": {"completion_statuses": ["build_complete", "done"], "artifact_root": str(ticket["artifact_root"])},
                    "qa": {
                        "artifact_root": str((ticket["artifact_root"] / "qa").resolve()),
                        "result_glob": "**/result.json",
                        "required_verdict": "pass",
                    },
                },
            }

            ok, reason, failures, payload = self.stop_hook.phase_result_gate(ticket, current_run, "qa")

        self.assertTrue(ok)
        self.assertEqual(reason, "")
        self.assertEqual(failures, [])
        assert payload is not None
        self.assertEqual(payload["phase"], "qa")


class StopHookCompletionReviewReceiptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()

    def test_extract_completion_password_reads_explicit_line(self) -> None:
        password = self.stop_hook.extract_completion_password(
            "work complete\nCOMPLETION_PASSWORD: CR-ABC123\nIMPL_RESULT: status=done next=building reason=ready"
        )

        self.assertEqual(password, "CR-ABC123")

    def test_completion_review_receipt_gate_accepts_matching_linked_receipt(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-completion-receipt-") as td:
            root = Path(td)
            reviewed_artifact = root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "result.json"
            review_artifact = root / "tickets" / "TASK-0042" / "artifacts" / "review" / "review.json"
            receipt_path = root / "tickets" / "TASK-0042" / "artifacts" / "review" / "2026-04-25T020000Z-completion-receipt.json"
            receipt_path.parent.mkdir(parents=True, exist_ok=True)
            reviewed_artifact.parent.mkdir(parents=True, exist_ok=True)
            reviewed_artifact.write_text("{}", encoding="utf-8")
            review_artifact.write_text("{}", encoding="utf-8")
            receipt_path.write_text(
                json.dumps(
                    {
                        "receipt_type": "completion_review",
                        "ticket_id": "TASK-0042",
                        "nonce": "CR-123ABC",
                        "reviewed_at": "2026-04-25T02:00:00Z",
                        "reviewer_mode": "visible_review_lane",
                        "reviewed_artifacts": [str(reviewed_artifact)],
                        "verdict": "pass",
                        "satisfies_user_query": True,
                        "user_query_reason": "",
                        "obvious_next_step": "",
                        "review_artifact": str(review_artifact),
                    }
                ),
                encoding="utf-8",
            )
            ticket = {
                "ticket_id": "TASK-0042",
                "updated_at": "2026-04-25T01:59:00Z",
                "artifact_root": (root / "tickets" / "TASK-0042" / "artifacts").resolve(),
                "linked_artifacts": [str(receipt_path.resolve()), str(review_artifact.resolve())],
                "missing_artifacts": [],
                "artifact_files": [str(receipt_path.resolve()), str(review_artifact.resolve()), str(reviewed_artifact.resolve())],
            }
            current_run = {
                "completion_review_nonce": "CR-123ABC",
                "completion_review_requested_at": "2026-04-25T01:58:00Z",
                "completion_review_required_artifacts": [str(reviewed_artifact.resolve())],
            }

            ok, reason, failures, receipt = self.stop_hook.completion_review_receipt_gate(ticket, current_run)

        self.assertTrue(ok)
        self.assertEqual(reason, "")
        self.assertEqual(failures, [])
        assert receipt is not None
        self.assertEqual(receipt["nonce"], "CR-123ABC")

    def test_completion_review_receipt_gate_fails_when_nonce_mismatches(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-completion-receipt-") as td:
            root = Path(td)
            receipt_path = root / "tickets" / "TASK-0042" / "artifacts" / "review" / "2026-04-25T020000Z-completion-receipt.json"
            receipt_path.parent.mkdir(parents=True, exist_ok=True)
            receipt_path.write_text(
                json.dumps(
                    {
                        "receipt_type": "completion_review",
                        "ticket_id": "TASK-0042",
                        "nonce": "CR-OLD123",
                        "reviewed_at": "2026-04-25T02:00:00Z",
                        "reviewer_mode": "visible_review_lane",
                        "reviewed_artifacts": [str(receipt_path)],
                        "verdict": "pass",
                        "satisfies_user_query": True,
                        "user_query_reason": "",
                        "obvious_next_step": "",
                        "review_artifact": str(receipt_path),
                    }
                ),
                encoding="utf-8",
            )
            ticket = {
                "ticket_id": "TASK-0042",
                "updated_at": "2026-04-25T01:59:00Z",
                "artifact_root": (root / "tickets" / "TASK-0042" / "artifacts").resolve(),
                "linked_artifacts": [str(receipt_path.resolve())],
                "missing_artifacts": [],
                "artifact_files": [str(receipt_path.resolve())],
            }
            current_run = {
                "completion_review_nonce": "CR-NEWWWW",
                "completion_review_requested_at": "2026-04-25T01:58:00Z",
            }

            ok, reason, failures, receipt = self.stop_hook.completion_review_receipt_gate(ticket, current_run)

        self.assertFalse(ok)
        self.assertEqual(reason, "completion review receipt gates are not passing")
        self.assertIn("completion_review_nonce=mismatch:CR-OLD123", failures)
        self.assertIsNone(receipt)

    def test_completion_review_receipt_gate_fails_when_receipt_is_missing(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-completion-receipt-") as td:
            root = Path(td)
            ticket = {
                "ticket_id": "TASK-0042",
                "updated_at": "2026-04-25T01:59:00Z",
                "artifact_root": (root / "tickets" / "TASK-0042" / "artifacts").resolve(),
                "linked_artifacts": [],
                "missing_artifacts": [],
                "artifact_files": [],
            }
            current_run = {
                "completion_review_nonce": "CR-123ABC",
                "completion_review_requested_at": "2026-04-25T01:58:00Z",
            }

            ok, reason, failures, receipt = self.stop_hook.completion_review_receipt_gate(ticket, current_run)

        self.assertFalse(ok)
        self.assertEqual(reason, "completion review receipt gates are not passing")
        self.assertIn("completion_review_receipt=missing", failures)
        self.assertIsNone(receipt)

    def test_completion_review_receipt_gate_fails_when_receipt_is_stale(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-completion-receipt-") as td:
            root = Path(td)
            reviewed_artifact = root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "result.json"
            review_artifact = root / "tickets" / "TASK-0042" / "artifacts" / "review" / "review.json"
            receipt_path = root / "tickets" / "TASK-0042" / "artifacts" / "review" / "2026-04-25T015700Z-completion-receipt.json"
            reviewed_artifact.parent.mkdir(parents=True, exist_ok=True)
            review_artifact.parent.mkdir(parents=True, exist_ok=True)
            reviewed_artifact.write_text("{}", encoding="utf-8")
            review_artifact.write_text("{}", encoding="utf-8")
            receipt_path.write_text(
                json.dumps(
                    {
                        "receipt_type": "completion_review",
                        "ticket_id": "TASK-0042",
                        "nonce": "CR-123ABC",
                        "reviewed_at": "2026-04-25T01:57:00Z",
                        "reviewer_mode": "visible_review_lane",
                        "reviewed_artifacts": [str(reviewed_artifact)],
                        "verdict": "pass",
                        "satisfies_user_query": True,
                        "user_query_reason": "",
                        "obvious_next_step": "",
                        "review_artifact": str(review_artifact),
                    }
                ),
                encoding="utf-8",
            )
            ticket = {
                "ticket_id": "TASK-0042",
                "updated_at": "2026-04-25T01:59:00Z",
                "artifact_root": (root / "tickets" / "TASK-0042" / "artifacts").resolve(),
                "linked_artifacts": [str(receipt_path.resolve()), str(review_artifact.resolve())],
                "missing_artifacts": [],
                "artifact_files": [str(receipt_path.resolve()), str(review_artifact.resolve()), str(reviewed_artifact.resolve())],
            }
            current_run = {
                "completion_review_nonce": "CR-123ABC",
                "completion_review_requested_at": "2026-04-25T01:58:00Z",
                "completion_review_required_artifacts": [str(reviewed_artifact.resolve())],
            }

            ok, reason, failures, receipt = self.stop_hook.completion_review_receipt_gate(ticket, current_run)

        self.assertFalse(ok)
        self.assertEqual(reason, "completion review receipt gates are not passing")
        self.assertIn("completion_review_receipt=stale", failures)
        self.assertIsNotNone(receipt)

    def test_completion_review_receipt_gate_fails_when_receipt_verdict_is_non_pass(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-completion-receipt-") as td:
            root = Path(td)
            reviewed_artifact = root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "result.json"
            review_artifact = root / "tickets" / "TASK-0042" / "artifacts" / "review" / "review.json"
            receipt_path = root / "tickets" / "TASK-0042" / "artifacts" / "review" / "2026-04-25T020000Z-completion-receipt.json"
            reviewed_artifact.parent.mkdir(parents=True, exist_ok=True)
            review_artifact.parent.mkdir(parents=True, exist_ok=True)
            reviewed_artifact.write_text("{}", encoding="utf-8")
            review_artifact.write_text("{}", encoding="utf-8")
            receipt_path.write_text(
                json.dumps(
                    {
                        "receipt_type": "completion_review",
                        "ticket_id": "TASK-0042",
                        "nonce": "CR-123ABC",
                        "reviewed_at": "2026-04-25T02:00:00Z",
                        "reviewer_mode": "visible_review_lane",
                        "reviewed_artifacts": [str(reviewed_artifact)],
                        "verdict": "revise",
                        "satisfies_user_query": False,
                        "user_query_reason": "still missing the final linked review artifact",
                        "obvious_next_step": "rerun visible completion review after linking the review artifact",
                        "review_artifact": str(review_artifact),
                    }
                ),
                encoding="utf-8",
            )
            ticket = {
                "ticket_id": "TASK-0042",
                "updated_at": "2026-04-25T01:59:00Z",
                "artifact_root": (root / "tickets" / "TASK-0042" / "artifacts").resolve(),
                "linked_artifacts": [str(receipt_path.resolve()), str(review_artifact.resolve())],
                "missing_artifacts": [],
                "artifact_files": [str(receipt_path.resolve()), str(review_artifact.resolve()), str(reviewed_artifact.resolve())],
            }
            current_run = {
                "completion_review_nonce": "CR-123ABC",
                "completion_review_requested_at": "2026-04-25T01:58:00Z",
                "completion_review_required_artifacts": [str(reviewed_artifact.resolve())],
            }

            ok, reason, failures, receipt = self.stop_hook.completion_review_receipt_gate(ticket, current_run)

        self.assertFalse(ok)
        self.assertEqual(reason, "completion review receipt gates are not passing")
        self.assertIn("completion_review_verdict=revise", failures)
        self.assertIn("completion_review_satisfies_user_query=false", failures)
        self.assertIn("completion_review_user_query_reason=still missing the final linked review artifact", failures)
        self.assertIsNotNone(receipt)

    def test_completion_review_receipt_gate_fails_when_required_artifact_was_not_reviewed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-completion-receipt-") as td:
            root = Path(td)
            required_artifact = root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "result.json"
            substituted_artifact = root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "other.json"
            review_artifact = root / "tickets" / "TASK-0042" / "artifacts" / "review" / "review.json"
            receipt_path = root / "tickets" / "TASK-0042" / "artifacts" / "review" / "2026-04-25T020000Z-completion-receipt.json"
            required_artifact.parent.mkdir(parents=True, exist_ok=True)
            review_artifact.parent.mkdir(parents=True, exist_ok=True)
            required_artifact.write_text("{}", encoding="utf-8")
            substituted_artifact.write_text("{}", encoding="utf-8")
            review_artifact.write_text("{}", encoding="utf-8")
            receipt_path.write_text(
                json.dumps(
                    {
                        "receipt_type": "completion_review",
                        "ticket_id": "TASK-0042",
                        "nonce": "CR-123ABC",
                        "reviewed_at": "2026-04-25T02:00:00Z",
                        "reviewer_mode": "visible_review_lane",
                        "reviewed_artifacts": [str(substituted_artifact)],
                        "verdict": "pass",
                        "satisfies_user_query": True,
                        "user_query_reason": "",
                        "obvious_next_step": "",
                        "review_artifact": str(review_artifact),
                    }
                ),
                encoding="utf-8",
            )
            ticket = {
                "ticket_id": "TASK-0042",
                "updated_at": "2026-04-25T01:59:00Z",
                "artifact_root": (root / "tickets" / "TASK-0042" / "artifacts").resolve(),
                "linked_artifacts": [str(receipt_path.resolve()), str(review_artifact.resolve()), str(required_artifact.resolve())],
                "missing_artifacts": [],
                "artifact_files": [
                    str(receipt_path.resolve()),
                    str(review_artifact.resolve()),
                    str(required_artifact.resolve()),
                    str(substituted_artifact.resolve()),
                ],
            }
            current_run = {
                "completion_review_nonce": "CR-123ABC",
                "completion_review_requested_at": "2026-04-25T01:58:00Z",
                "completion_review_required_artifacts": [str(required_artifact.resolve())],
            }

            ok, reason, failures, receipt = self.stop_hook.completion_review_receipt_gate(ticket, current_run)

        self.assertFalse(ok)
        self.assertEqual(reason, "completion review receipt gates are not passing")
        self.assertIn(f"completion_review_required_artifact=unreviewed:{required_artifact.resolve()}", failures)
        self.assertIsNotNone(receipt)

    def test_main_requests_visible_completion_review_without_hidden_role(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-main-") as td:
            root = Path(td)
            payload = {
                "hook_event_name": "Stop",
                "session_id": "sess-123",
                "last_assistant_message": "GROUNDING_SUMMARY: reviewer receipt requested\nIMPL_RESULT: status=done next=building reason=ready for completion gate",
            }
            current_run = {
                "ticket_id": "TASK-0042",
                "phase": "building",
                "status": "waiting_for_worker",
                "skill_name": "impl",
                "session_id": "sess-123",
                "impl_loop_active": True,
                "execution_phase": "impl",
            }
            ticket = {
                "ticket_id": "TASK-0042",
                "title": "receipt gate fixture",
                "phase": "building",
                "status": "building",
                "next_action": "test",
                "acceptance_gaps": [],
                "evidence_gaps": [],
                "blockers": [],
                "requires_qa": True,
                "requires_demo": False,
                "updated_at": "2026-04-25T01:59:00Z",
                "artifact_root": root / "tickets" / "TASK-0042" / "artifacts",
                "linked_artifacts": [str((root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "result.json").resolve())],
                "missing_artifacts": [],
                "artifact_files": [str((root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "result.json").resolve())],
            }
            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()
            stdin_buffer = io.StringIO(json.dumps(payload))

            with (
                patch.object(sys, "argv", ["stop_hook.py"]),
                patch.object(sys, "stdin", stdin_buffer),
                redirect_stdout(stdout_buffer),
                redirect_stderr(stderr_buffer),
                patch.object(self.stop_hook, "project_root_from_payload", return_value=root),
                patch.object(self.stop_hook, "hook_enabled_for_context", return_value=True),
                patch.object(self.stop_hook, "load_current_run", return_value=current_run),
                patch.object(self.stop_hook, "load_persisted_runtime_claim", return_value={"ticket_id": "TASK-0042", "session_id": "sess-123", "skill_name": "impl"}),
                patch.object(self.stop_hook, "load_persisted_last_user_turn", return_value={"summary": "finish the ticket", "intent_mode": "building", "requested_outcome": "done"}),
                patch.object(self.stop_hook, "resolve_ticket", return_value=ticket),
                patch.object(self.stop_hook, "classify_intent_alignment", return_value={"state": "aligned", "reason": "aligned", "turn_id": "turn-1", "summary": "finish the ticket", "expected_phase": "building", "observed_phase": "building", "continuation_message": "", "announce": ""}),
                patch.object(self.stop_hook, "run_impl_judge", return_value={"decision": "complete_ticket", "next_phase": "documenting", "reason": "builder finished", "orchestrator_message": "mark TASK-0042 complete", "evidence_ok": True}),
                patch.object(self.stop_hook, "emit_hook_telemetry"),
                patch.object(self.stop_hook, "announce_message"),
                patch.object(self.stop_hook, "persist_runtime_update", wraps=self.stop_hook.persist_runtime_update) as persist_runtime_update_mock,
                patch.object(self.stop_hook, "run_role") as run_role_mock,
            ):
                result = self.stop_hook.main()

        self.assertEqual(result, 0)
        response = json.loads(stdout_buffer.getvalue())
        self.assertEqual(response["decision"], "block")
        self.assertIn("Call the completion reviewer now", response["reason"])
        self.assertIn("COMPLETION_PASSWORD:", response["reason"])
        request_updates = [
            call.args[2]
            for call in persist_runtime_update_mock.call_args_list
            if len(call.args) >= 3 and isinstance(call.args[2], dict) and "completion_review_requested" in call.args[2]
        ]
        self.assertTrue(request_updates)
        self.assertTrue(request_updates[-1]["completion_review_requested"])
        self.assertEqual(request_updates[-1]["completion_review_receipt_status"], "requested")
        self.assertRegex(str(request_updates[-1]["completion_review_nonce"]), r"^CR-[0-9A-F]{6}$")
        self.assertEqual(
            request_updates[-1]["completion_review_required_artifacts"],
            [str((root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "result.json").resolve())],
        )
        run_role_mock.assert_not_called()

    def test_main_requires_completion_password_without_rerunning_review_when_receipt_is_already_valid(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-main-") as td:
            root = Path(td)
            receipt_path = root / "tickets" / "TASK-0042" / "artifacts" / "review" / "2026-04-25T020000Z-completion-receipt.json"
            payload = {
                "hook_event_name": "Stop",
                "session_id": "sess-123",
                "last_assistant_message": "GROUNDING_SUMMARY: reviewer receipt requested\nIMPL_RESULT: status=done next=building reason=ready for completion gate",
            }
            current_run = {
                "ticket_id": "TASK-0042",
                "phase": "building",
                "status": "waiting_for_worker",
                "skill_name": "impl",
                "session_id": "sess-123",
                "impl_loop_active": True,
                "execution_phase": "impl",
                "completion_review_requested": True,
                "completion_review_nonce": "CR-123ABC",
                "completion_review_requested_at": "2026-04-25T01:58:00Z",
                "completion_review_required_artifacts": [
                    str((root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "result.json").resolve())
                ],
            }
            ticket = {
                "ticket_id": "TASK-0042",
                "title": "receipt gate fixture",
                "phase": "building",
                "status": "building",
                "next_action": "test",
                "acceptance_gaps": [],
                "evidence_gaps": [],
                "blockers": [],
                "requires_qa": True,
                "requires_demo": False,
                "updated_at": "2026-04-25T01:59:00Z",
                "artifact_root": root / "tickets" / "TASK-0042" / "artifacts",
                "linked_artifacts": [str((root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "result.json").resolve())],
                "missing_artifacts": [],
                "artifact_files": [str((root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "result.json").resolve())],
            }
            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()
            stdin_buffer = io.StringIO(json.dumps(payload))

            with (
                patch.object(sys, "argv", ["stop_hook.py"]),
                patch.object(sys, "stdin", stdin_buffer),
                redirect_stdout(stdout_buffer),
                redirect_stderr(stderr_buffer),
                patch.object(self.stop_hook, "project_root_from_payload", return_value=root),
                patch.object(self.stop_hook, "hook_enabled_for_context", return_value=True),
                patch.object(self.stop_hook, "load_current_run", return_value=current_run),
                patch.object(self.stop_hook, "load_persisted_runtime_claim", return_value={"ticket_id": "TASK-0042", "session_id": "sess-123", "skill_name": "impl"}),
                patch.object(self.stop_hook, "load_persisted_last_user_turn", return_value={"summary": "finish the ticket", "intent_mode": "building", "requested_outcome": "done"}),
                patch.object(self.stop_hook, "resolve_ticket", return_value=ticket),
                patch.object(self.stop_hook, "classify_intent_alignment", return_value={"state": "aligned", "reason": "aligned", "turn_id": "turn-1", "summary": "finish the ticket", "expected_phase": "building", "observed_phase": "building", "continuation_message": "", "announce": ""}),
                patch.object(self.stop_hook, "run_impl_judge", return_value={"decision": "complete_ticket", "next_phase": "documenting", "reason": "builder finished", "orchestrator_message": "mark TASK-0042 complete", "evidence_ok": True}),
                patch.object(self.stop_hook, "emit_hook_telemetry"),
                patch.object(self.stop_hook, "announce_message"),
                patch.object(self.stop_hook, "completion_review_receipt_gate", return_value=(True, "", [], {"_path": str(receipt_path)})) as receipt_gate_mock,
            ):
                result = self.stop_hook.main()

        self.assertEqual(result, 0)
        response = json.loads(stdout_buffer.getvalue())
        self.assertEqual(response["decision"], "block")
        self.assertIn("completion review password is missing", response["reason"])
        self.assertIn("COMPLETION_PASSWORD: CR-123ABC", response["reason"])
        self.assertIn("Do not rerun completion review", response["reason"])
        self.assertNotIn("Call the completion reviewer now", response["reason"])
        receipt_gate_mock.assert_called_once()

    def test_main_requests_reviewer_again_when_password_is_missing_and_receipt_is_not_ready(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-main-") as td:
            root = Path(td)
            payload = {
                "hook_event_name": "Stop",
                "session_id": "sess-123",
                "last_assistant_message": "GROUNDING_SUMMARY: reviewer receipt requested\nIMPL_RESULT: status=done next=building reason=ready for completion gate",
            }
            current_run = {
                "ticket_id": "TASK-0042",
                "phase": "building",
                "status": "waiting_for_worker",
                "skill_name": "impl",
                "session_id": "sess-123",
                "impl_loop_active": True,
                "execution_phase": "impl",
                "completion_review_requested": True,
                "completion_review_nonce": "CR-123ABC",
                "completion_review_requested_at": "2026-04-25T01:58:00Z",
                "completion_review_required_artifacts": [
                    str((root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "result.json").resolve())
                ],
            }
            ticket = {
                "ticket_id": "TASK-0042",
                "title": "receipt gate fixture",
                "phase": "building",
                "status": "building",
                "next_action": "test",
                "acceptance_gaps": [],
                "evidence_gaps": [],
                "blockers": [],
                "requires_qa": True,
                "requires_demo": False,
                "updated_at": "2026-04-25T01:59:00Z",
                "artifact_root": root / "tickets" / "TASK-0042" / "artifacts",
                "linked_artifacts": [str((root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "result.json").resolve())],
                "missing_artifacts": [],
                "artifact_files": [str((root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "result.json").resolve())],
            }
            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()
            stdin_buffer = io.StringIO(json.dumps(payload))

            with (
                patch.object(sys, "argv", ["stop_hook.py"]),
                patch.object(sys, "stdin", stdin_buffer),
                redirect_stdout(stdout_buffer),
                redirect_stderr(stderr_buffer),
                patch.object(self.stop_hook, "project_root_from_payload", return_value=root),
                patch.object(self.stop_hook, "hook_enabled_for_context", return_value=True),
                patch.object(self.stop_hook, "load_current_run", return_value=current_run),
                patch.object(self.stop_hook, "load_persisted_runtime_claim", return_value={"ticket_id": "TASK-0042", "session_id": "sess-123", "skill_name": "impl"}),
                patch.object(self.stop_hook, "load_persisted_last_user_turn", return_value={"summary": "finish the ticket", "intent_mode": "building", "requested_outcome": "done"}),
                patch.object(self.stop_hook, "resolve_ticket", return_value=ticket),
                patch.object(self.stop_hook, "classify_intent_alignment", return_value={"state": "aligned", "reason": "aligned", "turn_id": "turn-1", "summary": "finish the ticket", "expected_phase": "building", "observed_phase": "building", "continuation_message": "", "announce": ""}),
                patch.object(self.stop_hook, "run_impl_judge", return_value={"decision": "complete_ticket", "next_phase": "documenting", "reason": "builder finished", "orchestrator_message": "mark TASK-0042 complete", "evidence_ok": True}),
                patch.object(self.stop_hook, "emit_hook_telemetry"),
                patch.object(self.stop_hook, "announce_message"),
                patch.object(self.stop_hook, "completion_review_receipt_gate", return_value=(False, "completion review receipt gates are not passing", ["completion_review_receipt=missing"], None)) as receipt_gate_mock,
            ):
                result = self.stop_hook.main()

        self.assertEqual(result, 0)
        response = json.loads(stdout_buffer.getvalue())
        self.assertEqual(response["decision"], "block")
        self.assertIn("completion review password is missing", response["reason"])
        self.assertIn("Call the completion reviewer now", response["reason"])
        self.assertNotIn("Do not rerun completion review", response["reason"])
        receipt_gate_mock.assert_called_once()

    def test_main_routes_to_orchestrator_after_password_and_receipt_pass(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-main-") as td:
            root = Path(td)
            receipt_path = root / "tickets" / "TASK-0042" / "artifacts" / "review" / "2026-04-25T020000Z-completion-receipt.json"
            payload = {
                "hook_event_name": "Stop",
                "session_id": "sess-123",
                "last_assistant_message": (
                    "GROUNDING_SUMMARY: reviewer receipt requested\n"
                    "COMPLETION_PASSWORD: CR-123ABC\n"
                    "IMPL_RESULT: status=done next=building reason=ready for completion gate"
                ),
            }
            current_run = {
                "ticket_id": "TASK-0042",
                "phase": "building",
                "status": "waiting_for_worker",
                "skill_name": "impl",
                "session_id": "sess-123",
                "impl_loop_active": True,
                "execution_phase": "impl",
                "completion_review_requested": True,
                "completion_review_nonce": "CR-123ABC",
                "completion_review_requested_at": "2026-04-25T01:58:00Z",
                "completion_review_required_artifacts": [
                    str((root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "result.json").resolve())
                ],
            }
            ticket = {
                "ticket_id": "TASK-0042",
                "title": "receipt gate fixture",
                "phase": "building",
                "status": "building",
                "next_action": "test",
                "acceptance_gaps": [],
                "evidence_gaps": [],
                "blockers": [],
                "requires_qa": True,
                "requires_demo": False,
                "updated_at": "2026-04-25T01:59:00Z",
                "artifact_root": root / "tickets" / "TASK-0042" / "artifacts",
                "linked_artifacts": [str((root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "result.json").resolve())],
                "missing_artifacts": [],
                "artifact_files": [str((root / "tickets" / "TASK-0042" / "artifacts" / "qa" / "result.json").resolve())],
            }
            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()
            stdin_buffer = io.StringIO(json.dumps(payload))

            def fake_orchestrator(**_: object) -> int:
                return self.stop_hook.emit_stop_payload(system_message="Stop hook: orchestrator reached")

            with (
                patch.object(sys, "argv", ["stop_hook.py"]),
                patch.object(sys, "stdin", stdin_buffer),
                redirect_stdout(stdout_buffer),
                redirect_stderr(stderr_buffer),
                patch.object(self.stop_hook, "project_root_from_payload", return_value=root),
                patch.object(self.stop_hook, "hook_enabled_for_context", return_value=True),
                patch.object(self.stop_hook, "load_current_run", return_value=current_run),
                patch.object(self.stop_hook, "load_persisted_runtime_claim", return_value={"ticket_id": "TASK-0042", "session_id": "sess-123", "skill_name": "impl"}),
                patch.object(self.stop_hook, "load_persisted_last_user_turn", return_value={"summary": "finish the ticket", "intent_mode": "building", "requested_outcome": "done"}),
                patch.object(self.stop_hook, "resolve_ticket", return_value=ticket),
                patch.object(self.stop_hook, "classify_intent_alignment", return_value={"state": "aligned", "reason": "aligned", "turn_id": "turn-1", "summary": "finish the ticket", "expected_phase": "building", "observed_phase": "building", "continuation_message": "", "announce": ""}),
                patch.object(self.stop_hook, "run_impl_judge", return_value={"decision": "complete_ticket", "next_phase": "documenting", "reason": "builder finished", "orchestrator_message": "mark TASK-0042 complete", "evidence_ok": True}),
                patch.object(self.stop_hook, "completion_review_receipt_gate", return_value=(True, "", [], {"_path": str(receipt_path)})) as receipt_gate_mock,
                patch.object(self.stop_hook, "run_orchestrator_decision", side_effect=fake_orchestrator) as orchestrator_mock,
                patch.object(self.stop_hook, "emit_hook_telemetry"),
                patch.object(self.stop_hook, "announce_message"),
            ):
                result = self.stop_hook.main()

        self.assertEqual(result, 0)
        response = json.loads(stdout_buffer.getvalue())
        self.assertEqual(response["systemMessage"], "Stop hook: orchestrator reached")
        receipt_gate_mock.assert_called_once()
        orchestrator_mock.assert_called_once()


class StopHookSkillRoutingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()

    def test_skill_name_for_phase_uses_close_ticket_for_documenting(self) -> None:
        self.assertEqual(self.stop_hook.skill_name_for_phase("documenting"), "close-ticket")


class StopHookTmuxFollowupTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()

    def test_spawn_tmux_followup_requests_json_output(self) -> None:
        ticket = {"path": "tickets/TASK-0033/ticket.md"}
        current_run = {
            "tmux_session": "main",
            "auto_continue": True,
            "run_state": ".harness/runs/task-0033-building.json",
        }
        captured: dict[str, object] = {}

        def fake_run(cmd, text, capture_output, check, cwd):
            captured["cmd"] = cmd
            captured["cwd"] = cwd
            return self.stop_hook.subprocess.CompletedProcess(
                cmd,
                0,
                stdout=json.dumps({"action": "followup", "tmux_pane": "%42"}),
                stderr="",
            )

        with patch.object(self.stop_hook.subprocess, "run", side_effect=fake_run):
            result = self.stop_hook.spawn_tmux_followup(
                ROOT,
                ticket,
                "building",
                current_run,
                "hook-driven follow-up",
            )

        self.assertEqual(result, {"action": "followup", "tmux_pane": "%42"})
        self.assertIn("--json", captured["cmd"])


class StopHookGroundingSummaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()

    def test_extract_grounding_summary_uses_first_non_empty_line_only(self) -> None:
        summary = self.stop_hook.extract_grounding_summary(
            "\n".join(
                [
                    "GROUNDING_SUMMARY: initial summary",
                    "working notes",
                    "GROUNDING_SUMMARY: reviewing TASK-0026 acceptance criteria",
                    "IMPL_RESULT: status=continue_impl next=building reason=test",
                ]
            )
        )

        self.assertEqual(summary, "initial summary")


class StopHookImplLoopGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()
        self.ticket = {
            "ticket_id": "TASK-0053",
            "title": "define impl session activation and stop-hook loop gating",
            "phase": "building",
            "status": "building",
        }
        self.current_run = {
            "ticket_id": "TASK-0053",
            "phase": "building",
            "status": "waiting_for_worker",
            "skill_name": "impl",
            "session_id": "sess-123",
            "impl_loop_active": True,
        }
        self.runtime_claim = {
            "ticket_id": "TASK-0053",
            "phase": "building",
            "status": "running",
            "skill_name": "impl",
            "session_id": "sess-123",
        }

    def test_impl_loop_continuation_allowed_requires_flag_ticket_and_session_match(self) -> None:
        self.assertTrue(
            self.stop_hook.impl_loop_continuation_allowed(
                self.ticket,
                self.current_run,
                self.runtime_claim,
                "sess-123",
            )
        )

    def test_impl_loop_continuation_rejects_auto_continue_without_activation_flag(self) -> None:
        current_run = dict(self.current_run)
        current_run["impl_loop_active"] = False
        current_run["auto_continue"] = True

        self.assertFalse(
            self.stop_hook.impl_loop_continuation_allowed(
                self.ticket,
                current_run,
                self.runtime_claim,
                "sess-123",
            )
        )

    def test_impl_loop_continuation_rejects_mismatched_session_claim(self) -> None:
        runtime_claim = dict(self.runtime_claim)
        runtime_claim["session_id"] = "sess-other"

        self.assertFalse(
            self.stop_hook.impl_loop_continuation_allowed(
                self.ticket,
                self.current_run,
                runtime_claim,
                "sess-123",
            )
        )

    def test_impl_loop_continuation_rejects_ralph_dispatcher_claim(self) -> None:
        runtime_claim = dict(self.runtime_claim)
        runtime_claim["skill_name"] = "ralph"

        self.assertFalse(
            self.stop_hook.impl_loop_continuation_allowed(
                self.ticket,
                self.current_run,
                runtime_claim,
                "sess-123",
            )
        )

    def test_next_impl_loop_active_for_action_clears_terminal_paths(self) -> None:
        self.assertTrue(
            self.stop_hook.next_impl_loop_active_for_action(
                "repeat_impl",
                next_phase="building",
                current_phase="building",
            )
        )
        self.assertTrue(
            self.stop_hook.next_impl_loop_active_for_action(
                "continue_same_ticket",
                current_phase="building",
            )
        )
        self.assertFalse(
            self.stop_hook.next_impl_loop_active_for_action(
                "block_ticket",
                current_phase="building",
            )
        )
        self.assertFalse(
            self.stop_hook.next_impl_loop_active_for_action(
                "route_to_orchestrator",
                current_phase="building",
            )
        )


class StopHookEvidenceArtifactGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()

    def test_load_ticket_exposes_linked_artifacts_for_evidence_gate(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-ticket-") as td:
            root = Path(td)
            ticket_path = root / "tickets" / "TASK-9999" / "ticket.md"
            artifact_path = root / "tickets" / "TASK-9999" / "artifacts" / "qa" / "report.md"
            artifact_path.parent.mkdir(parents=True, exist_ok=True)
            artifact_path.write_text("ok", encoding="utf-8")
            ticket_path.write_text(
                """---
ticket_id: TASK-9999
title: stale packet fixture
phase: building
status: building
owner: codex
priority: medium
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-05T00:00:00Z
updated_at: 2026-04-05T01:30:00Z
next_action: test fixture
last_verification: none
---

# TASK-9999: stale packet fixture

## Acceptance Criteria
- [x] AC-1

## Evidence
- [QA report](tickets/TASK-9999/artifacts/qa/report.md)

## Blockers
- none
""",
                encoding="utf-8",
            )

            ticket = self.stop_hook.load_ticket(ticket_path)
            ok, reason, failures = self.stop_hook.evidence_artifact_gate(ticket)

            self.assertEqual(ticket["updated_at"], "2026-04-05T01:30:00Z")
            self.assertTrue(ok)
            self.assertEqual(reason, "")
            self.assertEqual(failures, [])

    def test_evidence_artifact_gate_fails_when_linked_artifact_is_stale(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-ticket-") as td:
            root = Path(td)
            ticket_path = root / "tickets" / "TASK-9999" / "ticket.md"
            artifact_path = root / "tickets" / "TASK-9999" / "artifacts" / "qa" / "report.md"
            artifact_path.parent.mkdir(parents=True, exist_ok=True)
            artifact_path.write_text("old", encoding="utf-8")
            old_timestamp = datetime(2026, 4, 5, 0, 0, tzinfo=timezone.utc).timestamp()
            os.utime(artifact_path, (old_timestamp, old_timestamp))
            ticket_path.write_text(
                """---
ticket_id: TASK-9999
title: stale evidence fixture
phase: building
status: building
owner: codex
priority: medium
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-05T00:00:00Z
updated_at: 2026-04-05T01:30:00Z
next_action: test fixture
last_verification: none
---

# TASK-9999: stale evidence fixture

## Acceptance Criteria
- [x] AC-1

## Evidence
- [QA report](tickets/TASK-9999/artifacts/qa/report.md)

## Blockers
- none
""",
                encoding="utf-8",
            )

            ticket = self.stop_hook.load_ticket(ticket_path)
            ok, reason, failures = self.stop_hook.evidence_artifact_gate(ticket)

            self.assertFalse(ok)
            self.assertEqual(reason, "evidence artifact gates are not passing")
            self.assertIn("linked_artifacts=stale", failures)


if __name__ == "__main__":
    unittest.main()
