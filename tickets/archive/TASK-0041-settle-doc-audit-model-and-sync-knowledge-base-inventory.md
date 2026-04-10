---
ticket_id: TASK-0041
title: settle doc audit model and sync knowledge-base inventory
phase: complete
status: done
owner: codex
priority: medium
depends_on:
  - TASK-0044
blocked_by: []
ready: false
approval_required: false
created_at: 2026-04-08T19:29:01Z
updated_at: 2026-04-09T17:07:10+0100
next_action: none; ticket completed after landing the hybrid doc-governance workflow and syncing the knowledge-base inventory
last_verification: python3 tickets/scripts/check_ticket_metadata.py; python3 bin/check_doc_parity.py; python3 -m unittest bin/test_doc_parity.py; git diff --check
linked_docs:
  - README.md
  - ARCHITECTURE.md
  - docs/specs/README.md
  - docs/specs/harness-techniques.md
  - tickets/archive/TASK-0029-add-doc-freshness-and-gardening-loop.md
  - tickets/archive/TASK-0044-add-architecture-map-and-canonical-doc-index.md
---

# TASK-0041: settle doc audit model and sync knowledge-base inventory

## Summary
Settle the long-term doc-audit model for Codexter and sync the canonical knowledge-base inventory so current docs stop disagreeing about what is already implemented.

## Scope
- In:
  - deciding whether canonical doc audits should stay mechanical, move to `codex exec`, or use a hybrid model
  - syncing `docs/specs/harness-techniques.md` and nearby canonical surfaces with what `TASK-0029` and the new architecture map actually establish
  - defining the operator workflow for keeping the knowledge base fresh after the architecture/doc-map cleanup lands
- Out:
  - broad deletion of unrelated scripts
  - removal of structural validators such as ticket metadata checks
  - full docs taxonomy redesign

## Plan

### Pitch
- `Req:` settle how Codexter should audit flexible docs and fix the current mismatch where the knowledge-base inventory still understates what has already landed
- `Bet:` one explicit doc-governance pass can resolve both the audit mechanism question and the known inventory drift without mixing in broader architecture redesign
- `Win:` the repo's “docs as system of record” claim becomes more trustworthy because the audit workflow and the inventory agree with repo reality

### Recommendation
- `Best:` use a hybrid governance model: keep only tiny structural validators where wording-independence is essential, but move narrative doc-audit judgment to a documented `codex exec` workflow and sync the canonical inventory around the same policy
- `Why:` this keeps the user's preference for prompt-driven narrative doc audits while preserving the small amount of deterministic protection that genuinely structural surfaces still need
- `Tradeoff accepted:` hybrid governance is less ideologically clean than “all prompts” or “all scripts,” but it better matches the mixed nature of the current doc surfaces

### B -> A
- `Before:` doc parity is enforced by `bin/check_doc_parity.py` with fixed required/forbidden strings, while the techniques inventory still labels some landed doc-governance work as merely proposed
- `After:` the repo has an explicit doc-audit policy, the inventory reflects what is actually implemented, and the canonical surfaces know which checks are structural versus narrative
- `Outcome:` doc maintenance becomes both more trustworthy and easier to understand

### Delta
- `Touch:` `bin/check_doc_parity.py`, `bin/test_doc_parity.py`, `docs/specs/harness-techniques.md`, `docs/specs/README.md`, `README.md`, and any replacement prompt/workflow docs
- `Keep:` ticket metadata validation and any genuinely structural doc checks that remain justified
- `Change:` settle the audit policy and sync the knowledge-base inventory with current reality
- `Delete/Avoid:` growing a mini markdown-lint framework for flexible docs or leaving the repo in a half-script half-prompt limbo with contradictory docs

### Core Flow
```pseudo
read the canonical doc surfaces
compare public claims against repo truth, TASK-0029, and the architecture-map output
decide which checks are structural versus narrative
document the chosen audit workflow
sync the techniques inventory and nearby canonical docs
rerun the chosen audit path as a confirmation pass
```

### Proof
- `P1:` the resulting doc-governance workflow clearly explains when to use deterministic checks and when to use prompt-driven audits
- `P2:` `docs/specs/harness-techniques.md` no longer claims freshness/gardening work is merely proposed if the repo has already landed it
- `Risk:` the policy stays ambiguous and merely renames the current confusion
- `Rollback:` reduce the scope to one explicit policy note plus the minimum doc sync needed to remove contradictions

