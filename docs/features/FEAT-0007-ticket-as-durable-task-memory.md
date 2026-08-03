---
title: Ticket as durable task memory
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-08-02
tags:
  - farplane
  - feature
  - sys-0002
refs:
  - tickets/README.md
  - tickets/templates/ticket.md
  - skills/impl-plan
  - skills/spec-to-ticket
  - skills/close-ticket
  - docs/features/FEAT-0007-ticket-as-durable-task-memory.md
  - docs/features/README.md
  - "docs/MEMORY.md#MEM-0058"
  - "docs/MEMORY.md#MEM-0148"
  - docs/HISTORY.md
feature_id: FEAT-0007
system_id: SYS-0002
category: memory
public: true
surfaces:
  - tickets/README.md
  - tickets/templates/ticket.md
  - skills/impl-plan
  - skills/spec-to-ticket
  - skills/close-ticket
  - docs/features/FEAT-0007-ticket-as-durable-task-memory.md
source_refs:
  - docs/features/README.md
  - "docs/MEMORY.md#MEM-0058"
  - "docs/MEMORY.md#MEM-0148"
external_refs: []
evidence_refs:
  - docs/HISTORY.md
known_limits: Only works when agents keep the compact ticket-as-program body, ticket Links, progress logs, and artifact pointers current instead of hiding state in chat.
metrics: []
last_verified: 2026-08-02
experimental: false
superseded_by: false
---
# Ticket as durable task memory

Ticket as durable task memory exists to turn a request into a visible work contract that
survives handoff, interruption, review, and closeout. It belongs to [Work
Loop](../systems/work-loop.md) and keeps `FEAT-0007` as a stable capability handle
because the behavior has an owner, proof path, and maintenance boundary.

```text
ticket_memory(intent, repo_state?) -> ticket_contract + proof_scoreboard + resume_state
ticket_status(ticket, dependencies, reward_rows, claim?) -> executable | waiting | terminal
ticket_sort_key(ticket) -> priority + due_at? + ticket_id
```

## At A Glance

- Feature ID: `FEAT-0007`
- System: [Work Loop](../systems/work-loop.md)
- Status: `implemented`
- Category: `memory`
- Primary user: coding agent and operator
- Job: turn a request into a visible work contract that survives handoff, interruption, review, and closeout.

## Problem

Farplane agents do long, context-heavy work. If the plan only lives in chat, the next
agent cannot reliably tell what was promised, what changed, what proof is required, or
whether the task is blocked.

A ticket fixes that by making one bounded unit of work readable from the filesystem.
Chat can steer the work, but the ticket owns the durable contract.

## What It Does

- Creates or updates a `ticket.md` for each material unit of work.
- Keeps scope, delta, change plan, `Done`, `QA Strategy`, docs strategy, links, and notes in predictable sections.
- Moves bulky proof into `tickets/TASK-*/artifacts/` and links it from the ticket.
- Lets `impl-plan`, `spec-to-ticket`, Goal Packets, QA, review, and closeout all read the same task contract.
- Preserves resume state through `program.md`, `progress.md`, and artifact links when a work loop needs more than one turn.
- Turns each newly completed ticket into one verified closed issue in the
  project's configured GitHub repository, then retains only a compact local
  locator after completion mining succeeds.

## User Stories

- As an operator, I can open one ticket and see what the agent is trying to do, what is in scope, what proof is required, and what is blocked.
- As a coding agent, I can resume a ticket without relying on hidden transcript memory.
- As a reviewer, I can judge completion against the ticket's `Done`,
  `QA Strategy`, and linked artifacts.

## Operating Contract

A durable ticket is a small program for the next agent, not a generic task note.

- `Summary` says the job in one compact paragraph.
- `Scope` states what is in and out.
- `Delta` briefly describes the intended behavior change and problem deltas.
- `Change Plan` groups the executable program, read/write file map, operation,
  routes, proof, and failure modes by coherent change unit.
- `Done` is the completion scoreboard.
- `QA Strategy` carries proof weight, checks, delegated lanes, review gates,
  evidence, goal-advisor inputs, final checkpoint, and residual risk.
- Frontmatter carries one lifecycle status plus identity/freshness and only the
  sparse routing overrides that differ from defaults.
- Optional `due_at` is a delivery deadline as a timezone-bearing ISO-8601
  timestamp. It is used for ordinary executable-board ordering inside the same
  priority band; it is not priority, lifecycle state, delayed Reward
  `check_in_at`, or Goal Packet timing.
- `progress.md` carries current action, blockers, verification, review state,
  and delayed check-in observations.
- The first-load envelope is the full ticket, full Goal program when present,
  and the latest 80 progress lines. It targets 300 lines and blocks planning or
  completion above 400 through `ticket.context-budget`; length never licenses
  deleting required proof or hiding executable policy.
