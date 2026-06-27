---
title: "Behavior correction, hardcase metadata, and narrow eval capture"
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-27
tags:
  - farplane
  - feature
  - sys-0007
refs:
  - skills/gap-analysis
  - skills/harness-advisor
  - skills/metric-advisor
  - skills/optimize-harness
  - skills/eval
  - docs/LESSONS.md
  - experiments/hardcases
  - docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md
  - docs/HISTORY.md
  - docs/features/registry.jsonl#FEAT-0031
  - docs/features/registry.jsonl#FEAT-0063
feature_record_json: |
  {
    "id": "FEAT-0039",
    "name": "Behavior correction, hardcase metadata, and narrow eval capture",
    "status": "implemented",
    "system_id": "SYS-0007",
    "category": "improvement-loop",
    "public": true,
    "surfaces": [
      "skills/gap-analysis",
      "skills/harness-advisor",
      "skills/metric-advisor",
      "skills/optimize-harness",
      "skills/eval",
      "docs/LESSONS.md",
      "experiments/hardcases",
      "docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md"
    ],
    "source_refs": [
      "docs/HISTORY.md",
      "docs/features/registry.jsonl#FEAT-0031",
      "docs/features/registry.jsonl#FEAT-0063",
      "docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md"
    ],
    "external_refs": [],
    "evidence_refs": [
      "skills/gap-analysis/SKILL.md",
      "skills/harness-advisor/SKILL.md",
      "skills/metric-advisor/SKILL.md",
      "skills/optimize-harness/SKILL.md",
      "skills/eval/SKILL.md",
      "docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md",
      "experiments/hardcases/20260607-1917-repent-eval-capture/case.md",
      "tickets/TASK-0228/ticket.md",
      "docs/HISTORY.md"
    ],
    "known_limits": "Correction is skill-and-artifact driven. Hardcase is eval metadata and legacy standalone hardcase artifacts should become runnable eval rows when the expected behavior is testable. Metric selection routes through metric-advisor before self-improve. The loop does not train models, sell data, inspect full Codex histories without a seed anchor, or auto-apply broad harness migrations without proof.",
    "metrics": [
      "gap_packet_quality_pass",
      "harness_placement_quality_pass",
      "metric_card_traceability_pass",
      "hardcase_eval_metadata_pass",
      "narrow_regression_eval_pass"
    ],
    "last_verified": "2026-06-26"
  }
---

# Behavior correction, hardcase metadata, and narrow eval capture

Behavior correction, hardcase metadata, and narrow eval capture is a first-class Farplane feature in [Self-Improvement And Learning](../systems/self-improvement-learning.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0039, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Self-Improvement And Learning](../systems/self-improvement-learning.md)
- Feature ID: `FEAT-0039`
- Status: `implemented`
- Category: `improvement-loop`

## Feature Spec

This feature owns the self-improvement correction loop: behavior gaps become hardcases, eval rows, skill patches, lessons, or harness changes instead of vanishing into chat.

```text
behavior_fix(gap, evidence, owner_surface) -> hardcase? + patch? + eval? + lesson?
```

The former self-improvement contracts fold into this feature:

- Minimal behavior-fix SOP: identify the gap, bind it to an owner surface, make the smallest durable correction, and prove it on a representative case.
- Core skill signatures describe how gap-analysis, harness-advisor, eval, skill-maintenance, self-improve, and optimize-harness cooperate.
- Hardcases should capture task input, expected behavior, observed failure, owner, tags, proof artifacts, and promotion status.
- Skill self-healing patches local Farplane wrappers, fixtures, registries, or evals; it does not mutate external installed skills unless explicitly requested.

Non-goal: self-improvement is not a generic memory dump. It must land in an owner: feature doc, skill, eval, lesson, ticket, or source registry.

Proof gates:

- Repeated misses get a visible prevention surface.
- Hardcases are narrow enough to rerun or reason about.
- The correction route is named: skill, prompt, eval, doc, hook, validator, or ticket.

## Owner Surfaces

- `skills/gap-analysis`
- `skills/harness-advisor`
- `skills/metric-advisor`
- `skills/optimize-harness`
- `skills/eval`
- `docs/LESSONS.md`
- `experiments/hardcases`
- `docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md`

## Source Context

- `docs/HISTORY.md`
- `docs/features/registry.jsonl#FEAT-0031`
- `docs/features/registry.jsonl#FEAT-0063`
- `docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md`

## Evidence

- `skills/gap-analysis/SKILL.md`
- `skills/harness-advisor/SKILL.md`
- `skills/metric-advisor/SKILL.md`
- `skills/optimize-harness/SKILL.md`
- `skills/eval/SKILL.md`
- `docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md`
- `experiments/hardcases/20260607-1917-repent-eval-capture/case.md`
- `tickets/TASK-0228/ticket.md`
- `docs/HISTORY.md`

## Known Limits

Correction is skill-and-artifact driven. Hardcase is eval metadata and legacy standalone hardcase artifacts should become runnable eval rows when the expected behavior is testable. Metric selection routes through metric-advisor before self-improve. The loop does not train models, sell data, inspect full Codex histories without a seed anchor, or auto-apply broad harness migrations without proof.

## Metrics

- `gap_packet_quality_pass`
- `harness_placement_quality_pass`
- `metric_card_traceability_pass`
- `hardcase_eval_metadata_pass`
- `narrow_regression_eval_pass`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0039`.
