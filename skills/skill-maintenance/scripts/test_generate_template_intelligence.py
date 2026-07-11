#!/usr/bin/env python3
from __future__ import annotations

import unittest

import generate_template_intelligence as generator


class GenerateTemplateIntelligenceTests(unittest.TestCase):
    def test_evaluate_template_passes_current_signals(self) -> None:
        snapshot = generator.TemplateSnapshot(
            version="0.2.0",
            source_commit="abc123",
            introduced_at="2026-06-14",
            subject="test",
            text="""
description: "[TODO: Verb input/context into output/artifact when call-condition; <=220 chars.]"

## Phase Boundary

Externalized phase calls must shrink or specialize the current scope.

## Todo List

- [ ] 1. Verify with the named proof command or evidence surface.

## Templates

- Add evals/evals.json and qa_checklist.md when warranted.

## Output
""",
        )

        results = generator.evaluate_template(snapshot)

        self.assertEqual({result["verdict"] for result in results}, {"pass"})

    def test_rollout_rows_classify_current_missing_stale_and_external(self) -> None:
        rows = generator.rollout_rows(
            [
                {"name": "current", "source": "local", "skill_template_version": "0.2.0"},
                {"name": "missing", "source": "local"},
                {"name": "stale", "source": "local", "skill_template_version": "0.1.0"},
                {"name": "external", "source": "external", "skill_template_version": "0.1.0"},
            ],
            "0.2.0",
        )

        by_id = {row["skill_id"]: row for row in rows}

        self.assertEqual(by_id["current"]["status"], "current")
        self.assertEqual(by_id["missing"]["status"], "missing")
        self.assertEqual(by_id["stale"]["status"], "stale")
        self.assertEqual(by_id["external"]["status"], "external")

    def test_template_rollout_rows_classify_consumers_by_template_uses(self) -> None:
        rows = generator.template_rollout_rows(
            [
                {
                    "template_id": "skill-template",
                    "template_version": "0.3.1",
                    "feature_refs": ["FEAT-0001"],
                    "consumer_scope": "skill",
                },
                {
                    "template_id": "farplane-framework",
                    "template_version": "1.2.0",
                    "feature_refs": ["FEAT-0002"],
                    "consumer_scope": "project",
                },
            ],
            [
                {
                    "consumer_id": "advise",
                    "consumer_scope": "skill",
                    "path": "skills/advise/SKILL.md",
                    "template_uses": {"skill-template": "0.3.1"},
                    "surfaces": {"skill": True},
                },
                {
                    "consumer_id": "Farplane-UI",
                    "consumer_scope": "project",
                    "path": "../Farplane-UI/farplane/manifest.json",
                    "template_uses": {"farplane-framework": "1.1.0"},
                    "surfaces": {"project": True},
                },
            ],
        )

        by_template = {row["template_id"]: row for row in rows}

        self.assertEqual(by_template["skill-template"]["status"], "current")
        self.assertEqual(by_template["farplane-framework"]["status"], "stale")

    def test_feature_summaries_only_include_skill_category(self) -> None:
        features = generator.feature_summaries(
            [
                {"id": "FEAT-0001", "category": "skills", "name": "Skill feature"},
                {"id": "FEAT-0002", "category": "planning", "name": "Planning feature"},
            ]
        )

        self.assertEqual([feature["id"] for feature in features], ["FEAT-0001"])

    def test_template_version_summary_groups_snapshots_by_version(self) -> None:
        snapshots = [
            generator.TemplateSnapshot(
                version="0.2.0",
                source_commit="aaa111",
                introduced_at="2026-06-01",
                subject="release template",
                text="# T\n\n## Context\n",
            ),
            generator.TemplateSnapshot(
                version="0.2.0",
                source_commit="bbb222",
                introduced_at="2026-06-02",
                subject="patch wording",
                text="# T\n\n## Context\n\n## Output\n",
            ),
        ]

        versions = generator.summarize_template_versions(
            snapshots,
            {"aaa111": "archive/a.md", "bbb222": "archive/b.md"},
        )

        self.assertEqual(len(versions), 1)
        self.assertEqual(versions[0]["version"], "0.2.0")
        self.assertEqual(versions[0]["release_count"], 2)
        self.assertEqual(versions[0]["latest_commit"], "bbb222")
        self.assertEqual(versions[0]["snapshot_path"], "archive/b.md")


if __name__ == "__main__":
    unittest.main()
