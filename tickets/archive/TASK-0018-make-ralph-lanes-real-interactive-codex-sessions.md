---
ticket_id: TASK-0018
title: make ralph tmux lanes real interactive codex sessions
phase: documenting
status: building
owner: codex
priority: high
depends_on:
  - TASK-0014
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-05T00:00:00Z
updated_at: 2026-04-05T22:21:00Z
next_action: close out documenting writeback and decide whether to archive this ticket after repo-level push/PR work
last_verification: python3 -m py_compile bin/ralph_tmux.py bin/stop_hook.py bin/ralph_orchestrate.py plus detached tmux dry-run launch/followup and stop-hook replay smokes in session ralph-task0018-smoke and live tmux proof in session ralph-task0018-live2 where pane %37 stayed active after a real Stop hook block/continue cycle
linked_docs:
  - bin/ralph_tmux.py
  - bin/ralph_orchestrate.py
  - tickets/TASK-0014-tmux-visibility-and-followup.md
---

# TASK-0018: make ralph tmux lanes real interactive codex sessions

## Summary
The tmux visibility layer currently proves handoff and pane spawning, but the pane mostly shows wrapper/orchestrator output instead of a useful interactive Codex lane.

## Scope
- In: interactive lane design, `codex`/`codex resume` integration, pane/session id storage, attach/view ergonomics
- Out: generalized multi-worker team runtime

## Plan

### Pitch
- `Req:` a user expects to watch the next Ralph pass in tmux, not just see a shell wrapper complete
- `Bet:` reusing a real Codex session per ticket lane is the missing operator-facing piece
- `Win:` the visibility layer becomes genuinely useful, not just mechanically correct

### Core Flow
```pseudo
spawn tmux pane
launch interactive codex session
capture/store session_id
future follow-up uses codex resume in same pane
operator can attach and understand what the lane is doing
```

## Acceptance Criteria
- [x] AC-1: a Ralph tmux lane shows a real interactive Codex session, not only wrapper output
- [x] AC-2: follow-up passes reuse that lane through stored session information
- [x] AC-3: attach/tail becomes sufficient for a human to inspect the next pass

## Implementation Notes
- Touched areas: `bin/ralph_tmux.py`, `bin/stop_hook.py`, `bin/ralph_orchestrate.py`, `bin/README.md`, `bin/AGENTS.md`, `docs/MEMORY.md`, and `docs/HISTORY.md`
- Reused patterns: project-local `.ralph/state/current-run.json` as the runtime source of truth and hook-driven continuation decisions from `bin/stop_hook.py`
- Guardrails: keep tmux behavior explicit, reuse a live pane before recreating it, and use stored `session_id` only as the recovery path when the visible pane is gone

## Evidence
- [ ] Tests
- [x] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Validation details:
  - `python3 -m py_compile bin/ralph_tmux.py bin/stop_hook.py bin/ralph_orchestrate.py`
  - detached tmux smoke:
    - `tmux new-session -d -s ralph-task0018-smoke`
    - `python3 bin/ralph_tmux.py launch --ticket tickets/TASK-0018-make-ralph-lanes-real-interactive-codex-sessions.md --phase building --tmux-session ralph-task0018-smoke --layout pane --auto-continue --dry-run`
    - `python3 bin/ralph_tmux.py followup --ticket tickets/TASK-0018-make-ralph-lanes-real-interactive-codex-sessions.md --phase documenting --run-state .ralph/runs/task-0018-building-20260405T220701603899Z.json --reason 'smoke followup' --auto-continue --dry-run`
    - `CODEXTER_RALPH_HOOK=1 CODEXTER_RALPH_TMUX_DRY_RUN=1 python3 bin/stop_hook.py` replay with `RALPH_RESULT: status=build_complete next=documenting reason=smoke`
    - `tmux list-panes -t ralph-task0018-smoke -F '#{session_name}\t#{window_id}\t#{window_index}\t#{pane_id}\t#{pane_dead}\t#{pane_current_command}'`
  - live codex probe:
    - launched one local interactive `codex --no-alt-screen -C /Users/kenjipcx/coding-harness/Codexter -c 'thread_name="ralph-lane-test"' ...`
    - confirmed real session metadata lands immediately under `~/.codex/sessions/.../session_meta.payload.id`
  - live tmux proof:
    - `python3 bin/ralph_tmux.py launch --ticket tickets/TASK-9998-live-smoke.md --phase building --tmux-session ralph-task0018-live2 --layout pane --auto-continue`
    - `tmux capture-pane -t %37 -p -S -260`
    - `tmux list-panes -t ralph-task0018-live2 -F '#{session_name}\t#{window_id}\t#{window_index}\t#{pane_id}\t#{pane_dead}\t#{pane_current_command}'`
    - `tail -n 30 .ralph/logs/stop-hook.jsonl`
    - observed `session_id=019d5fba-6d5b-7c72-8895-d80fe53202b3`, `last_judge_verdict=repeat_ralph`, no new `spawn_followup` log for that verdict, and the same pane `%37` continued running after `Stop hook (blocked)`

## Blockers
- none

## Handoff
- Current state: the tmux helper now starts real interactive `codex` lanes with the phase prompt as the initial CLI prompt, the Stop hook continues live sessions in-place through the standard block/continue path, and `ralph_tmux.py followup` remains the recovery path for dry-run or resumed follow-ups.
- Resume from: documenting closeout only unless you want additional cleanup of the temporary smoke session/artifacts.

## Writeback
- Update this ticket as work progresses.
- Update `status` and `phase` in frontmatter when queue state changes.
