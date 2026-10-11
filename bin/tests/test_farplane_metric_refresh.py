from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "bin" / "core" / "farplane_metric_refresh.py"
SPEC = importlib.util.spec_from_file_location("farplane_metric_refresh", SCRIPT)
assert SPEC and SPEC.loader
metric_refresh = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(metric_refresh)


CONVEX_ENV = {
    "FARPLANE_CONFIG_DISABLE": "1",
    "FARPLANE_CONVEX_SITE_URL": "https://example-site.convex.site",
    "CONVEX_URL": "https://example-site.convex.cloud",
    "FARPLANE_TELEMETRY_TOKEN": "test-token",
}


def ms(iso: str) -> int:
    return int(datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp() * 1000)


class FakeConvex:
    """Answers `/api/query` like the deployment: hook rows, then runtime activity-feed pages."""

    def __init__(self, hook_rows: list[dict] | None = None, runtime_events: list[dict] | None = None) -> None:
        self.hook_rows = hook_rows or []
        self.runtime_events = runtime_events or []
        self.calls: list[dict] = []

    def __call__(self, req: object, timeout: float = 0) -> "FakeConvex.Answer":
        body = json.loads(req.data)  # type: ignore[attr-defined]
        self.calls.append(body)
        if body["path"].endswith(":listHookTelemetryEvents"):
            value: object = self.hook_rows
        else:
            value = {"events": self.runtime_events, "hasMore": False}
        return FakeConvex.Answer({"status": "success", "value": value})

    class Answer:
        status = 200

        def __init__(self, payload: dict) -> None:
            self.payload = payload

        def __enter__(self) -> "FakeConvex.Answer":
            return self

        def __exit__(self, *_: object) -> None:
            return None

        def read(self, *_: object) -> bytes:
            return json.dumps(self.payload).encode()


def hook_prompt(at: str, session: str, turn: str) -> dict:
    return {
        "hookName": "farplane-console-ping",
        "hookType": "UserPromptSubmit",
        "sessionId": session,
        "eventAt": ms(at),
        "payload": {"eventType": "turn_start", "turnId": turn},
    }


def convex(fake: object):
    return patch.dict(os.environ, CONVEX_ENV), patch("urllib.request.urlopen", side_effect=fake)


