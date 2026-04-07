---
ticket_id: TASK-0014
title: add tmux visibility and follow-up lane for ralph
phase: building
status: building
owner: codex
priority: high
depends_on:
  - TASK-0011
  - TASK-0013
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-05T00:00:00Z
updated_at: 2026-04-05T21:55:00Z
next_action: tighten attach or tail ergonomics, document the operator workflow, and only widen scope if a longer-run tmux smoke exposes a real follow-up bug
last_verification: launched TASK-0014 in tmux pane %13 and proved a stop-hook advance replay spawned a fresh visible follow-up in pane %14
linked_docs:
  - README.md
  - bin/README.md
  - docs/specs/ralph-orchestration-blueprint.md
  - docs/specs/ralph-run-state.schema.json
  - tickets/TASK-0011-ralph-hook-integration-and-evals.md
---

# TASK-0014: add tmux visibility and follow-up lane for ralph

## Summary
Close out the tmux visibility slice now that the core handoff works: make the operator workflow usable, keep the scope bounded to one visible follow-up lane per pass, and capture the proof needed to move this ticket toward documenting.

## Scope
- In: small `attach` or `tail` ergonomics if still needed, minimal operator docs for `launch` or `attach` or `tail`, and one longer-run smoke that confirms the visible follow-up lane remains inspectable after the initial proof
- Out: full multi-worker tmux runtime, hidden default auto-continue, queue or mailbox infrastructure, or unrelated install/rules churn

## Plan

### Pitch
- `Req:` the basic tmux-backed follow-up path is already proven, but the operator surface and closeout proof are still thinner than the code path itself
- `Bet:` one short stabilization pass focused on usability and proof is enough to finish this ticket without expanding it into a heavier runtime
- `Win:` the repo ships a bounded, inspectable tmux lane workflow and this ticket can move toward documenting instead of staying open as a vague runtime experiment

### B -> A
- `Before:` launch plus follow-up spawning work, but the ticket plan still reads like a greenfield build and does not identify the smallest remaining closeout slice
- `After:` the ticket, operator docs, and remaining build step agree that only ergonomics plus proof are left unless the longer-run smoke finds a concrete bug
- `Outcome:` the next builder can finish or split the work intentionally instead of re-opening architecture questions

### Delta
- `Touch:` `bin/ralph_tmux.py` only if attach or tail ergonomics need a small fix, `bin/README.md`, optionally `README.md`, and this ticket
- `Keep:` the existing tmux launch flow, run-state tmux metadata, stop-hook follow-up spawn path, and opt-in auto-continue guardrail
- `Change:` shift effort from proving basic viability to making the operator path obvious and deciding whether any remaining issue is real enough to keep in this ticket
- `Delete/Avoid:` do not rebuild the follow-up handoff from scratch and do not invent a generalized tmux orchestration layer here

### Core Flow
```pseudo
launch the ticket through bin/ralph_tmux.py
confirm attach/tail are enough to inspect the active lane
exercise one longer repeat/advance cycle
if no new bug appears:
  document the operator workflow and move toward documenting
else:
  fix the narrow surfaced bug or split a follow-up ticket
```

### Proof
- `P1:` the already-proven launch plus follow-up path remains stable across at least one longer-run tmux smoke
- `P2:` operators can inspect the active lane through the helper surface without falling back to ad hoc tmux commands for the common path
- `P3:` docs show the minimal `launch` or `attach` or `tail` workflow and keep auto-continue explicitly opt-in
- `Risk:` the remaining unknown is not core viability but whether a real usability or pane-management bug appears under slightly longer use
- `Rollback:` keep the current proven path, document any manual tmux fallback, and split deeper runtime concerns into a new ticket instead of bloating this one

### Plan Review
- `Refs:` linked docs, `TASK-0011`, `bin/ralph_tmux.py`, `bin/ralph_orchestrate.py`, `bin/stop_hook.py`, and the current stop-hook log evidence
- `Scope:` pass; the smallest remaining slice is operator-facing closeout work, not new runtime architecture
- `Proof:` pass if the helper workflow is documented and the longer-run smoke does not reveal an unresolved same-ticket bug
- `Guardrails:` keep auto-continue opt-in, keep the lane visible, and avoid turning this into stress infrastructure or multi-worker orchestration
- `Fixes:` treat any newly surfaced runtime bug as a narrow fix or an explicit follow-up ticket, not as permission to broaden scope implicitly

### Delegation
- `Need:` `Not needed`
- `Why:` the remaining work is localized closeout planning around already-identified files and evidence
- `Artifact:` none

### Ask
- `Ready: yes`
- `Next:` finish the operator-facing closeout pass and then move this ticket toward documenting if the longer-run smoke stays clean

### Ticket Move
- `Now:` `tickets/`
- `On approval:` stay in `tickets/`; approval already exists and the remaining work is execution/verification, not new planning
- `Follow-ups:` open a new ticket only if longer-run tmux use exposes a concrete bug or broader runtime need
- `Blocked in building?:` `no`

## Acceptance Criteria
- [x] AC-1: a helper exists to launch and inspect a Ralph tmux lane
- [x] AC-2: run state records tmux location for active ticket runs
- [x] AC-3: stop hook can spawn a follow-up pass into tmux instead of reusing the same session when auto-continue is enabled
- [ ] AC-4: repo docs show the minimal operator workflow for `launch`, `attach`, and `tail` without implying a heavier tmux runtime
- [ ] AC-5: one longer-run tmux smoke confirms the visible follow-up lane stays inspectable after the first proven handoff

## Working Notes
- The core visible follow-up handoff is already proven. Do not restart the ticket at the greenfield step.
- Keep auto-continue explicitly opt-in and ticket-bounded.
- If the longer-run smoke reveals a deeper runtime issue, split it instead of expanding this ticket by default.

## Implementation Notes
- Touched areas: `bin/ralph_tmux.py`, `bin/README.md`, optionally `README.md`, and this ticket; only re-open `bin/stop_hook.py` or `bin/ralph_orchestrate.py` if the longer-run smoke exposes a concrete bug
- Reused patterns: thin `codex exec` launches, ticket-first run-state tracking, and conservative stop-hook fallback behavior
- Guardrails: keep the current tmux session as a visibility anchor only; avoid hidden loops, mailbox features, or unrelated repo cleanup

## Evidence
- [ ] Tests
- [x] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Validation details:
  - `python3 -m py_compile bin/ralph_tmux.py bin/ralph_orchestrate.py bin/stop_hook.py`
  - `python3 bin/ralph_tmux.py launch --ticket tickets/TASK-0014-tmux-visibility-and-followup.md --phase planning --tmux-session ai-brain-local --layout pane --auto-continue`
  - `tmux capture-pane -t %13 -p -S -120`
  - manual stop-hook replay with `plan_ready -> building`
  - `tmux list-panes -a` confirmed new pane `%14`
  - `Codexter/.ralph/logs/stop-hook.jsonl` recorded `spawn_followup`

## Blockers
- none

## Handoff
- Current state: the core tmux launch and follow-up spawn path is proven; the remaining slice is operator ergonomics, docs, and one longer-run smoke to decide whether the ticket is ready for documenting.
- Resume from: this ticket, `bin/ralph_tmux.py`, `bin/README.md`, `TASK-0011`, and `Codexter/.ralph/logs/stop-hook.jsonl`.

## Writeback
- Update this ticket as work progresses.
- Update `status` and `phase` in frontmatter when queue state changes.
