---
ticket_id: TASK-0095
title: tighten bootstrap to ticket testability propagation
phase: complete
status: done
owner: codex
claimed_by:
priority: medium
depends_on: []
blocked_by: []
ready: true
approval_required: false
requires_qa: false
requires_demo: false
created_at: 2026-04-24T20:25:00Z
updated_at: 2026-04-24T20:35:00Z
next_action: archived; use spec-to-ticket to carry bootstrap testability defaults into ticket contracts and qa/cookbook seeds
last_verification: `python3 tickets/scripts/check_ticket_metadata.py` and `git diff --check`
linked_docs:
  - skills/spec-to-ticket/SKILL.md
  - tickets/templates/ticket.md
  - skills/init-project/references/BOOTSTRAP_BRIEF_TEMPLATE.md
  - qa/cookbook/TEMPLATE.md
---

# TASK-0095: tighten bootstrap to ticket testability propagation

## Summary
Bootstrap now captures agent-experience/testability, but the planning flow still leaves too much manual carry-forward work when the first UI-bearing ticket is written. This ticket tightens the loop by teaching `spec-to-ticket` and the canonical ticket docs to consume bootstrap testability defaults and seed matching `qa/cookbook` workflow docs when relevant.

## Scope
- In:
  - update `spec-to-ticket` to treat `docs/bootstrap-brief.md` agent-experience/testability as an input when no richer testability brief exists
  - update the canonical ticket docs/template so UI-bearing tickets have an explicit place for `Agent Contract` and `Evidence Checklist`
  - define when `spec-to-ticket` should create or update a matching `qa/cookbook/<workflow>.md`
- Out:
  - changing runtime behavior or adding new executable tooling
  - altering `deep-interview` or `agent-testability-plan`

## Plan
- `Change:` patch `skills/spec-to-ticket/*`, `tickets/templates/ticket.md`, and `tickets/README.md` so bootstrap testability defaults propagate into ticket contracts and a matching QA cookbook seed
- `Why:` bootstrap now asks the right question, but downstream ticket planning still depends on memory instead of a documented carry-forward rule
- `Before -> After:`
  - `Before:` bootstrap captures agent-experience/testability, but `spec-to-ticket` only talks about `Agent Testability Brief` and does not mention bootstrap defaults or cookbook seeding
  - `After:` ticketization consumes bootstrap defaults when needed, UI-bearing tickets have explicit `Agent Contract` / `Evidence Checklist` sections, and `qa/cookbook` seeding becomes part of the planning contract
- `Touch:` `skills/spec-to-ticket/*`, `tickets/templates/ticket.md`, `tickets/README.md`, `README.md`, `docs/MEMORY.md`, `docs/HISTORY.md`
- `Inspect:` `skills/spec-to-ticket/SKILL.md`, `skills/spec-to-ticket/references/*`, `tickets/templates/ticket.md`, `tickets/README.md`, `skills/init-project/references/BOOTSTRAP_BRIEF_TEMPLATE.md`, `qa/cookbook/TEMPLATE.md`
- `Signature delta:` none
- `Type Sketch:` none
- `Typed flow example:` none
- `Recommendation:` keep `init-project` as the capture step and make `spec-to-ticket` the propagation step, with canonical ticket docs showing where the resulting testability contract lives
- `Blast radius:` planning doctrine, ticket shape, and future UI/game ticket generation
- `Risks:` overfitting the ticket template for non-UI work; making cookbook seeding sound mandatory even when the repo has no `qa/` surface

## Acceptance Criteria
- [x] AC-1: `spec-to-ticket` explicitly consumes bootstrap `Agent Experience / Testability` defaults when no richer testability brief exists
- [x] AC-2: canonical ticket docs and template include optional `Agent Contract` and `Evidence Checklist` sections for UI-bearing work
- [x] AC-3: the planning contract says when to create or update a matching `qa/cookbook/<workflow>.md` entry

## Verification
- `Tests:` `python3 tickets/scripts/check_ticket_metadata.py`; `git diff --check`
- `Manual checks:` inspect the updated spec-to-ticket contract and ticket docs for a consistent bootstrap -> ticket -> cookbook flow
- `Evidence required:` linked ticket plus review artifact covering the updated planning surfaces
- `Artifacts path:` `tickets/artifacts/TASK-0095/`

## Evidence
- `Artifacts:`
  - [review.md](/Users/kenjipcx/coding-harness/Codexter/tickets/artifacts/TASK-0095/review/2026-04-24_203500_propagation-review/review.md)
  - [review.json](/Users/kenjipcx/coding-harness/Codexter/tickets/artifacts/TASK-0095/review/2026-04-24_203500_propagation-review/review.json)
- `Commands:`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `git diff --check`
- `Result summary:` tightened the loop by making `spec-to-ticket` consume bootstrap testability defaults, extending canonical ticket docs with `Agent Contract` and `Evidence Checklist`, and requiring matching `qa/cookbook` workflow seeds when the repo has that surface

## Blockers
- none
