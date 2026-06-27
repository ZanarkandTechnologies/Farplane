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

Symphony-compatible Farplane invocation contract is a first-class Farplane feature in [Invocation Runtime](../systems/invocation-runtime.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0015, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Invocation Runtime](../systems/invocation-runtime.md)
- Feature ID: `FEAT-0015`
- Status: `implemented`
- Category: `execution`

## Feature Spec

This feature owns the explicit invocation boundary. Farplane starts from a visible invocation, board item, Goal Packet, or compatible external runner envelope; it does not become a hidden daemon or scheduler.

```text
invoke_farplane(trigger, board?, compute_policy?) -> run_envelope + proof_packet
```

The invocation contract folds the adapter/runtime spec into this feature:

- `InvocationTrigger` records why work starts: local conversation, goal heartbeat, board adapter, or future worker envelope.
- `BoardAdapter` translates external boards into Farplane work items without making board state the source of truth.
- `WorkItem` binds scope, owner surface, proof obligations, and status.
- `ComputeTarget` and `ComputeDecision` keep local Codex, future Codex Cloud, or Symphony-style workers explicit.
- `FarplaneRunEnvelope` carries the executable context packet.
- `ProofPacket` carries evidence, status, and handoff back to the caller.

Non-goals:

- No hidden scheduler.
- No automatic hosted control plane.
- No start-work trigger based only on a ticket existing somewhere.

Proof gates:

- Every external or board-backed run has a visible envelope and proof packet.
- Runtime state stays in `.farplane/` or the owning ticket, not in chat.
- Public docs should describe `.farplane/` as the canonical live runtime root.
- There is no separate public retired execution surface anymore.
- Future worker compatibility does not weaken local proof requirements.

## Owner Surfaces

- `WORKFLOW.md`
- `skills/farplane-invocation`
- `bin/farplane_invocation.py`
- `docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md`

## Source Context

- `docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md`
- `docs/HISTORY.md`

## Evidence

- `tickets/archive/TASK-0107/ticket.md`
- `tickets/archive/TASK-0107/artifacts/qa/prepare-planning.json`
- `tickets/archive/TASK-0107/artifacts/qa/sample-proof-packet.json`

## Known Limits

Filesystem ticket adapter and local compute only; no daemon, polling, Linear/Notion adapter, cloud execution, or Codex-launching wrapper.

## Metrics

- `runner_contract_conformance`
- `proof_packet_parse_rate`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0015`.
