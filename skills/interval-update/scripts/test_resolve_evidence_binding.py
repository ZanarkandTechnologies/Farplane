from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml


MODULE_PATH = Path(__file__).with_name("resolve_evidence_binding.py")
SPEC = importlib.util.spec_from_file_location("resolve_evidence_binding", MODULE_PATH)
assert SPEC and SPEC.loader
binding = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(binding)


def write_bindings(root: Path, kanban: dict) -> None:
    farplane = root / "farplane"
    farplane.mkdir()
    (farplane / "bindings.yaml").write_text(
        yaml.safe_dump(
            {
                "kind": "project-bindings",
                "framework_template_version": "0.4.0",
                "project": {"id": "fixture"},
                "integrations": {"kanban": kanban},
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def test_filesystem_binding_preserves_ticket_evidence(tmp_path: Path) -> None:
    (tmp_path / "tickets" / "archive").mkdir(parents=True)
    write_bindings(
        tmp_path,
        {
            "provider": "filesystem_tickets",
            "filesystem_ticket_policy": "include",
            "tickets_dir": "tickets",
            "archive_dir": "tickets/archive",
        },
    )

    result = binding.resolve_binding(tmp_path)

    assert result["provider"] == "filesystem_tickets"
    assert result["access_ready"] is True
    assert result["provider_coordinates"] == {
        "tickets_dir": "tickets",
        "archive_dir": "tickets/archive",
    }
    assert result["source_gaps"] == []


def test_notion_binding_resolves_named_handle_and_ntn_without_private_values(
    tmp_path: Path, monkeypatch
) -> None:
    private_context = tmp_path / "private-notion.md"
    private_context.write_text("# Private\n\nHandle: notion.tasks.source\nID: private-value\n")
    write_bindings(
        tmp_path,
        {
            "provider": "notion",
            "task_source_handle": "notion.tasks.source",
            "filesystem_ticket_policy": "exclude",
        },
    )
    monkeypatch.setattr(binding.shutil, "which", lambda executable: "/opt/bin/ntn")

    result = binding.resolve_binding(tmp_path, private_context=private_context)

    assert result["provider"] == "notion"
    assert result["access_route"] == "private_handle_ntn"
    assert result["filesystem_ticket_policy"] == "exclude"
    assert result["access_ready"] is None
    assert result["access_check"] == "required_compact_ntn_query"
    assert "private-value" not in str(result)


def test_filesystem_binding_can_exclude_ticket_evidence_entirely(tmp_path: Path) -> None:
    (tmp_path / "tickets").mkdir()
    write_bindings(
        tmp_path,
        {
            "provider": "filesystem_tickets",
            "filesystem_ticket_policy": "exclude",
            "tickets_dir": "tickets",
            "archive_dir": "tickets/archive",
        },
    )

    result = binding.resolve_binding(tmp_path)

    assert result["access_ready"] is False
    assert result["access_route"] is None
    assert result["provider_coordinates"] == {}
    assert result["source_gaps"] == [
        {
            "code": "filesystem_tickets_excluded",
            "effect": "ticket evidence excluded by policy",
            "fallback": "none",
        }
    ]


def test_unavailable_notion_is_source_gap_without_filesystem_fallback(
    tmp_path: Path, monkeypatch
) -> None:
    (tmp_path / "tickets").mkdir()
    write_bindings(
        tmp_path,
        {
            "provider": "notion",
            "task_source_handle": "notion.tasks.source",
            "filesystem_ticket_policy": "exclude",
        },
    )
    monkeypatch.setattr(binding.shutil, "which", lambda executable: None)

    result = binding.resolve_binding(
        tmp_path,
        private_context=tmp_path / "missing-private-notion.md",
    )

    assert result["provider"] == "notion"
    assert result["access_ready"] is False
    assert result["filesystem_ticket_policy"] == "exclude"
    assert result["provider_coordinates"] == {"task_source_handle": "notion.tasks.source"}
    assert {gap["code"] for gap in result["source_gaps"]} == {
        "notion_private_context_missing",
        "ntn_unavailable",
    }
    assert all(gap["fallback"] == "none" for gap in result["source_gaps"])


def test_notion_binding_rejects_raw_url_as_private_handle(tmp_path: Path, monkeypatch) -> None:
    private_context = tmp_path / "private-notion.md"
    private_context.write_text("# Private\n", encoding="utf-8")
    write_bindings(
        tmp_path,
        {
            "provider": "notion",
            "task_source_handle": "https://notion.example/private-id",
            "filesystem_ticket_policy": "exclude",
        },
    )
    monkeypatch.setattr(binding.shutil, "which", lambda executable: "/opt/bin/ntn")

    result = binding.resolve_binding(tmp_path, private_context=private_context)

    assert result["access_ready"] is False
    assert {gap["code"] for gap in result["source_gaps"]} == {"notion_private_handle_invalid"}
    assert result["provider_coordinates"] == {}
