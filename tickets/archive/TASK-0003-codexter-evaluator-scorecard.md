---
ticket_id: TASK-0003
title: define review gates and evaluator scorecard
phase: complete
status: done
owner: codex
priority: medium
depends_on:
  - TASK-0002
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-07T00:00:00Z
next_action: archived; reopen only if review output must be written into ticket/progress-file templates instead of remaining a contract-level requirement
last_verification: review-gates contract is documented in docs/specs and reflected in the code-review skill + reviewer agent with no remaining active implementation work in this slice
linked_docs:
  - docs/specs/review-gates.md
  - docs/specs/spec-first-execution-loop.md
  - skills/code-review/SKILL.md
  - agents/code-reviewer.toml
---

# TASK-0003: define review gates and evaluator scorecard

## Summary
Define the review-gate contract for the spec-first execution loop: separate QA evidence from implementation review, then normalize both into one comparable scorecard that the Stop hook can sanity-check.

## Scope
- In: review rubric categories, QA evidence expectations, report shape, pass/fail semantics, and how review/QA outputs map into the final stop decision
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
- `Refs:` `/Users/kenjipcx/coding-harness/Codexter/tickets/TASK-0002-codexter-ticket-metadata-foundation.md`, `/Users/kenjipcx/coding-harness/Codexter/docs/research/web-research/2026-04-02_codexter-change-proposal.md`, `/Users/kenjipcx/coding-harness/Codexter/AGENTS.md`, `/Users/kenjipcx/coding-harness/Codexter/skills/tech-impl-plan/SKILL.md`
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
- `Next:` implement the contract and make it the default review gate for spec-first feature work packages

### Ticket Move
- `Now:` `tickets/`
- `On approval:` move to `tickets/`
- `Follow-ups:` none required if this remains contract-only; create a new ticket only if evaluator runtime wiring or artifact-path changes spill past one commit
- `Blocked in building?:` `no`

## Acceptance Criteria
- [x] AC-1: one review-gate contract exists that explicitly separates QA evidence collection from implementation review
- [x] AC-2: the shared scorecard covers at least functionality correctness, regression safety, code quality, and evidence adequacy
- [x] AC-3: the scorecard says how QA/review outputs feed the Stop hook without collapsing those roles into one
- [x] AC-4: the ticket remains contract-only and does not yet implement evaluator automation

## Working Notes
- This ticket depends on the locked `TASK-0002` metadata dialect so any evaluator artifact points at one canonical next step and one canonical verification summary field.

## Implementation Notes
- Touched areas: evaluator-facing docs/contracts/templates only
- Reused patterns: Codexter's file-based approval flow and existing evaluator/evidence doctrine
- Guardrails: keep the rubric minimal, preserve separate evaluator roles, and avoid hidden runtime coupling in this slice

## Evidence
- [ ] Tests
- [x] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Validation details:
  - `python3 -m py_compile bin/check_ticket_metadata.py`
  - reviewed `docs/specs/review-gates.md`
  - reviewed `skills/code-review/SKILL.md`
  - reviewed `agents/code-reviewer.toml`
  - reviewed rubric references under `skills/code-review/references/`

## Blockers
- none

## Handoff
- Current state: the review-gates contract is now canonicalized in docs/specs and reflected in the review skill plus reviewer agent.
- Resume from: this ticket, `docs/specs/review-gates.md`, and the next wiring slice if review outputs need to be emitted into ticket/progress-file templates.

## Writeback
- Update this ticket as work progresses.
- Update `status` and `phase` in frontmatter when queue state changes.
