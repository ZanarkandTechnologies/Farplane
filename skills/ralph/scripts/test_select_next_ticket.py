#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().with_name("select_next_ticket.py")
SPEC = importlib.util.spec_from_file_location("select_next_ticket", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"could not load {SCRIPT}")
selector = importlib.util.module_from_spec(SPEC)
sys.modules["select_next_ticket"] = selector
SPEC.loader.exec_module(selector)


def write_workflow(root: Path, *, board_source: str = "tickets/") -> None:
    (root / "WORKFLOW.md").write_text(
        f"""\
---
workflow:
  name: test-ralph
  version: 1

board:
  adapter: filesystem
  source: {board_source}
  active_phases: ["planning", "building", "documenting"]
  terminal_statuses: ["done", "failed"]

compute:
  default: local_shared
  allowed: ["local_shared", "local_worktree"]
  ticket_override_field: compute_target

routing:
  planning: impl-plan
  building: impl
  documenting: close-ticket

quality:
  writes_proof_packet: true
---

# Test Ralph Workflow
""",
        encoding="utf-8",
    )


def write_ticket(
    root: Path,
    ticket_id: str,
    frontmatter: dict[str, object],
    body: str = "",
    *,
    source: str = "tickets",
) -> Path:
    ticket_dir = root / source / ticket_id
    ticket_dir.mkdir(parents=True, exist_ok=True)
    path = ticket_dir / "ticket.md"
    defaults: dict[str, object] = {
        "ticket_id": ticket_id,
        "title": "example",
        "phase": "building",
        "status": "building",
        "owner": "codex",
        "claimed_by": "",
        "priority": "medium",
        "depends_on": [],
        "blocked_by": [],
        "ready": True,
        "approval_required": False,
        "next_action": "continue",
    }
    defaults.update(frontmatter)
    lines = ["---"]
    for key, value in defaults.items():
        if isinstance(value, list):
            if value:
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"{key}: []")
        elif isinstance(value, bool):
            lines.append(f"{key}: {str(value).lower()}")
        else:
            lines.append(f"{key}: {value}")
    lines.extend(["---", f"# {ticket_id}: example", body])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def archive_ticket(root: Path, ticket_id: str, *, source: str = "tickets") -> None:
    source_path = root / source / ticket_id / "ticket.md"
    target = root / source / "archive" / ticket_id / "ticket.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    text = source_path.read_text(encoding="utf-8").replace("status: building", "status: done")
    target.write_text(text, encoding="utf-8")
    source_path.unlink()


class RalphSelectorTests(unittest.TestCase):
    def test_selects_ready_building_ticket(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-0001", {"phase": "planning", "status": "review", "priority": "high"})
            write_ticket(root, "TASK-0002", {"phase": "building", "status": "building", "priority": "medium"})

            result = selector.select_next_ticket(selector.load_board(root))

        self.assertEqual(result["status"], "selected")
        self.assertEqual(result["selected_ticket_id"], "TASK-0002")
        self.assertEqual(result["recommended_skill"], "impl")
        self.assertEqual(result["selected"]["compute"]["target"], "local_shared")

    def test_stops_when_human_gate_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-0001", {"approval_required": True, "ready": False})

            result = selector.select_next_ticket(selector.load_board(root))

        self.assertEqual(result["status"], "stop")
        self.assertEqual(result["reason"], "human gate required")
        self.assertIn("approval required", result["skipped"][0]["reason"])

    def test_skips_blocked_claimed_and_unresolved_dependency_tickets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-0001", {"blocked_by": ["TASK-0099"]})
            write_ticket(root, "TASK-0002", {"claimed_by": "agent-02"})
            write_ticket(root, "TASK-0003", {"depends_on": ["TASK-0098"]})

            result = selector.select_next_ticket(selector.load_board(root))
            reasons = {item["ticket_id"]: item["reason"] for item in result["skipped"]}

        self.assertEqual(result["status"], "stop")
        self.assertIn("blocked by TASK-0099", reasons["TASK-0001"])
        self.assertIn("claimed by agent-02", reasons["TASK-0002"])
        self.assertIn("unresolved dependencies: TASK-0098", reasons["TASK-0003"])

    def test_dependency_can_be_satisfied_by_archive_or_ticket_body_waiver(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-0001", {})
            archive_ticket(root, "TASK-0001")
            write_ticket(root, "TASK-0002", {"depends_on": ["TASK-0001"], "priority": "low"})
            write_ticket(
                root,
                "TASK-0003",
                {"depends_on": ["TASK-0099"], "priority": "high"},
                body="- TASK-0099 is explicitly waived for this guarded v0.",
            )

            result = selector.select_next_ticket(selector.load_board(root))

        self.assertEqual(result["status"], "selected")
        self.assertEqual(result["selected_ticket_id"], "TASK-0003")

    def test_configured_board_source_uses_matching_archive_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_workflow(root, board_source="project-tickets/")
            write_ticket(root, "TASK-0001", {}, source="project-tickets")
            archive_ticket(root, "TASK-0001", source="project-tickets")
            write_ticket(
                root,
                "TASK-0002",
                {"depends_on": ["TASK-0001"]},
                source="project-tickets",
            )

            result = selector.select_next_ticket(selector.load_board(root))

        self.assertEqual(result["status"], "selected")
        self.assertEqual(result["selected_ticket_id"], "TASK-0002")
        self.assertEqual(result["selected_path"], "project-tickets/TASK-0002/ticket.md")

    def test_future_compute_targets_are_skipped_without_local_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-0001", {"compute_target": "symphony"})
            write_ticket(root, "TASK-0002", {"compute_target": "codex_cloud"})

            result = selector.select_next_ticket(selector.load_board(root))
            skipped = {item["ticket_id"]: item for item in result["skipped"]}

        self.assertEqual(result["status"], "stop")
        self.assertIsNone(result["selected_ticket_id"])
        self.assertIn("unsupported_target", skipped["TASK-0001"]["blocker_codes"])
        self.assertIn("unsupported_target", skipped["TASK-0002"]["blocker_codes"])
        self.assertEqual(skipped["TASK-0001"]["compute"]["target"], "symphony")
        self.assertEqual(skipped["TASK-0002"]["compute"]["target"], "codex_cloud")

    def test_local_worktree_requires_runtime_record_and_setup_hint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-0001", {"compute_target": "local_worktree"})

            result = selector.select_next_ticket(selector.load_board(root))
            skipped = result["skipped"][0]

        self.assertEqual(result["status"], "stop")
        self.assertIn("missing_worktree_runtime", skipped["blocker_codes"])
        self.assertIn("ticket_runtime.py ensure", skipped["required_setup"][0])
        self.assertEqual(skipped["compute"]["target"], "local_worktree")

    def test_local_worktree_selects_when_runtime_record_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-0001", {"compute_target": "local_worktree"})
            runtime_record = root / ".harness" / "state" / "tickets" / "TASK-0001.runtime.json"
            runtime_record.parent.mkdir(parents=True, exist_ok=True)
            runtime_record.write_text('{"ticket_id":"TASK-0001"}\n', encoding="utf-8")

            result = selector.select_next_ticket(selector.load_board(root))

        self.assertEqual(result["status"], "selected")
        self.assertEqual(result["selected_ticket_id"], "TASK-0001")
        self.assertEqual(result["selected"]["compute"]["target"], "local_worktree")
        self.assertEqual(result["selected"]["compute"]["runtimeRecordPath"], str(runtime_record.resolve()))


if __name__ == "__main__":
    unittest.main()
