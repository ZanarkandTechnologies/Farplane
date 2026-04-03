---
ticket_id: TASK-0007
title: define codexter context policy and handoff rules
phase: planning
status: blocked
owner: unassigned
priority: medium
depends_on:
  - TASK-0002
  - TASK-0006
blocked_by:
  - TASK-0006
ready: false
approval_required: true
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-03T03:44:43Z
next_action: keep this ticket in todo until TASK-0006 defines the orchestration contract, then move it to review
last_verification: none
linked_docs: []
---

# TASK-0007: define codexter context policy and handoff rules

## Summary
Define when Codexter should stay in-session, hand off through the ticket itself, or resume from a fresh session, with explicit documenting-phase rules before a ticket can be removed or archived.

## Scope
- In: context policy, required ticket handoff content, documentation/writeback boundary, and archive/delete rules for completed tickets
- Out: compression tooling, advanced automation, or hidden runtime resume behavior

## Plan

### Pitch
- `Req:` make long-context handling explicit instead of implicit
- `Bet:` a small written policy plus required ticket handoff content and documenting-phase rules is enough for v1
- `Win:` resets and resumes become safer without heavyweight runtime machinery or a second artifact system

### B -> A
- `Before:` session continuity depends too much on active chat context
- `After:` Codexter has clear stay-in-session, handoff, documenting, and archive/delete rules
- `Outcome:` a fresh session can restart from the ticket itself plus linked docs without hidden state

### Delta
- `Touch:` docs/contracts for ticket lifecycle and orchestration
- `Keep:` the simple ticket-first workflow and visible-file evidence
- `Change:` add explicit context and handoff policy once the orchestration loop exists
- `Delete/Avoid:` avoid new runtime layers, hidden continuation, or extra archive surfaces

### Core Flow
```pseudo
define short-task stay-in-session rule
define mandatory ticket handoff content
define when work enters documenting
define when durable notes move to docs
define when a completed ticket may be archived or deleted
```

### Proof
- `P1:` a reviewer can tell exactly when Codexter should stay, compact, or resume
- `P2:` a fresh session could restart from the ticket itself plus linked docs without extra runtime artifacts
- `Risk:` policy could drift back toward hidden state instead of strengthening ticket authority
- `Rollback:` keep the policy advisory-only until the upstream loop contract is stable

### Plan Review
- `Refs:` `TASK-0002`, `TASK-0006`
- `Scope:` context policy only
- `Proof:` pending the orchestration contract
- `Guardrails:` keep it minimal and ticket-first
- `Fixes:` canonicalized this backlog ticket and made the dependency on `TASK-0006` explicit

### Delegation
- `Need:` `Not needed`
- `Why:` small contract slice
- `Artifact:` none

### Ask
- `Ready: no`
- `Next:` keep this ticket parked until the orchestration-loop contract exists

### Ticket Move
- `Now:` `tickets/todo/`
- `On approval:` move to `tickets/review/` after `TASK-0006` is ready
- `Follow-ups:` none yet
- `Blocked in building?:` `yes`

## Acceptance Criteria
- [ ] AC-1: Codexter has explicit stay/compact/resume rules
- [ ] AC-2: ticket handoff requirements are defined for deliberate reset/resume
- [ ] AC-3: policy aligns with the ticket-frontmatter contract instead of competing with it
- [ ] AC-4: documentation writeback is an explicit completion phase before ticket archive/deletion

## Working Notes
- This ticket depends on the orchestration loop contract, so it stays parked in `tickets/todo/` until `TASK-0006` is ready to feed it.
- The handoff policy should strengthen ticket authority, not recreate hidden runtime state or a second archive surface.

## Implementation Notes
- Touched areas: docs/contracts only
- Reused patterns: file-based evidence and handoff philosophy
- Guardrails: no hidden reset or continuation behavior

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [ ] QA / manual verification

## Blockers
- `TASK-0006`

## Handoff
- Current state: canonicalized backlog ticket; still parked until the orchestration-loop contract exists.
- Resume from: this ticket, `TASK-0006`, and the metadata/lifecycle rules in `TASK-0002` when the backlog is ready to move forward.

## Writeback
- Update this ticket as work progresses.
- Move the ticket and update `tickets/INDEX.md` when its board state changes.
