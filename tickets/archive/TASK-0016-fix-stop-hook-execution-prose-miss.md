---
ticket_id: TASK-0016
title: fix stop hook miss on execution-mode prose completions
phase: building
status: building
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-05T00:00:00Z
updated_at: 2026-04-05T22:25:00+0100
next_action: capture the remaining tmux follow-up suite failure separately now that the prose-only missing-RALPH_RESULT regression is fixed and covered
last_verification: 2026-04-05T22:25:00+0100 | py_compile passes for bin/stop_hook.py and experiments/run_ralph_smoke_evals.py; check_ticket_metadata passes; direct Ralph-mode prose replay now blocks/continues with an explicit RALPH_RESULT requirement; full smoke suite still fails on the existing hook_tmux_followup assertion
linked_docs:
  - bin/stop_hook.py
  - experiments/2026-04-05-stop-hook-smoke.md
  - experiments/run_ralph_smoke_evals.py
---

# TASK-0016: fix stop hook miss on execution-mode prose completions

## Summary
The stop hook still misses some implementation-mode completions when the assistant ends with plain prose like "I can fix that now" instead of a structured `RALPH_RESULT`.

## Scope
- In: hook behavior for execution-mode prose completions, fallback classification, and explicit failure/continue policy
- Out: generic brainstorming/planning chat behavior

## Plan

### Pitch
- `Req:` a user reported a real execution pass that ended with a concrete next step, but the stop hook completed without continuing the work
- `Bet:` the fallback path needs stronger execution-mode semantics or a stricter requirement that implementation lanes must emit `RALPH_RESULT`
- `Win:` fewer false stops in real implementation sessions

### Core Flow
```pseudo
worker ends with plain prose instead of RALPH_RESULT
stop hook sees concrete next step
hook should either:
  force repeat/continue in execution mode
or
  treat the missing RALPH_RESULT as a contract failure and surface it explicitly
```

## Acceptance Criteria
- [x] AC-1: execution-mode prose no longer silently stops when the same-ticket next step is obvious
- [x] AC-2: missing `RALPH_RESULT` in execution mode is either handled explicitly or treated as a hard contract miss

## Evidence
- [x] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification

Validation details:
- `python3 -m py_compile bin/stop_hook.py experiments/run_ralph_smoke_evals.py`
- `python3 bin/check_ticket_metadata.py`
- direct stop-hook replay for a complete fixture ticket with prose-only execution output now returns:
  - `{"decision": "block", "reason": "Continue TASK-9997 in building ... finish with a RALPH_RESULT."}`
- `python3 experiments/run_ralph_smoke_evals.py`
  - regression case added for missing `RALPH_RESULT` prose path
  - current full-suite status still red on the existing `hook_tmux_followup` assertion, which is separate from this prose-completion fix

## Blockers
- none

## Handoff
- Current state: the stop hook now forces a same-ticket continuation when Ralph-mode execution ends in plain prose without `RALPH_RESULT`, and the legacy `continue_same_ticket` path no longer converts that decision into a fake success when ticket gaps happen to be empty.
- Resume from: `bin/stop_hook.py`, `experiments/run_ralph_smoke_evals.py`, and the remaining `hook_tmux_followup` smoke assertion if you want the whole Ralph suite green again.

## Writeback
- Update this ticket as work progresses.
- Update `status` and `phase` in frontmatter when queue state changes.
