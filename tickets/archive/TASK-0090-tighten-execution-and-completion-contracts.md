---
ticket_id: TASK-0090
title: tighten execution and completion contracts
phase: complete
status: done
owner: codex
claimed_by:
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: false
requires_qa: false
requires_demo: false
created_at: 2026-04-24T22:55:00Z
updated_at: 2026-04-24T23:05:00Z
next_action: none
last_verification: `python3 -m py_compile bin/user_turn.py bin/stop_hook.py skills/impl/scripts/tmux_helper.py`; `python3 -m unittest bin/test_runtime_state.py bin/test_stop_hook.py bin/test_tmux_helper.py bin/test_harness_invariants.py`; `python3 tickets/scripts/check_ticket_metadata.py`; `python3 bin/check_harness_invariants.py`
linked_docs:
  - docs/specs/runtime-surface.md
  - docs/specs/spec-first-execution-loop.md
  - docs/specs/review-gates.md
  - docs/specs/harness-techniques.md
  - docs/specs/harness-engineering-quickstart.md
  - templates/global/AGENTS.md
  - AGENTS.md
---

# TASK-0090: tighten execution and completion contracts

## Summary
Tighten the harness so `$impl` has explicit internal execution phases, Stop hook
can mechanically advance `impl -> qa -> demo`, the final completion reviewer is
named clearly, and operator-facing feature summaries are easier to scan.

## Scope
- In:
  - `$impl` execution-phase runtime seeding and Stop-hook progression
  - explicit `requires_qa` / `requires_demo` ticket flags
  - public `$qa` / `$demo` recovery surfaces
  - stronger final completion-review fields for QA quality, demo quality, and
    stakeholder readiness
  - renaming the Stop-hook `reviewer` role to `completion-reviewer`
  - global/local response-style guidance for `Before` / `After` / `Example`
- Out:
  - pushing or publishing
  - splitting the broader dirty worktree into multiple historical commits

## Plan
- `Change:` land one cohesive harness-contract slice covering execution-phase
  progression, final completion gating, reviewer-role naming clarity, and the
  global response-style rule for feature explanations.
- `Why:` these changes all tighten the same trust boundary: the assistant should
  not stop early, weak proof should not pass the final gate, role names should
  be unambiguous, and final operator-facing explanations should be easier to
  understand.
- `Before -> After:` before, `$impl` only carried loop ownership, the Stop-hook
  reviewer role name was generic, and feature summaries could still come back as
  dense prose; after, runtime carries `execution_phase`, the final gate can
  judge QA/demo/stakeholder readiness explicitly, the role is named
  `completion-reviewer`, and the shipped response contract prefers short
  `Before` / `After` / `Example` bullets.
- `Touch:` runtime and Stop-hook code under `bin/`, the `agents/` role files,
  `skills/impl`, `skills/qa`, `skills/demo`, review/QA references, the ticket
  contract, and the global/local AGENTS surfaces.
- `Inspect:` current runtime contract, review-gate docs, active ticket rules,
  and Stop-hook tests.
- `Signature delta:` `bin/user_turn.py / capture_user_turn(...): seeds execution_phase + phase_requirements`; `bin/stop_hook.py / decide_impl_transition(...): advance impl|qa|demo before completion`; `agents/completion-reviewer.toml / completion gate reviewer: final sufficiency role`.
- `Blast radius:` Stop-hook routing, runtime state, ticket metadata, QA/demo
  proof expectations, and future operator-facing completion summaries.
- `Risks:` the runtime contract could drift from docs/tests if not committed as
  one slice; the final reviewer rename could break hardcoded file lookups if any
  references are missed.

## Acceptance Criteria
- [x] AC-1: `$impl` runtime carries explicit execution phases and phase
      requirements for `impl`, `qa`, and `demo`
- [x] AC-2: Stop hook advances mechanically through required execution phases
      before final completion review
- [x] AC-3: the Stop-hook role is renamed clearly enough to distinguish it from
      `code-reviewer`
- [x] AC-4: final completion review can explicitly fail weak QA/demo output and
      PM/CEO-readiness
- [x] AC-5: future feature explanations default to shorter `Before` / `After` /
      `Example` summaries

## Verification
- `Tests:` `python3 -m unittest bin/test_runtime_state.py bin/test_stop_hook.py bin/test_tmux_helper.py bin/test_harness_invariants.py`
- `Manual checks:` inspect the renamed agent file, the new `$qa` / `$demo`
  skills, and the global/local AGENTS wording for the new response-style rule
- `Evidence required:` one review artifact plus the command/check summary for
  the committed slice
- `Artifacts path:` `tickets/artifacts/TASK-0090/`

## Refs
- `docs/specs/runtime-surface.md`
- `docs/specs/spec-first-execution-loop.md`
- `docs/specs/review-gates.md`

## Evidence
- `Artifacts:` [final-review.md](/Users/kenjipcx/coding-harness/Codexter/tickets/artifacts/TASK-0090/review/final-review.md)
- `Commands:` `python3 -m py_compile bin/user_turn.py bin/stop_hook.py skills/impl/scripts/tmux_helper.py`; `python3 -m unittest bin/test_runtime_state.py bin/test_stop_hook.py bin/test_tmux_helper.py bin/test_harness_invariants.py`; `python3 tickets/scripts/check_ticket_metadata.py`; `python3 bin/check_harness_invariants.py`
- `Result summary:` runtime, Stop-hook, tmux-helper, and invariant tests passed for the selected execution/closeout slice; review artifact linked; modular commit prepared; no push performed

## Blockers
- none
