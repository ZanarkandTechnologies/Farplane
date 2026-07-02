---
title: Skill signals
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-27
tags:
  - farplane
  - feature
  - sys-0006
refs:
  - docs/features/FEAT-0064-skill-signals.md
  - docs/skills/system.md
  - skills/taste-loop
  - farplane/automations.toml
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
  - docs/features/FEAT-0064-skill-signals.md
  - docs/skills/system.md
  - skills/taste-loop
  - farplane/automations.toml
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
known_limits: Official signal contract only; the current implementation is prompt-consumed by Taste Loop and generated graph data. No standalone scorer, UI renderer, hidden scheduler, or automatic skill mutation is shipped.
metrics:
  - skill_signal_contract_traceability_pass
  - taste_loop_signal_breakdown_pass
  - skill_registry_validation_pass
last_verified: 2026-06-26
---
# Skill signals

Skill signals exist to prioritize skill upkeep without hiding raw
evidence inside a brittle mega-score. It belongs to
[Skill System](../systems/skill-system.md) and keeps `FEAT-0064` as a stable
capability handle because the behavior has an owner, proof path, and
maintenance boundary.

```text
skill_signals(skill, usage_evidence, registry_evidence)
  -> direct_heat + composition_heat + maintenance_burden + uniqueness
  -> maintenance_recommendation
```

## At A Glance

- Feature ID: `FEAT-0064`
- System: [Skill System](../systems/skill-system.md)
- Status: `implemented`
- Category: `skills`
- Primary user: skill maintainer and roadmap planner
- Job: prioritize skill upkeep from a small set of explainable signals instead of one opaque scalar.

## Problem

Skill maintenance time is limited, and not every skill improvement compounds equally
across Farplane.

This feature gives maintainers a compact signal language for which skills
deserve hardening, refinement, merging, watching, or retirement review first.

## What It Does

- Separates raw skill signals from maintenance recommendations.
- Uses direct heat, composition heat, maintenance burden, and uniqueness as the
  durable signal set.
- Separates tier classification from maintenance priority.
- Highlights first-load bloat, overlap, stale checklists, missing evals, and
  source gaps without pretending they are direct usage.
- Feeds skill-maintenance planning and consolidation decisions.
- Helps decide when a skill should be split, merged, promoted, or retired.
- Feeds Taste Loop candidate selection while keeping human taste feedback
  separate as phase outcomes: `idea_pass_rate` for planning artifacts and
  `execution_pass_rate` for generated artifacts.

## User Stories

- As a maintainer, I can choose the next skill upgrade from clear evidence.
- As an operator, I can see why a boring workflow skill deserves investment.
- As a reviewer, I can challenge upgrades that add complexity without leverage.

## Operating Contract

Skill signals are a recommendation contract, not a skill tier or quality
grade.

- Reports expose the raw signal values before any recommendation.
- Direct heat means observed invocation or usage evidence.
- Composition heat means weaker indirect usefulness from deduped incoming refs
  from recently used skills.
- Maintenance burden means cost or risk: stale templates, bloated first-load
  text, missing evals or QA, unclear owners, or generated-output drift.
- Uniqueness means whether the skill owns a distinct trigger, workflow, proof
  surface, or user-facing capability.
- Recommendations use `keep`, `harden`, `refine`, `merge`, `watch`, or
  `retire_review`; destructive edits still require owner-specific review.
- Taste Loop uses these signals to choose which product-lane workflow to try
  next. It does not treat idea or execution pass rates as eval score.
  Those rates are human-feedback outcomes that can become evidence for future
  maintenance priority only when recorded with a comparable scenario and
  artifact refs.

Default recommendation rules:

```text
keep = direct_heat or composition_heat is high, or uniqueness is high
harden = failure evidence exists and a guardrail is missing
refine = heat is high and maintenance_burden is high
merge = uniqueness is low and overlap is high
watch = heat is low but evidence is incomplete
retire_review = heat is low, composition_heat is low, uniqueness is low,
                and the same finding survives at least two reviewed reports
```

## Surfaces

Owner surfaces:

- `docs/features/FEAT-0064-skill-signals.md`
- `docs/skills/system.md`
- `skills/taste-loop`
- `farplane/automations.toml`
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
- Known limit: Official signal and recommendation contract only; the current
  implementation is prompt-consumed by Taste Loop and generated graph data. No
  standalone scorer, UI renderer, hidden scheduler, or automatic skill mutation
  is shipped.
- Delete or merge this feature only when its current truth has moved into a clearer owner and all active refs are removed.

## Metrics

- `skill_signal_contract_traceability_pass`
- `taste_loop_signal_breakdown_pass`
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
- 2026-06-27: Simplified from a broad weighted score into direct heat,
  composition heat, maintenance burden, uniqueness, and recommendations.
