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


def write_ticket(root: Path, ticket_id: str, frontmatter: dict[str, object], body: str = "") -> Path:
    ticket_dir = root / "tickets" / ticket_id
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


def archive_ticket(root: Path, ticket_id: str) -> None:
    source = root / "tickets" / ticket_id / "ticket.md"
    target = root / "tickets" / "archive" / ticket_id / "ticket.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8").replace("status: building", "status: done")
    target.write_text(text, encoding="utf-8")
    source.unlink()


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


if __name__ == "__main__":
    unittest.main()
