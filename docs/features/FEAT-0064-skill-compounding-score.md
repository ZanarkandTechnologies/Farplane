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

Skill compounding score is a first-class Farplane feature in [Skill System](../systems/skill-system.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0064, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Skill System](../systems/skill-system.md)
- Feature ID: `FEAT-0064`
- Status: `implemented`
- Category: `skills`

## Feature Spec

This feature owns the official ranking function for deciding which skill improvement target is likely to compound most from one more improvement beat.

```text
skill_compounding_score(candidate, evidence) -> ranked_scorecard + caveats
```

The folded score contract is a reward-shaped prioritization function. The real objective is:

```text
one more improvement beat should increase the chance that Farplane creates
better product artifacts, proof, or reusable skill leverage
```

Component signals are shaping terms, not the objective itself. Normalize and cap them before weighting; report evidence and source gaps; penalize proxy-gaming paths such as hot but non-artifact targets, feedback without an artifact, fake metrics, ambiguous ownership, and open feedback spam.

Canonical components:

- tier leverage
- lifecycle reference fit
- product lane fit
- observed heat fit, split into direct heat and related heat
- downstream leverage fit
- improvement gap fit
- feedback fit
- proof fit

Observed heat uses direct invocation/ticket/thread signals plus weaker related heat from referencing skills. Related heat is a shaping potential, not proof of demand, and must never override the artifact-workflow gate.

Taste Loop is the first official consumer. It ranks product-lane artifact workflows using skill registry data, product lanes, direct/related heat, lifecycle refs, and controller memory.

Non-goal: this score is not an eval quality score and not a universal skill value judgment. It is a prioritization aid.

Proof gates:

- Scorecards name direct evidence and source gaps.
- Proxy-gaming paths are penalized.
- The selected target has an artifact workflow, not just heat.

## Owner Surfaces

- `docs/features/FEAT-0064-skill-compounding-score.md`
- `docs/skills/system.md`
- `skills/taste-loop`
- `farplane/automations.md`
- `docs/skills/registry.jsonl`

## Source Context

- `docs/farplane-framework/lifecycle.md`
- `docs/skills/system.md`
- `farplane/products.md`
- `skills/skill-maintenance/graph/README.md`

## Evidence

- `skills/taste-loop/SKILL.md`
- `skills/taste-loop/templates/heartbeat-prompt.md`
- `skills/taste-loop/eval_task.json`

## Known Limits

Official ranking contract only; the current implementation is prompt-consumed by Taste Loop and generated graph data. No standalone scorer, UI renderer, hidden scheduler, or automatic skill mutation is shipped.

## Metrics

- `skill_compounding_score_traceability_pass`
- `taste_loop_score_breakdown_pass`
- `skill_registry_validation_pass`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0064`.
