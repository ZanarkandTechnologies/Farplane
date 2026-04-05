---
ticket_id: TASK-0010
title: implement ralph thin prototype scripts
phase: building
status: active
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-05T00:00:00Z
updated_at: 2026-04-05T13:00:00Z
next_action: review the thin prototype behavior and decide whether the next slice should wire the judge into stop-hook flow or add board-state transitions
last_verification: bash -n bin/ralph_worker.sh plus python3 -m py_compile for the judge/orchestrator and a planning dry-run through bin/ralph_orchestrate.py
linked_docs:
  - docs/specs/ralph-orchestration-blueprint.md
  - docs/specs/ralph-flow-examples.md
  - docs/specs/ralph-run-state.schema.json
  - docs/specs/ralph-judge-verdict.schema.json
---

# TASK-0010: implement ralph thin prototype scripts

## Summary
Turn the drafted Ralph prompt/schema design into a minimal runnable prototype: one thin worker wrapper, one judge, and one orchestrator entrypoint.

## Scope
- In: tracked prototype scripts, prompt/schema integration, ticket/writeback notes, and doc updates required to explain the runnable shape
- Out: full stop-hook wiring, remote compute integration, tmux team orchestration, or automatic board-state mutation

## Plan

### Pitch
- `Req:` prove the new Ralph docs are executable, not just design prose
- `Bet:` one thin shell worker plus two small Python helpers is enough to validate the architecture without overbuilding
- `Win:` the repo gains a real prototype loop shape that can later be wired into hooks or richer orchestration

### B -> A
- `Before:` prompts and schemas exist, but no tracked scripts use them
- `After:` one worker wrapper, one judge, and one orchestrator entrypoint can run a bounded Ralph phase against a ticket
- `Outcome:` Ralph moves from concept docs to an actual harness prototype

### Delta
- `Touch:` `bin/`, `prompts/`, `docs/specs/`, `docs/HISTORY.md`, this ticket, and the ticket index
- `Keep:` ticket-first memory, thin wrapper contract, and explicit judge/orchestrator split
- `Change:` add the minimal runnable path from ticket + phase -> worker -> verdict
- `Delete/Avoid:` avoid hidden continuation, broad runtime state mutation, or network/cloud coupling in this slice

### Core Flow
```pseudo
resolve ticket + phase
write initial run-state json
launch codex exec with prompt file and env vars
parse one RALPH_RESULT line
judge ticket + result into verdict json
update run state and print next action
```

### Proof
- `P1:` one tracked script can launch a phase worker using the thin wrapper contract
- `P2:` one tracked judge can emit schema-shaped verdict JSON from a ticket + worker result
- `P3:` one orchestrator entrypoint can stitch the two together without hidden runtime magic
- `Risk:` mock/simple transition logic may be too naive for edge cases
- `Rollback:` remove the prototype scripts and keep only the docs/specs

### Plan Review
- `Refs:` linked docs plus existing `stop_hook.py` and `stop_hook_output.schema.json`
- `Scope:` pass; prototype only
- `Proof:` pass if scripts are syntactically valid and can explain their inputs/outputs clearly
- `Guardrails:` keep board state human-visible; do not auto-mutate lanes silently
- `Fixes:` use thin wrapper env vars and prompt files as the canonical behavior surface

### Delegation
- `Need:` `Not needed`
- `Why:` the work is tightly coupled across scripts, prompts, and docs
- `Artifact:` none

### Ask
- `Ready: yes`
- `Next:` implement the scripts, validate syntax, and update this ticket with the prototype contract

### Ticket Move
- `Now:` `tickets/building/`
- `On approval:` stay in `building/` until scripts and docs are validated
- `Follow-ups:` hook wiring and remote compute policy can be separate tickets later
- `Blocked in building?:` `no`

## Acceptance Criteria
- [x] AC-1: there is a runnable tracked worker wrapper that launches one Ralph phase via the thin wrapper contract
- [x] AC-2: there is a tracked judge that emits schema-shaped verdict JSON
- [x] AC-3: there is a tracked orchestrator entrypoint that composes worker + judge for one ticket/phase
- [x] AC-4: docs and this ticket explain the prototype's real inputs/outputs

## Working Notes
- Keep the worker thin and push phase behavior into prompt files.
- Keep the judge deterministic and conservative.
- Keep the orchestrator explicit; no hidden auto-looping in this slice.

## Implementation Notes
- Touched areas: `bin/ralph_worker.sh`, `bin/ralph_judge.py`, `bin/ralph_orchestrate.py`, `bin/README.md`, `bin/AGENTS.md`, `prompts/ralph-*.md`, `docs/specs/*`, `tickets/INDEX.md`
- Reused patterns: ticket-first active task object, small JSON schemas, and the existing stop-hook classifier's conservative evidence-driven routing style
- Guardrails: thin worker wrapper only, explicit judge/orchestrator split, no hidden continuation loop, no automatic board-lane mutation

## Evidence
- [ ] Tests
- [x] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Validation details:
  - `cd Codexter && python3 bin/check_ticket_metadata.py`
  - `bash -n Codexter/bin/ralph_worker.sh`
  - `python3 -m py_compile Codexter/bin/ralph_judge.py Codexter/bin/ralph_orchestrate.py`
  - `python3 -m json.tool Codexter/docs/specs/ralph-run-state.schema.json`
  - `python3 -m json.tool Codexter/docs/specs/ralph-judge-verdict.schema.json`
  - `python3 Codexter/bin/ralph_orchestrate.py --ticket Codexter/tickets/building/TASK-0010-ralph-thin-prototype.md --phase planning --dry-run --json`

## Blockers
- none

## Handoff
- Current state: the first runnable Ralph prototype exists and can dry-run a planning phase into a schema-shaped judge verdict.
- Resume from: this ticket, the linked spec files, and `python3 bin/ralph_orchestrate.py --ticket tickets/building/TASK-0010-ralph-thin-prototype.md --phase planning --dry-run --json`.

## Writeback
- Update this ticket as work progresses.
- Move the ticket and update `tickets/INDEX.md` when its board state changes.
