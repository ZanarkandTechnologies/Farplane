---
ticket_id: TASK-0004
title: add codexter discovery workflow
phase: planning
status: review
owner: codex
priority: medium
depends_on:
  - TASK-0001
blocked_by: []
ready: false
approval_required: true
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-03T02:06:03Z
next_action: await approval to implement the discovery workflow and move this ticket to building
last_verification: none
linked_docs: []
---

# TASK-0004: add codexter discovery workflow

## Summary
Create the smallest reviewable discovery workflow contract so ambiguous prompts have one explicit brainstorm/interview path before PRD or ticket planning.

## Scope
- In: one concrete discovery workflow surface, trigger conditions, output brief shape, and handoff rules into planner/PRD
- Out: deep research, runtime automation, evaluator logic, or a broad prompt/mode rewrite

## Plan

### Pitch
- `Req:` ship the missing discovery layer Codexter already references conceptually
- `Bet:` land one small discovery workflow artifact plus the minimum planner/PRD handoff wiring instead of stretching discovery across multiple prompts or modes
- `Win:` ambiguous requests get clarified through one reusable path before planning, without bloating `prd` or turning planner behavior into hidden convention

### B -> A
- `Before:` `agents/planner-agent.toml` and PRD guidance mention brainstorm/interview behavior, but there is no installed concrete workflow to own trigger rules, question shape, or handoff output
- `After:` Codexter has one explicit discovery workflow with a documented brief output and a clear bridge into `skills/prd` or planning/ticket work
- `Outcome:` vague prompts get normalized before PRD/ticketing, and follow-on orchestration work can reference a real discovery surface instead of implied behavior

### Delta
- `Touch:` a dedicated discovery workflow surface, `agents/planner-agent.toml`, and PRD/discovery reference text where handoff expectations are currently implied
- `Keep:` `skills/prd` as the product-spec authoring surface, ticket-first planning/build separation, and the "no tools first" ambiguity-reduction posture
- `Change:` make discovery a first-class reusable pre-PRD/pre-plan step with one output shape reviewers can inspect
- `Delete/Avoid:` avoid a second planning system, heavy interview appendix, or duplicate question sets spread across multiple files

### Core Flow
```pseudo
detect request ambiguity before PRD or ticket planning
invoke one discovery workflow with 6-10 high-signal questions
capture user, JTBD, slice, non-goals, constraints, and success signals
emit one compact discovery brief with explicit handoff recommendation
route to PRD when product shape is still needed
route to planning/ticketing when the brief is already executable
keep research optional and late
```

### Proof
- `P1:` the repo exposes one concrete discovery workflow artifact reviewers can open and understand without inferring behavior from planner prose
- `P2:` planner and PRD references point to the same discovery surface instead of carrying duplicated or drifting interview guidance
- `P3:` a reviewer can trace how an ambiguous request becomes a brief, then moves into PRD or plan/ticket work without adding runtime automation
- `Risk:` discovery scope could drift into full PRD authoring or duplicate existing PRD guidance
- `Rollback:` remove the dedicated discovery artifact and revert planner/PRD guidance to embedded interview instructions only

### Plan Review
- `Refs:` `AGENTS.md`, `skills/tech-impl-plan/SKILL.md`, `skills/tech-impl-plan/references/review.md`, `docs/research/web-research/2026-04-02_codexter-change-proposal.md`, `agents/planner-agent.toml`, `skills/prd/SKILL.md`, `skills/prd/references/requirements-discovery.md`, `docs/MEMORY.md`, `tickets/TASK-0006-codexter-orchestration-loop.md`
- `Scope:` pass; this stays one commit focused on a discovery artifact plus minimal handoff wiring, not runtime/orchestration implementation
- `Proof:` pass; success is reviewable through the new discovery contract and aligned planner/PRD references
- `Guardrails:` pass; reuses existing PRD and ticket flow, keeps research optional/late, and avoids prompt-surface sprawl beyond the one missing workflow
- `Fixes:` tightened the slice around a single reusable discovery surface, made touched areas explicit, added observable proof points, and called out the PRD-overlap risk directly

### Delegation
- `Need:` `Not needed`
- `Why:` single-ticket planning rewrite with bounded doc/skill surface
- `Artifact:` none

### Ask
- `Ready: yes`
- `Next:` on approval, implement the discovery surface and handoff wiring, then let `TASK-0006` consume that surface in the broader orchestration loop

### Ticket Move
- `Now:` `tickets/`
- `On approval:` move to `tickets/`
- `Follow-ups:` `TASK-0006` should consume this workflow once it exists; no new split ticket is required for this slice
- `Blocked in building?:` `no`

## Acceptance Criteria
- [ ] AC-1: one explicit discovery workflow surface exists with clear trigger conditions for ambiguous requests
- [ ] AC-2: the workflow defines one compact discovery brief output that captures intent, constraints, non-goals, and handoff direction
- [ ] AC-3: planner and PRD guidance point to the same discovery surface instead of duplicating or improvising interview behavior
- [ ] AC-4: the slice remains smaller than full PRD authoring and does not introduce runtime automation or extra planning modes

## Working Notes
- Keep this slice tied to the canonical ticket dialect so the discovery brief hands off into one predictable ticket shape instead of a second planning surface.

## Implementation Notes
- Touched areas: one discovery workflow artifact plus the minimum planner/PRD references needed to route into it
- Reused patterns: Codexter's existing interview-first PRD guidance, ticket-first planning flow, and approval-first `tech-impl-plan` shape
- Guardrails: no new runtime layer, no evaluator changes, no hidden autonomy, no duplicated long-form questionnaire across multiple files

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [ ] QA / manual verification

## Blockers
- none

## Handoff
- Current state: plan is review-ready and waiting for approval.
- Resume from: this ticket, the PRD references, and the planner/discovery surfaces named in Plan Review.

## Writeback
- Update this ticket as work progresses.
- Update `status` and `phase` in frontmatter when queue state changes.
