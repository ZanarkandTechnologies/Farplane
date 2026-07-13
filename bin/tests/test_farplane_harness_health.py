from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "bin" / "core"
if str(CORE) not in sys.path:
    sys.path.insert(0, str(CORE))

from farplane_harness_health import (
    build_metric_readings,
    compile_harness_health,
    write_metric_observations,
    write_projection,
)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def write_fixture(root: Path) -> None:
    graph_root = root / "skills" / "skill-maintenance" / "graph"
    write_json(
        graph_root / "skill-graph.json",
        {
            "nodes": [
                {
                    "id": "alpha",
                    "path": "skills/alpha/SKILL.md",
                    "source": "local",
                    "tier": 2,
                    "description": "Alpha workflow",
                    "methods": [],
                    "heat": {
                        "invocation_count_recent": 2,
                        "invocation_count_window": 4,
                        "distinct_threads_window": 1,
                        "distinct_tickets_window": 1,
                    },
                }
            ],
            "edges": [{"source": "caller", "target": "alpha", "type": "markdown-ref"}],
        },
    )
    write_json(
        graph_root / "skill-docs.json",
        {
            "skills": {
                "alpha": {
                    "path": "skills/alpha/SKILL.md",
                    "frontmatter": {
                        "name": "alpha",
                        "description": "Alpha workflow",
                        "qa_checklist": "qa_checklist.md",
                        "feature_refs": ["FEAT-1"],
                    },
                    "body": "# Alpha\n\n## Todo List\n- [ ] act\n\n## QA\nRun proof.\n",
                }
            }
        },
    )
    write_json(
        graph_root / "skill-template-intelligence.json",
        {
            "current_template_version": "1.0.0",
            "rollout_summary": {"total_skills": 1, "by_status": {"current": 1}},
            "rollout": [
                {
                    "skill_id": "alpha",
                    "path": "skills/alpha/SKILL.md",
                    "source": "local",
                    "tier": 2,
                    "status": "current",
                    "template_version": "1.0.0",
                    "eval": "evals/evals.json",
                    "qa_checklist": "qa_checklist.md",
                    "has_checklist": True,
                }
            ],
            "template_rollout": [],
            "template_rollout_summary": {},
            "features": [{"id": "FEAT-1"}],
            "template_versions": [
                {"version": "1.0.0", "template_metadata": {"feature_refs": ["FEAT-1"]}}
            ],
        },
    )
    registry = root / "docs" / "skills" / "registry.jsonl"
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(json.dumps({"name": "alpha", "source": "local", "tier": 2}) + "\n", encoding="utf-8")
    write_json(
        root / "skills" / "alpha" / "evals" / "evals.json",
        {"skill_name": "alpha", "evals": [{"id": f"alpha-{index}"} for index in range(5)]},
    )
    write_json(
        root / ".farplane" / "evals" / "runs" / "index.json",
        [{"job_id": "run-1", "created_at": "2026-07-13T00:00:00Z"}],
    )
    write_json(
        root / ".farplane" / "evals" / "runs" / "run-1" / "summary.json",
        {
            "job_id": "run-1",
            "created_at": "2026-07-13T00:00:00Z",
            "task_count": 1,
            "pass_rate": 1.0,
            "verdict_counts": {"A": 1},
            "tasks": [{"task_id": "alpha-case", "pass": True, "verdict": "A"}],
        },
    )
    write_json(
        root / ".farplane" / "evals" / "runs" / "run-1" / "tasks" / "alpha-case.json",
        {"task": {"id": "alpha-case", "tags": ["alpha"]}, "judge": {"pass": True, "verdict": "A"}},
    )


