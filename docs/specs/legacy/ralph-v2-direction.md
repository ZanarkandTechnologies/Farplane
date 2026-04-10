# Ralph V2 Direction

Date: 2026-04-06

## Goal

Centralize the current Ralph v2 direction so the repo stops accumulating
runtime ideas across tickets, research notes, and ad hoc discussion.

This document is not the final implementation spec.
It is the canonical summary of:

- what the system should become
- what should stay deliberately lightweight for now
- what should not be copied from OMX
- which follow-up slices should be ticketized next

## Executive Summary

Ralph v2 should be:

> a ticket-first execution system with explicit per-ticket loops, explicit proof
> gates, explicit runtime visibility, and lightweight parallelism built on
> claims/worktrees when needed.

Ralph v2 should not be:

- a hidden auto-nudge wrapper
- a tmux-typing control plane that steals the keyboard
- a giant workflow catalog with overlapping planner surfaces
- a heavyweight multi-agent runtime before the single-lane model is clean

## Current Position

Today the repo already has:

- good ticket/spec discipline
- a bounded `impl-plan` / `ralph` execution model
- a judge and Stop-hook loop
- tmux visibility for real interactive Codex lanes
- centralized lane inspection through the `impl` tmux helper status surface

Today the repo does not yet have:

- a durable multi-ticket dispatcher
- claim/worktree coordination for parallel tickets
- a fully normalized evaluator/review loop
- an archive surface for fully processed tickets
- a cleaned-up execution surface with no overlap between `impl` and `ralph`

## Product Stance

### 1. Todo list first, runtime second

For now, a Markdown ticket list is enough.

That means:

- `tickets/*.md` stay the canonical execution objects
- runtime state stays small and local
- the system should not grow a heavy mailbox/lease runtime unless real
  parallel execution pressure demands it

### 2. Strict execution, flexible planning

The system should allow flexible human planning and intake, but execution must
 stay strict:

- one selected ticket per execution lane
- explicit proof requirements
- explicit review/fix loops
- explicit integration boundaries

### 3. No hidden continuation pressure

Ralph v2 must not copy OMX's default continuation model.

Do not build:

- auto-injected `yes, proceed`
- fallback watcher continue-steers
- hidden runtime decisions on the operator's behalf

Use visible Stop-hook continuation and visible run state instead.

## Canonical Entities

### Ticket

The ticket remains the canonical work item and durable task memory.

Recommended v2 direction:

- keep `owner`
- add `claimed_by` for active execution ownership
- optionally add `claimed_at`

This keeps parallel coordination ticket-native instead of inventing a second
queue system too early.

### Run State

Run state remains runtime-only and lightweight.

It should answer:

- what lane is active
- which ticket is active
- which phase is active
- what the last judge/hook said
- what the next visible action is

It should not replace tickets as the primary execution contract.

### Archive

Add a future `tickets/archive/` folder for fully processed tickets once the
active queue and documenting flow are stable.

Active queue should stay in `tickets/`.
Archive should hold:

- fully completed tickets
- closed exploratory/runtime-smoke tickets
- no longer active implementation slices

The archive should be a visibility/output surface, not a hot runtime surface.

## Desired End-to-End Loop

The intended long-form loop is:

1. intake a request/spec
2. normalize it
3. decompose it into dependency-linked tickets
4. select ready unblocked work
5. assign claims and execution lanes
6. run per-ticket loops:
   - plan
   - build
   - prove
   - review
   - fix if needed
7. gather evidence through QA/review subagents
8. integrate with commit/PR boundaries
9. run a final evidence sanity check
10. archive the completed ticket

Important separation:

- spec decomposition belongs before ticket execution
- `impl-plan` should plan one selected ticket
- `ralph` should execute one selected ticket

`impl-plan` should not be the thing that explodes a broad spec into many tickets.

## Minimal Parallelism Model

If/when parallelism is added, start with a tiny dispatcher model.

That dispatcher does not need to be a separate service.
It can be a thin selection loop over Markdown tickets:

1. read all tickets
2. filter `ready && unblocked && not claimed`
3. respect a small `max_parallelization` runtime setting
4. claim chosen tickets
5. assign them to local lanes/worktrees
6. clear or update claims when verdicts land

The load-bearing state is:

- ticket dependency fields
- `claimed_by`
- one small runtime concurrency config

Not required yet:

- mailboxes
- leases
- a persistent dispatcher daemon
- cloud execution by default

## Evaluator / Judge Direction

The judge should stay narrow.

It should decide things like:

- `repeat_same_ticket`
- `advance_phase`
- `split_followup_ticket`
- `block_for_review`
- `complete_ticket`

It should not silently become a giant project manager that mutates the whole
board by itself.

Recommended split:

- judge emits structured verdict
- orchestrator mutates queue/runtime state
- ticket remains the visible truth surface

## Planning Surface Simplification

The planning surface is now `impl-plan`.
It should stay ticket-focused and keep consensus challenge as a mode instead of
reintroducing a second public planner.

Remaining naming overlap:

- `impl`
- `ralph`

The repo should next decide whether execution should also collapse to one public
name, or whether the distinction is load-bearing enough to keep.

## Review Loop Direction

The future execution loop should include explicit review prompts and thresholds,
but not a giant formal workflow before the basics are stable.

Recommended v2 shape:

- normalize evaluator outputs
- track failure reasons in a structured report
- let repeated failures create concrete follow-up work instead of hand-wavy
  retries

This is where the system should eventually support:

- build
- debloat
- code review
- test
- evidence collection
- re-run until the verdict is above threshold

But the loop should still be explicit and visible.

## Runtime Visibility Direction

The operator should always be able to answer:

- what ticket is active?
- what pane/session owns it?
- what did the judge decide?
- why is the system continuing or blocked?
- what is the next visible action?

The current `impl` tmux helper status surface is the correct direction.

The next visibility goal is not more hidden automation.
It is a cleaner central status summary for the current board/run state.

## What To Avoid From OMX

Do not copy:

- auto-nudge default behavior
- hidden tmux pane injection as the primary continuation mechanism
- fallback watcher continue-steers
- large control-plane complexity before ticket/lane ownership is stable

Steal selectively:

- explicit runtime state
- explicit worker identity
- worktree isolation when needed
- better observability

## Known Issues / Follow-Up Bugs

These need explicit follow-up tickets after this summary is accepted:

### 1. Stop-hook timeout behavior needs verification/fix

There is an observed concern that Stop-hook timeout behavior may not be acting
as expected in practice.

Current code in `bin/stop_hook.py` defaults to `30.0` seconds when the env var
is unset, but floors parsed env values with `max(parsed, 1.0)`.

This should be validated explicitly so the team is not relying on a mistaken
timeout assumption.

### 2. Completed ticket archival needs an official policy

The repo should define when to move tickets from `tickets/` to
`tickets/archive/` and which states count as fully processed.

### 3. Execution-surface overlap needs simplification

`impl` and `ralph` still overlap in naming and operator mental model even
though their behavior is not identical.

## Recommended Next Ticket Buckets

These should become tickets next, in roughly this order:

1. `v2 direction accepted + ticketization pass`
2. `archive completed tickets policy + tickets/archive/ surface`
3. `stop-hook timeout verification/fix`
4. `execution surface simplification`
5. `dispatcher v0`:
   - claim field
   - next-ready selector
   - small max parallelization setting
6. `worktree assignment for parallel tickets`
7. `normalized evaluator/review scorecard`

## Decision Boundary

For now:

- use the Markdown ticket board as the source of work
- keep the runtime thin
- keep the continuation boundary visible
- do not build a heavyweight OMX clone

Later:

- add dispatcher semantics only when parallel ticket ownership becomes the next
  real bottleneck
- add archive flow once the active/documenting lifecycle is stable
- add richer evaluator loops once planner/executor boundaries are clearer
