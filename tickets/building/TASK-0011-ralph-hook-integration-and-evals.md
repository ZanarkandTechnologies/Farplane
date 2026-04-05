---
ticket_id: TASK-0011
title: wire ralph hook integration and run toy evals
phase: building
status: active
owner: codex
priority: high
depends_on:
  - TASK-0010
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-05T00:00:00Z
updated_at: 2026-04-05T18:46:00Z
next_action: move this ticket through documenting/closeout now that the live stop-hook path, smoke eval suite, and explicit build evidence are all captured
last_verification: ticket metadata check passes; syntax/schema checks pass; 10-case smoke eval suite passes locally with fixture-based missing-evidence cases; git diff --check is clean; live ~/.codex payload_contract_probe_2 is logged against TASK-0011
linked_docs:
  - docs/specs/ralph-orchestration-blueprint.md
  - docs/specs/ralph-flow-examples.md
  - docs/specs/ralph-run-state.schema.json
  - docs/specs/ralph-judge-verdict.schema.json
  - tickets/building/TASK-0010-ralph-thin-prototype.md
---

# TASK-0011: wire ralph hook integration and run toy evals

## Summary
Take the first Ralph prototype and make it closer to the intended runtime: use `ralphplan` plus `ralph`, route evidence through a QA-aware judge path, and capture actual toy eval findings.

## Scope
- In: stop-hook integration, simpler `ralphplan` + `ralph` prompt/runtime model, install/config wiring needed for hooks, and a tracked experiments folder with findings
- Out: cloud compute execution, tmux team runtime, or full production reliability claims

## Plan

### Pitch
- `Req:` the prototype currently exists, but the stop hook is not actually wired and the code path still reflects an older multi-phase model
- `Bet:` a smaller, cleaner runtime with actual hook wiring plus a few toy evals will teach more than another round of architecture debate
- `Win:` we can prove whether the approach is autonomous enough to keep going or whether the design still breaks on obvious cases

### B -> A
- `Before:` docs and code disagree; the stop hook is quarantined in install/config; there is no tracked eval evidence
- `After:` one simpler end-to-end prototype exists, the stop hook is installable and testable, and experiments record what worked and what failed
- `Outcome:` the repo gains a scientific iteration loop instead of relying on intuition alone

### Delta
- `Touch:` `bin/`, `prompts/`, `hooks.json`, install/bootstrap docs, specs, and new `experiments/`
- `Keep:` ticket-first memory and thin wrapper execution
- `Change:` hook becomes part of the active prototype instead of a quarantined side path
- `Delete/Avoid:` avoid claiming production autonomy; focus on local toy eval evidence

### Core Flow
```pseudo
run ralphplan or ralph
gather evidence via qa subagent path
trigger stop hook judge
if evidence bad then rerun ralph
if evidence good then advance or complete ticket
log findings in experiments
```

### Proof
- `P1:` stop hook can be invoked against a realistic payload and ticket
- `P2:` ralphplan/ralph runtime path no longer depends on the older prove/review split
- `P3:` a 10-case smoke suite produces concrete findings instead of hand-wavy claims
- `Risk:` hook semantics in live Codex may still be awkward even after wiring
- `Rollback:` keep the thin orchestrator usable without the hook if hook integration proves too brittle

### Plan Review
- `Refs:` linked docs, `TASK-0010`, `bin/stop_hook.py`, `hooks.json`, `install.sh`, `config.toml.example`
- `Scope:` pass; focused on the prototype runtime and measurements
- `Proof:` pass if we can show real payload-driven behavior and documented findings
- `Guardrails:` preserve explicit orchestration and avoid hidden infinite loops
- `Fixes:` do the hook work under a dedicated post-v1 ticket instead of muddying the earlier scaffold slice

### Delegation
- `Need:` `Not needed`
- `Why:` the runtime path is tightly coupled across scripts, prompts, config, and experiments
- `Artifact:` none

### Ask
- `Ready: yes`
- `Next:` finish the convergence to the simpler model, wire the hook, and capture toy evals

