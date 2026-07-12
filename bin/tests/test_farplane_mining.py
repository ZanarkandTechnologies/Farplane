from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from farplane_file_events import create_json_exclusive, outbox_path, pending_events, sha256_value
from farplane_mining import (
    DEFAULT_PROGRAM_ROOT,
    drain_pending,
    list_runs,
    remove_route,
    replay_run,
    rerun_run,
    route_event,
    set_output_verdict,
    set_route,
    show_run,
    validate_routes,
)
from hooks.farplane_file_change import handle_payload


PROGRAM_REF = "core:ticket-completion-lean@1.0.0"


def ticket_text(status: str = "completed") -> str:
    return f"---\nstatus: {status}\n---\n\n# Ticket\n\nProof stays local.\n"


def write_project(root: Path, route_ids: tuple[str, ...] = ("completion",)) -> Path:
    farplane = root / "farplane"
    farplane.mkdir()
    routes = "".join(
        f"  - route_id: {route_id}\n    event_name: farplane.ticket.completed\n    program_ref: {PROGRAM_REF}\n"
        for route_id in route_ids
    )
    (farplane / "bindings.yaml").write_text(
        "kind: project-bindings\nproject:\n  id: mine-test\nmetric_bindings: {}\nevent_routes:\n" + routes,
        encoding="utf-8",
    )
    ticket = root / "tickets" / "TASK-0001" / "ticket.md"
    ticket.parent.mkdir(parents=True)
    ticket.write_text(ticket_text(), encoding="utf-8")
    return ticket


def event_for(ticket: Path) -> dict[str, object]:
    relative = "tickets/TASK-0001/ticket.md"
    return {
        "schema_version": 1,
        "event_id": "a" * 64,
        "event_name": "farplane.ticket.completed",
        "entity_ref": {"kind": "ticket", "id": "TASK-0001", "path": relative},
        "content_hash": sha256_value(ticket.read_text(encoding="utf-8")),
        "terminal": True,
    }


