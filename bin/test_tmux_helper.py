from __future__ import annotations

import importlib.util
import io
import sys
import unittest
from contextlib import redirect_stderr
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TMUX_HELPER_PATH = ROOT / "skills" / "impl" / "scripts" / "tmux_helper.py"


def load_tmux_helper_module():
    bin_dir = str((ROOT / "bin").resolve())
    if bin_dir not in sys.path:
        sys.path.insert(0, bin_dir)
    spec = importlib.util.spec_from_file_location("codexter_tmux_helper_test", TMUX_HELPER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load tmux helper module from {TMUX_HELPER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TmuxHelperBackpressureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmux_helper = load_tmux_helper_module()

    def test_annotate_backpressure_flags_over_budget_waits(self) -> None:
        payload = {
            "status": "running",
            "worker_started_at": "2026-04-10T00:00:00Z",
            "last_checkpoint_at": "2026-04-10T00:00:00Z",
            "worker_name": "builder",
            "main_artifact_path": "tickets/TASK-0034.md",
        }

        annotated = self.tmux_helper.annotate_backpressure(
            payload,
            now=datetime(2026, 4, 10, 0, 1, 20, tzinfo=timezone.utc),
        )

        self.assertEqual(annotated["backpressure_state"], "over_budget")
        self.assertEqual(annotated["stale_for_secs"], 80)
        self.assertEqual(annotated["backpressure_basis"], "last_checkpoint_at")
        self.assertIn("split work", annotated["recommended_action"])

    def test_annotate_backpressure_marks_recent_waits_within_budget(self) -> None:
        payload = {
            "status": "running",
            "worker_started_at": "2026-04-10T00:00:00Z",
            "last_checkpoint_at": "2026-04-10T00:00:30Z",
        }

        annotated = self.tmux_helper.annotate_backpressure(
            payload,
            now=datetime(2026, 4, 10, 0, 1, 0, tzinfo=timezone.utc),
        )

        self.assertEqual(annotated["backpressure_state"], "within_budget")
        self.assertEqual(annotated["stale_for_secs"], 30)
        self.assertNotIn("recommended_action", annotated)

    def test_annotate_backpressure_marks_inactive_non_running_payloads(self) -> None:
        annotated = self.tmux_helper.annotate_backpressure({"status": "complete"})
        self.assertEqual(annotated["backpressure_state"], "inactive")


class TmuxHelperOutputFormattingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmux_helper = load_tmux_helper_module()

    def test_format_followup_success_compacts_payload_for_default_output(self) -> None:
        line = self.tmux_helper.format_followup_success(
            {
                "ticket": str(ROOT / "tickets" / "TASK-0025-capture-turn-start-intent-for-stop-hook.md"),
                "phase": "building",
                "tmux_pane": "%42",
                "tmux_session": "main",
                "run_state": str(
                    ROOT / ".harness" / "runs" / "task-0025-building-20260410T091500000000Z.json"
                ),
            }
        )

        self.assertEqual(
            line,
            "followup ok: TASK-0025 -> building pane=%42 session=main run=.harness/runs/task-0025-building-20260410T091500000000Z.json",
        )

    def test_print_followup_failure_keeps_actionable_shape(self) -> None:
        stderr_buffer = io.StringIO()
        with redirect_stderr(stderr_buffer):
            exit_code = self.tmux_helper.print_followup_failure(
                "TASK-0025",
                "building",
                "tmux send-keys failed",
                pane_id="%42",
                stderr="pane no longer exists",
            )

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            stderr_buffer.getvalue(),
            "followup failed: TASK-0025 -> building | tmux send-keys failed | pane=%42\npane no longer exists\n",
        )
