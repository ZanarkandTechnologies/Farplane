"""A stale UI snapshot is local machine state, so doctor reports it, not lint."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "bin" / "core"))
from farplane_snapshot_freshness import snapshot_freshness_issues  # noqa: E402


def write_snapshot(root: Path, sources: object) -> None:
    path = root / ".farplane" / "project" / "ui" / "latest.json"
    path.parent.mkdir(parents=True)
    path.write_text(sources if isinstance(sources, str) else json.dumps({"sources": sources}), encoding="utf-8")


class SnapshotFreshnessTests(unittest.TestCase):
    def test_missing_or_fresh_snapshot_reports_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(snapshot_freshness_issues(root), [])
            (root / "metrics.yaml").write_text("a: 1\n", encoding="utf-8")
            digest = "sha256:" + hashlib.sha256(b"a: 1\n").hexdigest()
            write_snapshot(root, [{"path": "metrics.yaml", "hash": digest}])
            self.assertEqual(snapshot_freshness_issues(root), [])

    def test_changed_source_is_a_doctor_issue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "metrics.yaml").write_text("a: 2\n", encoding="utf-8")
            write_snapshot(root, [{"path": "metrics.yaml", "hash": "sha256:old"}])
            self.assertEqual(snapshot_freshness_issues(root), ["project_snapshot_stale:metrics.yaml"])

    def test_unreadable_snapshot_is_a_doctor_issue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_snapshot(root, "{not json")
            self.assertEqual(snapshot_freshness_issues(root),
                             ["project_snapshot_unreadable:.farplane/project/ui/latest.json"])


if __name__ == "__main__":
    unittest.main()
