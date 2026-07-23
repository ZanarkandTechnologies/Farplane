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

from farplane_event_store import create_json_exclusive, outbox_path, pending_events, sha256_value
from farplane_mining import (
    DEFAULT_PROGRAM_ROOT,
    MiningError,
    drain_pending,
    list_runs,
    mine_ticket,
    remove_route,
    replay_run,
    rerun_run,
    route_event,
    set_output_verdict,
    set_route,
    show_run,
    validate_routes,
)


PROGRAM_REF = "core:ticket-completion-lean@1.0.0"
LEARNING_PROGRAM_REF = "core:ticket-completion-learning@1.3.0"


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
    (farplane / "metrics.yaml").write_text(
        "kind: project-metrics\nmetrics:\n  accepted_harness_improvements:\n    direction: maximize\n",
        encoding="utf-8",
    )
    (farplane / "harness.yaml").write_text(
        "kind: project-harness\nareas:\n  self_improvement:\n    metric_refs:\n      - metric_id: accepted_harness_improvements\n",
        encoding="utf-8",
    )
    ticket = root / "tickets" / "TASK-0001" / "ticket.md"
    ticket.parent.mkdir(parents=True)
    ticket.write_text(ticket_text(), encoding="utf-8")
    return ticket


def event_for(ticket: Path) -> dict[str, object]:
    tickets_index = ticket.parts.index("tickets")
    relative = Path(*ticket.parts[tickets_index:]).as_posix()
    ticket_id = ticket.parent.name
    return {
        "schema_version": 1,
        "event_id": "a" * 64,
        "event_name": "farplane.ticket.completed",
        "entity_ref": {"kind": "ticket", "id": ticket_id, "path": relative},
        "content_hash": sha256_value(ticket.read_text(encoding="utf-8")),
        "terminal": True,
        "provenance": {"source": "ticket_close", "session_id": "sess-1", "thread_id": "sess-1"},
    }


