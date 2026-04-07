---
ticket_id: TASK-0017
title: make stop hook verdicts visible to operators
phase: documenting
status: building
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-05T00:00:00Z
updated_at: 2026-04-06T02:09:11Z
next_action: close out docs/ticket writeback and decide whether to archive this ticket after the repo push/PR step
last_verification: python3 -m py_compile bin/stop_hook.py bin/ralph_tmux.py plus stop-hook replay now returns systemMessage, the hook status line now reads Evaluating Ralph stop hook, and python3 bin/ralph_tmux.py status shows the latest hook verdict for TASK-9998 from run-state
linked_docs:
  - bin/stop_hook.py
  - README.md
  - experiments/2026-04-05-stop-hook-smoke.md
---

# TASK-0017: make stop hook verdicts visible to operators

## Summary
The current hook often only shows `Stop hook (completed)` or `hook: Stop Completed`, which hides whether it repeated, advanced, blocked, or no-op'd.

## Scope
- In: operator-visible verdict surface, better hook feedback, and maybe improved audio/notifications
- Out: changing the core judge semantics unless needed to expose the verdict cleanly

## Plan

### Pitch
- `Req:` a user cannot tell from the UI whether the hook actually did anything
- `Bet:` one concise explicit verdict surface will reduce confusion more than more hidden automation
- `Win:` users know whether the hook repeated the ticket, blocked it, advanced it, or ignored it

### Core Flow
```pseudo
hook runs
judge decides
operator should see:
  repeat / advance / block / complete / no-op
without reading raw logs manually
```

## Acceptance Criteria
- [x] AC-1: a real hook run exposes its verdict to the operator in a readable way
- [x] AC-2: operators no longer have to infer behavior from duplicated output or vague completion text

## Implementation Notes
- Touched areas: `bin/stop_hook.py`, `bin/ralph_tmux.py`, `bin/README.md`, `README.md`, `docs/specs/ralph-run-state.schema.json`, and this ticket
- Reused patterns: project-local current-run/run-state persistence plus tmux lane metadata already tracked for Ralph
- Guardrails: make verdicts visible without copying OMX auto-nudge behavior or injecting hidden continuation commands

## Evidence
- [ ] Tests
- [x] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Validation details:
  - `python3 -m py_compile bin/stop_hook.py bin/ralph_tmux.py`
  - `CODEXTER_RALPH_HOOK=1 CODEXTER_RALPH_TMUX_DRY_RUN=1 python3 bin/stop_hook.py` replay against a dry-run lane
  - `python3 bin/ralph_tmux.py status`
  - verified replay JSON now includes `systemMessage: "Stop hook: Ralph repeat: TASK-9998 -> building (transparency_probe)"`
  - verified `hooks.json` now uses `statusMessage: "Evaluating Ralph stop hook"`
  - live tmux verification in session `ralph-task0018-live2`:
    - pane `%37` stayed active
    - `Stop hook (blocked)` showed the continuation feedback
    - `python3 bin/ralph_tmux.py status` showed `last_hook_decision=repeat_ralph`, `last_hook_summary=Ralph repeat: TASK-9998 -> building (status_probe)`, and `hook_status_source=run-state`

## Blockers
- none

## Handoff
- Current state: Stop-hook verdicts now emit `systemMessage` so Codex can surface them in the UI/event stream, the in-flight label is `Evaluating Ralph stop hook`, and `python3 bin/ralph_tmux.py status` centralizes the latest lane + hook state.
- Resume from: documenting closeout only unless you want to change the wording/format of the verdict summaries.

## Writeback
- Update this ticket as work progresses.
- Update `status` and `phase` in frontmatter when queue state changes.
