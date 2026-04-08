---
ticket_id: TASK-0032
title: strengthen anti-self-agreement review loop
phase: planning
status: review
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: true
created_at: 2026-04-08T01:54:29Z
updated_at: 2026-04-08T01:54:29Z
next_action: review and approve the refined Ralph-judge hardening plan before implementation starts
last_verification: ralplan pass completed with architect and critic review; plan narrowed to the live Ralph judge path with a single canonical Review Packet contract
linked_docs:
  - docs/specs/harness-techniques.md
  - docs/specs/review-gates.md
  - docs/specs/orchestrator-subagent-loop.md
  - tickets/README.md
---

# TASK-0032: strengthen anti-self-agreement review loop

## Summary
Harden the current review loop so the system is less likely to praise its own work, approve weak evidence, or stop after shallow QA.

## Scope
- In: stronger reviewer/evidence-check skepticism, stricter evidence thresholds, and a sharper repeat path when proof is weak
- Out: multi-ticket runtime or dispatcher work

## Plan

### Pitch
- `Req:` harden the live Ralph completion path so weak, contradictory, stale, or untraceable proof cannot pass as complete
- `Bet:` make the Ralph judge consume one canonical structured `Review Packet` plus existing checklist proof instead of relying on optimistic prose or a second schema
- `Win:` same-ticket repeats happen for bad proof automatically, and completion requires both checklist completeness and a passing review/evidence gate

### B -> A
- `Before:` the live Ralph judge in `bin/stop_hook.py` mainly relies on `RALPH_RESULT` plus acceptance/evidence checkboxes, while the broader review surfaces already describe stronger evidence-quality concepts
- `After:` the Ralph judge reads a minimal deterministic `Review Packet` from the ticket, applies explicit hard-fail semantics, and only allows completion when both checklist proof and packet gates pass
- `Outcome:` the highest-leverage false-pass seam is hardened without redesigning the entire review stack

### Delta
- `Touch:` `tickets/templates/ticket.md`, `tickets/README.md`, `skills/review/SKILL.md`, `skills/review/references/review-rubric-index.md`, `docs/specs/review-gates.md`, `docs/specs/ralph-judge-verdict.schema.json`, `bin/stop_hook.py`, `experiments/run_ralph_smoke_evals.py`
- `Keep:` builder / reviewer / QA / evidence-check role separation and the broader `review` skill as the rich review surface
- `Change:` make the live Ralph judge consume a minimal canonical `Review Packet` projection with explicit precedence and hard-fail semantics
- `Delete/Avoid:` adding a second stop-hook-only evidence schema or broadening this ticket into a full review-system rewrite

### Core Flow
```pseudo
parse selected ticket
read acceptance/evidence checklist gaps
read minimal Review Packet fields from the ticket body
if blockers exist:
  block
if Review Packet is missing or malformed:
  repeat_ralph
if Review Packet says evidence is weak, contradictory, stale, or untraceable:
  repeat_ralph
if acceptance/evidence checklists still have gaps:
  repeat_ralph
otherwise:
  allow advance/complete path
```

### Proof
- `P1:` hermetic judge fixtures force `repeat_ralph` for missing packet, malformed packet, stale packet, contradictory packet, and low-traceability packet cases
- `P2:` a completion path only succeeds when checklist proof and `Review Packet` hard gates both pass
- `Risk:` contract sprawl or a second source of truth for review/evidence
- `Rollback:` keep the packet minimal and treat it as the single structured projection the Ralph judge consumes

### Plan Review
- `Refs:` OpenAI evaluator/invariant emphasis, Anthropic hard evaluator thresholds, Cursor role separation, `review-gates.md`, `orchestrator-subagent-loop.md`, `skills/review`, `tickets/README.md`, `bin/stop_hook.py`
- `Scope:` the live Ralph judge path plus the ticket/review contract surfaces it consumes; not a whole-stack review redesign
- `Proof:` hermetic machine-readable fixture assertions in `experiments/run_ralph_smoke_evals.py`
- `Guardrails:` do not create a second review schema; do not let the thin stop-hook reviewer become authoritative for completion
- `Fixes:` architect review narrowed the seam and removed the extra-schema idea; critic review forced explicit packet fields, precedence rules, and fixture coverage

### Delegation
- `Need:` yes
- `Why:` architect and critic review were used to harden the plan before approval
- `Artifact:` architect feedback on seam selection and source-of-truth design; critic feedback on packet contract, precedence, and proof coverage

### Ask
- `Ready: yes`
- `Next:` move to building and implement the minimal `Review Packet` contract plus Ralph-judge hard-fail rules

### Ticket Move
- `Now:` `status: review`, `phase: planning`
- `On approval:` set `status: building` and implement the judge-specific contract + fixture pass
- `Follow-ups:` may split broader `review` skill cleanup from the judge slice if the contract alignment grows beyond one commit
- `Blocked in building?:` no

## Acceptance Criteria
- [ ] AC-1: the ticket template and canonical ticket docs define a minimal machine-readable `Review Packet` with required fields: `reviewed_at`, `overall_verdict`, `rerun_required`, `blocking_findings`, `next_action`, `evidence_quality`, and `integration_readiness`
- [ ] AC-2: the live Ralph judge path in `bin/stop_hook.py` forces `repeat_ralph` when the `Review Packet` is missing, malformed, stale, contradictory, weak, or untraceable, even if checkboxes look complete
- [ ] AC-3: the live Ralph judge only allows `complete_ticket` when both checklist proof and `Review Packet` hard gates pass
- [ ] AC-4: hermetic smoke fixtures assert the machine-readable verdicts for missing packet, malformed packet, stale packet, contradictory packet, and low-traceability packet cases

## Working Notes
- Main weakness: the system still agrees with itself too easily.
- Blog technique mapping: Anthropic’s hard evaluator thresholds, Cursor’s clearer role separation, OpenAI’s emphasis on turning guardrails into real checks.
- The thin stop-hook `reviewer` role remains a routing fallback for ambiguous/no-`RALPH_RESULT` cases; this ticket should not make it a second independent source of completion truth.
- The canonical source of truth for this slice is one minimal `Review Packet` projection shared across ticket/spec/review surfaces, not a new stop-hook-only schema.

## Implementation Notes
- Touched areas: ticket/review contract docs, Ralph judge parsing/precedence, verdict schema, hermetic replay fixtures
- Reused patterns: current `review-gates` model, ticket-first progress surface, existing Ralph smoke-eval harness
- Guardrails: avoid adding a new hidden orchestrator, hidden reviewer role, or duplicate evidence schema

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [ ] QA / manual verification

## Review Packet
- `reviewed_at:` 2026-04-08 02:00 +0100
- `rubrics_used:` implementation-plan,evidence-quality,spec-contract
- `overall_score:` 96
- `overall_verdict:` pass
- `rerun_required:` false
- `blocking_findings:` none
- `next_action:` hold in review until approved for implementation of the judge-focused slice

## Blockers
- none

## Handoff
- Current state: `ralplan` pass completed; the ticket now has an approval-ready, judge-specific implementation plan.
- Resume from: `bin/stop_hook.py`, `tickets/templates/ticket.md`, `tickets/README.md`, `docs/specs/review-gates.md`, and `experiments/run_ralph_smoke_evals.py`

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
