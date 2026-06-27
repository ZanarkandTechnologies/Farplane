---
title: Symphony-compatible Farplane invocation contract
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-27
tags:
  - farplane
  - feature
  - sys-0004
refs:
  - WORKFLOW.md
  - skills/farplane-invocation
  - bin/farplane_invocation.py
  - docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md
  - docs/HISTORY.md
  - tickets/archive/TASK-0107/ticket.md
  - tickets/archive/TASK-0107/artifacts/qa/prepare-planning.json
  - tickets/archive/TASK-0107/artifacts/qa/sample-proof-packet.json
feature_id: FEAT-0015
system_id: SYS-0004
category: execution
public: true
surfaces:
  - WORKFLOW.md
  - skills/farplane-invocation
  - bin/farplane_invocation.py
  - docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md
source_refs:
  - docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md
  - docs/HISTORY.md
external_refs:
  - Symphony Service Specification draft v1
evidence_refs:
  - tickets/archive/TASK-0107/ticket.md
  - tickets/archive/TASK-0107/artifacts/qa/prepare-planning.json
  - tickets/archive/TASK-0107/artifacts/qa/sample-proof-packet.json
known_limits: Filesystem ticket adapter and local compute only; no daemon, polling, Linear/Notion adapter, cloud execution, or Codex-launching wrapper.
metrics:
  - runner_contract_conformance
  - proof_packet_parse_rate
last_verified: 2026-05-05
---
# Symphony-compatible Farplane invocation contract

Symphony-compatible Farplane invocation contract exists to make every run start from a
visible invocation envelope and end with an inspectable proof packet. It belongs to
[Invocation Runtime](../systems/invocation-runtime.md) and keeps `FEAT-0015` as a stable
capability handle because the behavior has an owner, proof path, and maintenance
boundary.

```text
invoke_farplane(trigger, board?, compute_policy?) -> run_envelope + proof_packet
```

## At A Glance

- Feature ID: `FEAT-0015`
- System: [Invocation Runtime](../systems/invocation-runtime.md)
- Status: `implemented`
- Category: `execution`
- Primary user: operator, board adapter, local Codex session, and future external runner
- Job: make every run start from a visible invocation envelope and end with an inspectable proof packet.

## Problem

Farplane needs to accept work from local conversations, filesystem tickets, board-backed
adapters, Goal Packets, and future external runners.

Without a clear invocation boundary, those sources can blur into hidden polling, ambient
ticket scanning, or scheduler behavior that is hard to inspect and harder to prove.

## What It Does

- Accepts an explicit invocation trigger from a local conversation, Goal heartbeat, board adapter, or future worker envelope.
- Normalizes one work item with scope, owner surface, proof obligations, and status.
- Selects an explicit compute target and compute decision.
- Produces a `FarplaneRunEnvelope` that carries the executable context packet.
- Produces or validates a `ProofPacket` that carries evidence, status, and handoff back to the caller.

## User Stories

- As an operator, I can inspect the route, phase, compute decision, and proof path before work proceeds.
- As a board adapter, I can translate external state into a Farplane work item without making the board the source of truth.
- As a future external runner, I can pass an envelope and receive a proof packet without requiring Farplane to become a hosted control plane.

## Operating Contract

Invocation is an edge contract, not a background runtime.

Public docs should describe `.farplane/` as the canonical live runtime root.
There is no separate public retired execution surface anymore.

- `InvocationTrigger` records why work starts.
- `BoardAdapter` translates external board state into one work item.
- `WorkItem` binds scope, owner surface, proof obligations, and status.
- `ComputeDecision` records whether the run is admitted, redirected, or blocked.
- `ProofPacket` carries result status, evidence, and handoff data.

## Surfaces

Owner surfaces:

- `WORKFLOW.md`
- `skills/farplane-invocation`
- `bin/farplane_invocation.py`
- `docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md`

Source context:

- `docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md`
- `docs/HISTORY.md`

External context:

- `Symphony Service Specification draft v1`

Evidence:

- `tickets/archive/TASK-0107/ticket.md`
- `tickets/archive/TASK-0107/artifacts/qa/prepare-planning.json`
- `tickets/archive/TASK-0107/artifacts/qa/sample-proof-packet.json`

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
- Maintenance owner: Invocation Runtime.

## Limits And Non-Goals

- This feature is not a daemon, poller, hosted control plane, or hidden cloud wrapper.
- This feature does not make ticket existence a start-work trigger.
- This feature does not replace Proof And Review.
- Known limit: Filesystem ticket adapter and local compute only; no daemon, polling, Linear/Notion adapter, cloud execution, or Codex-launching wrapper.
- Delete or merge this feature only when its current truth has moved into a clearer owner and all active refs are removed.

## Metrics

- `runner_contract_conformance`
- `proof_packet_parse_rate`

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