### Ticket Move
- `Now:` `tickets/building/`
- `On approval:` remain active until hook integration and experiments are complete
- `Follow-ups:` remote compute and heavier uptime testing can be separate tickets later
- `Blocked in building?:` `no`

## Acceptance Criteria
- [x] AC-1: executable prototype uses `ralphplan` plus `ralph` as the top-level runtime shape
- [x] AC-2: stop hook can evaluate a realistic worker result plus ticket state and emit a useful verdict under payload replay
- [x] AC-3: install/bootstrap surfaces no longer pretend the hook is out of scope for the active prototype
- [x] AC-4: tracked toy eval findings exist under `experiments/`
- [x] AC-5: live Codex sessions can resolve the active Ralph ticket inside the stop hook without manual payload replay

## Working Notes
- Do not optimize for pretty abstractions over measured behavior.
- Keep the hook conservative; if unsure, stop safely.
- Prefer one or two good experiments over many noisy ones.

## Implementation Notes
- Touched areas: `bin/stop_hook.py`, `bin/ralph_worker.sh`, `bin/ralph_judge.py`, `bin/ralph_orchestrate.py`, `bin/AGENTS.md`, `prompts/ralphplan.md`, `prompts/ralph.md`, `hooks.json`, `install.sh`, `config.toml.example`, `README.md`, `experiments/`, `docs/HISTORY.md`, `docs/MEMORY.md`
- Reused patterns: existing ticket-first memory, thin wrapper `codex exec` launches, and conservative stop-hook fallback behavior
- Guardrails: keep hook conservative, keep orchestration explicit, stop safely on uncertainty, and keep experiment findings in tracked files

## Evidence
- [x] Tests
- [x] Typecheck
- [x] Lint
- [x] QA / manual verification
- Validation details:
  - `cd Codexter && python3 bin/check_ticket_metadata.py`
  - `bash -n Codexter/bin/ralph_worker.sh`
  - `python3 -m py_compile Codexter/bin/ralph_judge.py Codexter/bin/ralph_orchestrate.py Codexter/bin/stop_hook.py`
  - `python3 -m py_compile Codexter/experiments/run_ralph_smoke_evals.py`
  - `python3 -m json.tool Codexter/docs/specs/ralph-run-state.schema.json`
  - `python3 -m json.tool Codexter/docs/specs/ralph-judge-verdict.schema.json`
  - `cd Codexter && python3 experiments/run_ralph_smoke_evals.py`
  - `cd Codexter && git diff --check`
  - manual lint/style review for the changed Python, shell, JSON, and docs surfaces; no dedicated repo linter is configured for this prototype
  - live `~/.codex` wiring:
    - linked `~/.codex/hooks.json`
    - enabled `codex_hooks`
    - added `CODEXTER_HOME` and `CODEXTER_RALPH_HOOK` to `~/.codex/config.toml`
  - real `codex exec` smoke tests showed:
    - `hook: Stop`
    - `hook: Stop Completed`
    - `hook: Stop Blocked`
  - project-local hook log written to `Codexter/.ralph/logs/stop-hook.jsonl`
  - live hook contract probe logged:
    - `payload_contract_probe_2`
    - `ticket_id=TASK-0011`
    - `decision=repeat_ralph`
    - `next_phase=building`

## Blockers
- none

## Handoff
- Current state: docs/code now largely agree on `ralphplan` plus `ralph`; the 10-case replay suite passes with fixture-based missing-evidence coverage; live hook firing and live stop-block behavior are both confirmed; the ticket now explicitly records the test/lint evidence that previously kept the hook in `building`.
- Resume from: this ticket, `experiments/2026-04-05-stop-hook-smoke.md`, `experiments/latest-runs.json`, `Codexter/.ralph/logs/stop-hook.jsonl`, and the local `~/.codex` install state.

## Writeback
- Update this ticket as work progresses.
- Move the ticket and update `tickets/INDEX.md` when its board state changes.
