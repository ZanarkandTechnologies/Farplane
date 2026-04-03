---
ticket_id: TASK-0003
title: define codexter evaluator scorecard
phase: planning
status: active
owner: codex
priority: medium
depends_on:
  - TASK-0002
blocked_by: []
ready: false
approval_required: true
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-03T02:06:03Z
next_action: await approval to implement the shared evaluator scorecard contract and move this ticket to building
last_verification: none
linked_docs: []
---

# TASK-0003: define codexter evaluator scorecard

## Summary
Define one normalized evaluator report format across `qa-tester`, `visual-qa`, and `code-review` so rounds end with a single comparable pass/fail artifact.

## Scope
- In: scorecard categories, thresholds, report shape, pass/fail semantics, integration notes for existing evaluator surfaces
- Out: implementing evaluator automation itself

## Plan

### Pitch
- `Req:` define one normalized evaluator scorecard that `qa-tester`, `visual-qa`, and `code-review` can all emit without losing their distinct remits
- `Bet:` make this next commit a docs-first contract slice: one shared report schema, one scoring rubric, and one adoption note for the existing evaluator surfaces, without adding evaluator automation yet
- `Win:` each build round ends with one comparable pass/fail artifact and a clear next action instead of scattered evaluator outputs

### B -> A
- `Before:` Codexter has specialized evaluators, but no canonical round-ending scorecard shape or normalized thresholding across them
- `After:` Codexter has one documented evaluator scorecard contract with shared categories, thresholds, pass/fail semantics, and required follow-up fields that each evaluator can map into
- `Outcome:` the planner -> builder -> evaluator loop gets a measurable stopping rule that stays compatible with existing evaluator specialization

### Delta
- `Touch:` evaluator-facing docs/contracts, any shared report template/example needed to make the schema concrete, and integration notes for `qa-tester`, `visual-qa`, and `code-review`
- `Keep:` specialized roles and their separate remits
- `Change:` add one normalized scorecard schema covering category scores, thresholds, pass/fail, failure reasons, and next required action
- `Delete/Avoid:` avoid merging evaluator prompts, avoid runtime automation, and avoid a rubric so heavy that small rounds become paperwork

### Core Flow
```pseudo
read TASK-0002 ticket metadata contract and change proposal
define one evaluator-scorecard artifact/report shape
set required categories:
  functionality, ux_visual_quality, code_quality,
  evidence_completeness, acceptance_criteria_coverage
define per-category fields:
  score, threshold, pass_fail, failure_reasons, next_required_action
define overall round pass/fail semantics from category thresholds
map qa-tester, visual-qa, and code-review outputs into the shared shape
document where the scorecard lives in the ticket flow and how failed rounds write follow-up action
```

### Proof
- `P1:` the contract explicitly covers the five categories named in the 2026-04-02 change proposal, each with score, threshold, pass/fail, failure reasons, and next required action
- `P2:` a reviewer can take one hypothetical round and see how `qa-tester`, `visual-qa`, and `code-review` would all write into the same final report shape without collapsing into one role
- `P3:` the ticket stays one-commit because it defines only the schema/report contract and adoption notes, not evaluator runtime automation
- `Risk:` overspecifying the rubric before a real round exercises it, or underspecifying it so evaluators still drift
- `Rollback:` remove the shared scorecard contract/template and continue using independent evaluator outputs until a smaller rubric lands

### Plan Review
- `Refs:` `/Users/kenjipcx/coding-harness/Codexter/tickets/building/TASK-0002-codexter-ticket-metadata-foundation.md`, `/Users/kenjipcx/coding-harness/Codexter/docs/research/web-research/2026-04-02_codexter-change-proposal.md`, `/Users/kenjipcx/coding-harness/Codexter/AGENTS.md`, `/Users/kenjipcx/coding-harness/Codexter/skills/tech-impl-plan/SKILL.md`
- `Scope:` pass; this commit is contract-only and does not hide evaluator automation, telemetry, or orchestration work
- `Proof:` pass; success is observable by inspecting the schema, categories, thresholds, and evaluator mapping notes
- `Guardrails:` pass; preserves evaluator specialization, ticket-first workflow, and approval-first planning
- `Fixes:` tightened `Touch` to docs/contracts/templates only, made the scorecard fields explicit, and added the ticket move/board-state path

### Delegation
- `Need:` `Not needed`
- `Why:` this is a compact docs/contract planning slice with enough local repo context already available
- `Artifact:` none

### Ask
- `Ready: yes`
- `Next:` on approval, implement the shared evaluator scorecard contract and template, then let the first planner -> builder -> evaluator workflow emit it

### Ticket Move
- `Now:` `tickets/review/`
- `On approval:` move to `tickets/building/`
- `Follow-ups:` none required if this remains contract-only; create a new ticket only if evaluator runtime wiring or artifact-path changes spill past one commit
- `Blocked in building?:` `no`

## Acceptance Criteria
- [ ] AC-1: a shared evaluator report schema exists with category scores, thresholds, pass/fail, and next action
- [ ] AC-2: the schema explicitly covers functionality, UX/visual quality, code quality, evidence completeness, and acceptance coverage
- [ ] AC-3: existing evaluator roles can adopt it without losing specialization
- [ ] AC-4: the ticket's implementation slice remains one commit and stops short of evaluator automation

## Working Notes
- This ticket depends on the locked `TASK-0002` metadata dialect so any evaluator artifact points at one canonical next step and one canonical verification summary field.

## Implementation Notes
- Touched areas: evaluator-facing docs/contracts/templates only
- Reused patterns: Codexter's file-based approval flow and existing evaluator/evidence doctrine
- Guardrails: keep the rubric minimal, preserve separate evaluator roles, and avoid hidden runtime coupling in this slice

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [ ] QA / manual verification

## Blockers
- none

## Handoff
- Current state: plan is review-ready and waiting for approval.
- Resume from: this ticket plus the `TASK-0002` contract and the evaluator references named in Plan Review.

## Writeback
- Update this ticket as work progresses.
- Move the ticket when its board state changes. Do not update `tickets/INDEX.md` in this planning pass.
