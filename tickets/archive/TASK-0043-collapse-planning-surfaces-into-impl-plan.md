---
ticket_id: TASK-0043
title: collapse planning surfaces into impl-plan
phase: complete
status: done
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: false
created_at: 2026-04-09T03:12:42Z
updated_at: 2026-04-09T03:25:19Z
next_action: none; ticket archived after the impl-plan cutover landed and verified cleanly
last_verification: python3 -m py_compile bin/stop_hook.py bin/user_turn.py bin/check_doc_parity.py bin/test_doc_parity.py skills/impl/scripts/tmux_helper.py experiments/run_ralph_smoke_evals.py; python3 -m unittest discover -s bin -p 'test_*.py'; python3 tickets/scripts/check_ticket_metadata.py; python3 bin/check_doc_parity.py; git diff --check; rg -n "\\bralplan\\b|\\btech-impl-plan\\b" AGENTS.md README.md bin docs/specs skills tickets/README.md tickets/templates/ticket.md experiments -g '!skills/impl-plan/**'
linked_docs:
  - AGENTS.md
  - README.md
  - docs/specs/harness-techniques.md
  - docs/specs/ralph-v2-direction.md
  - skills/impl-plan/SKILL.md
  - tickets/templates/ticket.md
---

# TASK-0043: collapse planning surfaces into impl-plan

## Summary
Merge `ralplan` and `tech-impl-plan` into one public planning surface named `impl-plan`.

## Scope
- In: public planner naming, merged planner skill contract, runtime planning mappings, and canonical repo docs/reference updates
- Out: collapsing `impl` and `ralph`, or broader discovery-surface changes

## Plan

### Pitch
- `Req:` remove the duplicate public planning surfaces because they effectively do the same job
- `Bet:` keep one planner named `impl-plan`, make consensus a mode of that planner, and hard-cut repo references to the new name
- `Win:` the repo stops teaching two overlapping planners and becomes easier to learn and operate

### Recommendation
- `Best:` merge into `impl-plan`, keep ticket planning only, and defer `impl`/`ralph` collapse to a separate follow-up
- `Why:` this fixes the current naming/flow confusion without expanding into execution-surface redesign in the same slice
- `Tradeoff accepted:` the cutover touches many docs and mappings at once, but avoids a lingering alias period

### B -> A
- `Before:` `ralplan` is the consensus planner, `tech-impl-plan` is the approval-first planner, and the repo documents both
- `After:` `impl-plan` is the only public planner; consensus becomes a mode inside that one surface
- `Outcome:` one public planning entrypoint, one planner story, less routing ambiguity

### Delta
- `Touch:` planning skill module, canonical docs, runtime mappings, handoff skill references, ticket/docs memory
- `Keep:` discovery surfaces before planning, `impl` as the execution orchestrator, `ralph` unchanged for now
- `Change:` planner naming, planner contract, repo references, and planning runtime enums/mappings
- `Delete/Avoid:` public `ralplan` and `tech-impl-plan` surfaces after the cutover

### Proof
- `P1:` no live canonical surface still describes both planners as current public options
- `P2:` runtime and hook mappings resolve planning work to `impl-plan`
- `Risk:` partial rename leaves the repo in a mixed planner state
- `Rollback:` restore the removed skill surface and prior naming only if the merged contract proves internally inconsistent

### Plan Review
- `Refs:` root `AGENTS.md`, `README.md`, `docs/specs/harness-techniques.md`, `docs/specs/ralph-v2-direction.md`, `skills/impl-plan/*`, `skills/impl/SKILL.md`, `skills/deep-interview/SKILL.md`, `bin/user_turn.py`, `bin/stop_hook.py`, `skills/impl/scripts/tmux_helper.py`
- `Scope:` one planner merge only; execution-surface collapse stays out of scope
- `Proof:` static reference sweep plus runtime/ticket validators
- `Guardrails:` no permanent aliases, no discovery-surface merge, no execution-behavior rewrite
- `Fixes:` keep consensus as a mode inside the merged planner instead of trying to preserve two planner names

### Delegation
- `Need:` Not needed
- `Why:` bounded repo-local rewrite
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` implement the merged planner module and update live references in one cutover

### Ticket Move
- `Now:` `status: done`, `phase: complete`, archived under `tickets/archive/`
- `On approval:` already approved by user request to implement
- `Follow-ups:` execution-surface collapse (`impl`/`ralph`) remains a separate ticket
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: a single public planning skill named `impl-plan` exists and encodes both approval-first planning and consensus-mode planning
- [x] AC-2: public `ralplan` and `tech-impl-plan` planner surfaces are removed from live repo docs and skill references
- [x] AC-3: runtime planning mappings and enums that previously emitted `ralplan` now emit `impl-plan`
- [x] AC-4: discovery and execution skills describe the merged planning surface consistently
- [x] AC-5: the repo explicitly defers `impl`/`ralph` collapse instead of half-merging it here

## Working Notes
- User decision: keep `impl-plan`, hard cutover, ticket-planning only, consensus as a mode, and merge execution later.
- This ticket supersedes planner-surface ambiguity without expanding into execution-surface consolidation.
- TASK-0042 was partially absorbed here and is archived as superseded after the shared planning-artifact work landed through `impl-plan`.

## Implementation Notes
- Touched areas: `skills/impl-plan/*`, `tickets/templates/ticket.md`, `tickets/README.md`, root `AGENTS.md`, `README.md`, runtime mappings under `bin/` and `skills/impl/scripts/tmux_helper.py`, canonical specs, `docs/HISTORY.md`, `docs/MEMORY.md`
- Reused patterns: ticket-first planning, consensus loop, approval-first plan structure
- Guardrails: no permanent alias layer and no mixed public planner story after the patch
- Result: the repo now teaches one public planner surface, while `impl` and `ralph` remain explicitly separate for a later follow-up

## Evidence
- [x] Tests
- [x] Typecheck
- [x] Lint
- [x] QA / manual verification

- `python3 -m py_compile bin/stop_hook.py bin/user_turn.py bin/check_doc_parity.py bin/test_doc_parity.py skills/impl/scripts/tmux_helper.py experiments/run_ralph_smoke_evals.py`
- `python3 -m unittest discover -s bin -p 'test_*.py'`
- `python3 tickets/scripts/check_ticket_metadata.py`
- `python3 bin/check_doc_parity.py`
- `git diff --check`
- `rg -n "\bralplan\b|\btech-impl-plan\b" AGENTS.md README.md bin docs/specs skills tickets/README.md tickets/templates/ticket.md experiments -g '!skills/impl-plan/**'`

## Review Packet
- `reviewed_at:` 2026-04-09 03:25 +0100
- `rubrics_used:` implementation-plan,code-quality,integration-readiness,evidence-quality
- `overall_score:` 4.8
- `overall_threshold:` 4.0
- `overall_verdict:` pass
- `rerun_required:` false
- `evidence_quality:` pass
- `integration_readiness:` pass
- `traceability:` pass
- `freshness:` pass
- `hard_gate_failures:` []
- `blocking_findings:` []
- `next_action:` none; archive the completed planner-merge ticket

## Blockers
- none

## Handoff
- Current state: complete and archived.
- Resume from: no resume required

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
