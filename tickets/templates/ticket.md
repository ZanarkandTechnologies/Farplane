---
ticket_id: TASK-XXXX
title: short title
phase: planning
status: review
owner: unassigned
claimed_by:
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: true
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-03T00:00:00Z
next_action: define the one current step and keep it in this field
last_verification: none
linked_docs: []
---

# TASK-XXXX: title

## Summary
Short description of the next ambitious executable slice.

## Scope
- In:
- Out:

## User Story
- `Actor:`
- `Need:`
- `Outcome:`

## User Pain / JTBD
- `Current pain:`
- `Why now:`

## Non-Goals
- `Do not solve:`

## High-Fidelity Example
- `Example flow/artifact:`

## What Good Looks Like
- `Quality bar:`

## Proof Target
- `Reviewer-visible proof:`

## Plan

### Human

#### Decision
- `Req:`
- `Best:`
- `Why:`
- `Tradeoff accepted:`
- `Not chosen:`

#### Diagram
- `Required:` yes for material, cross-module, workflow/tooling, or
  architecture-facing work; optional for trivial localized fixes
- `Legend:` keep | change | add | remove
```mermaid
flowchart LR
  %% Tier 1: top-level delta map
  %% Put short signatures in nodes when the interface or ownership boundary matters.
```
- `Tier 2:` optional zoom-in or component view only when Tier 1 is not enough

#### Signature Sketch
- `Format:` `module / symbol(input): output`
- `Use:` 3-7 seams that prove codebase understanding
- `Avoid:` full type dumps

#### B -> A
- `Before:`
- `After:`
- `Outcome:`

#### Proof
- `P1:`
- `P2:`
- `Risk:`
- `Rollback:`

#### Ask
- `Ready: yes|no`
- `Next:`

### Agent

#### Delta
- `Touch:`
- `Keep:`
- `Change:`
- `Delete/Avoid:`

#### Execution Plan
```mermaid
flowchart LR
  %% Prefer a numbered critical-path data-flow diagram for material work.
```
```pseudo
inspect current state
name the real seams
apply smallest safe delta
validate changed surfaces
update docs/evidence
```

#### Risk / Rollback
- `Primary risk:`
- `Containment:`
- `Rollback:`

#### Plan Review
- `Refs:`
- `Checks:`
- `Fixes:`

#### Options Appendix
- `Option 1:`
- `Pros:`
- `Cons:`
- `Why not chosen:`
- `Option 2:`
- `Pros:`
- `Cons:`
- `Why not chosen:`
- `Option 3:`
- `Pros:`
- `Cons:`
- `Why not chosen:`

#### Delegation
- `Need:`
- `Why:`
- `Artifact:`

#### Ticket Move
- `Now:`
- `On approval:`
- `Follow-ups:`
- `Blocked in building?:`

## Acceptance Criteria
- [ ] AC-1
- [ ] AC-2

## Working Notes
- Active task-local memory only. Durable cross-task lessons move to docs on completion.
- `approval_required: true`, any active `blocked_by` entry, or an unresolved dependency that prevents the next step all imply `ready: false`.
- `owner` is the broad work owner; `claimed_by` is optional live-session claim state for board visibility. Do not store raw `session_id` values in ticket frontmatter.
- `next_action` is the authoritative current step. Explain it here if useful, but do not create a second state field.
- `last_verification` is the authoritative verification summary. Put detailed commands and observations in `Evidence`.
- for material work, the top of the plan should be approvable from `Decision + Diagram + Signature Sketch + B -> A + Proof` before the reviewer reads the lower prose
- when the user did not provide a take on a material choice, capture three viable options plus the recommended path in the plan instead of leaving the tradeoff implicit
- when this ticket exists because a larger capability was split, name the real split trigger and show why this slice is proof-coherent, foundation-coherent, or value-coherent rather than an arbitrary micro-step
- `User Story`, `User Pain / JTBD`, `Non-Goals`, `High-Fidelity Example`, `What Good Looks Like`, and `Proof Target` are required for material feature work, workflow/tooling changes, ambiguous implementation work, and any ticket where the implementer would otherwise need to infer desired behavior
- those sections may be short or omitted for trivial, narrowly localized fixes where the file, symbol, or error already anchors the work concretely

## Inspiration
- Optional: source links and a short note on which external idea, article, talk, or incident motivated this ticket.
- Keep at least one durable source URL here when the ticket was created from outside inspiration.

## Implementation Notes
- Touched areas:
- Reused patterns:
- Guardrails:

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [ ] QA / manual verification

## Review Packet
- Scores use the anchored `1.0`-to-`5.0` rubric scale.
- `work_type:` `[]`
- `search_scope:` `{changed_files: [], related_files: [], invariants_checked: [], docs_checked: []}`
- `reviewed_at:` `YYYY-MM-DD HH:mm ±ZZZZ`
- `rubrics_used:` `[]`
- `overall_score:`
- `overall_threshold:`
- `overall_verdict:` `pass|revise|block`
- `rerun_required:` `true|false`
- `evidence_quality:` `pass|fail`
- `integration_readiness:` `pass|fail`
- `traceability:` `pass|fail`
- `freshness:` `pass|fail`
- `hard_gate_failures:` `[]`
- `finding_log:` `[]`
- `blocking_findings:` `[]`
- `next_action:`

## Blockers
- none

## Handoff
- Current state:
- Resume from:

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
