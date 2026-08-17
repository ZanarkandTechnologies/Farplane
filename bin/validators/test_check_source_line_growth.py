from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("check_source_line_growth.py")
SPEC = importlib.util.spec_from_file_location("check_source_line_growth", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class SourceLineGrowthTests(unittest.TestCase):
    def make_repo(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
        return root

    def test_new_file_over_limit_fails(self) -> None:
        delta = MODULE.SourceDelta("bin/core/new.py", None, 501)
        self.assertEqual(1, len(MODULE.violations([delta], 500)))

    def test_new_file_at_limit_passes(self) -> None:
        delta = MODULE.SourceDelta("bin/core/new.py", None, 500)
        self.assertEqual([], MODULE.violations([delta], 500))

    def test_oversized_legacy_file_may_shrink(self) -> None:
        delta = MODULE.SourceDelta("bin/farplane.py", 1570, 900)
        self.assertEqual([], MODULE.violations([delta], 500))

    def test_oversized_legacy_file_may_hold(self) -> None:
        delta = MODULE.SourceDelta("bin/farplane.py", 1570, 1570)
        self.assertEqual([], MODULE.violations([delta], 500))

    def test_oversized_legacy_file_may_not_grow(self) -> None:
        delta = MODULE.SourceDelta("bin/farplane.py", 1570, 1571)
        errors = MODULE.violations([delta], 500)
        self.assertEqual(1, len(errors))
        self.assertIn("grew from 1570 to 1571", errors[0])

    def test_file_crossing_limit_fails(self) -> None:
        delta = MODULE.SourceDelta("bin/core/old.py", 499, 501)
        self.assertEqual(1, len(MODULE.violations([delta], 500)))

    def test_strict_mode_blocks_oversized_legacy_file_that_holds(self) -> None:
        delta = MODULE.SourceDelta("skills/legacy/SKILL.md", 250, 250)
        errors = MODULE.violations([delta], 200, strict=True)
        self.assertEqual(
            ["skills/legacy/SKILL.md: source file has 250 lines; max is 200"],
            errors,
        )

    def test_strict_mode_allows_file_at_limit(self) -> None:
        delta = MODULE.SourceDelta("skills/demo/SKILL.md", 199, 200)
        self.assertEqual([], MODULE.violations([delta], 200, strict=True))

    def test_default_glob_matches_top_level_and_nested_python(self) -> None:
        globs = ["bin/**/*.py"]
        self.assertTrue(MODULE.matches("bin/farplane.py", globs))
        self.assertTrue(MODULE.matches("bin/core/module.py", globs))
        self.assertFalse(MODULE.matches("docs/example.py", globs))

    def test_skill_glob_matches_only_skill_entrypoints(self) -> None:
        globs = ["skills/**/SKILL.md"]
        self.assertTrue(MODULE.matches("skills/demo/SKILL.md", globs))
        self.assertTrue(MODULE.matches("skills/group/demo/SKILL.md", globs))
        self.assertFalse(MODULE.matches("skills/demo/reference.md", globs))

    def test_adoption_baseline_is_valid(self) -> None:
        root = MODULE_PATH.parents[2]
        baseline = MODULE.load_baseline(root / "rules/source-line-baseline.toml")
        self.assertEqual(1753, baseline["bin/core/farplane_mining.py"])
        self.assertNotIn("bin/farplane.py", baseline)

    def test_adoption_baseline_covers_current_oversized_python(self) -> None:
        root = MODULE_PATH.parents[2]
        baseline = MODULE.load_baseline(root / "rules/source-line-baseline.toml")
        for path in (root / "bin").rglob("*.py"):
            relative = path.relative_to(root).as_posix()
            current_lines = len(path.read_bytes().splitlines())
            if current_lines > 500:
                self.assertIn(relative, baseline)
                self.assertLessEqual(current_lines, baseline[relative])

    def test_staged_mode_reads_index_blob_for_new_file(self) -> None:
        root = self.make_repo()
        subprocess.run(["git", "commit", "--allow-empty", "-qm", "base"], cwd=root, check=True)
        source = root / "bin/new.py"
        source.parent.mkdir(parents=True)
        source.write_text("pass\n" * 501, encoding="utf-8")
        subprocess.run(["git", "add", "bin/new.py"], cwd=root, check=True)

        deltas = MODULE.source_deltas("staged", "origin/main", ["bin/**/*.py"], root=root)

        self.assertEqual([MODULE.SourceDelta("bin/new.py", None, 501)], deltas)
        self.assertEqual(1, len(MODULE.violations(deltas, 500)))

    def test_staged_mode_blocks_growth_from_head(self) -> None:
        root = self.make_repo()
        source = root / "bin/legacy.py"
        source.parent.mkdir(parents=True)
        source.write_text("pass\n" * 501, encoding="utf-8")
        subprocess.run(["git", "add", "bin/legacy.py"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "base"], cwd=root, check=True)
        source.write_text("pass\n" * 502, encoding="utf-8")
        subprocess.run(["git", "add", "bin/legacy.py"], cwd=root, check=True)

        deltas = MODULE.source_deltas("staged", "origin/main", ["bin/**/*.py"], root=root)

        self.assertEqual([MODULE.SourceDelta("bin/legacy.py", 501, 502)], deltas)
        self.assertEqual(1, len(MODULE.violations(deltas, 500)))

    def test_staged_strict_mode_blocks_unchanged_oversized_skill_size(self) -> None:
        root = self.make_repo()
        source = root / "skills/legacy/SKILL.md"
        source.parent.mkdir(parents=True)
        source.write_text("before\n" + "line\n" * 200, encoding="utf-8")
        subprocess.run(["git", "add", "skills/legacy/SKILL.md"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "base"], cwd=root, check=True)
        source.write_text("after\n" + "line\n" * 200, encoding="utf-8")
        subprocess.run(["git", "add", "skills/legacy/SKILL.md"], cwd=root, check=True)

        deltas = MODULE.source_deltas(
            "staged",
            "origin/main",
            ["skills/**/SKILL.md"],
            root=root,
        )

        self.assertEqual([MODULE.SourceDelta("skills/legacy/SKILL.md", 201, 201)], deltas)
        self.assertEqual(1, len(MODULE.violations(deltas, 200, strict=True)))


if __name__ == "__main__":
    unittest.main()
