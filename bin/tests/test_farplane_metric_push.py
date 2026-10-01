from __future__ import annotations

import argparse
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.core import farplane_metric_push as push  # noqa: E402

DAY_MS = 1_782_950_400_000  # 2026-07-02T00:00:00Z


class Accepted:
    status = 200

    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def __enter__(self) -> "Accepted":
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def read(self, *_: object) -> bytes:
        return json.dumps(self.payload).encode()


class FakeSite:
    """Records `/metrics/readings` posts and answers like the deployment."""

    def __init__(self) -> None:
        self.posts: list[tuple[str, dict[str, str], dict]] = []

    def __call__(self, req: object, timeout: float = 0) -> Accepted:
        body = json.loads(req.data)  # type: ignore[attr-defined]
        self.posts.append((req.full_url, dict(req.header_items()), body))  # type: ignore[attr-defined]
        return Accepted({"ok": True, "result": {"inserted": len(body["readings"]), "updated": 0}})


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def snapshot(points: list[dict]) -> dict:
    return {
        "metrics": {
            "definitions": {
                "revenue_usd": {"unit": "usd", "refresh_ref": "billing_metrics", "primitive_id": "manual_source_gap"},
                "auto_time_ratio": {"unit": "ratio", "primitive_id": "autonomy_time_feedback"},
            },
            "series": [
                {"metric_id": "revenue_usd", "unit": "usd", "series": points},
                {"metric_id": "auto_time_ratio", "unit": "ratio", "series": [{"date": "2026-07-02", "value": 0.25}]},
                {"metric_id": "never_read", "unit": "x", "series": []},
            ],
        }
    }


class SnapshotReadingsTests(unittest.TestCase):
    def test_every_series_point_becomes_a_reading_with_the_recipe_source(self) -> None:
        readings, gaps = push.snapshot_readings(
            snapshot([{"date": "2026-07-01", "value": 120.5}, {"date": "2026-07-02", "value": 1200}]),
            "globex",
        )

        self.assertEqual(gaps, [])
        by_metric = {(row["metric"], row["at"]): row for row in readings}
        revenue = by_metric[("revenue_usd", DAY_MS)]
        self.assertEqual(revenue["project"], "globex")
        self.assertEqual(revenue["value"], 1200.0)
        self.assertEqual(revenue["display"], "$1,200")
        self.assertEqual(revenue["source"], "billing_metrics")
        self.assertEqual(by_metric[("auto_time_ratio", DAY_MS)]["source"], "autonomy_time_feedback")
        self.assertEqual(by_metric[("auto_time_ratio", DAY_MS)]["display"], "0.25 ratio")
        self.assertEqual(len(readings), 3)

    def test_project_slug_matches_the_office(self) -> None:
        self.assertEqual(push.project_slug("Globex Media Co."), "globex-media-co")


class WhopCashTests(unittest.TestCase):
    def test_bound_companies_balances_sum_to_todays_company_cash(self) -> None:
        balances = {"biz_A": 100.5, "biz_B": 20}
        fetch = lambda url, key: {"treasury_balance": {"balance_usd": balances[url.rsplit("/", 1)[1]]}}
        readings, gaps = push.whop_cash_readings(["biz_A", "biz_B"], "key", fetch)
        self.assertEqual(gaps, [])
        (cash,) = readings
        self.assertEqual((cash["project"], cash["metric"], cash["source"], cash["value"]), ("company", "cash", "whop", 120.5))
        self.assertEqual(cash["at"], push.today_ms())

    def test_a_forbidden_balance_is_a_gap_naming_the_scope_never_zero(self) -> None:
        def fetch(url: str, key: str) -> dict:
            raise urllib.error.HTTPError(url, 403, "forbidden", None, None)
        readings, gaps = push.whop_cash_readings(["biz_A"], "key", fetch)
        self.assertEqual(readings, [])
        self.assertIn("company:balance:read", gaps[0])

    def test_an_accessible_ledger_with_no_balances_holds_zero(self) -> None:
        readings, gaps = push.whop_cash_readings(["biz_A"], "key", lambda *_: {"balances": [], "treasury_balance": None})
        self.assertEqual((readings[0]["value"], gaps), (0.0, []))
        self.assertEqual(push.whop_balance_usd({"balances": [{"currency": "usd", "balance": 5}], "treasury_balance": None}), 5.0)
        self.assertIsNone(push.whop_balance_usd({"balances": [{"currency": "eur", "balance": 5}]}))

    def test_no_key_or_no_binding_is_a_gap(self) -> None:
        self.assertEqual(push.whop_cash_readings(["biz_A"], "", lambda *_: {}), ([], ["whop_api_key_missing"]))
        self.assertEqual(push.whop_cash_readings([], "key", lambda *_: {}), ([], ["no_whop_company_bound"]))

    def test_whop_company_is_read_from_bindings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "bindings.yaml").write_text("kanban:\n  provider: github_issues\nwhop:\n  company: biz_Test123\n", encoding="utf-8")
            self.assertEqual(push.whop_companies([root, root, Path(tmp) / "none"]), ["biz_Test123"])


