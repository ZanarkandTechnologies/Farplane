---
title: Metric advisor cards
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-27
tags:
  - farplane
  - feature
  - sys-0007
refs:
  - skills/metric-advisor
  - docs/skills/README.md
  - docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md
  - docs/features/FEAT-0008-artifact-first-qa-and-completion-proof.md
  - tickets/TASK-0228/ticket.md
  - skills/best-of-worlds/references/metric-discovery.md
  - skills/metric-advisor/SKILL.md
  - skills/metric-advisor/eval_task.json
feature_id: FEAT-0063
system_id: SYS-0007
category: skills
public: true
surfaces:
  - skills/metric-advisor
  - docs/skills/README.md
  - docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md
  - docs/features/FEAT-0008-artifact-first-qa-and-completion-proof.md
source_refs:
  - tickets/TASK-0228/ticket.md
  - skills/best-of-worlds/references/metric-discovery.md
  - docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md
external_refs: []
evidence_refs:
  - skills/metric-advisor/SKILL.md
  - skills/metric-advisor/eval_task.json
  - tickets/TASK-0228/ticket.md
known_limits: Advisory metric-card contract only; callers still own execution, proof, review, and writeback. It must preserve qualitative `none mechanical` cases instead of forcing fake scores.
metrics:
  - metric_card_traceability_pass
  - skill_eval_query_lint_pass
last_verified: 2026-06-26
---
# Metric advisor cards

Metric advisor cards exists to turn fuzzy improvement goals into honest metric cards
with guards and anti-metrics. It belongs to [Self-Improvement And
Learning](../systems/self-improvement-learning.md) and keeps `FEAT-0063` as a stable
capability handle because the behavior has an owner, proof path, and maintenance
boundary.

```text
metric_card(objective, evidence) -> metric + guard_metrics + anti_metrics + route
```

## At A Glance

- Feature ID: `FEAT-0063`
- System: [Self-Improvement And Learning](../systems/self-improvement-learning.md)
- Status: `implemented`
- Category: `skills`
- Primary user: operator, maintainer, and self-improvement agent
- Job: turn fuzzy improvement goals into honest metric cards with guards and anti-metrics.

## Problem

Optimization work becomes sloppy when agents choose convenient numbers that do not match
the actual objective.

Metric advisor cards force the metric, guardrails, failure modes, and evidence route to
be stated before self-improvement or productization claims.

## What It Does

- Defines one primary metric for an objective and the evidence it depends on.
- Adds guard metrics and anti-metrics to prevent gaming.
- Names the measurement window, owner, and route into tickets, evals, reports, or docs.
- Keeps judgment-heavy work honest by allowing qualitative or rubric-based scores when numeric metrics would be fake.
- Feeds self-improvement, documentation QA, skill maintenance, and product learning loops.

## User Stories

- As an operator, I can see what an optimization is actually trying to improve.
- As a maintainer, I can reject fake metrics before they guide work.
- As a self-improvement agent, I can route evidence into the right proof surface.

## Operating Contract

A metric card makes the measurement choice explicit and falsifiable.

- Every card names objective, primary metric, evidence source, guard metrics, and anti-metrics.
- The card states what would make the metric misleading.
- Judgment rubrics are allowed when they are more honest than pseudo-precision.
- Metric changes update the downstream workflow that consumes them.

## Surfaces

Owner surfaces:

- `skills/metric-advisor`
- `docs/skills/README.md`
- `docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md`
- `docs/features/FEAT-0008-artifact-first-qa-and-completion-proof.md`

Source context:

- `tickets/TASK-0228/ticket.md`
- `skills/best-of-worlds/references/metric-discovery.md`
- `docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md`

Evidence:

- `skills/metric-advisor/SKILL.md`
- `skills/metric-advisor/eval_task.json`
- `tickets/TASK-0228/ticket.md`

## Proof And Quality

Required checks:

- `python3 docs/features/validate_features.py`
- `python3 bin/validators/check_doc_refs.py`

Acceptance signals:

- The feature remains listed under exactly one owning system.
- The owner surfaces still exist and agree with this contract.
- Evidence refs support the current status.

## Rollout And Maintenance

- Update this feature page first when the capability contract changes.
- Then update owner surfaces and regenerate feature/system registries when metadata changes.
- Preserve the feature ID while active templates, skills, tickets, or docs still reference it.
- Maintenance owner: Self-Improvement And Learning.

## Limits And Non-Goals

- This feature does not invent fake quantitative metrics for subjective work.
- This feature does not run experiments by itself.
- This feature does not replace evals or proof artifacts.
- Known limit: Advisory metric-card contract only; callers still own execution, proof, review, and writeback. It must preserve qualitative `none mechanical` cases instead of forcing fake scores.
- Delete or merge this feature only when its current truth has moved into a clearer owner and all active refs are removed.

## Metrics

- `metric_card_traceability_pass`
- `skill_eval_query_lint_pass`

## Alternatives Considered

- Keep this only as a registry row.
  Decision: reject.
  Reason: Farplane features must be readable specs, not opaque metadata entries.
- Fold this entirely into the owning system page.
  Decision: defer.
  Reason: keep the `FEAT-*` page while templates, skills, tickets, or proof surfaces need a stable capability handle.

## Change History

- 2026-06-26: Feature spec created.
- 2026-06-27: Migrated into the reader-first feature-spec shape.
