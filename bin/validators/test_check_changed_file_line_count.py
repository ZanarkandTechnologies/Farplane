import tempfile
import unittest
from pathlib import Path

from bin.validators.check_changed_file_line_count import (
    LineLimitRule,
    collect_warnings,
    line_count,
    load_rules,
)


class ChangedFileLineCountTests(unittest.TestCase):
    def test_load_rules_reuses_explicit_enrolled_limits(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config = Path(temp_dir) / "gates.toml"
            config.write_text(
                '''[changed_file_line_count]
[[changed_file_line_count.rule]]
name = "project-memory"
globs = ["memory.mb", "docs/MEMORY.md"]
max_lines = 500
''',
                encoding="utf-8",
            )

            self.assertEqual(
                load_rules(config),
                [
                    LineLimitRule(
                        "project-memory",
                        ("memory.mb", "docs/MEMORY.md"),
                        (),
                        500,
                    )
                ],
            )

    def test_collect_warnings_reads_only_matching_changed_files(self) -> None:
        blobs = {
            "memory.mb": b"one\ntwo\nthree\n",
            "README.md": b"one\ntwo\nthree\nfour\n",
        }
        rules = [LineLimitRule("memory", ("memory.mb",), (), 2)]

        warnings = collect_warnings(
            ["memory.mb", "README.md"],
            rules,
            lambda path: blobs.get(path),
        )

        self.assertEqual(len(warnings), 1)
        self.assertEqual(warnings[0].path, "memory.mb")
        self.assertEqual(warnings[0].line_count, 3)
        self.assertEqual(warnings[0].rule.max_lines, 2)

    def test_collect_warnings_skips_excluded_and_binary_files(self) -> None:
        blobs = {
            "skills/foo/SKILL.md": b"one\ntwo\nthree\n",
            "skills/foo/assets/output.svg": b"one\ntwo\nthree\n",
            "skills/foo/image.png": b"binary\0data\nmore\n",
        }
        rules = [
            LineLimitRule(
                "skill-source",
                ("skills/**",),
                ("skills/**/assets/**",),
                2,
            )
        ]

        warnings = collect_warnings(list(blobs), rules, blobs.get)

        self.assertEqual([warning.path for warning in warnings], ["skills/foo/SKILL.md"])

    def test_line_count(self) -> None:
        for blob, expected in (
            (b"", 0),
            (b"one", 1),
            (b"one\ntwo\n", 2),
            (b"one\n\ntwo\n", 3),
        ):
            with self.subTest(blob=blob):
                self.assertEqual(line_count(blob), expected)


if __name__ == "__main__":
    unittest.main()
