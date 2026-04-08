---
ticket_id: TASK-0038
title: normalize stop-hook role configs
phase: complete
status: done
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-08T15:58:00Z
updated_at: 2026-04-08T16:08:41Z
next_action: archived after documenting the TOML hook-role contract and reviewer-owned completion gate
last_verification: `python3 -m py_compile bin/stop_hook.py bin/test_stop_hook.py`, `python3 -m unittest discover -s bin -p 'test_*.py'`, `git diff --check`, and `python3 tickets/scripts/check_ticket_metadata.py` passed; `python3 experiments/run_ralph_smoke_evals.py` still fails on the broader `hook_plan_payload` assertion in the current worktree
linked_docs:
  - docs/specs/harness-techniques.md
  - docs/specs/harness-engineering-quickstart.md
  - docs/specs/review-gates.md
  - bin/README.md
---

# TASK-0038: normalize stop-hook role configs

## Summary
Move stop-hook role prompts onto canonical TOML agent configs, remove the standalone `evidence-reviewer`, and keep the hook deterministic by injecting exact `developer_instructions` into `codex exec`.

## Scope
- In:
  - TOML-backed `reviewer` and `orchestrator` hook roles
  - `stop_hook.py` TOML role loading and prompt injection
  - merged reviewer completion-gate path
  - surrounding config/docs/test updates
- Out:
  - general subagent loading redesign
  - new runtime control planes
  - non-hook agent prompt rewrites

## Plan

### Pitch
- `Req:` make stop-hook roles consistent with the rest of `agents/` and remove the redundant evidence-review split
- `Bet:` load exact hook role instructions from TOML in Python instead of relying on Markdown-only prompts or agent-name prompting
- `Win:` one source of truth, deterministic hook behavior, and no install/runtime mismatch

### B -> A
- `Before:` stop-hook roles live as Markdown files, normal subagents live as TOML, and `evidence-reviewer` duplicates logic the main reviewer can own
- `After:` hook roles are TOML configs, `stop_hook.py` injects their exact instructions into `codex exec`, and reviewer handles both missing-result and completion-gate review
- `Outcome:` the hook path matches the repo contract and no longer depends on special-case role files

### Delta
- `Touch:` `agents/`, `config.toml.example`, `bin/stop_hook.py`, `bin/README.md`, selected docs, and stop-hook tests
- `Keep:` existing stop-hook schema, ticket review-packet gates, and fail-closed behavior
- `Change:` role loading mechanism and reviewer/evidence-review control flow
- `Delete/Avoid:` Markdown hook-role files and prompt-level “load agent by name” indirection

### Core Flow
```pseudo
load reviewer/orchestrator TOML config by role name
extract developer_instructions plus optional model settings
run codex exec with those exact instructions and JSON context
route all completion-gate review through reviewer
remove evidence-reviewer-specific files, logs, and docs
```

### Proof
- `P1:` direct hook-role loading uses TOML files only
- `P2:` completion review still forces same-ticket continuation on weak or stale review-packet state
- `P3:` config/docs/install surfaces all point to TOML role files
- `Risk:` reviewer contract changes could break stop-hook routing
- `Rollback:` restore the previous role files and `stop_hook.py` prompt loading path

### Plan Review
- `Refs:` `docs/prd.md`, `docs/MEMORY.md`, `docs/TROUBLES.md`, `bin/stop_hook.py`, `config.toml.example`, `tickets/templates/ticket.md`
- `Scope:` one commit focused on hook-role normalization
- `Proof:` unit coverage plus py_compile and smoke-style replay checks
- `Guardrails:` keep the hook deterministic, fail closed on missing role config, and avoid adding subagent indirection
- `Fixes:` no broader agent-surface redesign in this slice

### Delegation
- `Need:` Not needed
- `Why:` local refactor with a small, bounded test surface
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` implement the TOML loader, merge reviewer gating, then update docs and verification

### Ticket Move
- `Now:` `status: building`, `phase: building`
- `On approval:` n/a
- `Follow-ups:` only if further agent-surface normalization is needed beyond the hook path
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: stop-hook reviewer and orchestrator roles are canonical TOML configs under `agents/`
- [x] AC-2: `stop_hook.py` loads hook role instructions from TOML and no longer depends on `agents/*.md` role files
- [x] AC-3: `evidence-reviewer` is removed and reviewer owns completion-gate output
- [x] AC-4: config and docs describe the TOML-backed hook-role surface consistently
- [x] AC-5: stop-hook verification covers TOML role loading and merged reviewer gating behavior

## Working Notes
- Direct `codex exec` tests showed that naming an installed agent in the prompt does not auto-load its TOML config.
- Asking the model to “use the subagent” can work heuristically, but only after extra search/read/spawn behavior that is wrong for a deterministic hook path.

## Implementation Notes
- Touched areas: hook role configs, stop-hook runtime shim, docs, tests
- Reused patterns: existing TOML agent config format and current review-packet gate semantics
- Guardrails: fail closed when role config is missing or malformed

## Evidence
- [x] Tests
- [x] Typecheck / syntax verification
- [x] Lint / diff hygiene
- [x] QA / manual verification

- Commands:
  - `python3 -m py_compile bin/stop_hook.py bin/test_stop_hook.py`
  - `python3 -m unittest discover -s bin -p 'test_*.py'`
  - `git diff --check`
  - `python3 tickets/scripts/check_ticket_metadata.py`
- Manual verification:
  - direct `codex exec` checks showed that naming an installed agent in the prompt does not auto-load its TOML config
  - direct `codex exec` checks showed that explicitly injected `developer_instructions` do produce the expected role contract
- Residual note:
  - `python3 experiments/run_ralph_smoke_evals.py` still fails on the broader `hook_plan_payload` assertion in the current worktree, so the focused role-loading and reviewer-gate checks pass but the full Ralph smoke suite is not green in this workspace snapshot

## Review Packet
- `reviewed_at:` 2026-04-08 17:08 +0100
- `rubrics_used:` ["code-quality", "debloatability", "evidence-quality", "integration-readiness"]
- `overall_score:` 4.5
- `overall_threshold:` 4.0
- `overall_verdict:` pass
- `rerun_required:` false
- `evidence_quality:` pass
- `integration_readiness:` pass
- `traceability:` pass
- `freshness:` pass
- `hard_gate_failures:` []
- `blocking_findings:` []
- `next_action:` keep the TOML hook-role path as the canonical implementation and avoid reintroducing Markdown-only hook prompts

## Blockers
- none

## Handoff
- Current state: implemented and documented; the active hook path now loads TOML role configs and the reviewer owns completion gating
- Resume from: no follow-up required for this slice unless a later ticket wants a broader agent-surface normalization pass

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
