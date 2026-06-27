---
title: Artifact-first QA and completion proof
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-27
tags:
  - farplane
  - feature
  - sys-0005
refs:
  - tickets/README.md
  - tickets/templates/ticket.md
  - skills/qa
  - skills/review
  - docs/features/FEAT-0008-artifact-first-qa-and-completion-proof.md
  - "docs/MEMORY.md#MEM-0048"
  - "docs/MEMORY.md#MEM-0064"
  - "docs/MEMORY.md#MEM-0148"
  - docs/HISTORY.md
feature_id: FEAT-0008
system_id: SYS-0005
category: proof
public: true
surfaces:
  - tickets/README.md
  - tickets/templates/ticket.md
  - skills/qa
  - skills/review
  - docs/features/FEAT-0008-artifact-first-qa-and-completion-proof.md
source_refs:
  - "docs/MEMORY.md#MEM-0048"
  - "docs/MEMORY.md#MEM-0064"
  - "docs/MEMORY.md#MEM-0148"
external_refs: []
evidence_refs:
  - docs/HISTORY.md
known_limits: Depends on compact `Done / Proof` obligations plus linked artifacts, progress logs, and reviewer gates, not ticket-body proof theater.
metrics: []
last_verified: 2026-06-12
---
# Artifact-first QA and completion proof

Artifact-first QA and completion proof is a first-class Farplane feature in [Proof And Review](../systems/proof-review.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0008, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Proof And Review](../systems/proof-review.md)
- Feature ID: `FEAT-0008`
- Status: `implemented`
- Category: `proof`

## Feature Spec

This feature owns proof-before-completion behavior. Farplane work is not done because the implementer says it is done; it is done when the ticket's proof gates, QA evidence, reviewer checks, and completion path agree.

```text
proof_gate(work_type, ticket, artifacts) -> pass | needs_revision | blocked
```

The former review-gates spec folds into this feature:

- Ticket `Done / Proof` is the scoreboard for required checks, evidence, and review gates.
- QA owns user-visible or runtime evidence such as screenshots, traces, command outputs, console logs, and failure captures.
- Reviewer owns material plan, implementation, prompt, evidence, and completion-claim judgment.
- Stop-hook completion for active Goal-backed work stays mechanical and visible: implementation, QA, demo when required, and a final completion-review receipt.
- Normalized review outputs should identify verdict, TAS gate status, hard blockers, findings, evidence checked, and residual risk.

Non-goal: this feature does not make every task heavyweight. Proof scales with risk, blast radius, and user-facing impact.

Proof gates:

- Completion claims name the checks and evidence used.
- Material work is not self-approved when a reviewer or QA lane is available.
- Missing evidence is recorded as a blocker or residual risk, not silently ignored.

## Owner Surfaces

- `tickets/README.md`
- `tickets/templates/ticket.md`
- `skills/qa`
- `skills/review`
- `docs/features/FEAT-0008-artifact-first-qa-and-completion-proof.md`

## Source Context

- `docs/MEMORY.md#MEM-0048`
- `docs/MEMORY.md#MEM-0064`
- `docs/MEMORY.md#MEM-0148`

## Evidence

- `docs/HISTORY.md`

## Known Limits

Depends on compact `Done / Proof` obligations plus linked artifacts, progress logs, and reviewer gates, not ticket-body proof theater.

## Metrics

- no dedicated metric yet

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0008`.