class RunPushTests(unittest.TestCase):
    def run_push(self, home: Path, urlopen: object, project_root: Path | None = None, cash: float | None = None) -> tuple[int, dict]:
        env = {
            "FARPLANE_CONFIG_DISABLE": "1",
            "FARPLANE_STATE_DIR": str(home),
            "FARPLANE_CONVEX_SITE_URL": "https://example-site.convex.site",
            "FARPLANE_TELEMETRY_TOKEN": "test-token",
        }
        args = argparse.Namespace(project_root=str(project_root) if project_root else None, json=True, cash=cash)
        out = io.StringIO()
        with patch.dict(os.environ, env, clear=True), patch("urllib.request.urlopen", side_effect=urlopen), redirect_stdout(out):
            code = push.run_push(args)
        return code, json.loads(out.getvalue())

    def make_home(self, tmp: Path) -> tuple[Path, Path]:
        home = tmp / "state"
        project = tmp / "globex"
        write_json(project / ".farplane" / "project" / "ui" / "latest.json", snapshot([{"date": "2026-07-02", "value": 10}]))
        write_json(
            home / "company.json",
            {"projects": [{"name": "Globex", "trackingContext": str(project)}, {"name": "Initech", "trackingContext": str(tmp / "none")}]},
        )
        return home, project

    def test_pushes_every_project_and_cash_with_the_token_header(self) -> None:
        site = FakeSite()
        with tempfile.TemporaryDirectory() as tmp:
            home, _ = self.make_home(Path(tmp))
            code, payload = self.run_push(home, site)

        self.assertEqual(code, 0)
        statuses = {row["project"]: row["status"] for row in payload["results"]}
        self.assertEqual(statuses, {"globex": "pushed", "initech": "skipped", "company": "pushed"})
        url, headers, body = site.posts[0]
        self.assertEqual(url, "https://example-site.convex.site/metrics/readings")
        self.assertEqual(headers["X-farplane-telemetry-token"], "test-token")
        self.assertEqual({row["project"] for row in body["readings"]}, {"globex"})
        company = next(row for row in payload["results"] if row["project"] == "company")
        self.assertEqual((company["readings"], company["gaps"]), (0, ["no_whop_company_bound"]))
        self.assertNotIn("test-token", json.dumps(payload))

    def test_operator_reported_cash_is_pushed_as_today_s_cash(self) -> None:
        site = FakeSite()
        with tempfile.TemporaryDirectory() as tmp:
            home, _ = self.make_home(Path(tmp))
            code, _ = self.run_push(home, site, cash=42.0)
        self.assertEqual(code, 0)
        reading = site.posts[-1][2]["readings"][0]
        self.assertEqual((reading["metric"], reading["source"], reading["value"]), ("cash", "operator", 42.0))

    def test_one_project_root_pushes_only_that_snapshot(self) -> None:
        site = FakeSite()
        with tempfile.TemporaryDirectory() as tmp:
            home, project = self.make_home(Path(tmp))
            code, payload = self.run_push(home, site, project)

        self.assertEqual(code, 0)
        self.assertEqual([row["project"] for row in payload["results"]], ["globex"])
        self.assertEqual(len(site.posts), 1)

    def test_batches_of_two_hundred(self) -> None:
        site = FakeSite()
        readings = [{"metric": "m", "at": index + 1} for index in range(450)]
        with patch.dict(os.environ, {"FARPLANE_CONFIG_DISABLE": "1"}, clear=True), patch("urllib.request.urlopen", side_effect=site):
            totals = push.push_readings(readings, {"site_url": "https://example-site.convex.site", "deployment_url": "", "token": "t"})

        self.assertEqual([len(post[2]["readings"]) for post in site.posts], [200, 200, 50])
        self.assertEqual(totals, {"sent": 450, "inserted": 450, "updated": 0})

    def test_unreachable_convex_fails_the_run_with_the_reason(self) -> None:
        def offline(req: object, timeout: float = 0) -> None:
            raise URLError("offline")

        with tempfile.TemporaryDirectory() as tmp:
            home, _ = self.make_home(Path(tmp))
            code, payload = self.run_push(home, offline)

        self.assertEqual(code, 1)
        failed = [row for row in payload["results"] if row["status"] == "failed"]
        self.assertEqual({row["project"] for row in failed}, {"globex"})
        self.assertIn("/metrics/readings: unreachable", failed[0]["reason"])


if __name__ == "__main__":
    unittest.main()