class FarplaneMiningTests(unittest.TestCase):
    def test_partial_fanout_failure_retains_outbox_until_all_routes_succeed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            path = root / "farplane" / "bindings.yaml"
            path.write_text(
                path.read_text(encoding="utf-8")
                + "  - route_id: unavailable\n"
                + "    event_name: farplane.ticket.completed\n"
                + "    program_ref: core:missing@1.0.0\n",
                encoding="utf-8",
            )
            event = event_for(ticket)
            create_json_exclusive(outbox_path(root, str(event["event_id"])), event)

            failed = drain_pending(root)

            self.assertFalse(failed["ok"])
            self.assertEqual(failed["pending"], 1)
            self.assertEqual(len(list_runs(root)), 1)
            remove_route(root, "unavailable")
            recovered = drain_pending(root)
            self.assertTrue(recovered["ok"])
            self.assertEqual(recovered["pending"], 0)
            self.assertEqual(pending_events(root), [])
            detail = show_run(root, list_runs(root)[0]["run_id"])
            self.assertEqual(len(detail["attempts"]), 1)

    def test_hook_drains_before_capture_and_routes_completion_after_capture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            ticket.write_text(ticket_text("todo"), encoding="utf-8")
            hook_payload = {
                "hook_event_name": "PostToolUse",
                "tool_name": "apply_patch",
                "cwd": str(root),
                "session_id": "hook-test",
                "tool_input": {"patch": "*** Update File: tickets/TASK-0001/ticket.md"},
            }
            baseline = handle_payload(hook_payload, root, wait_for_drain=True)
            self.assertEqual(len(baseline["captured_event_ids"]), 1)
            self.assertNotEqual(baseline["drain_launch"]["parent_pid"], baseline["drain_launch"]["child_pid"])
            self.assertEqual(baseline["drain_launch"]["status"], "complete")
            self.assertEqual(list_runs(root), [])

            ticket.write_text(ticket_text("completed"), encoding="utf-8")
            completed = handle_payload(hook_payload, root, wait_for_drain=True)

            self.assertTrue(completed["ok"])
            self.assertEqual(completed["drain_launch"]["status"], "complete")
            self.assertEqual(len(list_runs(root)), 1)

    def test_failed_hook_drain_launch_leaves_pending_event_for_later_drain(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            ticket.write_text(ticket_text("todo"), encoding="utf-8")
            payload = {
                "hook_event_name": "PostToolUse",
                "tool_name": "apply_patch",
                "cwd": str(root),
                "session_id": "hook-test",
                "tool_input": {"patch": "*** Update File: tickets/TASK-0001/ticket.md"},
            }
            handle_payload(payload, root, wait_for_drain=True)
            ticket.write_text(ticket_text("completed"), encoding="utf-8")

            failed = handle_payload(payload, root, drain_command=["/definitely/missing/farplane-miner"])

            self.assertFalse(failed["ok"])
            self.assertEqual(failed["drain_launch"]["status"], "failed_to_launch")
            self.assertEqual(len(pending_events(root)), 1)
            recovered = drain_pending(root)
            self.assertTrue(recovered["ok"])
            self.assertEqual(len(pending_events(root)), 0)
            self.assertEqual(len(list_runs(root)), 1)

    def test_route_fanout_is_deterministic_atomic_and_lean(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root, ("completion-a", "completion-b"))
            event = event_for(ticket)

            first = route_event(event, root)
            second = route_event(event, root)

            self.assertEqual([row["run_id"] for row in first], [row["run_id"] for row in second])
            self.assertEqual(len(set(row["run_id"] for row in first)), 2)
            self.assertEqual(len(list_runs(root)), 2)
            for run in first:
                detail = show_run(root, run["run_id"])
                self.assertEqual(len(detail["attempts"]), 1)
                self.assertNotIn("score", detail["report"])
                self.assertNotIn("reward", detail["report"])
                self.assertNotIn("content", detail["input"])
                self.assertNotIn("body", detail["input"])
                self.assertNotIn("Proof stays local.", json.dumps(detail))
                self.assertFalse(list((root / ".farplane" / "mine" / "runs" / run["run_id"]).glob("*.tmp")))

    def test_concurrent_delivery_claims_one_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            event = event_for(ticket)
            with ThreadPoolExecutor(max_workers=6) as pool:
                results = list(pool.map(lambda _: route_event(event, root)[0]["run_id"], range(12)))

            self.assertEqual(len(set(results)), 1)
            detail = show_run(root, results[0])
            self.assertEqual(len(detail["attempts"]), 1)

    def test_frozen_replay_and_current_source_rerun_have_distinct_semantics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            original = route_event(event_for(ticket), root)[0]
            original_detail = show_run(root, original["run_id"])
            ticket.write_text(ticket_text() + "\nA later edit.\n", encoding="utf-8")

            replayed = replay_run(root, original["run_id"])
            replay_detail = show_run(root, replayed["run_id"])
            rerun = rerun_run(root, original["run_id"])
            rerun_detail = show_run(root, rerun["run_id"])

            self.assertEqual(replayed["run_id"], original["run_id"])
            self.assertEqual(replay_detail["report"], original_detail["report"])
            self.assertEqual(len(replay_detail["attempts"]), 2)
            self.assertNotEqual(rerun["run_id"], original["run_id"])
            self.assertEqual(rerun["parent_run_id"], original["run_id"])
            self.assertEqual(rerun_detail["input"]["source_mode"], "current_rerun")
            self.assertEqual(rerun_detail["report"]["escalation"]["decision"], "deep")
            self.assertEqual(rerun_detail["report"]["source_gaps"][0]["reason"], "source_changed_after_event")

    def test_missing_required_source_is_reported_not_invented(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            event = event_for(ticket)
            ticket.unlink()

            run = route_event(event, root)[0]
            report = show_run(root, run["run_id"])["report"]

            self.assertEqual(report["coverage"]["available"], [])
            self.assertEqual(report["escalation"]["decision"], "deep")
            self.assertEqual(report["source_gaps"][0]["reason"], "required_input_missing")

    def test_route_editor_preserves_unowned_bindings_sections_and_validates_program(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_project(root)
            path = root / "farplane" / "bindings.yaml"
            path.write_text(
                "# owned header\nproject:\n  id: mine-test\nevent_routes:\n"
                "  - route_id: old\n    event_name: farplane.ticket.completed\n"
                f"    program_ref: {PROGRAM_REF}\nmetric_bindings:\n  keep: yes\n",
                encoding="utf-8",
            )

            set_route(
                root,
                route_id="second",
                event_name="farplane.ticket.completed",
                program_ref=PROGRAM_REF,
            )
            edited = path.read_text(encoding="utf-8")
            self.assertTrue(edited.startswith("# owned header\nproject:\n  id: mine-test\n"))
            self.assertIn("metric_bindings:\n  keep: yes\n", edited)
            self.assertTrue(validate_routes(root)["ok"])
            remove_route(root, "old")
            self.assertEqual([row["route_id"] for row in validate_routes(root)["routes"]], ["second"])

    def test_route_validation_rejects_non_object_unknown_event_and_extra_keys(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_project(root)
            path = root / "farplane" / "bindings.yaml"
            path.write_text("event_routes:\n  - not-an-object\n", encoding="utf-8")
            self.assertEqual(validate_routes(root)["issues"], ["invalid_event_routes:entries_must_be_objects"])
            path.write_text(
                "event_routes:\n"
                "  - route_id: invalid\n"
                "    event_name: farplane.unknown\n"
                f"    program_ref: {PROGRAM_REF}\n"
                "    surprise: true\n",
                encoding="utf-8",
            )
            issues = validate_routes(root)["issues"]
            self.assertIn("event_routes.0.event_name_unsupported:farplane.unknown", issues)
            self.assertIn("event_routes.0.unsupported_keys:surprise", issues)

    def test_verdict_is_separate_from_lean_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            run = route_event(event_for(ticket), root)[0]

            verdict = set_output_verdict(root, run["run_id"], "report", "promoted")
            detail = show_run(root, run["run_id"])

            self.assertEqual(verdict["verdict"], "promoted")
            self.assertEqual(detail["verdicts"]["report"]["verdict"], "promoted")
            self.assertNotIn("verdict", detail["report"])

    def test_cli_lists_programs_and_validates_project_routes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_project(root)
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "bin" / "farplane.py"),
                    "mining",
                    "routes",
                    "validate",
                    "--project-root",
                    str(root),
                    "--json",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)["ok"])
            programs = subprocess.run(
                [sys.executable, str(ROOT / "bin" / "farplane.py"), "mining", "programs", "list", "--json"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(programs.returncode, 0, programs.stderr)
            refs = {row["program_ref"] for row in json.loads(programs.stdout)["programs"]}
            self.assertIn(PROGRAM_REF, refs)
            self.assertTrue(DEFAULT_PROGRAM_ROOT.is_dir())


if __name__ == "__main__":
    unittest.main()
