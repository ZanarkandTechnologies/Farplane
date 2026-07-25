from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

import farplane_skill_rollout as rollout


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")


class FarplaneSkillRolloutTests(unittest.TestCase):
    def test_resolves_skill_rollout_payload_for_ui(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "docs" / "skills" / "registry.jsonl"
            intelligence = root / ".farplane" / "generated" / "graphs" / "skill-template-intelligence.json"
            write_jsonl(
                registry,
                [
                    {"name": "alpha", "tier": 1, "source": "local"},
                    {"name": "beta", "tier": 3, "source": "external"},
                ],
            )
            write_json(
                intelligence,
                {
                    "current_template_version": "0.3.2",
                    "rollout_summary": {
                        "total_skills": 3,
                        "by_status": {"current": 1, "external": 1, "stale": 1},
                        "by_template_version": {"0.3.2": 1, "0.2.0": 1, "missing": 1},
                        "by_source": {"external": 1, "local": 2},
                    },
                    "rollout": [
                        {
                            "skill_id": "alpha",
                            "path": "skills/alpha/SKILL.md",
                            "source": "local",
                            "tier": 1,
                            "template_version": "0.3.2",
                            "status": "current",
                            "eval": "evals/evals.json",
                            "qa_checklist": "",
                            "skill_ui": "",
                            "has_checklist": True,
                        },
                        {
                            "skill_id": "beta",
                            "path": "skills/beta/SKILL.md",
                            "source": "external",
                            "tier": 3,
                            "template_version": "missing",
                            "status": "external",
                            "eval": "",
                            "qa_checklist": "",
                            "skill_ui": "",
                            "has_checklist": False,
                        },
                        {
                            "skill_id": "gamma",
                            "path": "skills/gamma/SKILL.md",
                            "source": "local",
                            "tier": 2,
                            "template_version": "0.2.0",
                            "status": "stale",
                            "eval": "",
                            "qa_checklist": "qa_checklist.md",
                            "skill_ui": "viewer.html",
                            "has_checklist": False,
                        },
                    ],
                    "template_rollout_summary": {
                        "skill-template": {
                            "current_version": "0.3.2",
                            "total_consumers": 2,
                            "by_status": {"current": 1, "stale": 1},
                        }
                    },
                    "template_rollout": [
                        {
                            "template_id": "skill-template",
                            "current_version": "0.3.2",
                            "feature_refs": ["FEAT-0048"],
                            "target_basis": "local skills that declare skill-template usage",
                            "consumer_id": "alpha",
                            "consumer_scope": "skill",
                            "path": "skills/alpha/SKILL.md",
                            "used_version": "0.3.2",
                            "status": "current",
                        },
                        {
                            "template_id": "skill-template",
                            "current_version": "0.3.2",
                            "feature_refs": ["FEAT-0048"],
                            "target_basis": "local skills that declare skill-template usage",
                            "consumer_id": "gamma",
                            "consumer_scope": "skill",
                            "path": "skills/gamma/SKILL.md",
                            "used_version": "0.2.0",
                            "status": "stale",
                        },
                    ],
                },
            )

            result = rollout.resolve_skill_rollout_stats(
                standard_root=root,
                registry_path=registry,
                intelligence_path=intelligence,
            )

        self.assertEqual(result["schema"], "farplane_skill_rollout")
        self.assertEqual(result["currentTemplateVersion"], "0.3.2")
        self.assertEqual(result["counts"]["skills"], 3)
        self.assertEqual(result["counts"]["current"], 1)
        self.assertEqual(result["counts"]["stale"], 1)
        self.assertEqual(result["counts"]["external"], 1)
        self.assertEqual(result["counts"]["withEval"], 1)
        self.assertEqual(result["counts"]["withQaChecklist"], 1)
        self.assertEqual(result["counts"]["withSkillUi"], 1)
        self.assertEqual(result["counts"]["templateDriftItems"], 1)
        self.assertEqual(result["registryCounts"]["byTier"], {"1": 1, "3": 1})
        self.assertEqual(result["skills"][0]["skillId"], "alpha")
        self.assertEqual(result["skills"][2]["qaChecklist"], "qa_checklist.md")
        self.assertEqual(result["templateRollout"][1]["consumerId"], "gamma")

    def test_run_scan_prints_json_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "docs" / "skills" / "registry.jsonl"
            intelligence = root / ".farplane" / "generated" / "graphs" / "skill-template-intelligence.json"
            write_jsonl(registry, [])
            write_json(
                intelligence,
                {
                    "current_template_version": "0.3.2",
                    "rollout_summary": {},
                    "rollout": [],
                    "template_rollout_summary": {},
                    "template_rollout": [],
                },
            )
            args = argparse.Namespace(
                standard_root=str(root),
                registry=str(registry),
                intelligence=str(intelligence),
                json=True,
            )
            stream = io.StringIO()

            with contextlib.redirect_stdout(stream):
                code = rollout.run_scan(args)

        self.assertEqual(code, 0)
        payload = json.loads(stream.getvalue())
        self.assertEqual(payload["schema"], "farplane_skill_rollout")

    def test_missing_intelligence_reports_clean_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "docs" / "skills" / "registry.jsonl"
            write_jsonl(registry, [])

            with self.assertRaises(rollout.SkillRolloutError) as raised:
                rollout.resolve_skill_rollout_stats(
                    standard_root=root,
                    registry_path=registry,
                    intelligence_path=root / "missing.json",
                )

        self.assertIn("missing_json:", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
