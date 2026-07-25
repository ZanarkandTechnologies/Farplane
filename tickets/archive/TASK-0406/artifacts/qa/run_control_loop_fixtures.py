#!/usr/bin/env python3
"""Replay TASK-0406's two deterministic control-loop integration fixtures."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from types import ModuleType


REPO_ROOT = Path(__file__).resolve().parents[4]
OUTPUT_ROOT = Path(__file__).resolve().parent / "fixture-output"
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "bin" / "core"))


def load_module(name: str, relative_path: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / relative_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {relative_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


snapshot = load_module("task0406_snapshot", "bin/core/farplane_project_snapshot.py")
board = load_module("task0406_board", "skills/pulse-update/scripts/list_pulse_board.py")
highlights = load_module(
    "task0406_highlights", "skills/interval-update/scripts/highlight_ledger.py"
)
wave_guard = load_module(
    "task0406_wave_guard", "skills/pulse-update/scripts/plan_wave_guard.py"
)


def write_json(name: str, value: object) -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / name).write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def write_report(root: Path, interval_id: str, body: str) -> Path:
    ref = f"reports/interval/{interval_id}/2026-07-25T15-30-00Z"
    path = root / ".farplane" / f"{ref}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        f"ref: {ref}\n"
        "kind: interval-report\n"
        "status: complete\n"
        f"interval_id: {interval_id}\n"
        "created_at: 2026-07-25T15:30:00Z\n"
        "completed_at: 2026-07-25T15:31:00Z\n"
        "---\n\n"
        + body,
        encoding="utf-8",
    )
    return path


def replay_known_intervention() -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="task0406-known-") as raw_root:
        root = Path(raw_root)
        movement = snapshot.derive_metric_movement(
            "maximize",
            {"date": "2026-07-23T00:00:00+08:00", "value": 0.42},
            {"date": "2026-07-25T00:00:00+08:00", "value": 0.37},
        )
        assert movement["momentum_state"] == "worsening"

        report = write_report(
            root,
            "daily",
            "# Daily Interval\n\n"
            "Dominant bottleneck: accepted tickets lack concrete QA receipts.\n\n"
            "Decision: admit a known correction with a ticket-scoped proof artifact.\n",
        )
        report_ref = report.relative_to(root / ".farplane").with_suffix("").as_posix()
        highlight_row = {
            "team": "farplane",
            "report": report_ref,
            "summary": "The regression was traced to a missing closeout receipt.",
        }
        first_append = highlights.append_highlight(root, "failure", {
            **highlight_row,
            "lesson": "Generate and validate the QA receipt before ticket close.",
        })
        second_append = highlights.append_highlight(root, "failure", {
            **highlight_row,
            "lesson": "Generate and validate the QA receipt before ticket close.",
        })
        assert first_append == "appended"
        assert second_append == "already_exists"

        admitted_ticket = {
            "ticket_id": "TASK-9001",
            "status": "todo",
            "priority": "high",
            "due_at": "2026-07-26T18:00:00+08:00",
            "artifact": "validated QA receipt",
            "report_ref": report_ref,
        }
        ticket_path = root / "tickets" / admitted_ticket["ticket_id"] / "ticket.md"
        ticket_path.parent.mkdir(parents=True)
        ticket_path.write_text(
            "---\n"
            "ticket_id: TASK-9001\n"
            "status: todo\n"
            "priority: high\n"
            "due_at: 2026-07-26T18:00:00+08:00\n"
            "---\n\n"
            "# TASK-9001\n\nProduce and validate the ticket-scoped QA receipt.\n",
            encoding="utf-8",
        )

        candidates = [
            admitted_ticket,
            {
                "ticket_id": "TASK-8999",
                "status": "todo",
                "priority": "high",
                "due_at": "2026-07-27T09:00:00+08:00",
            },
            {
                "ticket_id": "TASK-1000",
                "status": "todo",
                "priority": "high",
                "due_at": None,
            },
            {
                "ticket_id": "TASK-0001",
                "status": "todo",
                "priority": "medium",
                "due_at": "2026-07-25T09:00:00+08:00",
            },
        ]
        ordered = [
            row["ticket_id"] for row in sorted(candidates, key=board.ticket_sort_key)
        ]
        assert ordered == ["TASK-9001", "TASK-8999", "TASK-1000", "TASK-0001"]
        assert not (root / ".farplane" / "automation" / "decisions.jsonl").exists()

        (OUTPUT_ROOT / "known-interval-report.md").parent.mkdir(
            parents=True, exist_ok=True
        )
        (OUTPUT_ROOT / "known-interval-report.md").write_text(
            report.read_text(encoding="utf-8"), encoding="utf-8"
        )
        (OUTPUT_ROOT / "known-admitted-ticket.md").write_text(
            ticket_path.read_text(encoding="utf-8"), encoding="utf-8"
        )
        return {
            "fixture_id": "control-loop-known-intervention",
            "verdict": "pass",
            "movement": movement,
            "report_finalized_before_highlight": True,
            "highlight_receipts": [first_append, second_append],
            "ticket_delta": admitted_ticket,
            "pulse_order": ordered,
            "plan_next_wave_called": False,
        }


def replay_refill_fallback() -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="task0406-refill-") as raw_root:
        root = Path(raw_root)
        movement = snapshot.derive_metric_movement(
            "maximize",
            {"date": "2026-07-18T00:00:00+08:00", "value": 1200},
            {"date": "2026-07-25T00:00:00+08:00", "value": 1185},
        )
        assert movement["momentum_state"] == "worsening"
        report = write_report(
            root,
            "weekly",
            "# Weekly Interval\n\n"
            "Source gap: channel attribution is unavailable.\n\n"
            "Decision: no ticket; the proposed investigation lacks a "
            "decision-changing output contract.\n",
        )
        assert not (root / "tickets").exists()

        planning_input = {
            "as_of": "2026-07-25T15:32:00Z",
            "board": {"ready_supply": 0, "low_watermark": 1},
            "problems": ["unattended_autonomy"],
            "objective_movement": [movement],
            "semantic_time_state": {
                "metric_freshness": {
                    "evidence_distribution_reach": "2026-07-25T00:00:00+08:00"
                },
                "matured_reward_ids": [],
                "operator_availability": {"available": True},
            },
        }
        begin_receipt = wave_guard.begin_wave(root, planning_input, 1)
        assert begin_receipt["status"] == "acquired"
        finish_receipt = wave_guard.finish_wave(
            root,
            begin_receipt["claim_id"],
            "no_op",
            [],
            reason="source_gap",
        )
        assert finish_receipt["status"] == "no_op"
        decisions = wave_guard.read_jsonl(wave_guard.decision_path(root))
        assert [row["status"] for row in decisions] == ["claimed", "no_op"]

        (OUTPUT_ROOT / "refill-interval-report.md").parent.mkdir(
            parents=True, exist_ok=True
        )
        (OUTPUT_ROOT / "refill-interval-report.md").write_text(
            report.read_text(encoding="utf-8"), encoding="utf-8"
        )
        return {
            "fixture_id": "control-loop-refill-fallback",
            "verdict": "pass",
            "movement": movement,
            "interval_ticket_delta": None,
            "source_gap_preserved": True,
            "low_watermark_guard": {
                "begin": begin_receipt,
                "finish": finish_receipt,
                "decision_statuses": [row["status"] for row in decisions],
            },
        }


def main() -> int:
    known = replay_known_intervention()
    refill = replay_refill_fallback()
    write_json("known-replay.json", known)
    write_json("refill-replay.json", refill)
    print(
        json.dumps(
            {
                "verdict": "pass",
                "artifacts": [
                    str(OUTPUT_ROOT / "known-replay.json"),
                    str(OUTPUT_ROOT / "known-interval-report.md"),
                    str(OUTPUT_ROOT / "known-admitted-ticket.md"),
                    str(OUTPUT_ROOT / "refill-replay.json"),
                    str(OUTPUT_ROOT / "refill-interval-report.md"),
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
