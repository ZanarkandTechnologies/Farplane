from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.core import farplane_zernio as zernio  # noqa: E402

# A fictional studio's profile: two posts on 1 Oct, one on 3 Oct.
POSTS = [
    {"publishedAt": "2026-10-01T10:00:00", "analytics": {"views": 100}},
    {"publishedAt": "2026-10-01T15:00:00", "analytics": {"views": 300}},
    {"publishedAt": "2026-10-03T09:00:00", "analytics": {"views": 50}},
]


ACCOUNT = {"platform": "instagram", "username": "northwind.studio", "displayName": "Northwind Studio", "followersCount": 1200, "isActive": True}


class ZernioTests(unittest.TestCase):
    def test_each_connected_account_fills_only_the_metrics_the_project_defines(self) -> None:
        defined = {"instagram_followers", "instagram_views"}
        days = zernio.account_readings(POSTS, [ACCOUNT, {**ACCOUNT, "platform": "x", "username": "northwind"}], defined, date(2026, 10, 3), days=3)
        by = lambda day, metric: [r for r in days.get(day, []) if r["metric_id"] == metric]
        self.assertEqual(by("2026-10-03", "instagram_views")[0]["value"], 450.0)  # every post in the 30 days to 3 Oct
        self.assertEqual(by("2026-10-02", "instagram_views")[0]["value"], 400.0)
        self.assertEqual(by("2026-10-03", "instagram_followers")[0]["value"], 1200.0)
        self.assertEqual(by("2026-10-02", "instagram_followers"), [])  # followers: today only
        self.assertEqual(by("2026-10-03", "x_views"), [])  # not defined, so not written
        tag = by("2026-10-03", "instagram_followers")[0]["payload"]["distribution_account"]
        self.assertEqual(tag, {"platform": "instagram", "account_id": "northwind.studio", "label": "Northwind Studio"})

    def test_the_profile_comes_from_the_bindings(self) -> None:
        self.assertEqual(zernio.zernio_profile("kind: x\nzernio:\n  profile: abc123\n  access: read_only\n"), "abc123")
        self.assertIsNone(zernio.zernio_profile("whop:\n  company: biz_1\n"))

    def test_each_day_counts_its_posts_and_averages_the_weeks_views(self) -> None:
        days = zernio.daily_readings(POSTS, date(2026, 10, 3), days=4)
        by = lambda day, metric: next(r for r in days[day] if r["metric_id"] == metric)
        self.assertEqual(by("2026-10-01", "posts_published")["value"], 2.0)
        self.assertEqual(by("2026-10-02", "posts_published")["value"], 0.0)
        self.assertEqual(by("2026-10-03", "views_per_post")["value"], 150.0)  # (100 + 300 + 50) / 3
        self.assertEqual(by("2026-09-30", "views_per_post")["status"], "source_gap")  # no posts that week: a gap, not zero

    def test_refresh_writes_observations_and_pages_through_zernio(self) -> None:
        calls = []

        def fetch(url: str, key: str):
            calls.append(url)
            if "/accounts" in url:
                return {"accounts": [ACCOUNT]}
            page = 1 if "page=1" in url else 2
            return {"posts": POSTS[:2] if page == 1 else POSTS[2:], "pagination": {"pages": 2}}

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "bindings.yaml").write_text("zernio:\n  profile: abc123\n")
            (root / "farplane" / "metrics.yaml").write_text("metrics:\n  instagram_views:\n    refresh_ref: zernio_content\n")
            result = zernio.refresh_zernio(root, "key", date(2026, 10, 3), fetch)
            written = json.loads((root / zernio.OBSERVATIONS / "2026-10-01.json").read_text())
        self.assertEqual(result, {"status": "read", "posts": 3, "accounts": 1})
        self.assertEqual(len(calls), 3)
        views = next(r for r in written["observations"] if r["metric_id"] == "instagram_views")
        self.assertEqual(views["payload"]["distribution_account"]["account_id"], "northwind.studio")
        self.assertEqual(views["payload"]["source"]["provider"], "zernio")
        self.assertEqual(written["source_id"], "zernio_content")
        self.assertEqual(written["observations"][0]["payload"]["source"]["provider"], "zernio")

    def test_no_key_or_no_binding_is_said_plainly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(zernio.refresh_zernio(root, "key", date(2026, 10, 3))["status"], "none")
            (root / "farplane").mkdir()
            (root / "farplane" / "bindings.yaml").write_text("zernio:\n  profile: abc123\n")
            self.assertEqual(zernio.refresh_zernio(root, "", date(2026, 10, 3))["status"], "gap")


if __name__ == "__main__":
    unittest.main()
