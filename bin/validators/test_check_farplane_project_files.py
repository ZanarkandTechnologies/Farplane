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
                "version_history": [
                    {"version": "1.0.0", "adds": ["farplane/", ".farplane/", "tickets/"]},
                    {"version": "1.1.0", "adds": ["farplane/pm.json"]},
                ],
                "surfaces": [
                    {
                        "path": "farplane/",
                        "kind": "tracked_config_dir",
                        "tracked": True,
                        "required": True,
                        "introduced_in": "1.0.0",
                    },
                    {
                        "path": "farplane/manifest.json",
                        "kind": "framework_manifest",
                        "tracked": True,
                        "required": True,
                        "introduced_in": "1.0.0",
                    },
                    {
                        "path": ".farplane/",
                        "kind": "ignored_runtime_dir",
                        "tracked": False,
                        "required": True,
                        "introduced_in": "1.0.0",
                    },
                    {
                        "path": ".farplane/state/run-ledger.json",
                        "kind": "runtime_run_ledger",
                        "tracked": False,
                        "required": True,
                        "introduced_in": "1.0.0",
                    },
                    {
                        "path": "tickets/",
                        "kind": "ticket_queue",
                        "tracked": True,
                        "required": True,
                        "introduced_in": "1.0.0",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )


def test_automations_requires_bindings(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    (farplane / "automations.md").write_text("---\nkind: project-automations\n---\n", encoding="utf-8")

    errors = validate(tmp_path)

    assert "farplane/automations.md requires farplane/bindings.md." in errors


def test_retired_integrations_file_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    (farplane / "bindings.md").write_text(
        "---\nkind: project-bindings\nframework_template_version: \"0.1.0\"\n---\n",
        encoding="utf-8",
    )
    (farplane / "integrations.md").write_text("# old\n", encoding="utf-8")

    errors = validate(tmp_path)

    assert f"{RETIRED_INTEGRATIONS_REF} is retired; use farplane/bindings.md." in errors


def test_valid_bindings_pass(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    (farplane / "automations.md").write_text("---\nkind: project-automations\n---\n", encoding="utf-8")
    (farplane / "bindings.md").write_text(
        "---\nkind: project-bindings\nframework_template_version: \"0.1.0\"\n---\n\n# Project Bindings\n",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "farplane/automations.md must declare framework_template_version in front matter." in errors


def test_valid_versioned_files_pass(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    (farplane / "automations.md").write_text(
        "---\nkind: project-automations\nframework_template_version: \"0.1.0\"\n---\n",
        encoding="utf-8",
    )
    (farplane / "bindings.md").write_text(
        "---\nkind: project-bindings\nframework_template_version: \"0.1.0\"\n---\n\n# Project Bindings\n",
        encoding="utf-8",
    )

    assert validate(tmp_path) == []


def test_missing_pm_manifest_passes(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)

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
                "version_history": [],
                "surfaces": [
                    {
                        "path": "",
                        "kind": "",
                        "tracked": "yes",
                        "required": "yes",
                        "introduced_in": "",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "farplane/manifest.json schema must be farplane_project." in errors
    assert "farplane/manifest.json spec_version must be a non-empty string." in errors
    assert "farplane/manifest.json version_history must be a non-empty list." in errors
    assert "farplane/manifest.json surfaces[0].path must be a non-empty string." in errors
    missing_surface_error = next(
        error for error in errors if error.startswith("farplane/manifest.json missing required surface paths:")
    )
    for path in [".farplane/", ".farplane/state/run-ledger.json", "farplane/", "farplane/manifest.json", "tickets/"]:
        assert path in missing_surface_error


def test_valid_pm_manifest_passes(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
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