- `Links` points to evidence, artifacts, related specs, sidecars, and handoffs.
- `$close-ticket` owns remote publication: create or resume one marked issue in
  `integrations.github.repo`, render concise `Before`, `After`, `Example`, `Key
  decisions`, and `Proof`, upload the reviewed `$demo` MP4 first for material
  feature tickets followed by explicitly selected supporting media as marked
  browser comments, verify the issue, and close it.
- `farplane ticket finalize TASK-XXXX` owns the successful local terminal
  transaction: re-verify the closed issue and media markers, update metadata,
  mine the still-local packet, atomically write the compact locator, emit
  completion, and only then delete the exact active packet.
- Any failed remote, mining, locator, or deletion prerequisite retains the
  packet for a retry against the same marked issue. Agents do not manually move
  or delete it.

The required frontmatter is only `ticket_id`, `title`, `status`, `created_at`,
and `updated_at`. Optional `priority`, `due_at`, `claimed_by`, `depends_on`,
`human_gate`, and `compute_target` exist only when they change routing. There is
no parallel `phase`, hand-maintained `ready`, approval boolean, blocker list,
QA/demo flags, next action, or verification field.

## Feature Flow

```mermaid
flowchart TD
  classDef keep fill:#f3f4f6,stroke:#6b7280,color:#111827
  classDef changed fill:#fef3c7,stroke:#b45309,color:#111827
  classDef added fill:#dcfce7,stroke:#15803d,color:#111827
  classDef retired fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d,stroke-dasharray: 5 3

  trigger["Trigger<br/>accepted task or planning handoff"]:::keep
  owner["Owner surface<br/>tickets/README.md<br/>tickets/templates/ticket.md"]:::changed
  readers["Files and fields read<br/>Summary, Scope, Delta<br/>Change Plan, Done, QA Strategy<br/>frontmatter state, Links"]:::keep
  routes["Execution routes<br/>impl-plan, spec-to-ticket<br/>Pulse priority + due_at ordering"]:::changed
  artifact["Created artifact/evidence<br/>tickets/TASK-XXXX/ticket.md<br/>with proof scoreboard"]:::added
  close["Terminal record<br/>verified closed configured-repo issue<br/>compact local locator"]:::added
  old["Retired<br/>chat-only task memory"]:::retired

  trigger --> owner --> readers --> routes --> artifact
  artifact --> close
  old -. replaced by .-> artifact
```

Legend:

- `gray = existing input, fields, or evidence read`
- `amber = owning or changed live surface`
- `green = created artifact or proof`
- `red dashed = retired or superseded path`

## Surfaces

Owner surfaces:

- `tickets/README.md`
- `tickets/templates/ticket.md`
- `skills/impl-plan`
- `skills/spec-to-ticket`
- `skills/close-ticket`
- `docs/features/FEAT-0007-ticket-as-durable-task-memory.md`

Source context:

- `docs/features/README.md`
- `docs/MEMORY.md#MEM-0058`
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
- Optional `due_at` stays timezone-bearing and affects ordering only after
  priority; tickets without it sort last inside their priority band.
- New closes resolve terminal identity from one compact GitHub issue locator,
  while legacy local archive directories remain readable.
- Local packet deletion happens only after remote verification, completion
  mining, and locator write succeed.
- Evidence refs support the current status.

## Rollout And Maintenance

- Update this feature page first when the capability contract changes.
- Then update owner surfaces and regenerate feature/system registries when metadata changes.
- Preserve the feature ID while active templates, skills, tickets, or docs still reference it.
- Maintenance owner: Work Loop.

## Limits And Non-Goals

- This feature is not a project-management app.
- This feature does not make ticket existence an invocation trigger.
- This feature does not replace feature specs, system specs, review rubrics, or bulky proof artifacts.
- GitHub Releases, release assets, tags, downloadable bundles, remote restore,
  and migration of existing local archives are future work, not part of the
  current ticket-memory contract.
- Known limit: Only works when agents keep the compact ticket-as-program body, ticket Links, progress logs, and artifact pointers current instead of hiding state in chat.
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

- 2026-08-02: Bound new terminal issues to the project's existing
  `integrations.github.repo`; configured public, private, and internal
  repositories are valid targets.
- 2026-08-01: Made one verified closed GitHub issue the terminal record for new
  closes, with mine-and-index-before-delete ordering and readable legacy local
  archives.
- 2026-06-26: Feature spec created.
- 2026-06-27: Migrated into the reader-first feature-spec shape.
- 2026-06-28: Merged Program and Map into `Change Plan` and moved body state
  duties to frontmatter, Links, and Goal progress logs.
- 2026-07-11: Collapsed ticket metadata to one status-owned lifecycle and
  moved mutable review/check-in/next-action/proof state into the ticket body,
  `progress.md`, and ticket artifacts.
- 2026-07-25: Added optional `due_at` as a timezone-bearing delivery deadline
  for same-priority executable-board ordering.
