# PR Runtime

## Purpose

Prepare an isolated checkout and ticket runtime record for PR follow-up or any
task where more than one live writer would otherwise share one filesystem, then
optionally launch the ticket-scoped runtime for QA.

## Public API / Entrypoints

- `SKILL.md`: main workflow contract
- `AGENTS.md`: maintenance rules
- `bin/ticket-runtime`: helper command surface for runtime records, optional
  isolated checkout creation, runtime launch/stop, and QA targets

## Minimal Example

1. Resolve the PR branch or ticket branch.
2. Decide whether the task can stay shared or needs an isolated worktree.
3. Run `python3 bin/ticket_runtime.py up --ticket TASK-0123 --branch pr-123 --checkout-mode worktree --runtime-mode branch-runtime --create-worktree --reserve frontend --reserve backend --frontend-cmd "npm run dev" --backend-cmd "npm run api"`.
4. Run `python3 bin/ticket_runtime.py qa --ticket TASK-0123` to read the
   current runtime status plus the live QA targets for that ticket.
5. Run `python3 bin/ticket_runtime.py down --ticket TASK-0123` when the ticket
   runtime should stop.

## How to Test

- `python3 -m unittest bin/test_ticket_runtime.py`
- `python3 tickets/scripts/check_ticket_metadata.py`
- `python3 bin/ticket_runtime.py up --ticket TASK-0123 --branch feat/task-0123 --checkout-mode shared --runtime-mode branch-runtime --reserve frontend --frontend-cmd "npm run dev" --json`
