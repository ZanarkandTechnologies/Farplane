from pathlib import Path

from bin.validators.check_farplane_project_files import validate


def test_automations_requires_bindings(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    (farplane / "automations.md").write_text("---\nkind: project-automations\n---\n", encoding="utf-8")

    errors = validate(tmp_path)

    assert "farplane/automations.md requires farplane/bindings.md." in errors


def test_retired_integrations_file_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    (farplane / "bindings.md").write_text(
        "---\nkind: project-bindings\nframework_template_version: \"0.1.0\"\n---\n",
        encoding="utf-8",
    )
    (farplane / "integrations.md").write_text("# old\n", encoding="utf-8")

    errors = validate(tmp_path)

    assert "farplane/integrations.md is retired; use farplane/bindings.md." in errors


def test_valid_bindings_pass(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
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
    (farplane / "automations.md").write_text(
        "---\nkind: project-automations\nframework_template_version: \"0.1.0\"\n---\n",
        encoding="utf-8",
    )
    (farplane / "bindings.md").write_text(
        "---\nkind: project-bindings\nframework_template_version: \"0.1.0\"\n---\n\n# Project Bindings\n",
        encoding="utf-8",
    )

    assert validate(tmp_path) == []
