from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.core import farplane_test_versions as versions  # noqa: E402

START = "2026-10-01T00:00:00Z"


def test_with(*options):
    return {"project": "northwind", "id": "price-test", "status": "running", "startedAt": START, "options": list(options)}


class TestVersionsTests(unittest.TestCase):
    def test_whop_counts_paid_sales_on_the_plan_since_the_test_began(self) -> None:
        pages = [
            {"data": [
                {"plan_id": "plan_a", "status": "paid", "usd_total": 29, "created_at": "2026-10-02T10:00:00Z"},
                {"plan_id": "plan_a", "status": "failed", "usd_total": 0, "created_at": "2026-10-02T09:00:00Z"},
                {"plan_id": "plan_b", "status": "paid", "usd_total": 49, "created_at": "2026-10-02T08:00:00Z"},
            ], "page_info": {"has_next_page": True, "end_cursor": "c1"}},
            {"data": [
                {"plan_id": "plan_a", "status": "paid", "usd_total": 29, "refunded_at": "2026-10-03", "created_at": "2026-10-01T12:00:00Z"},
                {"plan_id": "plan_a", "status": "paid", "usd_total": 29, "created_at": "2026-09-30T12:00:00Z"},
            ], "page_info": {"has_next_page": True, "end_cursor": "c2"}},
        ]
        calls = []
        fetch = lambda url, key: (calls.append(url), pages[len(calls) - 1])[1]
        since = versions._ms(START)
        self.assertEqual(versions.whop_plan_totals("biz_x", "plan_a", since, "key", fetch), (1, 3))  # refunded and pre-test sales don't count
        self.assertEqual(len(calls), 2)  # stops once a page reaches before the test began
        self.assertIn("after=c1", calls[1])

    def test_zernio_counts_clicks_out_of_views(self) -> None:
        data = {"p1": {"analytics": {"views": 1000, "clicks": 20, "websiteClicks": 5}}, "p2": {"analytics": {"views": 500, "clicks": 10}}}
        fetch = lambda url, key: data[url.rsplit("=", 1)[1]]
        self.assertEqual(versions.zernio_post_totals(["p1", "p2"], "key", fetch), (35, 1500))

    def test_refresh_records_each_sourced_version_and_reports_gaps(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "bindings.yaml").write_text("whop:\n  company: biz_x\n")
            tests = [
                test_with({"id": "a", "metricSource": {"kind": "whop_plan", "ref": "plan_a"}}, {"id": "b", "metricSource": {"kind": "zernio_posts", "ref": "p1"}}, {"id": "c"}),
                {**test_with({"id": "a", "metricSource": {"kind": "whop_plan", "ref": "plan_a"}}), "status": "proposed"},
            ]
            sent = []
            fetch = lambda url, key: {"data": [{"plan_id": "plan_a", "status": "paid", "usd_total": 9, "created_at": "2026-10-02T00:00:00Z"}], "page_info": {}}
            lines = versions.refresh_versions(tests, {"northwind": root}, {"whop": "k", "zernio": ""}, sent.append, 1_790_000_000_000, fetch)
        self.assertEqual([(l["version"], l["status"]) for l in lines], [("a", "counted"), ("b", "gap")])
        self.assertEqual(sent, [{"op": "source-totals", "project": "northwind", "testId": "price-test", "option": "a", "successes": 1, "attempts": 1, "at": 1_790_000_000_000}])


if __name__ == "__main__":
    unittest.main()