class FarplaneMetricRefreshTests(unittest.TestCase):
    def test_resolve_refresh_plan_keeps_pinned_markdown_edge_in_its_own_job(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            metrics_file = Path(tmp) / "metrics.yaml"
            metrics_file.write_text(
                """kind: project-metrics
metrics:
  edge:
    refresh: Summarize the newest verified advantage for <YYYY-MM-DD>.
    type: markdown
    leverage: edge
    pinned: true
""",
                encoding="utf-8",
            )

            plan = metric_refresh.resolve_refresh_plan(metrics_file, ["edge"], "2026-08-12")

        self.assertEqual(plan["source_gaps"], [])
        self.assertEqual(plan["refresh_groups"][0]["requested_metric_ids"], ["edge"])
        self.assertEqual(plan["refresh_groups"][0]["metric_types"], {"edge": "markdown"})

    def test_record_refresh_result_turns_invalid_markdown_into_a_source_gap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = metric_refresh.record_refresh_result(
                root,
                "2026-08-12",
                {
                    "refresh_id": "metric:edge",
                    "requested_metric_ids": ["edge"],
                    "metric_types": {"edge": "markdown"},
                },
                {"edge": {"value": 4, "status": "available"}},
            )
            payload = json.loads(Path(result["path"]).read_text(encoding="utf-8"))

        observation = payload["observations"][0]
        self.assertEqual(observation["metric_id"], "edge")
        self.assertEqual(observation["status"], "source_gap")
        self.assertIsNone(observation["value"])
        self.assertEqual(observation["payload"]["reason"], "invalid_markdown_refresh_value")

    def test_record_refresh_result_writes_a_gap_for_missing_markdown_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = metric_refresh.record_refresh_result(
                root,
                "2026-08-12",
                {
                    "refresh_id": "metric:edge",
                    "requested_metric_ids": ["edge"],
                    "metric_types": {"edge": "markdown"},
                },
                {},
            )
            payload = json.loads(Path(result["path"]).read_text(encoding="utf-8"))

        self.assertEqual(payload["observations"][0]["status"], "source_gap")
        self.assertEqual(payload["observations"][0]["payload"]["reason"], "missing_markdown_refresh_output")

    def test_counts_completed_ticket_kpi_rewards_for_date(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket_dir = root / "tickets" / "TASK-0001"
            ticket_dir.mkdir(parents=True)
            (ticket_dir / "ticket.md").write_text(
                """---
ticket_id: TASK-0001
phase: complete
status: done
updated_at: 2026-07-02T09:00:00Z
---

# TASK-0001

## Reward

```yaml
kpi_rewards:
  - reward_id: accepted-harness-7d
    kpi_id: accepted_harness_improvements
    expected_reward: "one shipped harness fix"
    actual_result: "shipped fix remained after review"
    decision: accept
    evaluated_at: 2026-07-02T09:00:00Z
    evaluation_key: eval-accepted-harness-7d
    evidence_refs: [artifacts/proof.md]
guard: "proof required"
```

## Done / Proof
- Evidence: artifacts/proof.md
- TAS-A verdict: pass
""",
                encoding="utf-8",
            )

            reading = metric_refresh.count_ticket_kpi_rewards(
                root / "tickets",
                "2026-07-02",
                "accepted_harness_improvements",
            )

        self.assertEqual(reading["status"], "available")
        self.assertEqual(reading["value"], 1)
        self.assertEqual(reading["payload"]["tickets"][0]["ticket_id"], "TASK-0001")

    def test_calculates_autonomy_time_ratio_from_convex_events(self) -> None:
        # The hook and the runtime both record human-1's first prompt; it counts once.
        fake = FakeConvex(
            hook_rows=[
                hook_prompt("2026-07-02T10:00:00Z", "human-1", "t1"),
                hook_prompt("2026-07-02T10:20:00Z", "human-1", "t2"),
                hook_prompt("2026-07-02T12:00:00Z", "human-2", "t3"),
                hook_prompt("2026-07-03T08:00:00Z", "human-2", "t4"),
            ],
            runtime_events=[
                {
                    "activityType": "turn_start",
                    "sessionKey": "human-1",
                    "occurredAt": ms("2026-07-02T10:00:00.400Z"),
                    "detail": json.dumps({"turnId": "t1"}),
                },
                {"activityType": "skill_requested", "sessionKey": "human-1", "occurredAt": ms("2026-07-02T10:00:01Z")},
            ],
        )
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp) / ".farplane"
            state_dir = runtime / "state"
            state_dir.mkdir(parents=True)
            (state_dir / "ticket-thread-associations.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "ticket_id": "TASK-0001",
                                "thread_id": "auto-1",
                                "execution_started_at": "2026-07-02T09:00:00Z",
                                "observed_at": "2026-07-02T09:45:00Z",
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            automation_dir = runtime / "automation"
            automation_dir.mkdir(parents=True)
            (automation_dir / "rewards.jsonl").write_text(
                json.dumps(
                    {
                        "timestamp": "2026-07-02T09:45:00Z",
                        "outcome": "positive",
                        "evidence": ["tickets/TASK-0001/artifacts/proof.md"],
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            env, urlopen = convex(fake)
            with env, urlopen:
                reading = metric_refresh.calculate_autonomy_time_ratio(runtime, "2026-07-02")

        hook_query = fake.calls[0]
        self.assertEqual(hook_query["args"]["hookType"], "UserPromptSubmit")
        self.assertTrue(hook_query["args"]["projectId"].startswith("codex-proj-"))
        self.assertEqual(fake.calls[1]["path"], "modules/telemetry/queries:getTeamActivityFeed")
        self.assertEqual(reading["status"], "available")
        self.assertEqual(reading["value"], 1.5)
        self.assertEqual(reading["payload"]["human_prompt_count"], 3)
        self.assertEqual(reading["payload"]["autonomous_worker_elapsed_minutes"], 45)

    def test_calculates_ticket_intervention_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket_dir = root / "tickets" / "TASK-0001"
            ticket_dir.mkdir(parents=True)
            (ticket_dir / "ticket.md").write_text(
                """---
ticket_id: TASK-0001
phase: complete
status: done
updated_at: 2026-07-02T10:30:00Z
---

# TASK-0001

## Done / Proof
- Evidence: proof.md
""",
                encoding="utf-8",
            )
            runtime = root / ".farplane"
            state_dir = runtime / "state"
            state_dir.mkdir(parents=True)
            (state_dir / "ticket-thread-associations.jsonl").write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0001",
                        "thread_id": "thread-a",
                        "execution_started_at": "2026-07-02T10:00:00Z",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            fake = FakeConvex(hook_rows=[hook_prompt("2026-07-02T10:10:00Z", "thread-a", "t1"), hook_prompt("2026-07-02T11:10:00Z", "thread-a", "t2")])
            env, urlopen = convex(fake)
            with env, urlopen:
                readings = metric_refresh.calculate_ticket_intervention_metrics(root / "tickets", runtime, "2026-07-02")

        self.assertEqual(readings["ticket_intervention_turn_count"]["value"], 1)
        self.assertEqual(readings["intervention_free_ticket_count"]["value"], 0)
        self.assertEqual(readings["auto_completion_rate"]["value"], 0.0)

    def test_unreachable_convex_is_a_named_source_gap_not_a_zero(self) -> None:
        def offline(req: object, timeout: float = 0) -> None:
            raise URLError("offline")

        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp) / ".farplane"
            runtime.mkdir()
            env, urlopen = convex(offline)
            with env, urlopen:
                reading = metric_refresh.calculate_autonomy_time_ratio(runtime, "2026-07-02")
            with patch.dict(os.environ, {"FARPLANE_CONFIG_DISABLE": "1"}, clear=True):
                unset = metric_refresh.calculate_autonomy_time_ratio(runtime, "2026-07-02")

        self.assertEqual(reading["status"], "source_gap")
        self.assertIsNone(reading["value"])
        self.assertIn("telemetry_unavailable:convex events", reading["payload"]["gaps"][0])
        self.assertIn("unreachable", reading["payload"]["gaps"][0])
        self.assertNotIn("test-token", json.dumps(reading))
        self.assertIn("CONVEX_URL is not set", unset["payload"]["gaps"][0])

    def test_ticket_intervention_empty_window_is_not_source_gap_for_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket_dir = root / "tickets"
            ticket_dir.mkdir()
            runtime = root / ".farplane"
            (runtime / "state").mkdir(parents=True)
            (runtime / "state" / "ticket-thread-associations.jsonl").write_text("", encoding="utf-8")

            # No completed ticket needs a thread's prompts, so Convex isn't asked at all.
            with patch("urllib.request.urlopen", side_effect=AssertionError("no telemetry read expected")):
                readings = metric_refresh.calculate_ticket_intervention_metrics(ticket_dir, runtime, "2026-07-02")

        self.assertEqual(readings["ticket_intervention_turn_count"]["status"], "available")
        self.assertEqual(readings["ticket_intervention_turn_count"]["value"], 0)
        self.assertEqual(readings["intervention_free_ticket_count"]["status"], "available")
        self.assertEqual(readings["intervention_free_ticket_count"]["value"], 0)
        self.assertEqual(readings["auto_completion_rate"]["status"], "not_applicable")
        self.assertIsNone(readings["auto_completion_rate"]["value"])

    def test_selects_content_metric_targets_for_window(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / ".farplane" / "content" / "ledger.jsonl"
            ledger.parent.mkdir(parents=True)
            ledger.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "content_id": "instagram:old",
                                "platform": "instagram",
                                "external_id": "old",
                                "status": "posted",
                                "published_at": "2026-06-20T10:00:00Z",
                                "kpis": ["instagram_views"],
                            }
                        ),
                        json.dumps(
                            {
                                "content_id": "instagram:fresh",
                                "platform": "instagram",
                                "external_id": "fresh",
                                "status": "posted",
                                "published_at": "2026-07-02T10:00:00Z",
                                "kpis": ["instagram_views", "evidence_distribution_reach"],
                            }
                        ),
                        json.dumps(
                            {
                                "content_id": "instagram:draft",
                                "platform": "instagram",
                                "external_id": "draft",
                                "status": "draft",
                                "published_at": "2026-07-02T10:00:00Z",
                                "kpis": ["instagram_views"],
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            packet = metric_refresh.select_content_metric_targets(
                ledger,
                "instagram",
                "instagram_views",
                "2026-07-02",
                7,
            )

        self.assertEqual(packet["status"], "available")
        self.assertEqual(packet["external_ids"], ["fresh"])

    def test_select_content_metric_targets_reports_missing_ledger_gap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            packet = metric_refresh.select_content_metric_targets(
                Path(tmp) / ".farplane" / "content" / "ledger.jsonl",
                "x",
                "x_views",
                "2026-07-02",
                7,
            )

        self.assertEqual(packet["status"], "source_gap")
        self.assertEqual(packet["external_ids"], [])
        self.assertTrue(packet["payload"]["gaps"][0].startswith("missing:"))


if __name__ == "__main__":
    unittest.main()