class FarplaneMiningTests(unittest.TestCase):
    def test_mine_ticket_resolves_archived_ticket_and_associated_thread_from_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            (root / "farplane" / "bindings.yaml").write_text(
                "kind: project-bindings\nproject:\n  id: mine-test\nevent_routes:\n"
                "  - route_id: completion-learning\n"
                "    event_name: farplane.ticket.completed\n"
                f"    program_ref: {LEARNING_PROGRAM_REF}\n",
                encoding="utf-8",
            )
            archive = root / "tickets" / "archive" / "TASK-0001"
            archive.parent.mkdir(parents=True)
            ticket.parent.rename(archive)
            state = root / ".farplane" / "state"
            state.mkdir(parents=True)
            (state / "ticket-thread-associations.jsonl").write_text(
                json.dumps({"ticket_id": "TASK-0001", "thread_id": "thread-1"}) + "\n",
                encoding="utf-8",
            )

            def no_signal_runner(command: list[str], prompt: str, cwd: Path, timeout: int):
                Path(command[command.index("--output-last-message") + 1]).write_text(
                    json.dumps({
                        "status": "no_signal",
                        "summary": "No actionable issue found.",
                        "material_findings": [],
                        "source_gaps": [],
                    }),
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            first = mine_ticket(root, "task-0001", codex_runner=no_signal_runner)
            second = mine_ticket(root, "TASK-0001", codex_runner=no_signal_runner)

            self.assertEqual(first["ticket_path"], "tickets/archive/TASK-0001/ticket.md")
            self.assertEqual(first["thread_id"], "thread-1")
            self.assertEqual(first["runs"][0]["run_id"], second["runs"][0]["run_id"])
            detail = show_run(root, first["runs"][0]["run_id"])
            self.assertEqual(detail["report"]["ticket_output"]["reason"], "report_status:no_signal")

            archived_ticket = archive / "ticket.md"
            archived_ticket.write_text(ticket_text("todo"), encoding="utf-8")
            with self.assertRaisesRegex(MiningError, "ticket_not_terminal:TASK-0001"):
                mine_ticket(root, "TASK-0001", codex_runner=no_signal_runner)

    def test_completion_learning_joins_bounded_window_and_runs_once(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            bindings = root / "farplane" / "bindings.yaml"
            bindings.write_text(
                "event_routes:\n"
                "  - route_id: completion-learning\n"
                "    event_name: farplane.ticket.completed\n"
                f"    program_ref: {LEARNING_PROGRAM_REF}\n",
                encoding="utf-8",
            )
            window_dir = root / ".farplane" / "state" / "message-windows"
            window_dir.mkdir(parents=True)
            raw_prompt = "This correction should become a reusable skill instead of another manual fix."
            (window_dir / "sess-1.json").write_text(
                json.dumps(
                    {
                        "session_id": "sess-1",
                        "turn_count": 1,
                        "rolling_exchanges": [
                            {
                                "user_turn_id": "turn-1",
                                "user_turn": {"turn_id": "turn-1", "raw_text": raw_prompt},
                                "assistant_text": "Implemented the direct repair.",
                            }
                        ],
                        "pending_user_turn": {},
                    }
                ),
                encoding="utf-8",
            )
            calls = []

            def fake_runner(command: list[str], prompt: str, cwd: Path, timeout: int):
                calls.append((command, prompt, cwd, timeout))
                output_path = Path(command[command.index("--output-last-message") + 1])
                output_path.write_text(
                    json.dumps(
                        {
                            "status": "complete",
                            "summary": "One reusable workflow opportunity found.",
                            "material_findings": [
                                {
                                    "issue": "The same correction requires manual reconstruction.",
                                    "inefficiency": "The skill-signature workflow is rebuilt manually on every occurrence.",
                                    "proposed_improvement": "Create or refine the owning reusable skill.",
                                    "dedupe_key": "repeated_correction_workflow",
                                    "owner_surface": "skill",
                                    "evidence_refs": ["tickets/TASK-0001/ticket.md", "turn-1"],
                                    "confidence": "high",
                                }
                            ],
                            "source_gaps": [],
                        }
                    ),
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            first = route_event(event_for(ticket), root, codex_runner=fake_runner)
            second = route_event(event_for(ticket), root, codex_runner=fake_runner)

            self.assertEqual(len(first), 1)
            self.assertEqual([row["run_id"] for row in first], [row["run_id"] for row in second])
            self.assertEqual(len(calls), 1)
            learning = next(show_run(root, row["run_id"]) for row in first if row["program_ref"] == LEARNING_PROGRAM_REF)
            self.assertTrue(learning["input"]["semantic_context"]["conversation_window_found"])
            self.assertEqual(learning["report"]["material_findings"][0]["owner_surface"], "skill")
            self.assertEqual(learning["report"]["ticket_output"]["decision"], "created")
            self.assertEqual(learning["report"]["ticket_output"]["mode"], "improve_or_reject")
            self.assertIn(learning["report"]["ticket_output"]["ticket_path"], learning["run"]["outputs"])
            projected = root / learning["report"]["ticket_output"]["ticket_path"]
            self.assertTrue(projected.is_file())
            projected_text = projected.read_text(encoding="utf-8")
            self.assertIn("status: todo", projected_text)
            self.assertIn("title: \"Improve repeated correction workflow\"", projected_text)
            self.assertNotIn("## Reward", projected_text)
            self.assertIn("mode: improve_or_reject", projected_text)
            self.assertIn("completion_learning_fingerprint:", projected_text)
            self.assertEqual(len(list((root / "tickets").glob("TASK-*/ticket.md"))), 2)
            replay_run(root, learning["run"]["run_id"], codex_runner=fake_runner)
            replay_detail = show_run(root, learning["run"]["run_id"])
            self.assertEqual(replay_detail["report"]["ticket_output"]["decision"], "created")
            self.assertEqual(len(list((root / "tickets").glob("TASK-*/ticket.md"))), 2)
            self.assertNotIn(raw_prompt, json.dumps(learning["report"]))
            self.assertNotIn("assistant_text", json.dumps(learning["input"]["semantic_context"]["conversation_window"]))
            self.assertIn("--disable", calls[0][0])
            self.assertIn("read-only", calls[0][0])
            self.assertIn("--ignore-user-config", calls[0][0])
            self.assertIn("--ignore-rules", calls[0][0])

    def test_completion_learning_redelivery_reuses_frozen_window(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            (root / "farplane" / "bindings.yaml").write_text(
                "event_routes:\n"
                "  - route_id: completion-learning\n"
                "    event_name: farplane.ticket.completed\n"
                f"    program_ref: {LEARNING_PROGRAM_REF}\n",
                encoding="utf-8",
            )
            window_dir = root / ".farplane" / "state" / "message-windows"
            window_dir.mkdir(parents=True)
            window_path = window_dir / "sess-1.json"
            window_path.write_text(
                json.dumps({"session_id": "sess-1", "rolling_exchanges": [], "pending_user_turn": {"user_turn_id": "turn-1", "user_text": "first correction"}}),
                encoding="utf-8",
            )
            calls = []

            def fake_runner(command: list[str], prompt: str, cwd: Path, timeout: int):
                calls.append(prompt)
                Path(command[command.index("--output-last-message") + 1]).write_text(
                    json.dumps({
                        "status": "no_signal",
                        "summary": "No reusable pattern found.",
                        "material_findings": [],
                        "source_gaps": [],
                    }),
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            first = route_event(event_for(ticket), root, codex_runner=fake_runner)[0]
            window_path.write_text(
                json.dumps({"session_id": "sess-1", "rolling_exchanges": [], "pending_user_turn": {"user_turn_id": "turn-2", "user_text": "later unrelated message"}}),
                encoding="utf-8",
            )
            second = route_event(event_for(ticket), root, codex_runner=fake_runner)[0]

            self.assertEqual(first["run_id"], second["run_id"])
            self.assertEqual(len(calls), 1)
            detail = show_run(root, first["run_id"])
            self.assertEqual(detail["input"]["semantic_context"]["conversation_window"]["pending_user_turn"]["user_turn_id"], "turn-1")
            self.assertEqual(detail["report"]["ticket_output"]["decision"], "no_ticket")
            self.assertEqual(detail["report"]["ticket_output"]["reason"], "report_status:no_signal")
            self.assertEqual(len(list((root / "tickets").glob("TASK-*/ticket.md"))), 1)

    def test_completion_learning_projects_improvement_once_and_skips_low_confidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            (root / "farplane" / "bindings.yaml").write_text(
                "event_routes:\n"
                "  - route_id: completion-learning\n"
                "    event_name: farplane.ticket.completed\n"
                f"    program_ref: {LEARNING_PROGRAM_REF}\n",
                encoding="utf-8",
            )
            window_dir = root / ".farplane" / "state" / "message-windows"
            window_dir.mkdir(parents=True)
            (window_dir / "sess-1.json").write_text(
                json.dumps({"session_id": "sess-1", "pending_user_turn": {"user_turn_id": "turn-1", "user_text": "fix the repeated validator failure"}}),
                encoding="utf-8",
            )
            confidence = "high"
            problem = "The same validator rejects valid ticket timestamps."
            pattern = "Canonicalize supported YAML scalar values before hashing."
            solution = "Encode date and datetime values deterministically and retain fail-closed behavior."
            dedupe_key = "yaml_scalar_canonicalization"
            evidence_ticket = "tickets/TASK-0001/ticket.md"

            def fake_runner(command: list[str], prompt: str, cwd: Path, timeout: int):
                Path(command[command.index("--output-last-message") + 1]).write_text(
                    json.dumps({
                        "status": "complete",
                        "summary": "One validator correction is actionable.",
                        "material_findings": [{
                            "issue": problem,
                            "inefficiency": pattern,
                            "proposed_improvement": solution,
                            "dedupe_key": dedupe_key,
                            "owner_surface": "validator",
                            "evidence_refs": [evidence_ticket, "turn-1"],
                            "confidence": confidence,
                        }],
                        "source_gaps": [],
                    }),
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            first_event = event_for(ticket)
            first_event["event_id"] = "b" * 64
            first = route_event(first_event, root, codex_runner=fake_runner)[0]
            first_detail = show_run(root, first["run_id"])
            self.assertEqual(first_detail["report"]["ticket_output"]["decision"], "created")
            self.assertEqual(first_detail["report"]["ticket_output"]["mode"], "improve_or_reject")
            created_path = root / first_detail["report"]["ticket_output"]["ticket_path"]
            self.assertIn("mode: improve_or_reject", created_path.read_text(encoding="utf-8"))

            second_event = {**first_event, "event_id": "c" * 64}
            second = route_event(second_event, root, codex_runner=fake_runner)[0]
            second_detail = show_run(root, second["run_id"])
            self.assertEqual(second_detail["report"]["ticket_output"]["decision"], "existing")
            self.assertEqual(second_detail["report"]["ticket_output"]["ticket_path"], created_path.relative_to(root).as_posix())
            self.assertEqual(len(list((root / "tickets").glob("TASK-*/ticket.md"))), 2)

            created_path.write_text(
                created_path.read_text(encoding="utf-8")
                .replace("status: todo", "status: completed", 1)
                .replace("## Notes", f"## Large Evidence\n\n{'x' * 26_000}\n\n## Notes", 1),
                encoding="utf-8",
            )
            problem = "A new wording tries to extend the generated learning ticket."
            pattern = "Continue projecting follow-up learning tickets."
            solution = "Create another follow-up ticket."
            dedupe_key = "followup_learning_projection"
            evidence_ticket = created_path.relative_to(root).as_posix()
            recursive_event = event_for(created_path)
            recursive_event["event_id"] = "d" * 64
            recursive = route_event(recursive_event, root, codex_runner=fake_runner)[0]
            recursive_detail = show_run(root, recursive["run_id"])
            self.assertNotIn(
                "generated_by: core:ticket-completion-learning",
                recursive_detail["input"]["semantic_context"]["ticket_packet"][0]["text"],
            )
            self.assertTrue(
                recursive_detail["input"]["semantic_context"]["source_lineage"]["generated_by_completion_learning"]
            )
            self.assertEqual(recursive_detail["report"]["ticket_output"]["decision"], "no_ticket")
            self.assertEqual(
                recursive_detail["report"]["ticket_output"]["reason"],
                "recursive_source_projection_blocked",
            )
            self.assertEqual(len(list((root / "tickets").glob("TASK-*/ticket.md"))), 2)

            problem = "Supported ticket dates are incorrectly rejected by the validator"
            pattern = "Normalize valid YAML date-like scalars before computing their digest"
            solution = "Use one deterministic encoding for dates while keeping invalid values closed"
            dedupe_key = "yaml_scalar_canonicalization"
            evidence_ticket = "tickets/TASK-0001/ticket.md"
            punctuation_event = {**first_event, "event_id": "e" * 64}
            punctuation_run = route_event(punctuation_event, root, codex_runner=fake_runner)[0]
            punctuation_detail = show_run(root, punctuation_run["run_id"])
            self.assertEqual(punctuation_detail["report"]["ticket_output"]["decision"], "existing")
            self.assertEqual(
                punctuation_detail["report"]["ticket_output"]["ticket_path"],
                created_path.relative_to(root).as_posix(),
            )
            self.assertEqual(len(list((root / "tickets").glob("TASK-*/ticket.md"))), 2)

            confidence = "low"
            third_event = {**first_event, "event_id": "f" * 64}
            third = route_event(third_event, root, codex_runner=fake_runner)[0]
            third_detail = show_run(root, third["run_id"])
            self.assertEqual(third_detail["report"]["ticket_output"]["decision"], "no_ticket")
            self.assertEqual(third_detail["report"]["ticket_output"]["reason"], "no_actionable_finding")
            self.assertEqual(len(list((root / "tickets").glob("TASK-*/ticket.md"))), 2)

            confidence = "high"
            problem = "A separate completion guard still wastes a manual verification step."
            dedupe_key = "manual_completion_verification"
            (root / "farplane" / "metrics.yaml").unlink()
            (root / "farplane" / "harness.yaml").unlink()
            fourth_event = {**first_event, "event_id": "1" * 64}
            fourth = route_event(fourth_event, root, codex_runner=fake_runner)[0]
            fourth_detail = show_run(root, fourth["run_id"])
            self.assertEqual(fourth_detail["report"]["ticket_output"]["decision"], "created")
            self.assertEqual(fourth_detail["report"]["ticket_output"]["status"], "todo")
            no_kpi_ticket = root / fourth_detail["report"]["ticket_output"]["ticket_path"]
            no_kpi_text = no_kpi_ticket.read_text(encoding="utf-8")
            self.assertIn("status: todo", no_kpi_text)
            self.assertNotIn("## Reward", no_kpi_text)

    def test_completion_learning_selects_strongest_finding_independent_of_model_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            (root / "farplane" / "bindings.yaml").write_text(
                "event_routes:\n"
                "  - route_id: completion-learning\n"
                "    event_name: farplane.ticket.completed\n"
                f"    program_ref: {LEARNING_PROGRAM_REF}\n",
                encoding="utf-8",
            )
            window_dir = root / ".farplane" / "state" / "message-windows"
            window_dir.mkdir(parents=True)
            (window_dir / "sess-1.json").write_text(
                json.dumps({"session_id": "sess-1", "pending_user_turn": {"user_turn_id": "turn-1", "user_text": "review completion"}}),
                encoding="utf-8",
            )

            def fake_runner(command: list[str], prompt: str, cwd: Path, timeout: int):
                Path(command[command.index("--output-last-message") + 1]).write_text(
                    json.dumps({
                        "status": "complete",
                        "summary": "Two accepted findings with different strengths.",
                        "material_findings": [
                            {
                                "issue": "A possible workflow improvement needs proof.",
                                "inefficiency": "The optional workflow adds repeated manual work.",
                                "proposed_improvement": "Run a bounded proof.",
                                "dedupe_key": "optional_workflow_proof",
                                "owner_surface": "skill",
                                "evidence_refs": ["tickets/TASK-0001/ticket.md", "turn-1"],
                                "confidence": "medium",
                            },
                            {
                                "issue": "A completion validator accepts invalid state.",
                                "inefficiency": "Invalid state requires manual detection after completion.",
                                "proposed_improvement": "Add the missing validation branch and regression.",
                                "dedupe_key": "invalid_completion_state",
                                "owner_surface": "validator",
                                "evidence_refs": ["tickets/TASK-0001/ticket.md", "turn-1"],
                                "confidence": "high",
                            },
                        ],
                        "source_gaps": [],
                    }),
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            run = route_event(event_for(ticket), root, codex_runner=fake_runner)[0]
            detail = show_run(root, run["run_id"])
            receipt = detail["report"]["ticket_output"]
            self.assertEqual(receipt["decision"], "created")
            self.assertEqual(receipt["mode"], "improve_or_reject")
            projected = (root / receipt["ticket_path"]).read_text(encoding="utf-8")
            self.assertIn("A completion validator accepts invalid state", projected)
            self.assertNotIn("A possible workflow improvement needs proof", projected)

    def test_completion_learning_runs_from_ticket_when_window_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            (root / "farplane" / "bindings.yaml").write_text(
                "event_routes:\n"
                "  - route_id: completion-learning\n"
                "    event_name: farplane.ticket.completed\n"
                f"    program_ref: {LEARNING_PROGRAM_REF}\n",
                encoding="utf-8",
            )

            def no_signal_runner(command: list[str], prompt: str, cwd: Path, timeout: int):
                Path(command[command.index("--output-last-message") + 1]).write_text(
                    json.dumps({
                        "status": "no_signal",
                        "summary": "No actionable issue found in the ticket packet.",
                        "material_findings": [],
                        "source_gaps": [],
                    }),
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            run = route_event(event_for(ticket), root, codex_runner=no_signal_runner)[0]
            report = show_run(root, run["run_id"])["report"]

            self.assertEqual(report["status"], "no_signal")
            self.assertEqual(report["source_gaps"], [])
            self.assertEqual(report["material_findings"], [])
            self.assertEqual(report["ticket_output"]["reason"], "report_status:no_signal")

    def test_completion_learning_executor_failure_is_reported_and_replayable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            (root / "farplane" / "bindings.yaml").write_text(
                "event_routes:\n"
                "  - route_id: completion-learning\n"
                "    event_name: farplane.ticket.completed\n"
                f"    program_ref: {LEARNING_PROGRAM_REF}\n",
                encoding="utf-8",
            )
            window_dir = root / ".farplane" / "state" / "message-windows"
            window_dir.mkdir(parents=True)
            (window_dir / "sess-1.json").write_text(
                json.dumps({"session_id": "sess-1", "turn_count": 1, "rolling_exchanges": [], "pending_user_turn": {"raw_text": "review this"}}),
                encoding="utf-8",
            )

            attempts = 0

            def recovering_runner(command: list[str], prompt: str, cwd: Path, timeout: int):
                nonlocal attempts
                attempts += 1
                if attempts == 1:
                    return subprocess.CompletedProcess(command, 9, stdout="", stderr="model unavailable")
                Path(command[command.index("--output-last-message") + 1]).write_text(
                    json.dumps({
                        "status": "complete",
                        "summary": "One replayable issue was recovered.",
                        "material_findings": [{
                            "issue": "A failed mining attempt previously blocked issue discovery.",
                            "inefficiency": "The useful finding would be lost without replay.",
                            "proposed_improvement": "Allow a successful replay to replace a prior no-ticket decision.",
                            "dedupe_key": "replay_no_ticket_recovery",
                            "owner_surface": "feature",
                            "evidence_refs": ["tickets/TASK-0001/ticket.md"],
                            "confidence": "high",
                        }],
                        "source_gaps": [],
                    }),
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            run = route_event(event_for(ticket), root, codex_runner=recovering_runner)[0]
            detail = show_run(root, run["run_id"])

            self.assertEqual(detail["report"]["status"], "source_gap")
            self.assertEqual(detail["report"]["source_gaps"][0]["reason"], "codex_executor_nonzero")
            self.assertTrue((root / ".farplane" / "mine" / "runs" / run["run_id"] / "executor.stderr.log").is_file())
            replayed = replay_run(root, run["run_id"], codex_runner=recovering_runner)
            self.assertEqual(replayed["run_id"], run["run_id"])
            replay_detail = show_run(root, run["run_id"])
            self.assertEqual(len(replay_detail["attempts"]), 2)
            self.assertEqual(replay_detail["report"]["ticket_output"]["decision"], "created")

    def test_completion_learning_rejects_raw_message_echo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            (root / "farplane" / "bindings.yaml").write_text(
                "event_routes:\n"
                "  - route_id: completion-learning\n"
                "    event_name: farplane.ticket.completed\n"
                f"    program_ref: {LEARNING_PROGRAM_REF}\n",
                encoding="utf-8",
            )
            window_dir = root / ".farplane" / "state" / "message-windows"
            window_dir.mkdir(parents=True)
            raw = "This exact private user message is deliberately longer than forty characters and must never be echoed."
            (window_dir / "sess-1.json").write_text(
                json.dumps({"session_id": "sess-1", "turn_count": 1, "rolling_exchanges": [{"user_turn": {"raw_text": raw}}]}),
                encoding="utf-8",
            )

            def echoing_runner(command: list[str], prompt: str, cwd: Path, timeout: int):
                output_path = Path(command[command.index("--output-last-message") + 1])
                output_path.write_text(
                    json.dumps(
                        {
                            "status": "complete",
                            "summary": raw,
                            "material_findings": [],
                            "source_gaps": [],
                        }
                    ),
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            run = route_event(event_for(ticket), root, codex_runner=echoing_runner)[0]
            report = show_run(root, run["run_id"])["report"]

            self.assertEqual(report["status"], "source_gap")
            self.assertEqual(report["source_gaps"][0]["reason"], "raw_source_echo_detected")
            self.assertEqual(report["ticket_output"]["decision"], "no_ticket")
            self.assertNotIn(raw, json.dumps(report))

    def test_completion_learning_rejects_partial_ticket_echo_and_short_secret(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            ticket.write_text(ticket_text() + "\nA private launch sequence needs careful operator approval before any external write.\n", encoding="utf-8")
            event = event_for(ticket)
            (root / "farplane" / "bindings.yaml").write_text(
                "event_routes:\n"
                "  - route_id: completion-learning\n"
                "    event_name: farplane.ticket.completed\n"
                f"    program_ref: {LEARNING_PROGRAM_REF}\n",
                encoding="utf-8",
            )
            window_dir = root / ".farplane" / "state" / "message-windows"
            window_dir.mkdir(parents=True)
            (window_dir / "sess-1.json").write_text(
                json.dumps({"session_id": "sess-1", "pending_user_turn": {"user_turn_id": "turn-1", "user_text": "credential sk-test-123456789012345678901234 must stay private"}}),
                encoding="utf-8",
            )

            outputs = iter([
                "private launch sequence needs careful operator approval",
                "sk-test-123456789012345678901234",
            ])

            def leaking_runner(command: list[str], prompt: str, cwd: Path, timeout: int):
                Path(command[command.index("--output-last-message") + 1]).write_text(
                    json.dumps({
                        "status": "complete",
                        "summary": next(outputs),
                        "material_findings": [],
                        "source_gaps": [],
                    }),
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            first = route_event(event, root, codex_runner=leaking_runner)[0]
            first_report = show_run(root, first["run_id"])["report"]
            self.assertEqual(first_report["source_gaps"][0]["reason"], "raw_source_echo_detected")
            replay_run(root, first["run_id"], codex_runner=leaking_runner)
            second_report = show_run(root, first["run_id"])["report"]
            self.assertEqual(second_report["source_gaps"][0]["reason"], "raw_source_echo_detected")
            self.assertNotIn("sk-test", json.dumps(second_report))

    def test_completion_learning_rejects_invalid_schema_and_unknown_evidence_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            (root / "farplane" / "bindings.yaml").write_text(
                "event_routes:\n"
                "  - route_id: completion-learning\n"
                "    event_name: farplane.ticket.completed\n"
                f"    program_ref: {LEARNING_PROGRAM_REF}\n",
                encoding="utf-8",
            )
            window_dir = root / ".farplane" / "state" / "message-windows"
            window_dir.mkdir(parents=True)
            (window_dir / "sess-1.json").write_text(
                json.dumps({"session_id": "sess-1", "pending_user_turn": {"user_turn_id": "turn-1", "user_text": "review the completed ticket"}}),
                encoding="utf-8",
            )
            outputs = iter([
                {},
                {
                    "status": "complete",
                    "summary": "A reusable correction was found.",
                    "material_findings": [{
                        "issue": "A workflow correction recurred.",
                        "inefficiency": "The correction is repeated manually.",
                        "proposed_improvement": "Refine the owning skill.",
                        "dedupe_key": "owned_workflow_correction",
                        "owner_surface": "skill",
                        "evidence_refs": ["/Users/private/person@example.com"],
                        "confidence": "high",
                    }],
                    "source_gaps": [],
                },
            ])

            def invalid_runner(command: list[str], prompt: str, cwd: Path, timeout: int):
                Path(command[command.index("--output-last-message") + 1]).write_text(json.dumps(next(outputs)), encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            run = route_event(event_for(ticket), root, codex_runner=invalid_runner)[0]
            self.assertEqual(show_run(root, run["run_id"])["report"]["source_gaps"][0]["reason"], "structured_output_invalid")
            replay_run(root, run["run_id"], codex_runner=invalid_runner)
            report = show_run(root, run["run_id"])["report"]
            self.assertEqual(report["source_gaps"][0]["reason"], "invalid_evidence_ref")
            self.assertNotIn("/Users/", json.dumps(report))
            self.assertNotIn("person@example.com", json.dumps(report))

    def test_completion_learning_rejects_redundant_or_contradictory_reasoning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            (root / "farplane" / "bindings.yaml").write_text(
                "event_routes:\n"
                "  - route_id: completion-learning\n"
                "    event_name: farplane.ticket.completed\n"
                f"    program_ref: {LEARNING_PROGRAM_REF}\n",
                encoding="utf-8",
            )
            outputs = iter([
                {
                    "status": "complete",
                    "summary": "A finding was reported.",
                    "material_findings": [{
                        "issue": "The same manual correction recurred.",
                        "inefficiency": "The same manual correction recurred.",
                        "proposed_improvement": "Refine the owning skill.",
                        "dedupe_key": "manual_correction_recurrence",
                        "owner_surface": "skill",
                        "evidence_refs": ["tickets/TASK-0001/ticket.md"],
                        "confidence": "high",
                    }],
                    "source_gaps": [],
                },
                {
                    "status": "no_signal",
                    "summary": "No actionable issue was found.",
                    "material_findings": [{
                        "issue": "A repeated correction was found.",
                        "inefficiency": "The correction consumed avoidable turns.",
                        "proposed_improvement": "Refine the owning skill.",
                        "dedupe_key": "repeated_correction_turns",
                        "owner_surface": "skill",
                        "evidence_refs": ["tickets/TASK-0001/ticket.md"],
                        "confidence": "high",
                    }],
                    "source_gaps": [],
                },
            ])

            def quality_failure_runner(command: list[str], prompt: str, cwd: Path, timeout: int):
                Path(command[command.index("--output-last-message") + 1]).write_text(
                    json.dumps(next(outputs)),
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            run = route_event(event_for(ticket), root, codex_runner=quality_failure_runner)[0]
            first = show_run(root, run["run_id"])["report"]
            self.assertEqual(first["source_gaps"][0]["reason"], "semantic_quality_invalid")
            self.assertIn("redundant_reasoning_fields", first["source_gaps"][0]["input_ref"])

            replay_run(root, run["run_id"], codex_runner=quality_failure_runner)
            second = show_run(root, run["run_id"])["report"]
            self.assertEqual(second["source_gaps"][0]["reason"], "semantic_quality_invalid")
            self.assertIn("no_signal_with_findings", second["source_gaps"][0]["input_ref"])
            self.assertEqual(second["ticket_output"]["decision"], "no_ticket")

    def test_completion_learning_redacts_timeout_command_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            (root / "farplane" / "bindings.yaml").write_text(
                "event_routes:\n"
                "  - route_id: completion-learning\n"
                "    event_name: farplane.ticket.completed\n"
                f"    program_ref: {LEARNING_PROGRAM_REF}\n",
                encoding="utf-8",
            )
            window_dir = root / ".farplane" / "state" / "message-windows"
            window_dir.mkdir(parents=True)
            (window_dir / "sess-1.json").write_text(
                json.dumps({"session_id": "sess-1", "pending_user_turn": {"user_turn_id": "turn-1", "user_text": "review completion"}}),
                encoding="utf-8",
            )

            def timeout_runner(command: list[str], prompt: str, cwd: Path, timeout: int):
                raise subprocess.TimeoutExpired([*command, "/Users/private/project", "/tmp/private-run"], timeout)

            run = route_event(event_for(ticket), root, codex_runner=timeout_runner)[0]
            report = show_run(root, run["run_id"])["report"]

            self.assertEqual(report["source_gaps"][0]["reason"], "codex_executor_failed")
            self.assertNotIn("/Users/", json.dumps(report))
            self.assertNotIn("/tmp/", json.dumps(report))

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
