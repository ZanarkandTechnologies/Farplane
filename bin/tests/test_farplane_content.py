from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "bin" / "farplane.py"


class FarplaneContentTests(unittest.TestCase):
    def test_content_add_and_list_upserts_ledger_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            add = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "content",
                    "add",
                    "--project-root",
                    str(root),
                    "--platform",
                    "instagram",
                    "--external-id",
                    "reel-1",
                    "--url",
                    "https://instagram.example/reel-1",
                    "--status",
                    "posted",
                    "--approval",
                    "approved",
                    "--published-at",
                    "2026-07-02T10:00:00Z",
                    "--campaign",
                    "evidence_distribution",
                    "--kpis",
                    "instagram_views,evidence_distribution_reach",
                    "--approval-ref",
                    "tickets/TASK-0001/ticket.md",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(add.returncode, 0, add.stderr + add.stdout)
            add_payload = json.loads(add.stdout)
            self.assertEqual(add_payload["content_id"], "instagram:reel-1")

            update = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "content",
                    "add",
                    "--project-root",
                    str(root),
                    "--platform",
                    "instagram",
                    "--external-id",
                    "reel-1",
                    "--status",
                    "measured",
                    "--approval",
                    "approved",
                    "--kpis",
                    "instagram_views,evidence_distribution_reach",
                    "--notes",
                    "metrics fetched",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(update.returncode, 0, update.stderr + update.stdout)

            listed = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "content",
                    "list",
                    "--project-root",
                    str(root),
                    "--platform",
                    "instagram",
                    "--kpi",
                    "instagram_views",
                    "--since-date",
                    "2026-07-01",
                    "--until-date",
                    "2026-07-03",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(listed.returncode, 0, listed.stderr + listed.stdout)
            payload = json.loads(listed.stdout)

        self.assertEqual(payload["row_count"], 1)
        self.assertEqual(payload["external_ids"], ["reel-1"])
        self.assertEqual(payload["rows"][0]["content_id"], "instagram:reel-1")
        self.assertEqual(payload["rows"][0]["status"], "measured")
        self.assertEqual(payload["rows"][0]["notes"], "metrics fetched")
        self.assertEqual(payload["rows"][0]["url"], "https://instagram.example/reel-1")

    def test_content_add_requires_valid_status_and_kpis(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "content",
                    "add",
                    "--project-root",
                    str(root),
                    "--platform",
                    "x",
                    "--status",
                    "published",
                    "--kpis",
                    "",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertIn("invalid_status:published", payload["issues"])
        self.assertIn("invalid:kpis", payload["issues"])

    def test_content_list_filters_by_publish_window(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for external_id, published_at in [
                ("old", "2026-06-20T10:00:00Z"),
                ("fresh", "2026-07-02T10:00:00Z"),
            ]:
                result = subprocess.run(
                    [
                        sys.executable,
                        str(CLI),
                        "content",
                        "add",
                        "--project-root",
                        str(root),
                        "--platform",
                        "instagram",
                        "--external-id",
                        external_id,
                        "--published-at",
                        published_at,
                        "--kpis",
                        "instagram_views",
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

            listed = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "content",
                    "list",
                    "--project-root",
                    str(root),
                    "--platform",
                    "instagram",
                    "--status",
                    "posted",
                    "--kpi",
                    "instagram_views",
                    "--since-date",
                    "2026-06-26",
                    "--until-date",
                    "2026-07-03",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(listed.returncode, 0, listed.stderr + listed.stdout)
            payload = json.loads(listed.stdout)

        self.assertEqual(payload["external_ids"], ["fresh"])
        self.assertEqual(payload["row_count"], 1)


if __name__ == "__main__":
    unittest.main()
