from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
CLI = ROOT / "bin" / "farplane.py"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_reports import build_report_registry


def write_report(path: Path, frontmatter: str, body: str = "# Report\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{frontmatter.strip()}\n---\n\n{body}", encoding="utf-8")


class FarplaneReportRegistryTests(unittest.TestCase):
    def test_registry_includes_nested_refs_and_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            parent = root / ".farplane" / "reports" / "interval" / "daily_interval" / "2026-07-08T053300+0800.md"
            child = (
                root
                / ".farplane"
                / "reports"
                / "interval"
                / "daily_interval"
                / "2026-07-08T053300+0800"
                / "feed-scout.md"
            )
            write_report(
                parent,
                """
ref: reports/interval/daily_interval/2026-07-08T053300+0800
kind: interval-report
created_at: "2026-07-08T05:33:00+08:00"
ui_summary: Parent report summary.
interval_id: daily_interval
status: draft
""",
            )
            write_report(
                child,
                """
ref: reports/interval/daily_interval/2026-07-08T053300+0800/feed-scout
kind: feed-scout
created_at: "2026-07-08T05:34:00+08:00"
ui_summary: Child feed scout summary.
""",
            )

            registry = build_report_registry(root)

        self.assertEqual(registry["counts"], {"included": 2, "excluded": 0})
        parent_ref = "reports/interval/daily_interval/2026-07-08T053300+0800"
        child_ref = f"{parent_ref}/feed-scout"
        parent_record = registry["by_ref"][parent_ref]
        child_record = registry["by_ref"][child_ref]
        self.assertIsNone(parent_record["parent_ref"])
        self.assertEqual(parent_record["children_refs"], [child_ref])
        self.assertEqual(parent_record["frontmatter"]["interval_id"], "daily_interval")
        self.assertEqual(child_record["parent_ref"], parent_ref)
        self.assertEqual(child_record["group_ref"], parent_ref)

    def test_registry_reports_malformed_and_missing_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reports = root / ".farplane" / "reports"
            write_report(
                reports / "pulse" / "valid.md",
                """
ref: reports/pulse/2026-07-08T030000Z
kind: pulse
created_at: "2026-07-08T03:00:00Z"
ui_summary: Valid pulse summary.
""",
            )
            (reports / "pulse" / "missing-frontmatter.md").write_text("# Missing\n", encoding="utf-8")
            (reports / "pulse" / "invalid-yaml.md").write_text(
                "---\nref: [unterminated\n---\n\n# Invalid\n",
                encoding="utf-8",
            )
            write_report(
                reports / "pulse" / "missing-required.md",
                """
kind: pulse
created_at: "2026-07-08T03:00:00Z"
ui_summary: Missing ref.
""",
            )
            write_report(
                reports / "pulse" / "bad-ref.md",
                """
ref: /reports/pulse/bad
kind: pulse
created_at: "2026-07-08T03:00:00Z"
ui_summary: Bad ref.
""",
            )

            registry = build_report_registry(root)

        self.assertEqual(registry["counts"], {"included": 1, "excluded": 4})
        issue_reasons = {issue["reason"] for issue in registry["issues"]}
        self.assertIn("missing_frontmatter", issue_reasons)
        self.assertTrue(any(reason.startswith("invalid_frontmatter:") for reason in issue_reasons))
        self.assertIn("missing_required:ref", issue_reasons)
        self.assertIn("invalid_ref_path", issue_reasons)

    def test_cli_writes_index_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_report(
                root / ".farplane" / "reports" / "pulse" / "2026-07-08T030000Z.md",
                """
ref: reports/pulse/2026-07-08T030000Z
kind: pulse
created_at: "2026-07-08T03:00:00Z"
ui_summary: Pulse summary.
""",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "reports",
                    "index",
                    "--project-root",
                    str(root),
                    "--json",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(result.stdout)
            index_path = root / ".farplane" / "reports" / "index.json"
            written = json.loads(index_path.read_text(encoding="utf-8"))

        self.assertEqual(payload["counts"]["included"], 1)
        self.assertEqual(written["reports"][0]["ref"], "reports/pulse/2026-07-08T030000Z")


if __name__ == "__main__":
    unittest.main()
