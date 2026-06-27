---
title: Skill compounding score
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-27
tags:
  - farplane
  - feature
  - sys-0006
refs:
  - docs/features/FEAT-0064-skill-compounding-score.md
  - docs/skills/system.md
  - skills/taste-loop
  - farplane/automations.md
  - docs/skills/registry.jsonl
  - docs/farplane-framework/lifecycle.md
  - farplane/products.md
  - skills/skill-maintenance/graph/README.md
  - skills/taste-loop/SKILL.md
  - skills/taste-loop/templates/heartbeat-prompt.md
  - skills/taste-loop/eval_task.json
feature_id: FEAT-0064
system_id: SYS-0006
category: skills
public: true
surfaces:
  - docs/features/FEAT-0064-skill-compounding-score.md
  - docs/skills/system.md
  - skills/taste-loop
  - farplane/automations.md
  - docs/skills/registry.jsonl
source_refs:
  - docs/farplane-framework/lifecycle.md
  - docs/skills/system.md
  - farplane/products.md
  - skills/skill-maintenance/graph/README.md
external_refs: []
evidence_refs:
  - skills/taste-loop/SKILL.md
  - skills/taste-loop/templates/heartbeat-prompt.md
  - skills/taste-loop/eval_task.json
known_limits: Official ranking contract only; the current implementation is prompt-consumed by Taste Loop and generated graph data. No standalone scorer, UI renderer, hidden scheduler, or automatic skill mutation is shipped.
metrics:
  - skill_compounding_score_traceability_pass
  - taste_loop_score_breakdown_pass
  - skill_registry_validation_pass
last_verified: 2026-06-26
---
# Skill compounding score

Skill compounding score exists to prioritize skill upgrades by reusable leverage instead
of recency or loudness. It belongs to [Skill System](../systems/skill-system.md) and
keeps `FEAT-0064` as a stable capability handle because the behavior has an owner, proof
path, and maintenance boundary.

```text
score_skill_compounding(skill, usage_evidence) -> leverage_score + maintenance_priority
```

## At A Glance

- Feature ID: `FEAT-0064`
- System: [Skill System](../systems/skill-system.md)
- Status: `implemented`
- Category: `skills`
- Primary user: skill maintainer and roadmap planner
- Job: prioritize skill upgrades by reusable leverage instead of recency or loudness.

## Problem

Skill maintenance time is limited, and not every skill improvement compounds equally
across Farplane.

This feature gives maintainers a scoring language for which skills deserve hardening,
evals, templates, or documentation first.

## What It Does

- Scores skills by reuse, routing centrality, proof leverage, failure cost, and dependency impact.
- Separates tier classification from maintenance priority.
- Highlights first-load bloat, overlap, stale checklists, and missing evals.
- Feeds skill-maintenance planning and consolidation decisions.
- Helps decide when a skill should be split, merged, promoted, or retired.
- Feeds Taste Loop candidate selection while keeping human taste feedback
  separate as phase outcomes: `idea_pass_rate` for planning artifacts and
  `execution_pass_rate` for generated artifacts.

## User Stories

- As a maintainer, I can choose the next skill upgrade based on compounding value.
- As an operator, I can see why a boring workflow skill deserves investment.
- As a reviewer, I can challenge upgrades that add complexity without leverage.

## Operating Contract

Compounding score is a prioritization signal, not a skill tier.

- Scores cite evidence such as usage, references, failure patterns, or dependency roles.
- High score implies stronger QA, eval, and documentation expectations.
- Low score can justify deferring, merging, or retiring a skill.
- The score does not override direct user priority or urgent bug fixes.
- Taste Loop uses compounding score to choose which product-lane workflow to
  try next. It does not treat idea or execution pass rates as eval score.
  Those rates are human-feedback outcomes that can become evidence for future
  maintenance priority only when recorded with a comparable scenario and
  artifact refs.

## Surfaces

Owner surfaces:

- `docs/features/FEAT-0064-skill-compounding-score.md`
- `docs/skills/system.md`
- `skills/taste-loop`
- `farplane/automations.md`
- `docs/skills/registry.jsonl`

Source context:

- `docs/farplane-framework/lifecycle.md`
- `docs/skills/system.md`
- `farplane/products.md`
- `skills/skill-maintenance/graph/README.md`

Evidence:

- `skills/taste-loop/SKILL.md`
- `skills/taste-loop/templates/heartbeat-prompt.md`
- `skills/taste-loop/eval_task.json`

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
- Maintenance owner: Skill System.

## Limits And Non-Goals

- This feature does not auto-rewrite skills.
- This feature does not make every skill high priority because it is useful once.
- This feature does not replace skill-maintenance review.
- Known limit: Official ranking contract only; the current implementation is prompt-consumed by Taste Loop and generated graph data. No standalone scorer, UI renderer, hidden scheduler, or automatic skill mutation is shipped.
- Delete or merge this feature only when its current truth has moved into a clearer owner and all active refs are removed.

## Metrics

- `skill_compounding_score_traceability_pass`
- `taste_loop_score_breakdown_pass`
- `skill_registry_validation_pass`

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
