---
title: "Self-Improvement And Learning"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-07-11
tags:
  - farplane
  - systems
  - self-improvement-and-learning
refs:
  - docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md
  - docs/features/FEAT-0069-taste-loop-human-feedback-optimization.md
  - docs/features/FEAT-0070-experimental-feature-evaluation-reports.md
  - docs/LESSONS.md
  - docs/TROUBLES.md
  - skills/metric-advisor/SKILL.md
system_record_json: |
  {
    "id": "SYS-0007",
    "name": "Self-Improvement And Learning",
    "status": "implemented",
    "summary": "The learning loop that reviews experiment Goal Packets, chooses bounded harness experiments, and turns proven outcomes into skills, evals, docs, features, or policy.",
    "owner_spec": "docs/systems/self-improvement-learning.md",
    "primary_feature_ref": "FEAT-0063",
    "feature_refs": [
      "FEAT-0063",
      "FEAT-0069",
      "FEAT-0070"
    ],
    "refs": [
      "docs/features/FEAT-0069-taste-loop-human-feedback-optimization.md",
      "docs/features/FEAT-0070-experimental-feature-evaluation-reports.md",
      "docs/LESSONS.md",
      "docs/TROUBLES.md",
      "skills/metric-advisor/SKILL.md"
    ],
    "last_verified": "2026-07-11"
  }
---
# Self-Improvement And Learning

The learning loop that observes behavior gaps, reviews experiment Goal Packets,
chooses bounded experiments, and turns proven outcomes into skills, evals,
docs, features, or policy. This page owns self-improvement selection and
learning; Work Pulse still owns experiment execution and check-ins.

```text
self_improvement_and_learning(change, repo_state?) -> owned_feature_set + boundary_decision + maintenance_signal
```

## At A Glance

- System ID: `SYS-0007`
- Status: `implemented`
- Primary feature: `FEAT-0063`
- Owner spec: `docs/systems/self-improvement-learning.md`
- Feature count: `3`

## Role

Self-Improvement And Learning owns correction loops: observe behavior gaps,
review existing experiments, choose metrics and proof routes, create bounded
experiment Goal Packets, and promote repeated evidence into durable owners.

## Feature Docs

- [FEAT-0063 Metric advisor cards](../features/FEAT-0063-metric-advisor-cards.md)
- [FEAT-0069 Retired Taste Loop human-feedback optimization](../features/FEAT-0069-taste-loop-human-feedback-optimization.md)
- [FEAT-0070 Experimental feature evaluation reports](../features/FEAT-0070-experimental-feature-evaluation-reports.md)

## What Belongs Here

Gap analysis, metric cards, hardcase capture, lesson promotion, Dogfood
experiment review/ticket supply, human-feedback optimization, and
correction-route decisions.

## What Belongs Elsewhere

Execution of a selected build remains in Work Loop; reusable skill packaging remains in
Skill System; source discovery remains in Source And Sidecar Systems; BAU
problem reports remain in Horizon Loop.

## Operating Contract

- Corrections name the gap, evidence, owner, and proof path.
- Metric cards choose honest primary and guard metrics before optimization.
- Repeated misses promote into durable prevention surfaces.
- Broad self-improvement migrations require representative proof.
- Dogfood Review runs as the weekly portfolio learner/planner: it reads active
  and recent archived experiment packets plus its prior report, carries a
  derived outcome ledger, and creates a bounded non-interfering next wave from
  available capacity.
- Every experiment carries Reward rows and Goal Packet state; Work Pulse alone
  executes the experiment and resumes matured check-ins. Delayed packets put
  the executable check-in instructions in `program.md`; the resumed worker
  reads and runs that program directly.
- Feature-level behavior belongs in `docs/features/FEAT-*.md`; this page owns the system boundary and feature grouping.
- Registry data is generated from system and feature docs, not edited by hand.
- When a capability no longer deserves a feature page, fold its current truth into the best owner and remove active refs.

## System Flow

```mermaid
flowchart LR
  classDef keep fill:#f3f4f6,stroke:#6b7280,color:#111827
  classDef changed fill:#fef3c7,stroke:#b45309,color:#111827
  classDef added fill:#dcfce7,stroke:#15803d,color:#111827
  classDef retired fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d,stroke-dasharray: 5 3

  signals["behavior gaps + experiment outcomes<br/>reports, tickets, feedback"]:::keep
  metrics["FEAT-0063<br/>metric advisor cards"]:::changed
  taste["FEAT-0069 retired<br/>human feedback decomposed"]:::retired
  dogfood["FEAT-0070<br/>portfolio ledger + next wave"]:::changed
  packet["experiment Goal Packets<br/>Reward + executable program + progress"]:::added
  pulse["Work Pulse<br/>execute + check in"]:::keep
  memory["docs/TROUBLES.md<br/>docs/LESSONS.md"]:::added
  action["skill / eval / feature change<br/>next experiment"]:::added

  signals --> dogfood --> packet --> pulse --> action
  signals --> metrics --> action
  signals --> taste --> action
  dogfood --> metrics
  action --> memory
```

Self-Improvement And Learning converts failures, feedback, and experiment
results into metrics, lessons, evals, transfer candidates, and the next
bounded experiment wave.

## Surfaces

- `docs/features/FEAT-0069-taste-loop-human-feedback-optimization.md`
- `docs/features/FEAT-0070-experimental-feature-evaluation-reports.md`
- `docs/LESSONS.md`
- `docs/TROUBLES.md`
- `skills/metric-advisor/SKILL.md`
- `skills/dogfood-review/SKILL.md`
- `skills/self-improve/SKILL.md`
- `farplane/automations.toml`

## Proof And Maintenance

- Registry proof: `python3 docs/features/validate_features.py`.
- Link proof: `python3 bin/validators/check_doc_refs.py`.
- Update this system page when product-layer boundaries or feature membership changes.
- Update feature pages when capability behavior changes.
- Regenerate registries and commit generated outputs with the source docs.

## Change History

- 2026-06-27: Migrated into the reader-first system-spec shape.
- 2026-07-07: Added experimental Taste Loop human-feedback optimization as a
  self-improvement feature.
- 2026-07-11: Retired Taste Loop as a controller; Dogfood creates ordinary
  feedback experiment packets and Work Pulse owns execution/check-ins/review waits.
- 2026-07-07: Moved consolidated eval feature ownership to Proof And Review.
- 2026-07-07: Added experimental feature evaluation reports as a
  self-improvement feature.
- 2026-07-11: Made Dogfood Review the weekly experiment-review and Goal Packet
  ticket-supply owner while keeping execution/check-ins in Work Pulse.
- 2026-07-11: Made Dogfood a history-aware portfolio learner/planner and moved
  delayed check-in execution instructions into each experiment `program.md`.
