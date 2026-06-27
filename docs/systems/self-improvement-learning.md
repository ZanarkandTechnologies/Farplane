---
title: "Self-Improvement And Learning"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - self-improvement-and-learning
refs:
  - docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md
  - docs/LESSONS.md
  - docs/TROUBLES.md
  - skills/metric-advisor/SKILL.md
system_record_json: |
  {
    "id": "SYS-0007",
    "name": "Self-Improvement And Learning",
    "status": "implemented",
    "summary": "The learning loop that observes behavior gaps, captures hardcases, chooses metrics, routes correction, and turns repeated failures into skills, evals, or docs.",
    "owner_spec": "docs/systems/self-improvement-learning.md",
    "primary_feature_ref": "FEAT-0039",
    "feature_refs": [
      "FEAT-0039",
      "FEAT-0063"
    ],
    "refs": [
      "docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md",
      "docs/LESSONS.md",
      "docs/TROUBLES.md",
      "skills/metric-advisor/SKILL.md"
    ],
    "last_verified": "2026-06-26"
  }
---

# Self-Improvement And Learning

The learning loop that observes behavior gaps, captures hardcases, chooses metrics, routes correction, and turns repeated failures into skills, evals, or docs.

## Role

Self-Improvement and Learning turns failures, feedback, metrics, hardcases, and lessons into narrower improvements without pretending there is a hidden autonomous optimizer.

## What Belongs Here

Gap analysis, metric cards, hardcase capture, lesson promotion, and improvement-routing contracts.

## What Belongs Elsewhere

Execution of a selected build remains in Work Loop; reusable skill packaging remains in Skill System; source discovery remains in Source and Sidecar Systems.

## Feature Docs

- [FEAT-0039 Behavior correction, hardcase metadata, and narrow eval capture](../features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md)
- [FEAT-0063 Metric advisor cards](../features/FEAT-0063-metric-advisor-cards.md)

## Maintenance

This system page owns only the system-level contract. Feature registry rows are authored as feature pages in `docs/features/` and generated into `docs/features/registry.jsonl`.
