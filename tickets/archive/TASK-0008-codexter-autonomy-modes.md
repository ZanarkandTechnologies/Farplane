---
ticket_id: TASK-0008
title: park autonomy-mode policy outside v1
phase: planning
status: blocked
owner: unassigned
priority: medium
depends_on:
  - TASK-0002
blocked_by: []
ready: false
approval_required: true
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-03T06:30:00Z
next_action: keep this ticket in todo until the repo deliberately re-opens post-v1 autonomy work as a separate scope from the ticket-metadata foundation
last_verification: none
linked_docs: []
---

# TASK-0008: park autonomy-mode policy outside v1

## Summary
Keep autonomy-mode policy visible as deferred backlog, not active review. The repo-level decision for the current rollout is simpler: assisted continuation is outside v1 of the ticket metadata feature.

## Scope
- In: explicit quarantine status, the repo-level boundary for v1, and re-entry conditions for any future post-v1 autonomy policy work
- Out: autonomy mode definitions, mode-selection config, notify hooks, assisted continuation behavior, durable team runtime, hidden approval injection, or runtime enforcement code

## Plan

### Pitch
- `Req:` remove the implication that Codexter is actively defining opt-in autonomy modes as part of the current metadata rollout
- `Bet:` park this ticket in backlog with a clear blocker instead of keeping it as an active review item
- `Win:` the board matches the shipped repo surface, and the v1 boundary is easier for an autonomous coding agent to follow

### B -> A
- `Before:` this ticket appeared to be active review work even though the repo is explicitly removing tracked continuation surfaces from the v1 foundation
- `After:` this ticket is parked in backlog as post-v1 policy work, with the current repo decision expressed directly in docs and board state instead of through a future autonomy matrix
- `Outcome:` trust improves because the repo no longer suggests that autonomy-mode work is part of the current rollout

### Delta
- `Touch:` this ticket, `tickets/README.md`, and the repo-level docs/contracts that make the v1 boundary explicit
- `Keep:` autonomy policy as traceable backlog only
- `Change:` stop treating autonomy modes as active review work in the current rollout
- `Delete/Avoid:` avoid active-scope language, mode matrices, config examples, or any feature-proof text that implies post-v1 autonomy is already in flight

### Core Flow
```pseudo
move the ticket out of active review
reset it to backlog/quarantine semantics
record the repo-level v1 decision explicitly
require a future post-v1 rescope before any autonomy policy or runtime work returns to review
```

### Proof
- `P1:` this ticket no longer lives in `tickets/`
- `P2:` its frontmatter and body now describe deferred backlog only
- `P3:` the board and repo docs use the direct v1 boundary instead of implying that a mode matrix is about to ship
- `Risk:` future loops may try to revive autonomy work by editing runtime surfaces instead of re-scoping the board first
- `Rollback:` none needed for v1; if this work becomes valid later, rewrite the ticket from this parked state as a fresh post-v1 slice

### Plan Review
- `Refs:` `Codexter/AGENTS.md`, `Codexter/skills/tech-impl-plan/SKILL.md`, `Codexter/docs/research/web-research/2026-04-02_codexter-change-proposal.md`, `Codexter/docs/research/web-research/2026-04-02_codexter-vs-omx-gap-analysis.md`, `Codexter/tickets/templates/ticket.md`, `Codexter/tickets/TASK-0002-codexter-ticket-metadata-foundation.md`, `Codexter/docs/prd.md`, `Codexter/docs/MEMORY.md`, `Codexter/docs/TROUBLES.md`
- `Scope:` pass; ticket-coherence cleanup only
- `Proof:` pass; success is visible in the lane move plus the rewritten metadata/body
- `Guardrails:` pass; preserves operator trust by keeping post-v1 autonomy work out of active lanes
- `Fixes:` replaced active-scope autonomy-mode language with an explicit backlog boundary that matches the shipped repo surface

### Delegation
- `Need:` `Not needed`
- `Why:` this is a local board/doc coherence rewrite only
- `Artifact:` none

### Ask
- `Ready: no`
- `Next:` leave this ticket parked unless the repo deliberately re-opens post-v1 autonomy work as a separate scope

### Ticket Move
- `Now:` `tickets/`
- `On approval:` remain parked until a future non-v1 decision exists
- `Follow-ups:` if revived later, rewrite this as a fresh post-v1 policy or implementation ticket instead of restoring active-review notes
- `Blocked in building?:` `yes`

## Acceptance Criteria
- [ ] AC-1: the repo deliberately changes the v1 boundary to re-open autonomy work
- [ ] AC-2: this ticket is rewritten as a separate post-v1 policy or implementation slice instead of being revived implicitly
- [ ] AC-3: explicit approval is granted before the ticket re-enters `tickets/`

## Working Notes
- The current repo-level decision is intentionally simpler than a mode matrix. That keeps the active board and shipped docs more trustworthy during the v1 metadata rollout.

## Implementation Notes
- Touched areas: this ticket plus the board/docs surfaces that now state the v1 boundary directly
- Reused patterns: canonical ticket dialect, explicit blockers, and lane-as-truth board rules
- Guardrails: no hooks, no assisted continuation, no autonomy implementation, and no hidden runtime behavior

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification

## Blockers
- repo decision: assisted continuation and autonomy work are outside v1 of the ticket metadata feature

## Handoff
- Current state: quarantined backlog item only; not part of the active metadata rollout.
- Resume from: the repo-level v1 boundary and the downstream backlog only if a future loop deliberately re-opens post-v1 autonomy work.

## Writeback
- Update this ticket as work progresses.
- Update `status` and `phase` in frontmatter when queue state changes.
