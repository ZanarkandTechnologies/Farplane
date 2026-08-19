from pathlib import Path

from bin.validators.check_farplane_project_files import validate_bindings_file


def test_bindings_reject_retired_sidecar_key_and_unsafe_scout_brief(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    bindings = farplane / "bindings.yaml"
    bindings.write_text(
        '''kind: project-bindings
framework_template_version: "0.5.0"
project: {}
feed_scout:
  world_memory: .farplane/feed-scout/world-memory.md
  scout_brief: ../scout-brief.txt
''',
        encoding="utf-8",
    )
    errors = validate_bindings_file(tmp_path, bindings)
    assert any("feed_scout.world_memory is retired" in error for error in errors)
    assert any("feed_scout.scout_brief must be a safe project-relative Markdown path" in error for error in errors)
