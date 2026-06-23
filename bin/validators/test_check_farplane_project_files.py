import json
from pathlib import Path

from bin.validators.check_farplane_project_files import validate

RETIRED_INTEGRATIONS_REF = "farplane/" + "integrations.md"


def write_framework_manifest(farplane: Path) -> None:
    (farplane / "manifest.json").write_text(
        json.dumps(
            {
                "schema": "farplane_project",
                "spec_version": "1.1.0",
                "standard": {
                    "tracked": [
                        "AGENTS.md",
                        "PROJECT_RULES.md",
                        "ARCHITECTURE.md",
                        "farplane/README.md",
                        "farplane/manifest.json",
                        "farplane/harness.md",
                        "farplane/goals.md",
                        "farplane/automations.md",
                        "farplane/steer.config.json",
                        "farplane/bindings.md",
                        "farplane/evals.md",
                        "tickets/templates/ticket.md",
                    ],
                    "ignored": [".farplane/state/run-ledger.json", ".farplane/state/steer-scheduler.json"],
                },
                "optional": {
                    "tracked": ["farplane/pm.json"],
                    "ignored": [".farplane/reviews/"],
                },
            }
        ),
        encoding="utf-8",
    )


def write_steer_config(farplane: Path) -> None:
    (farplane / "steer.config.json").write_text(
        json.dumps(
            {
                "schema": "farplane_steer_config",
                "version": "2026-06-23.1",
                "timezone": "UTC",
                "state_ref": ".farplane/state/steer-scheduler.json",
                "jobs": [
                    {
                        "id": "daily_plan",
                        "cadence": "FREQ=DAILY;INTERVAL=1",
                        "prompt": "Run the daily Steer plan.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


def write_automations_md(farplane: Path) -> None:
    (farplane / "automations.md").write_text(
        "---\nkind: project-automations\nframework_template_version: \"0.2.0\"\n---\n\n# Project Automations\n",
        encoding="utf-8",
    )


def write_required_project_files(root: Path) -> None:
    farplane = root / "farplane"
    for path in ("AGENTS.md", "PROJECT_RULES.md", "ARCHITECTURE.md"):
        (root / path).write_text(f"# {path}\n", encoding="utf-8")

    for name in ("README.md", "harness.md", "goals.md", "evals.md"):
        (farplane / name).write_text(
            "---\nframework_template_version: \"0.1.0\"\n---\n\n# Test\n",
            encoding="utf-8",
        )

    (farplane / "bindings.md").write_text(
        "---\nkind: project-bindings\nframework_template_version: \"0.1.0\"\n---\n\n# Project Bindings\n",
        encoding="utf-8",
    )
    write_automations_md(farplane)
    tickets = root / "tickets" / "templates"
    tickets.mkdir(parents=True)
    (tickets / "ticket.md").write_text("# Ticket\n", encoding="utf-8")
    state = root / ".farplane" / "state"
    state.mkdir(parents=True)
    (state / "run-ledger.json").write_text("{\"runs\": []}\n", encoding="utf-8")
    (state / "steer-scheduler.json").write_text("{\"jobs\": {}}\n", encoding="utf-8")


def test_missing_automations_file_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)

    errors = validate(tmp_path)

    assert "farplane/automations.md is required for reviewable Codex automation prompts." in errors


def test_retired_integrations_file_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_automations_md(farplane)
    write_steer_config(farplane)
    (farplane / "bindings.md").write_text(
        "---\nkind: project-bindings\nframework_template_version: \"0.1.0\"\n---\n",
        encoding="utf-8",
    )
    (farplane / "integrations.md").write_text("# old\n", encoding="utf-8")

    errors = validate(tmp_path)

    assert f"{RETIRED_INTEGRATIONS_REF} is retired; use farplane/bindings.md." in errors


def test_invalid_steer_config_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_automations_md(farplane)
    (farplane / "steer.config.json").write_text(json.dumps({"schema": "wrong", "version": "", "jobs": [{}]}), encoding="utf-8")

    errors = validate(tmp_path)

    assert "farplane/steer.config.json schema must be farplane_steer_config." in errors
    assert "farplane/steer.config.json version must be a non-empty string." in errors
    assert "farplane/steer.config.json jobs[0].id must be a non-empty string." in errors
    assert "farplane/steer.config.json jobs[0].cadence must be a non-empty string." in errors
    assert "farplane/steer.config.json jobs[0].prompt must be a non-empty string." in errors


def test_valid_versioned_files_pass(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_steer_config(farplane)
    write_required_project_files(tmp_path)

    assert validate(tmp_path) == []


def test_missing_pm_manifest_passes(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_steer_config(farplane)
    write_required_project_files(tmp_path)

    assert validate(tmp_path) == []


def test_missing_framework_manifest_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()

    assert "farplane/manifest.json is required for Farplane project manifests." in validate(tmp_path)


def test_framework_manifest_shape_is_validated(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    (farplane / "manifest.json").write_text(
        json.dumps(
            {
                "schema": "other",
                "spec_version": "",
                "standard": {
                    "tracked": ["farplane/manifest.json", "farplane/manifest.json", ".farplane/state/run-ledger.json"],
                    "ignored": [".farplane/state/run-ledger.json"],
                },
                "optional": {
                    "tracked": "farplane/pm.json",
                    "ignored": [""],
                },
            }
        ),
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "farplane/manifest.json schema must be farplane_project." in errors
    assert "farplane/manifest.json spec_version must be a non-empty string." in errors
    assert "farplane/manifest.json standard.tracked must not contain duplicate paths." in errors
    assert "farplane/manifest.json optional.tracked must be a list." in errors
    assert "farplane/manifest.json optional.ignored must contain only non-empty strings." in errors
    assert "farplane/manifest.json paths cannot be both tracked and ignored: .farplane/state/run-ledger.json." in errors
    missing_surface_error = next(
        error for error in errors if error.startswith("farplane/manifest.json missing required standard paths:")
    )
    for path in ["AGENTS.md", "PROJECT_RULES.md", "ARCHITECTURE.md", "farplane/README.md", "tickets/templates/ticket.md"]:
        assert path in missing_surface_error


def test_valid_pm_manifest_passes(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_steer_config(farplane)
    write_required_project_files(tmp_path)
    (farplane / "pm.json").write_text(
        json.dumps(
            {
                "version": 1,
                "name": "Project PM",
                "role": "founder_operator",
                "threads": {
                    "chats": ["019ecbfb-26dd-77d1-8f7d-b0fe2f8c7ea4"],
                    "automations": ["019ecbfb-9d19-7058-a516-f96f4a3515d4"],
                },
            }
        ),
        encoding="utf-8",
    )

    assert validate(tmp_path) == []


def test_pm_manifest_shape_is_validated(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_steer_config(farplane)
    (farplane / "pm.json").write_text(
        json.dumps(
            {
                "version": 2,
                "name": "",
                "role": "operator",
                "threads": {
                    "chats": ["chat-1", "chat-1"],
                    "automations": [123],
                    "extra": [],
                },
                "unsupported": True,
            }
        ),
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "farplane/pm.json has unsupported keys: unsupported." in errors
    assert "farplane/pm.json version must be 1." in errors
    assert "farplane/pm.json name must be a non-empty string." in errors
    assert "farplane/pm.json role must be founder_operator." in errors
    assert "farplane/pm.json threads has unsupported keys: extra." in errors
    assert "farplane/pm.json threads.automations must contain only non-empty strings." in errors
    assert "farplane/pm.json threads.chats must not contain duplicate thread IDs." in errors
