---
ticket_id: TASK-9998
title: live Ralph tmux smoke
phase: building
status: building
owner: codex
priority: low
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-05T00:00:00Z
updated_at: 2026-04-06T23:28:03Z
next_action: let the Stop hook consume this explicit same-ticket build_complete result now that the missing-RALPH_RESULT recovery note is recorded on the temp ticket
last_verification: 2026-04-06T23:28:03Z | refreshed .ralph/state/current-run.json, confirmed TASK-9998 remained the active building ticket after a missing_ralph_result hook decision, and kept the recovery write-back isolated to this temp ticket
linked_docs: []
---

# TASK-9998: live Ralph tmux smoke

## Summary
Bounded live smoke ticket for verifying the tmux-backed Ralph lane.

## Scope
- In: update this temp ticket only, then emit a `RALPH_RESULT`
- Out: repo code changes, docs changes, or any work outside this file

## Plan

### Pitch
- `Req:` prove the live tmux lane can continue after a Stop-hook verdict
- `Bet:` one no-op Ralph pass on a temp ticket is enough
- `Win:` same-pane live continuation is verified without touching tracked repo files

### Core Flow
```pseudo
read current run state
append one short note to this temp ticket only
do not edit repo files
emit RALPH_RESULT: status=build_complete next=building reason=live_smoke
```

## Acceptance Criteria
- [x] AC-1: live tmux lane receives one real Ralph worker pass
- [x] AC-2: Stop-hook repeat path can continue the same live lane

## Working Notes
- 2026-04-05T22:19:42Z: Replayed the bounded Ralph pass against the same live run state and kept the change isolated to this smoke ticket.
- 2026-04-05T22:20:28Z: Added explicit evidence coverage for the repeat pass, including refreshed run-state details and a successful ticket metadata validation.
- 2026-04-06T23:28:03Z: Stop-hook replay flagged a missing explicit `RALPH_RESULT`, so this bounded continuation pass records the live run-state recovery and re-emits the required result line from the same ticket.

## Implementation Notes
- Smoke-only ticket. Do not edit files outside this temp ticket.
- Completed one bounded Ralph pass by resolving the active run state, confirming this ticket as the execution unit, and appending this local smoke note only.
- Completed a second fresh write-back pass after re-reading `.ralph/state/current-run.json` so the active lane has current ticket evidence for the Stop-hook repeat path.
- Added explicit missing-evidence coverage for the repeat pass by validating the touched ticket surface with `python3 bin/check_ticket_metadata.py` and recording why build-system checks remain intentionally out of scope for this markdown-only smoke ticket.
- Recorded the later `missing_ralph_result` hook decision from the live run state so this temp ticket explains why the lane repeated and why this pass ends with an explicit result line.

## Changed Surfaces
- `tickets/TASK-9998-live-smoke.md`

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Command: `sed -n '1,220p' .ralph/state/current-run.json`
  - Outcome: confirmed `ticket_id=TASK-9998`, `ticket_path=/Users/kenjipcx/coding-harness/Codexter/tickets/TASK-9998-live-smoke.md`, and active `phase=building`
- Command: `sed -n '1,220p' .ralph/state/current-run.json`
  - Outcome: re-confirmed the same live run state at `2026-04-05T22:19:42Z`, including `run_id=run-task-9998-building-20260405T221902802036Z` and `status=running`
- Command: `sed -n '1,220p' .ralph/state/current-run.json`
  - Outcome: refreshed the live run state at `2026-04-05T22:20:28Z`, confirming `status=waiting_for_worker`, `last_worker_result=RALPH_RESULT: status=build_complete next=building reason=live_smoke`, and `last_judge_verdict=repeat_ralph`
- Command: `python3 bin/check_ticket_metadata.py`
  - Outcome: passed with `ticket metadata OK (20 ticket files checked)`, covering the only touched surface in this pass
- Command: ticket write-back in `tickets/TASK-9998-live-smoke.md`
  - Outcome: smoke pass evidence, changed surface, next action, and verification timestamp are now recorded on the active ticket
- Command: `sed -n '1,220p' .ralph/state/current-run.json`
  - Outcome: refreshed the live run state at `2026-04-06T23:28:03Z`, confirming `status=waiting_for_worker`, `last_hook_decision=missing_ralph_result`, `last_hook_summary=Ralph missing result: TASK-9998 in building`, and `last_judge_verdict=repeat_ralph`
- Command: scope review against `tickets/TASK-9998-live-smoke.md`
  - Outcome: tests, typecheck, and lint remain intentionally unrun because this bounded smoke pass changes only the temp ticket markdown and does not touch executable repo code

## Blockers
- none

## Handoff
- Current state: the active temp ticket now records the missing-result recovery context from live run state; no repo code or docs were changed.
- Resume from: this temp ticket only, then let the Stop hook consume the explicit `RALPH_RESULT` from this pass.

## Writeback
- Update this ticket if you need a note, but keep the change local to this file.
