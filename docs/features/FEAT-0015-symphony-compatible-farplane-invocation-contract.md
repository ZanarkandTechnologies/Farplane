---
title: Retired Symphony-compatible invocation contract
status: retired
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-07-26
tags:
  - farplane
  - feature
  - retired
refs:
  - docs/HISTORY.md
  - tickets/archive/TASK-0107/ticket.md
  - tickets/archive/TASK-0414/ticket.md
feature_id: FEAT-0015
system_id: SYS-0004
category: execution
public: true
surfaces:
  - docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md
source_refs:
  - docs/HISTORY.md
external_refs:
  - Symphony Service Specification draft v1
evidence_refs:
  - tickets/archive/TASK-0107/ticket.md
  - tickets/archive/TASK-0414/ticket.md
known_limits: Historical record only; the workflow, skill, command family, runtime records, board adapter, and compute selector were removed.
metrics: []
last_verified: 2026-07-26
experimental: false
superseded_by: false
---

# Retired Symphony-compatible invocation contract

The experimental invocation envelope, board adapter, compute selector,
`WORKFLOW.md`, `farplane-invocation` skill, and Ticket Runtime were removed.
They had no active callers and duplicated native Codex checkout selection plus
Farplane's existing ticket and QA handoffs.

```text
current_local_execution(ticket, codex_task)
  -> selected_checkout + ordinary_skill_route + ticket_scoped_proof
```

Public docs should describe `.farplane/` as the canonical live runtime root.
There is no separate public retired execution surface anymore.

## Current boundary

- Codex chooses the local checkout or worktree for its task.
- Tickets own scope and proof obligations.
- QA receives an explicit target or a verified cookbook entry when an app must
  be running.
- `farplane` is the only user-facing installed command.
- Remote compute and per-ticket runtime orchestration require a new ticket
  based on current needs.

Historical implementation and proof remain in `docs/HISTORY.md` and
`tickets/archive/TASK-0107/`.
