#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "sync_skill_registry",
    ROOT / "bin" / "sync_skill_registry.py",
)
assert SPEC and SPEC.loader
sync_skill_registry = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync_skill_registry)


def write_skill(repo: Path, name: str, *, template_version: str | None = None) -> None:
    skill_dir = repo / "skills" / name
    skill_dir.mkdir(parents=True)
    template_line = (
        f"skill_template_version: {template_version}\n"
        if template_version is not None
        else ""
    )
    (skill_dir / "SKILL.md").write_text(
        "\n".join(
            [
                "---",
                f"name: {name}",
                "description: Test skill.",
                "tier: 2",
                "source: local",
                template_line.rstrip(),
                "---",
                "",
                f"# {name}",
                "",
                "<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->",
                "## Todo List",
                "",
                "- [ ] Test.",
                "<!-- END FARPLANE_IMPORTANT_CHECKLIST -->",
                "",
            ]
        ).replace("\n\n---", "\n---"),
        encoding="utf-8",
    )


class SyncSkillRegistryTests(unittest.TestCase):
    def test_copies_skill_template_version_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "example", template_version="0.1.0")

            rows = sync_skill_registry.build_registry(repo)

            self.assertEqual(rows[0]["skill_template_version"], "0.1.0")

    def test_omits_skill_template_version_when_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "example")

            rows = sync_skill_registry.build_registry(repo)

            self.assertNotIn("skill_template_version", rows[0])


if __name__ == "__main__":
    unittest.main()
