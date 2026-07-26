---
title: "Retired Invocation Runtime"
status: retired
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-07-26
tags:
  - farplane
  - systems
  - retired
refs:
  - docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md
  - tickets/archive/TASK-0414/ticket.md
system_record_json: |
  {
    "id": "SYS-0004",
    "name": "Retired Invocation Runtime",
    "status": "retired",
    "summary": "Historical record for the removed invocation envelope, board, compute, and ticket-runtime experiment.",
    "owner_spec": "docs/systems/invocation-runtime.md",
    "primary_feature_ref": "FEAT-0015",
    "feature_refs": [
      "FEAT-0015"
    ],
    "refs": [
      "docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md",
      "tickets/archive/TASK-0414/ticket.md"
    ],
    "last_verified": "2026-07-26"
  }
---

# Retired Invocation Runtime

SYS-0004 is a historical owner for the removed invocation envelope, board
adapter, compute selector, and ticket-runtime experiment. It has no active
runtime or skill surface.

```text
local Codex task -> selected checkout -> ticket/skill/QA flow
```

Future remote compute should start from a new current requirement and ticket,
not revive this contract by default.

## Feature Docs

- [FEAT-0015 retired invocation contract](../features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md)
