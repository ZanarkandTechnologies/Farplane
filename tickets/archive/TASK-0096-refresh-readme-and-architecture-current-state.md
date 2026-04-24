---
ticket_id: TASK-0096
title: refresh readme and architecture current state
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
created_at: 2026-04-24T20:50:00Z
updated_at: 2026-04-24T20:58:00Z
next_action: archived; top-level docs now match the current harness contract more closely
last_verification: `python3 tickets/scripts/check_ticket_metadata.py`; `git diff --check -- README.md ARCHITECTURE.md docs/HISTORY.md tickets/TASK-0096-refresh-readme-and-architecture-current-state.md`
linked_docs:
  - README.md
  - ARCHITECTURE.md
  - tickets/templates/ticket.md
  - tickets/README.md
---

# TASK-0096: refresh readme and architecture current state

## Summary
The top-level docs have drifted behind the live harness contract. This ticket updates `README.md` and `ARCHITECTURE.md` so they stop claiming already-shipped planning capabilities are still missing and so they describe the current bootstrap, QA, and artifact-first ticket surfaces accurately.

## Scope
- In:
  - remove stale current-state claims from `README.md`
  - align `ARCHITECTURE.md` with the current ticket/evidence/QA contract
  - refresh the top-level flow description where it now omits visible bootstrap or QA surfaces
- Out:
  - changing lower-level specs or skill contracts
  - broad README restructuring unrelated to the stale/current-state drift

## Plan
- `Change:` patch the two top-level docs to match the current harness state and live canonical surfaces
- `Why:` top-level orientation docs should not contradict the shipped repo or hide now-important surfaces like bootstrap testability and `qa/`
- `Before -> After:`
  - `Before:` README still says file-map-first planning is missing, and architecture still describes the ticket template in older review-packet terms
  - `After:` both docs reflect file-map-first planning as live, describe artifact-first ticket proof, and show bootstrap/QA surfaces where they now matter
- `Touch:` `README.md`, `ARCHITECTURE.md`, `docs/HISTORY.md`
- `Inspect:` `tickets/templates/ticket.md`, `tickets/README.md`, `skills/impl-plan/SKILL.md`, `qa/README.md`
- `Signature delta:` none
- `Type Sketch:` none
- `Typed flow example:` none
- `Recommendation:` keep the changes narrow and factual so top-level docs stay map-like
- `Blast radius:` operator orientation, public repo story, and future doc-gardening audits
- `Risks:` over-expanding top-level docs instead of correcting only the stale claims

## Acceptance Criteria
- [x] AC-1: `README.md` no longer claims already-shipped file-map-first planning/signature-delta capability is missing
- [x] AC-2: `ARCHITECTURE.md` describes the current artifact-first ticket contract rather than older review-packet wording
- [x] AC-3: the top-level flow and surfaces mention bootstrap/QA/testability where it materially changes repo orientation

## Verification
- `Tests:` `python3 tickets/scripts/check_ticket_metadata.py`; `git diff --check`
- `Manual checks:` re-read `README.md` and `ARCHITECTURE.md` against `tickets/templates/ticket.md`, `tickets/README.md`, and `qa/README.md`
- `Evidence required:` linked ticket plus review artifact covering the changed docs
- `Artifacts path:` `tickets/artifacts/TASK-0096/`

## Evidence
- `Artifacts:`
  - [review.md](/Users/kenjipcx/coding-harness/Codexter/tickets/artifacts/TASK-0096/review/2026-04-24_205800_doc-review/review.md)
  - [review.json](/Users/kenjipcx/coding-harness/Codexter/tickets/artifacts/TASK-0096/review/2026-04-24_205800_doc-review/review.json)
- `Commands:`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `git diff --check -- README.md ARCHITECTURE.md docs/HISTORY.md tickets/TASK-0096-refresh-readme-and-architecture-current-state.md`
- `Result summary:` refreshed the top-level repo docs to remove stale capability claims, describe artifact-first tickets accurately, and surface bootstrap/qa guidance where it now matters

## Blockers
- none
