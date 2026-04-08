---
ticket_id: TASK-0025
title: add openai harness findings
phase: complete
status: done
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-08T01:48:34Z
updated_at: 2026-04-08T01:48:34Z
next_action: archived; use the updated techniques inventory for cross-source harness prioritization
last_verification: manual review passed; verified the techniques doc and history writeback with git diff --check clean on the changed files
linked_docs:
  - docs/specs/harness-techniques.md
  - docs/HISTORY.md
---

# TASK-0025: add openai harness findings

## Summary
Read OpenAI's harness engineering article, compare it to the Anthropic and Cursor ideas already reflected in the repo, and update the harness techniques inventory with any additional overlapping techniques or clear deltas.

## Scope
- In: article comparison, techniques inventory update, history writeback
- Out: runtime behavior changes or new harness features

## Plan

### Pitch
- `Req:` fold the OpenAI article into the current harness-techniques view and identify the highest-ROI next features
- `Bet:` the new value is in surfacing repo legibility, mechanical invariant enforcement, and application legibility as explicit techniques
- `Win:` the techniques doc better reflects the shared patterns across OpenAI, Anthropic, and Cursor and highlights the best next bets

### B -> A
- `Before:` the techniques inventory reflects prior repo truth and earlier articles, but not the OpenAI harness article explicitly
- `After:` the inventory includes OpenAI-overlapping techniques already present in Codexter plus clearly labeled new deltas
- `Outcome:` cross-source convergence is documented in one canonical place

### Delta
- `Touch:` `docs/specs/harness-techniques.md`, `docs/HISTORY.md`, this ticket
- `Keep:` current implemented/proposed separation
- `Change:` coverage of repo legibility, docs-as-system-of-record, application legibility, and mechanical invariant enforcement
- `Delete/Avoid:` overclaiming OpenAI-only patterns as already implemented here

### Core Flow
```pseudo
read the openai article
compare it to current codexter docs and earlier anthropic/cursor findings
update the techniques inventory with grounded overlaps and deltas
review the docs and archive the ticket
```

### Proof
- `P1:` new rows or refinements in the techniques inventory map to real repo surfaces or clear proposed deltas
- `P2:` final synthesis can rank the highest-ROI next features from the article set without blurring current and future behavior
- `Risk:` article ideas get added as vague aspiration instead of concrete techniques
- `Rollback:` trim back to only grounded overlaps and explicit deltas

### Plan Review
- `Refs:` OpenAI harness article, prior Anthropic/Cursor notes, `docs/specs/harness-techniques.md`, `README.md`, `AGENTS.md`, `skills/*`, `hooks.json`, `bin/stop_hook.py`
- `Scope:` docs-only update and synthesis
- `Proof:` manual review and `git diff --check`
- `Guardrails:` no undocumented behavior claims; keep implemented/proposed explicit
- `Fixes:` encode only the useful overlaps

### Delegation
- `Need:` Not needed
- `Why:` bounded doc synthesis
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` update docs, review, archive

### Ticket Move
- `Now:` `status: building`, `phase: building`
- `On approval:` n/a; user directly requested the change
- `Follow-ups:` none required for this doc slice
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: the techniques inventory includes overlapping OpenAI-described techniques that are already live in Codexter
- [x] AC-2: the techniques inventory includes clearly labeled proposed deltas for OpenAI techniques not yet live here
- [x] AC-3: history writeback records the doc update

## Working Notes
- The user also wants a recommendation on highest-ROI features across OpenAI, Anthropic, and Cursor.
- Treat “repo legibility” as the main new theme from the OpenAI article.

## Implementation Notes
- Touched areas: `docs/specs/`, `docs/HISTORY.md`, `tickets/`
- Reused patterns: canonical techniques inventory, docs-only ticket closeout
- Guardrails: keep source synthesis concise and grounded

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Validation details:
  - reviewed OpenAI's harness engineering article against the current Codexter techniques inventory and repo surfaces
  - added implemented overlaps for short `AGENTS.md` as map, docs as system of record, progressive disclosure, and agent-legible UI validation
  - added proposed deltas for mechanical doc freshness checks, recurring doc-gardening, mechanical architecture/taste invariants, and agent-visible observability
  - ran `git diff --check -- docs/specs/harness-techniques.md docs/HISTORY.md tickets/archive/TASK-0025-add-openai-harness-findings.md`
  - review pass: `rubrics_used=[implementation-plan,evidence-quality]`, `overall_score=95`, `verdict=pass`, `rerun_required=false`

## Blockers
- none

## Handoff
- Current state: the techniques inventory now reflects the OpenAI article overlap and deltas.
- Resume from: `docs/specs/harness-techniques.md` when re-ranking future harness experiments.

## Writeback
- Update this ticket as work progresses.
- When the docs and review pass are complete, archive the ticket.
