---
ticket_id: TASK-0108
title: add frontend guidelines review metric
phase: complete
status: done
owner: codex
claimed_by:
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: false
requires_qa: false
requires_demo: false
created_at: 2026-05-04T20:57:57Z
updated_at: 2026-05-04T20:57:57Z
next_action: none; implementation and review complete
last_verification: 2026-05-04T20:57:57Z validators and visible review pass
---

# TASK-0108: add frontend guidelines review metric

## Summary
Integrate `web-design-guidelines` into the frontend skill topology as a
source-fresh standards audit and expose it through `review` as a separate
`frontend-guidelines` score. This lets Codexter compare agent taste judgment
against external interface fundamentals instead of blending both into one vague
UI score.

## Scope
- In: `frontend-craft`, `web-design-guidelines`, `review` references, root
  frontend policy, memory/history.
- Out: rendered UI changes, hooks/runtime enforcement, committing unrelated
  Symphony or registry worktree changes.

## Acceptance Criteria
- [x] `frontend-craft` calls `web-design-guidelines` for changed UI source files.
- [x] `review` has a frontend reference that converts guideline findings into a
  `1.0`-to-`5.0` score.
- [x] `ui-quality` and `frontend-guidelines` remain separate scores.
- [x] `web-design-guidelines` remains source-fresh and does not vendor the
  upstream rule list.
- [x] Validators pass.

## Evidence
- `Artifacts:`
  - [review artifact](artifacts/review/2026-05-04-frontend-guidelines-review.json)
- `Commands:`
  - `python3 skills/skill-creator/scripts/quick_validate.py skills/frontend-craft` -> passed
  - `python3 skills/skill-creator/scripts/quick_validate.py skills/review` -> passed
  - `python3 skills/skill-creator/scripts/quick_validate.py skills/web-design-guidelines` -> passed
  - `python3 tickets/scripts/check_ticket_metadata.py` -> passed
  - `python3 bin/check_harness_invariants.py` -> passed
  - `python3 bin/check_doc_parity.py` -> passed
  - `git diff --check -- AGENTS.md docs/MEMORY.md docs/HISTORY.md skills/frontend-craft skills/review skills/web-design-guidelines` -> passed
- `Result summary:` Added the `frontend-guidelines` review metric, wired
  `frontend-craft` to run `web-design-guidelines`, made `web-design-guidelines`
  validator-clean, and recorded the invariant in memory.

## Blockers
- none
