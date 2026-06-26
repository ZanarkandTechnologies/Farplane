---
title: "Symphony-compatible Farplane invocation contract"
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0004
refs:
  - WORKFLOW.md
  - skills/farplane-invocation
  - bin/farplane_invocation.py
  - docs/specs/invocation-and-adapters.md
  - docs/HISTORY.md
  - tickets/archive/TASK-0107/ticket.md
  - tickets/archive/TASK-0107/artifacts/qa/prepare-planning.json
  - tickets/archive/TASK-0107/artifacts/qa/sample-proof-packet.json
feature_record_json: |
  {
    "id": "FEAT-0015",
    "name": "Symphony-compatible Farplane invocation contract",
    "status": "implemented",
    "system_id": "SYS-0004",
    "category": "execution",
    "public": true,
    "surfaces": [
      "WORKFLOW.md",
      "skills/farplane-invocation",
      "bin/farplane_invocation.py",
      "docs/specs/invocation-and-adapters.md"
    ],
    "source_refs": [
      "docs/specs/invocation-and-adapters.md",
      "docs/HISTORY.md"
    ],
    "external_refs": [
      "Symphony Service Specification draft v1"
    ],
    "evidence_refs": [
      "tickets/archive/TASK-0107/ticket.md",
      "tickets/archive/TASK-0107/artifacts/qa/prepare-planning.json",
      "tickets/archive/TASK-0107/artifacts/qa/sample-proof-packet.json"
    ],
    "known_limits": "Filesystem ticket adapter and local compute only; no daemon, polling, Linear/Notion adapter, cloud execution, or Codex-launching wrapper.",
    "metrics": [
      "runner_contract_conformance",
      "proof_packet_parse_rate"
    ],
    "last_verified": "2026-05-05"
  }
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

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `WORKFLOW.md`
- `skills/farplane-invocation`
- `bin/farplane_invocation.py`
- `docs/specs/invocation-and-adapters.md`

## Source Context

- `docs/specs/invocation-and-adapters.md`
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