### Plan Review
- `Refs:` `TASK-0029`, `TASK-0044`, `docs/specs/harness-techniques.md`, `docs/specs/README.md`, `docs/TROUBLES.md`, current `bin/check_doc_parity.py`
- `Scope:` doc-governance and inventory sync only
- `Proof:` compare the current script-based path against the proposed prompt or hybrid path, then remove inventory contradictions
- `Guardrails:` do not conflate narrative docs with machine-readable ticket-state protection
- `Fixes:` keep the slice centered on knowledge-base governance, not a generalized anti-script position

### Options Appendix
- `Option 1:` keep the Python validator and tune its rules
- `Pros:` deterministic; already implemented; easy to run in CI
- `Cons:` brittle for flexible docs; stores low-leverage code; needs edits for wording shifts
- `Why not chosen:` it directly conflicts with the user’s preference for prompt-driven doc checks
- `Option 2:` replace it with a codex-exec audit workflow
- `Pros:` flexible; closer to how docs are actually judged; reduces one-off scripts
- `Cons:` less deterministic; quality depends on prompt clarity
- `Why not chosen:` strong option, but it may over-rotate away from still-useful structural checks
- `Option 3:` hybrid approach with codex-exec primary and a tiny structural fallback
- `Pros:` preserves only the most valuable deterministic checks; fits the mixed nature of current docs; easier to explain in `ARCHITECTURE.md`
- `Cons:` still stores some program logic; boundaries must be kept crisp
- `Why not chosen:` recommended

### Delegation
- `Need:` Not needed
- `Why:` planning slice only
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` approve the doc-governance direction, then implement the chosen audit model and sync the canonical inventory after `TASK-0044`

### Ticket Move
- `Now:` `status: done`, `phase: complete`, archived under `tickets/archive/`
- `On approval:` approved on 2026-04-09 and implemented after `TASK-0044` landed in the same batch
- `Follow-ups:` may split prompt design from script removal if the governance slice proves broader than expected
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: the ticket defines when doc checks should use prompt-driven audits versus stored structural validators
- [x] AC-2: the resulting workflow shows one concrete stale-doc example and how the chosen audit path catches it
- [x] AC-3: `docs/specs/harness-techniques.md` and nearby canonical docs are synced with the actual status of freshness/gardening work
- [x] AC-4: any remaining mechanical check is justified as structural rather than narrative
- [x] AC-5: the resulting governance story is easier to understand than the current script-only parity setup

## Working Notes
- User take is explicit: docs are flexible; prefer prompt-driven `codex exec` over stored programs for this class of maintenance task.
- This is a direct follow-up to TASK-0029 rather than a rejection of all validators.
- The current techniques inventory still marks freshness/gardening checks as proposed, which is now a concrete trust break this ticket should resolve.
- This ticket is the doc-governance leg of the three-ticket batch alongside `TASK-0044` and `TASK-0045`.
- Result: added `docs/specs/doc-governance.md`, narrowed `bin/check_doc_parity.py` to structural entrypoint checks, and synced `harness-techniques.md` so implemented versus proposed status is no longer contradictory.

## Implementation Notes
- Touched areas: `docs/specs/doc-governance.md`, `bin/check_doc_parity.py`, `bin/test_doc_parity.py`, `docs/specs/harness-techniques.md`, `docs/specs/README.md`, `README.md`
- Reused patterns: ticket-first change tracking and docs writeback
- Guardrails: do not conflate narrative doc drift with machine-readable metadata drift

## Evidence
- [x] Tests
- [x] Typecheck
- [x] Lint
- [x] QA / manual verification

- `python3 tickets/scripts/check_ticket_metadata.py`
- `python3 bin/check_doc_parity.py`
- `python3 -m unittest bin/test_doc_parity.py`
- `python3 -m py_compile bin/check_doc_parity.py bin/test_doc_parity.py`
- `git diff --check`
- Manual review of `docs/specs/doc-governance.md`, `docs/specs/harness-techniques.md`, `docs/specs/README.md`, and `bin/check_doc_parity.py`

## Review Packet
- `reviewed_at:` 2026-04-09 17:07 +0100
- `rubrics_used:` implementation-plan,spec-contract
- `overall_score:` 4.6
- `overall_threshold:` 4.0
- `overall_verdict:` pass
- `rerun_required:` false
- `evidence_quality:` pass
- `integration_readiness:` pass
- `traceability:` pass
- `freshness:` pass
- `hard_gate_failures:` []
- `blocking_findings:` []
- `next_action:` none; archive the completed ticket after writeback

## Blockers
- none

## Handoff
- Current state: complete and archived. Codexter now uses a hybrid doc-governance model: structural entrypoint checks stay mechanical, while narrative drift is audited through the documented `codex exec` workflow.
- Resume from: `docs/specs/doc-governance.md` when the audit policy or canonical doc set changes

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
