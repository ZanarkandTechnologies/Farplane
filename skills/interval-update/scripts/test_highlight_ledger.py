from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).with_name("highlight_ledger.py")
SPEC = importlib.util.spec_from_file_location("interval_highlight_ledger", MODULE_PATH)
assert SPEC and SPEC.loader
ledger = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ledger)


def write_report(
    root: Path,
    ref: str = "reports/interval/daily/2026-07-24T053429+0800",
    *,
    status: str = "complete",
    kind: str = "interval-report",
) -> str:
    path = root / ".farplane" / f"{ref}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\nref: {ref}\nkind: {kind}\nstatus: {status}\n---\n\n# Report\n",
        encoding="utf-8",
    )
    return ref


def test_valid_minimal_rows_and_generic_links(tmp_path: Path) -> None:
    report = write_report(tmp_path)
    win = ledger.validate_highlight(
        "win",
        {
            "team": "farplane",
            "report": report,
            "summary": "Acceptance rate rose from 61% to a record 84%.",
            "links": [
                "tickets/TASK-0405/ticket.md",
                "skills/interval-update/SKILL.md#gotchas",
            ],
        },
    )
    failure = ledger.validate_highlight(
        "failure",
        {
            "team": "farplane",
            "report": report,
            "summary": "A delegated one-line edit took three review cycles.",
            "lesson": "Do not delegate a simple local edit when coordination costs more.",
        },
    )

    assert win["links"][0].startswith("tickets/")
    assert failure["lesson"].startswith("Do not delegate")
    assert "links" not in failure


@pytest.mark.parametrize(
    "field,value,error",
    [
        ("id", "derived-id", "unsupported_fields:id"),
        ("project", "farplane", "unsupported_fields:project"),
        ("cadence", "daily", "unsupported_fields:cadence"),
        ("period", "2026-07-24", "unsupported_fields:period"),
        ("created_at", "2026-07-24T00:00:00Z", "unsupported_fields:created_at"),
        ("origin", "backfill", "unsupported_fields:origin"),
        ("status", "active", "unsupported_fields:status"),
        ("tickets", ["TASK-0405"], "unsupported_fields:tickets"),
        ("skills", ["interval-update"], "unsupported_fields:skills"),
    ],
)
def test_derived_and_typed_reference_fields_are_rejected(
    tmp_path: Path, field: str, value: object, error: str
) -> None:
    row = {
        "team": "farplane",
        "report": write_report(tmp_path),
        "summary": "Metric rose from 10 to a record 20.",
        field: value,
    }
    with pytest.raises(ledger.HighlightValidationError, match=error):
        ledger.validate_highlight("win", row)


def test_failure_requires_a_reusable_lesson(tmp_path: Path) -> None:
    with pytest.raises(ledger.HighlightValidationError, match="missing_fields:lesson"):
        ledger.validate_highlight(
            "failure",
            {
                "team": "farplane",
                "report": write_report(tmp_path),
                "summary": "The run duplicated work.",
            },
        )


def test_repeated_append_is_idempotent_by_kind_team_report(tmp_path: Path) -> None:
    report = write_report(tmp_path)
    row = {
        "team": "farplane",
        "report": report,
        "summary": "Acceptance rate rose from 61% to a record 84%.",
    }

    assert ledger.append_highlight(tmp_path, "win", row) == "appended"
    assert ledger.append_highlight(tmp_path, "win", row) == "already_exists"
    rows = ledger.read_highlights(tmp_path, "win", validate_reports=True)

    assert rows == [row]
    assert (
        tmp_path / ".farplane" / "highlights" / "wins.jsonl"
    ).read_text().count("\n") == 1


def test_same_report_can_have_one_win_and_one_failure(tmp_path: Path) -> None:
    report = write_report(tmp_path)
    assert (
        ledger.append_highlight(
            tmp_path,
            "win",
            {
                "team": "farplane",
                "report": report,
                "summary": "Acceptance rate rose from 61% to a record 84%.",
            },
        )
        == "appended"
    )
    assert (
        ledger.append_highlight(
            tmp_path,
            "failure",
            {
                "team": "farplane",
                "report": report,
                "summary": "The run duplicated work.",
                "lesson": "Check the natural key before appending durable state.",
            },
        )
        == "appended"
    )


@pytest.mark.parametrize("status", ["draft", "source_gap"])
def test_append_requires_completed_report(tmp_path: Path, status: str) -> None:
    report = write_report(tmp_path, status=status)
    with pytest.raises(
        ledger.HighlightValidationError, match="report_is_not_complete"
    ):
        ledger.append_highlight(
            tmp_path,
            "win",
            {
                "team": "farplane",
                "report": report,
                "summary": "Metric rose from 10 to a record 20.",
            },
        )


def test_append_rejects_missing_or_non_report_ref(tmp_path: Path) -> None:
    missing = "reports/interval/daily/2026-07-23T053429+0800"
    with pytest.raises(ledger.HighlightValidationError, match="missing_report_ref"):
        ledger.append_highlight(
            tmp_path,
            "win",
            {
                "team": "farplane",
                "report": missing,
                "summary": "Metric rose from 10 to a record 20.",
            },
        )

    context_ref = write_report(
        tmp_path,
        "reports/interval/daily/2026-07-22T053429+0800",
        kind="interval-context",
    )
    with pytest.raises(
        ledger.HighlightValidationError, match="report_is_not_interval_report"
    ):
        ledger.append_highlight(
            tmp_path,
            "win",
            {
                "team": "farplane",
                "report": context_ref,
                "summary": "Metric rose from 10 to a record 20.",
            },
        )


def test_unsafe_or_redundant_links_are_rejected(tmp_path: Path) -> None:
    report = write_report(tmp_path)
    base = {
        "team": "farplane",
        "report": report,
        "summary": "Metric rose from 10 to a record 20.",
    }
    for links in (
        [],
        ["https://example.com/private"],
        ["/absolute/private.md"],
        ["tickets/../private.md"],
        ["tickets/TASK-1/ticket.md", "tickets/TASK-1/ticket.md"],
    ):
        with pytest.raises(ledger.HighlightValidationError):
            ledger.validate_highlight("win", {**base, "links": links})


def test_malformed_or_duplicate_existing_ledger_blocks_append(tmp_path: Path) -> None:
    report = write_report(tmp_path)
    path = ledger.ledger_path(tmp_path, "win")
    path.parent.mkdir(parents=True)
    path.write_text("{not-json}\n", encoding="utf-8")
    row = {
        "team": "farplane",
        "report": report,
        "summary": "Metric rose from 10 to a record 20.",
    }
    with pytest.raises(ledger.HighlightValidationError, match="malformed_jsonl"):
        ledger.append_highlight(tmp_path, "win", row)
    assert path.read_text(encoding="utf-8") == "{not-json}\n"

    duplicate = json.dumps(row, separators=(",", ":"))
    path.write_text(f"{duplicate}\n{duplicate}\n", encoding="utf-8")
    with pytest.raises(ledger.HighlightValidationError, match="duplicate_ledger_key"):
        ledger.read_highlights(tmp_path, "win")
