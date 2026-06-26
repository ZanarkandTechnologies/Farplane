---
title: "Metric advisor cards"
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0007
refs:
  - skills/metric-advisor
  - docs/skills/README.md
  - docs/specs/self-improvement-contracts.md
  - docs/specs/review-gates.md
  - tickets/TASK-0228/ticket.md
  - skills/best-of-worlds/references/metric-discovery.md
  - skills/metric-advisor/SKILL.md
  - skills/metric-advisor/eval_task.json
feature_record_json: |
  {
    "id": "FEAT-0063",
    "name": "Metric advisor cards",
    "status": "implemented",
    "system_id": "SYS-0007",
    "category": "skills",
    "public": true,
    "surfaces": [
      "skills/metric-advisor",
      "docs/skills/README.md",
      "docs/specs/self-improvement-contracts.md",
      "docs/specs/review-gates.md"
    ],
    "source_refs": [
      "tickets/TASK-0228/ticket.md",
      "skills/best-of-worlds/references/metric-discovery.md",
      "docs/specs/self-improvement-contracts.md"
    ],
    "external_refs": [],
    "evidence_refs": [
      "skills/metric-advisor/SKILL.md",
      "skills/metric-advisor/eval_task.json",
      "tickets/TASK-0228/ticket.md"
    ],
    "known_limits": "Advisory metric-card contract only; callers still own execution, proof, review, and writeback. It must preserve qualitative `none mechanical` cases instead of forcing fake scores.",
    "metrics": [
      "metric_card_traceability_pass",
      "skill_eval_query_lint_pass"
    ],
    "last_verified": "2026-06-26"
  }
---

# Metric advisor cards

Metric advisor cards is a first-class Farplane feature in [Self-Improvement And Learning](../systems/self-improvement-learning.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0063, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Self-Improvement And Learning](../systems/self-improvement-learning.md)
- Feature ID: `FEAT-0063`
- Status: `implemented`
- Category: `skills`

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `skills/metric-advisor`
- `docs/skills/README.md`
- `docs/specs/self-improvement-contracts.md`
- `docs/specs/review-gates.md`

## Source Context

- `tickets/TASK-0228/ticket.md`
- `skills/best-of-worlds/references/metric-discovery.md`
- `docs/specs/self-improvement-contracts.md`

## Evidence

- `skills/metric-advisor/SKILL.md`
- `skills/metric-advisor/eval_task.json`
- `tickets/TASK-0228/ticket.md`

## Known Limits

Advisory metric-card contract only; callers still own execution, proof, review, and writeback. It must preserve qualitative `none mechanical` cases instead of forcing fake scores.

## Metrics

- `metric_card_traceability_pass`
- `skill_eval_query_lint_pass`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0063`.
