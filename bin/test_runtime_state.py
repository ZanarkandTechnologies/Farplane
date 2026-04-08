from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from user_turn import build_runtime_claim, load_runtime_claim


class RuntimeClaimTests(unittest.TestCase):
    def test_build_runtime_claim_groups_active_ownership(self) -> None:
        claim = build_runtime_claim(
            {
                "ticket_id": "TASK-0035",
                "ticket_path": "/tmp/TASK-0035.md",
                "run_id": "run-task-0035-building-01",
                "phase": "building",
                "status": "running",
                "skill_name": "ralph",
                "session_id": "sess-123",
                "tmux_session": "main",
                "tmux_window": "@5",
                "tmux_pane": "%9",
                "updated_at": "2026-04-08T15:00:00Z",
            }
        )

        self.assertEqual(
            claim,
            {
                "ticket_id": "TASK-0035",
                "ticket_path": "/tmp/TASK-0035.md",
                "run_id": "run-task-0035-building-01",
                "claimed_at": "2026-04-08T15:00:00Z",
                "phase": "building",
                "status": "running",
                "skill_name": "ralph",
                "session_id": "sess-123",
                "tmux_session": "main",
                "tmux_window": "@5",
                "tmux_pane": "%9",
            },
        )

    def test_build_runtime_claim_preserves_existing_claimed_at(self) -> None:
        claim = build_runtime_claim(
            {
                "ticket_id": "TASK-0035",
                "run_id": "run-task-0035-building-01",
                "phase": "building",
                "status": "waiting_for_judge",
                "updated_at": "2026-04-08T16:00:00Z",
                "claim": {
                    "ticket_id": "TASK-0035",
                    "run_id": "run-task-0035-building-01",
                    "claimed_at": "2026-04-08T15:00:00Z",
                    "phase": "building",
                    "status": "running",
                },
            }
        )

        self.assertIsNotNone(claim)
        self.assertEqual(claim["claimed_at"], "2026-04-08T15:00:00Z")
        self.assertEqual(claim["status"], "waiting_for_judge")

    def test_load_runtime_claim_prefers_nested_run_state_claim(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".ralph" / "state"
            state_dir.mkdir(parents=True, exist_ok=True)
            run_state = project_root / ".ralph" / "runs" / "task-0035-building.json"
            run_state.parent.mkdir(parents=True, exist_ok=True)
            run_state.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0035",
                        "run_id": "run-task-0035-building-01",
                        "phase": "building",
                        "status": "running",
                        "claim": {
                            "ticket_id": "TASK-0035",
                            "run_id": "run-task-0035-building-01",
                            "claimed_at": "2026-04-08T15:00:00Z",
                            "phase": "building",
                            "status": "running",
                            "session_id": "sess-123",
                        },
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "current-run.json").write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0035",
                        "run_id": "run-task-0035-building-01",
                        "phase": "building",
                        "status": "running",
                        "run_state": str(run_state.relative_to(project_root)),
                    }
                ),
                encoding="utf-8",
            )

            claim = load_runtime_claim(project_root)

        self.assertIsNotNone(claim)
        self.assertEqual(claim["session_id"], "sess-123")
        self.assertEqual(claim["claimed_at"], "2026-04-08T15:00:00Z")


if __name__ == "__main__":
    unittest.main()
