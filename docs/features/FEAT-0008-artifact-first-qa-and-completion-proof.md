---
title: Artifact-first QA and completion proof
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-28
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
known_limits: Depends on compact `Done` conditions, `QA Strategy`, linked artifacts, progress logs, and reviewer gates, not ticket-body proof theater.
metrics: []
last_verified: 2026-06-12
---
# Artifact-first QA and completion proof

Artifact-first QA and completion proof exists to make completion inspectable through
ticket proof obligations, linked artifacts, and review verdicts. It belongs to [Proof
And Review](../systems/proof-review.md) and keeps `FEAT-0008` as a stable capability
handle because the behavior has an owner, proof path, and maintenance boundary.

```text
proof_gate(work_type, ticket, artifacts) -> pass | needs_revision | blocked
```

## At A Glance

- Feature ID: `FEAT-0008`
- System: [Proof And Review](../systems/proof-review.md)
- Status: `implemented`
- Category: `proof`
- Primary user: operator, QA lane, reviewer, and coding agent
- Job: make completion inspectable through ticket proof obligations, linked artifacts, and review verdicts.

## Problem

Farplane work often spans planning, implementation, QA, review, and closeout. If
completion is declared only in chat, the next reader cannot tell which checks ran, where
the evidence lives, which risks remain, or whether a reviewer agreed with the claim.

This feature gives each task a visible scoreboard: the ticket names the required proof,
artifacts carry the evidence, and review or QA lanes judge the result against that
contract.

## What It Does

- Reads ticket `Done` conditions and `QA Strategy` as the scoreboard for checks, evidence, and review gates.
- Produces or links command output, screenshots, traces, console logs, failure captures, review reports, and QA notes.
- Routes material plans, implementations, prompts, evidence bundles, and completion claims through reviewer judgment when required.
- Keeps Goal-backed completion mechanical and visible: implementation, QA, demo when required, and final completion review receipt.
- Refuses silent completion when required evidence is missing.

## User Stories

- As an operator, I can open a ticket and see exactly what proof is required before accepting the result.
- As a QA lane, I can attach browser, command, or runtime evidence without turning the ticket body into a proof dump.
- As a reviewer, I can judge the work against named gates, hard blockers, evidence checked, and residual risk.

## Operating Contract

Proof scales with risk, blast radius, and user-facing impact.

- Ticket `Done` names completion conditions.
- Ticket `QA Strategy` names the expected checks, evidence, review gates, and acceptance signals.
- For material features, `QA Strategy` also names the critical path in flexible
  prose or bullets: the real workflow or lifecycle being claimed, smaller
  ordered sanity checks when a full end-to-end run is long, expected
  observations, evidence, and any residual risk for unrun final paths.
- Ticket-local artifacts hold bulky proof and reports.
- QA owns user-visible and runtime evidence capture.
- Reviewer owns material judgment of plans, implementations, prompts, evidence, and completion claims.
- Completion claims must name the checks and evidence used.

## Surfaces

Owner surfaces:

- `tickets/README.md`
- `tickets/templates/ticket.md`
- `skills/qa`
- `skills/review`
- `docs/features/FEAT-0008-artifact-first-qa-and-completion-proof.md`

Source context:

- `docs/MEMORY.md#MEM-0048`
- `docs/MEMORY.md#MEM-0064`
- `docs/MEMORY.md#MEM-0148`

Evidence:

- `docs/HISTORY.md`

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
- Maintenance owner: Proof And Review.

## Limits And Non-Goals

- This feature does not make every task heavyweight.
- This feature does not require proof to live inside the ticket body.
- This feature does not replace ticket scope, specs, or review rubrics.
- Known limit: Depends on compact `Done` conditions, `QA Strategy`, linked artifacts, progress logs, and reviewer gates, not ticket-body proof theater.
- Delete or merge this feature only when its current truth has moved into a clearer owner and all active refs are removed.

## Metrics

- no dedicated metric yet

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
- 2026-06-28: Split completion obligations into `Done` conditions and `QA Strategy`.