class HarnessHealthTests(unittest.TestCase):
    def test_compiles_rollout_skill_and_eval_health(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_fixture(root)
            payload = compile_harness_health(project_root=root, standard_root=root)

        self.assertEqual(payload["schema"], "farplane_harness_health")
        self.assertEqual(payload["rollout"]["counts"]["current"], 1)
        self.assertEqual(payload["skillHealth"]["weighted"]["score"], 100)
        skill = payload["skillHealth"]["skills"][0]
        self.assertEqual(skill["evidence"]["evalTaskCount"], 5)
        self.assertEqual(
            {row["id"] for row in skill["signals"]},
            {"direct_heat", "composition_heat", "maintainability", "uniqueness"},
        )
        maintainability = next(row for row in skill["signals"] if row["id"] == "maintainability")
        self.assertEqual(maintainability["score"], 100)
        self.assertEqual(payload["evalHealth"]["score"], 100)
        self.assertEqual(payload["evalHealth"]["skills"][0]["status"], "healthy")
        self.assertEqual(payload["sourceGaps"], [])
        reading = payload["metricReadings"]["priority_skill_health_gap_count"]
        self.assertEqual(reading["value"], 0)
        self.assertEqual(reading["payload"]["priority_skill_ids"], ["alpha"])

    def test_missing_eval_runs_stay_unscored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_fixture(root)
            (root / ".farplane" / "evals" / "runs" / "index.json").unlink()
            payload = compile_harness_health(project_root=root, standard_root=root)

        self.assertIsNone(payload["evalHealth"]["score"])
        self.assertEqual(payload["evalHealth"]["status"], "no_runs")
        self.assertTrue(any("index.json" in gap for gap in payload["sourceGaps"]))
        self.assertEqual(
            payload["metricReadings"]["priority_skill_health_gap_count"]["status"],
            "source_gap",
        )
        self.assertIsNone(payload["metricReadings"]["priority_skill_health_gap_count"]["value"])
        self.assertGreater(
            payload["metricReadings"]["harness_health_source_gap_count"]["value"], 0
        )

    def test_priority_cohort_counts_each_unhealthy_skill_once(self) -> None:
        skills = [
            {
                "skillId": "tier-one",
                "source": "local",
                "tier": 1,
                "evidence": {"invocationCount30d": 0},
                "gaps": [
                    {"id": "template_age", "status": "risk"},
                    {"id": "eval_coverage", "status": "missing"},
                    {"id": "qa_checklist", "status": "missing"},
                ],
            },
            {
                "skillId": "used",
                "source": "local",
                "tier": 3,
                "evidence": {"invocationCount30d": 2},
                "gaps": [
                    {"id": "template_age", "status": "good"},
                    {"id": "eval_coverage", "status": "good"},
                    {"id": "qa_checklist", "status": "good"},
                ],
            },
            {
                "skillId": "inactive",
                "source": "local",
                "tier": 3,
                "evidence": {"invocationCount30d": 0},
                "gaps": [],
            },
            {
                "skillId": "external",
                "source": "external",
                "tier": 1,
                "evidence": {"invocationCount30d": 5},
                "gaps": [],
            },
        ]
        readings = build_metric_readings(
            {"skillHealth": {"skills": skills}, "sourceGaps": [], "sources": []}
        )
        reading = readings["priority_skill_health_gap_count"]

        self.assertEqual(reading["value"], 1)
        self.assertEqual(reading["payload"]["priority_skill_ids"], ["tier-one", "used"])
        self.assertEqual(reading["payload"]["template_gap_count"], 1)
        self.assertEqual(reading["payload"]["eval_gap_count"], 1)
        self.assertEqual(reading["payload"]["qa_gap_count"], 1)
        self.assertEqual(len(reading["payload"]["anti_metrics"]), 4)

    def test_writes_schema_valid_metric_batch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_fixture(root)
            payload = compile_harness_health(project_root=root, standard_root=root)
            path = write_metric_observations(root, "2026-07-13", payload)
            batch = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(batch["source_id"], "harness_health")
        self.assertEqual(
            {row["metric_id"] for row in batch["observations"]},
            {"priority_skill_health_gap_count", "harness_health_source_gap_count"},
        )

    def test_write_projection_uses_atomic_project_state_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = write_projection(root, {"schema": "test"})

            self.assertEqual(path, root / ".farplane" / "state" / "harness-health.json")
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), {"schema": "test"})
            self.assertFalse(path.with_suffix(".json.tmp").exists())


if __name__ == "__main__":
    unittest.main()
