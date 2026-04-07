---
ticket_id: TASK-0007
title: define codexter context policy and handoff rules
phase: complete
status: done
owner: codex
priority: medium
depends_on:
  - TASK-0006
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-07T00:00:00Z
next_action: archived; future lifecycle changes should extend the documented policy rather than recreate hidden runtime handoff state
last_verification: documented the canonical progress-surface, deliberate reset/resume, documenting, and archive rules in docs/specs/context-and-handoff-policy.md and linked them from tickets/README.md
linked_docs:
  - docs/specs/spec-first-execution-loop.md
  - docs/specs/orchestrator-subagent-loop.md
  - skills/impl/SKILL.md
  - docs/specs/context-and-handoff-policy.md
  - tickets/README.md
---

# TASK-0007: define codexter context policy and handoff rules

## Summary
Define the progress-surface, handoff, and archive rules for the spec-first loop so resets and resumes are understandable without hidden runtime state.

## Scope
- In: progress-surface policy, required handoff content, documentation/writeback boundary, and archive rules for completed or outdated tickets
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
- `Change:` add explicit context and handoff policy now that the orchestration loop and `$impl` surface exist
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
- `Proof:` ready to evaluate against the shipped orchestration contract
- `Guardrails:` keep it minimal and ticket-first
- `Fixes:` canonicalized this backlog ticket and made the dependency on `TASK-0006` explicit

### Delegation
- `Need:` `Not needed`
- `Why:` small contract slice
- `Artifact:` none

### Ask
- `Ready: no`
- `Next:` plan the handoff/archive rules against the current ticket + `$impl` + Stop-hook flow

### Ticket Move
- `Now:` `tickets/`
- `On approval:` move to `tickets/` for active planning/building work
- `Follow-ups:` none yet
- `Blocked in building?:` `yes`

## Acceptance Criteria
- [x] AC-1: the system has explicit rules for what stays in the progress surface versus what lives only in runtime state
- [x] AC-2: handoff requirements are defined for deliberate reset/resume of a spec-first run
- [x] AC-3: archive movement rules are explicit for completed and superseded tickets
- [x] AC-4: documenting/writeback remains an explicit phase before archive

## Working Notes
- This ticket depends on the orchestration loop contract, which is now documented and can be consumed directly.
- The handoff policy should strengthen ticket authority, not recreate hidden runtime state or a second archive surface.

## Implementation Notes
- Touched areas: docs/contracts only
- Reused patterns: file-based evidence and handoff philosophy
- Guardrails: no hidden reset or continuation behavior

## Evidence
- [ ] Tests
- [x] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Validation details:
  - `python3 bin/check_ticket_metadata.py`
  - reviewed `docs/specs/context-and-handoff-policy.md`
  - reviewed `tickets/README.md`
  - reviewed `docs/specs/spec-first-execution-loop.md`

## Blockers
- none

## Handoff
- Current state: the handoff/archive/progress-surface policy is now explicit and anchored to visible ticket + docs surfaces instead of transcript memory or hidden runtime state.
- Resume from: `docs/specs/context-and-handoff-policy.md`, `tickets/README.md`, and any future lifecycle ticket that changes documenting/archive behavior.

## Writeback
- Update this ticket as work progresses.
- Update `status` and `phase` in frontmatter when queue state changes.
