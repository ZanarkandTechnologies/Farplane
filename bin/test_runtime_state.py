from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from user_turn import (
    build_runtime_claim,
    capture_user_turn,
    load_current_run,
    load_runtime_claim,
    session_state_path,
)


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
                "worker_name": "builder",
                "main_artifact_path": "/tmp/TASK-0035.md",
                "grounding_summary": "reviewing TASK-0035 acceptance criteria",
                "worker_started_at": "2026-04-08T14:59:00Z",
                "last_checkpoint_at": "2026-04-08T15:00:00Z",
                "checkpoint_summary": "worker launched",
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
                "worker_name": "builder",
                "main_artifact_path": "/tmp/TASK-0035.md",
                "grounding_summary": "reviewing TASK-0035 acceptance criteria",
                "worker_started_at": "2026-04-08T14:59:00Z",
                "last_checkpoint_at": "2026-04-08T15:00:00Z",
                "checkpoint_summary": "worker launched",
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
            state_dir = project_root / ".harness" / "state"
            state_dir.mkdir(parents=True, exist_ok=True)
            run_state = project_root / ".harness" / "runs" / "task-0035-building.json"
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

    def test_load_current_run_prefers_session_state_over_global_pointer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".harness" / "state"
            state_dir.mkdir(parents=True, exist_ok=True)
            session_path = session_state_path(project_root, "sess-123")
            session_path.parent.mkdir(parents=True, exist_ok=True)
            session_path.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-1234",
                        "run_id": "run-task-1234-building-01",
                        "phase": "building",
                        "status": "running",
                        "session_id": "sess-123",
                        "last_user_turn": {"turn_id": "turn-a", "raw_text": "build task 1234"},
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "current-run.json").write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-9999",
                        "run_id": "run-task-9999-building-01",
                        "phase": "building",
                        "status": "running",
                        "session_id": "sess-other",
                    }
                ),
                encoding="utf-8",
            )

            current = load_current_run(project_root, session_id="sess-123")

        self.assertIsNotNone(current)
        assert current is not None
        self.assertEqual(current["ticket_id"], "TASK-1234")
        self.assertEqual(current["session_id"], "sess-123")

    def test_load_current_run_explicit_run_state_outranks_session_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            run_state = project_root / ".harness" / "runs" / "task-0042-building.json"
            run_state.parent.mkdir(parents=True, exist_ok=True)
            run_state.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0042",
                        "run_id": "run-task-0042-building-01",
                        "phase": "building",
                        "status": "running",
                    }
                ),
                encoding="utf-8",
            )
            session_path = session_state_path(project_root, "sess-123")
            session_path.parent.mkdir(parents=True, exist_ok=True)
            session_path.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-9999",
                        "run_id": "run-task-9999-building-01",
                        "phase": "building",
                        "status": "running",
                        "session_id": "sess-123",
                    }
                ),
                encoding="utf-8",
            )

            current = load_current_run(
                project_root,
                session_id="sess-123",
                explicit_run_state=str(run_state.relative_to(project_root)),
            )

        self.assertIsNotNone(current)
        assert current is not None
        self.assertEqual(current["ticket_id"], "TASK-0042")
        self.assertEqual(current["run_state"], str(run_state.relative_to(project_root)))

    def test_load_current_run_ignores_legacy_ralph_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".ralph" / "state"
            state_dir.mkdir(parents=True, exist_ok=True)
            (state_dir / "current-run.json").write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-7777",
                        "run_id": "run-task-7777-building-01",
                        "phase": "building",
                        "status": "running",
                    }
                ),
                encoding="utf-8",
            )

            current = load_current_run(project_root)

        self.assertIsNone(current)

    def test_capture_user_turn_updates_only_resolved_session_lane(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".harness" / "state"
            state_dir.mkdir(parents=True, exist_ok=True)

            run_state_a = project_root / ".harness" / "runs" / "task-0042-building.json"
            run_state_b = project_root / ".harness" / "runs" / "task-0041-planning.json"
            run_state_a.parent.mkdir(parents=True, exist_ok=True)
            run_state_a.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0042",
                        "run_id": "run-task-0042-building-01",
                        "phase": "building",
                        "status": "running",
                        "session_id": "sess-a",
                    }
                ),
                encoding="utf-8",
            )
            run_state_b.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0041",
                        "run_id": "run-task-0041-planning-01",
                        "phase": "planning",
                        "status": "running",
                        "session_id": "sess-b",
                        "last_user_turn": {"turn_id": "turn-b", "raw_text": "plan task 41"},
                    }
                ),
                encoding="utf-8",
            )
            session_state_a = session_state_path(project_root, "sess-a")
            session_state_b = session_state_path(project_root, "sess-b")
            session_state_a.parent.mkdir(parents=True, exist_ok=True)
            session_state_a.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0042",
                        "run_id": "run-task-0042-building-01",
                        "phase": "building",
                        "status": "running",
                        "session_id": "sess-a",
                        "run_state": str(run_state_a.relative_to(project_root)),
                    }
                ),
                encoding="utf-8",
            )
            session_state_b.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0041",
                        "run_id": "run-task-0041-planning-01",
                        "phase": "planning",
                        "status": "running",
                        "session_id": "sess-b",
                        "run_state": str(run_state_b.relative_to(project_root)),
                        "last_user_turn": {"turn_id": "turn-b", "raw_text": "plan task 41"},
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "current-run.json").write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0041",
                        "run_id": "run-task-0041-planning-01",
                        "phase": "planning",
                        "status": "running",
                        "session_id": "sess-b",
                        "run_state": str(run_state_b.relative_to(project_root)),
                    }
                ),
                encoding="utf-8",
            )

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="Implement TASK-0042 in this session only.",
                turn_id="turn-a",
                source="test",
                session_id="sess-a",
            )

            session_a = json.loads(session_state_a.read_text(encoding="utf-8"))
            session_b = json.loads(session_state_b.read_text(encoding="utf-8"))
            persisted_run_state_a = json.loads(run_state_a.read_text(encoding="utf-8"))

        self.assertIsNotNone(captured)
        assert captured is not None
        self.assertEqual(captured["turn_id"], "turn-a")
        self.assertEqual(session_a["last_user_turn"]["turn_id"], "turn-a")
        self.assertEqual(session_a["last_user_turn"]["raw_text"], "Implement TASK-0042 in this session only.")
        self.assertEqual(session_b["last_user_turn"]["turn_id"], "turn-b")
        self.assertEqual(persisted_run_state_a["last_user_turn"]["turn_id"], "turn-a")


if __name__ == "__main__":
    unittest.main()
