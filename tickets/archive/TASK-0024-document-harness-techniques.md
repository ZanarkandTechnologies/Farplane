---
ticket_id: TASK-0024
title: document harness techniques
phase: complete
status: done
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-07T20:37:56Z
updated_at: 2026-04-07T20:39:51Z
next_action: archived; use the techniques inventory as the canonical implemented-vs-proposed harness catalog
last_verification: manual review passed; verified the new techniques doc, README pointer, specs index, history writeback, and ticket with git diff --check clean on the changed files
linked_docs:
  - docs/specs/harness-techniques.md
  - docs/specs/README.md
  - README.md
---

# TASK-0024: document harness techniques

## Summary
Document the harness techniques Codexter already uses today, plus the highest-value proposed techniques, in one canonical doc with a compact README pointer.

## Scope
- In: current-state audit, canonical techniques inventory, README discoverability, specs/history writeback
- Out: runtime or prompt behavior changes beyond documentation

## Plan

### Pitch
- `Req:` document the techniques the harness already uses and the deltas worth trying next
- `Bet:` one honest implemented-vs-proposed catalog will reduce repeated rediscovery and make future harness experiments easier to ticket
- `Win:` agents can inspect one doc and understand the current harness, its main techniques, and the next bets

### B -> A
- `Before:` techniques are spread across specs, skills, agents, and research notes
- `After:` one canonical spec catalogs live techniques and proposed experiments, with README pointing to it
- `Outcome:` the harness has a discoverable feature inventory instead of relying on chat memory

### Delta
- `Touch:` `docs/specs/harness-techniques.md`, `docs/specs/README.md`, `README.md`, `docs/HISTORY.md`, this ticket
- `Keep:` existing execution/review specs as source-of-truth behavior docs
- `Change:` documentation discoverability and technique inventory clarity
- `Delete/Avoid:` duplicating the full catalog in README

### Core Flow
```pseudo
audit the live harness surfaces from specs, skills, agents, and hooks
separate implemented techniques from proposed experiments
write a canonical techniques inventory
add a compact README pointer and history/spec-index writeback
review the docs and archive the ticket
```

### Proof
- `P1:` every implemented technique listed in the new doc has a real repo surface backing it
- `P2:` proposed techniques are clearly labeled as deltas, not current behavior
- `Risk:` the doc collapses implemented and proposed ideas into one blurry list
- `Rollback:` tighten the status split and remove anything not grounded in repo truth

### Plan Review
- `Refs:` `README.md`, `AGENTS.md`, `docs/specs/*`, `skills/*`, `agents/qa-tester.toml`, `docs/MEMORY.md`, `docs/TROUBLES.md`
- `Scope:` docs-only inventory and discoverability changes
- `Proof:` manual review and `git diff --check`
- `Guardrails:` no behavior changes; do not misrepresent future ideas as implemented
- `Fixes:` keep the README summary short and move full detail into the dedicated doc

### Delegation
- `Need:` Not needed
- `Why:` bounded doc synthesis from local repo truth
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` complete the docs, run a review pass, archive

### Ticket Move
- `Now:` `status: building`, `phase: building`
- `On approval:` n/a; user directly requested implementation
- `Follow-ups:` none required for this docs slice
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: a canonical techniques doc lists implemented techniques with repo-surface references
- [x] AC-2: the doc lists proposed techniques separately with clear deltas
- [x] AC-3: README points to the new doc and summarizes the main live techniques without duplicating the full catalog
- [x] AC-4: specs/history writeback makes the inventory discoverable

## Working Notes
- Use a `tech-impl-plan` style audit mindset: inspect current state first, then write the delta.
- Document the `tech-impl-plan` / `ralplan` overlap as a delta, not as a resolved design.

## Implementation Notes
- Touched areas: `docs/specs/`, `README.md`, `docs/HISTORY.md`, `tickets/`
- Reused patterns: canonical spec docs, ticket writeback, honest prototype-vs-direction framing
- Guardrails: implemented vs proposed must stay explicit

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Validation details:
  - reviewed the new inventory against `README.md`, root `AGENTS.md`, `docs/specs/*`, `skills/*`, `agents/qa-tester.toml`, `docs/MEMORY.md`, and `docs/TROUBLES.md`
  - confirmed implemented techniques are backed by live repo surfaces and proposed techniques are labeled as deltas
  - ran `git diff --check -- docs/specs/harness-techniques.md docs/specs/README.md README.md docs/HISTORY.md tickets/archive/TASK-0024-document-harness-techniques.md`
  - review pass: `rubrics_used=[implementation-plan,evidence-quality]`, `overall_score=94`, `verdict=pass`, `rerun_required=false`

## Blockers
- none

## Handoff
- Current state: the harness techniques inventory is now canonical and linked from the README.
- Resume from: `docs/specs/harness-techniques.md` when adding or reclassifying techniques in future harness work.

## Writeback
- Update this ticket as work progresses.
- When the docs and review pass are complete, archive the ticket.
