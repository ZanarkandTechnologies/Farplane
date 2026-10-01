from __future__ import annotations

import argparse
import io
import json
import sys
import tempfile
import threading
import unittest
from contextlib import redirect_stdout
from datetime import date
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.core import farplane_loop as loop  # noqa: E402

MONDAY = date(2026, 10, 19)
# A fictional studio's Distribution plan, as the office's `/office/local/plans` returns it.
PLAN = {
    "input": {"metric": "posts_published", "label": "Videos posted", "target": 100, "from": "2026-10-01", "by": "2026-12-31"},
    "output": {"metric": "store_clicks_per_post", "label": "Store clicks per video"},
    "routine": {"job": "Make and post one video", "test": "reel-hook", "gate": "publish"},
    "setup": [],
}


def at(day: date, hour: int = 12) -> int:
    return loop.ms(day) + hour * 3_600_000


class FakeOffice:
    """Answers `/office/local/plans` and `/office/local/seed` like the office, queueing each key once.

    The office counts what's done itself (`done`); None is an input with no reading since the plan began.
    """

    def __init__(self, token: str) -> None:
        self.token = token
        self.done: int | None = 14
        self.keys: set[str] = set()
        self.seeds: list[dict] = []
        office = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_: object) -> None:
                return None

            def reply(self, status: int, body: dict) -> None:
                data = json.dumps(body).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self) -> None:  # noqa: N802
                if self.headers.get("Authorization") != f"Bearer {office.token}":
                    return self.reply(401, {"error": "token"})
                self.reply(200, {"floors": [
                    {"id": "globex-studio", "name": "Globex Studio", "dir": "/nowhere/globex", "project": "globex-studio-co", "plans": {"offer": None, "leads": PLAN, "sales": None, "delivery": None}},
                    {"id": "initech", "name": "Initech", "dir": "/nowhere/initech", "plans": {"offer": None, "leads": None, "sales": None, "delivery": None}},
                ]})

            def do_POST(self) -> None:  # noqa: N802
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                office.seeds.append(body)
                if office.done is None:
                    return self.reply(200, {"added": 0, "tasks": [], "blocked": "no reading of posts_published since 2026-10-01, so what's done is unknown"})
                quota = -(-(PLAN["input"]["target"] - office.done) // 11)
                added = 0
                if not body["dryRun"]:
                    for i in range(1, quota + 1):
                        key = f"{body['step']}-W43-{i}"
                        added += key not in office.keys
                        office.keys.add(key)
                self.reply(200, {"week": "2026-W43", "done": office.done, "target": 100, "weeksLeft": 11, "quota": quota, "added": added})

        self.server = HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    @property
    def port(self) -> int:
        return self.server.server_address[1]


def convex(readings: dict[str, list[dict]]):
    """A Convex site whose `/metrics/history` holds these readings per metric."""

    def post(path: str, body: dict, _settings: object = None):
        assert path == "/metrics/history", path
        assert body["project"] == "globex-studio-co", body  # the floor's Convex project, from the office
        return [r for r in readings.get(body["metric"], []) if r["at"] >= body.get("since", 0)]

    return post


class LoopMondayTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name)
        self.office = FakeOffice("t0ken")
        data = self.folder / ".agent-office"
        data.mkdir()
        (data / "hook-port").write_text(str(self.office.port))
        (data / "local-token").write_text("t0ken")

    def tearDown(self) -> None:
        self.office.server.shutdown()
        self.tmp.cleanup()

    def run_monday(self, **flags: object) -> dict:
        args = argparse.Namespace(**{"office": str(self.folder), "today": MONDAY.isoformat(), "dry_run": False, "json": True, **flags})
        out = io.StringIO()
        with redirect_stdout(out):
            code = loop.run_monday(args)
        self.assertEqual(code, 0, out.getvalue())
        return json.loads(out.getvalue())

    def test_review_compares_last_week_with_the_week_before(self) -> None:
        readings = [
            {"value": 9.0, "at": at(date(2026, 9, 30))},
            {"value": 7.0, "at": at(date(2026, 10, 7))},
            {"value": 6.5, "at": at(date(2026, 10, 9))},  # the week before's last reading
            {"value": 5.0, "at": at(date(2026, 10, 15))},
        ]
        self.assertEqual(loop.review(readings, MONDAY), {"last_week": 5.0, "week_before": 6.5, "verdict": "worse", "worse_two_weeks_running": True})
        self.assertEqual(loop.review([], MONDAY)["verdict"], "no readings")
        self.assertEqual(loop.review(readings[-1:], MONDAY)["verdict"], "one week only")

    def test_seeds_each_plan_once_and_names_floors_without_one(self) -> None:
        clicks = [{"value": 6.0, "at": at(date(2026, 10, 8))}, {"value": 7.0, "at": at(date(2026, 10, 14))}]
        with patch.object(loop, "site_post", convex({"store_clicks_per_post": clicks})):
            first = self.run_monday()
            again = self.run_monday()
        [step] = first["steps"]
        self.assertEqual((step["floor"], step["step"], step["status"], step["done"], step["quota"], step["added"]), ("globex-studio", "leads", "seeded", 14, 8, 8))
        self.assertEqual(step["review"]["verdict"], "better")
        self.assertEqual(first["skipped"], ["Initech"])
        self.assertEqual(again["steps"][0]["added"], 0)
        self.assertEqual(len(self.office.keys), 8)
        # Farplane doesn't count what's done: the office does, with the CEO desk's rule.
        self.assertEqual(self.office.seeds[0], {"floor": "globex-studio", "step": "leads", "today": "2026-10-19", "by": "the Morning job", "dryRun": False})

    def test_no_input_reading_means_no_seed(self) -> None:
        self.office.done = None
        with patch.object(loop, "site_post", convex({})):
            result = self.run_monday()
        self.assertEqual(result["steps"][0]["status"], "blocked")
        self.assertIn("no reading of posts_published since 2026-10-01", result["steps"][0]["reason"])
        self.assertEqual(self.office.keys, set())

    def test_without_convex_the_review_is_a_gap_and_the_office_still_seeds(self) -> None:
        def down(*_: object) -> None:
            raise loop.ConvexUnavailable("FARPLANE_CONVEX_SITE_URL is not set")

        with patch.object(loop, "site_post", down):
            result = self.run_monday()
        self.assertEqual(result["steps"][0]["review"], {"verdict": "unknown", "gap": "FARPLANE_CONVEX_SITE_URL is not set"})
        self.assertEqual(result["steps"][0]["status"], "seeded")

    def test_dry_run_and_a_missing_office(self) -> None:
        with patch.object(loop, "site_post", convex({})):
            result = self.run_monday(dry_run=True)
        self.assertEqual(result["steps"][0]["status"], "dry-run")
        self.assertEqual(self.office.keys, set())
        args = argparse.Namespace(office=str(self.folder / "elsewhere"), today=None, dry_run=False, json=True)
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(loop.run_monday(args), 1)
        self.assertIn("no office in", json.loads(out.getvalue())["reason"])

if __name__ == "__main__":
    unittest.main()
