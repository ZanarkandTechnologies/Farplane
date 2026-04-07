---
ticket_id: TASK-0021
title: simplify ralph runtime surface
phase: complete
status: done
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-07T00:00:00Z
updated_at: 2026-04-07T00:00:00Z
next_action: archived; follow-on runtime deletion or shim rewrites can consume the documented keep/remove/rewrite decisions without reopening the control-plane question
last_verification: documented the canonical runtime-surface decisions in docs/specs/ralph-runtime-surface.md and rewrote the main bin/docs surfaces so `$impl` is the control plane and legacy binaries are transitional
linked_docs:
  - docs/specs/spec-first-execution-loop.md
  - docs/specs/orchestrator-subagent-loop.md
  - bin/README.md
  - docs/specs/ralph-runtime-surface.md
---

# TASK-0021: simplify ralph runtime surface

## Summary
Reduce the Ralph runtime surface so the system relies more on prompts + `codex exec` and less on a pile of Python helpers that are hard to reason about.

## Scope
- In: identify which Ralph binaries are still load-bearing, decide what stays as a thin shim, and define which scripts/docs should be removed or rewritten
- Out: implementing the full new orchestrator loop in this ticket

## Acceptance Criteria
- [x] AC-1: there is one explicit keep/remove/rewrite decision for each current Ralph runtime binary
- [x] AC-2: the target runtime model is prompt-first, with only minimal hook/runtime shims left in `bin/`
- [x] AC-3: docs no longer imply that the archived prototype binaries are the primary future control plane

## Evidence
- [ ] Tests
- [x] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Validation details:
  - `python3 -m py_compile bin/stop_hook.py`
  - reviewed `docs/specs/ralph-runtime-surface.md`
  - reviewed `bin/README.md`
  - reviewed `docs/specs/README.md`
  - reviewed `docs/specs/ralph-orchestration-blueprint.md`

## Blockers
- none

## Handoff
- Current state: the binary fate decisions are now explicit and the public docs treat `$impl` as the control plane while keeping only thin runtime/operator shims in the foreground.
- Resume from: `docs/specs/ralph-runtime-surface.md`, `bin/README.md`, and any future deletion ticket that retires `ralph_worker.sh` or `ralph_orchestrate.py`.

## Writeback
- Update this ticket as work progresses.
- Update `status` and `phase` in frontmatter when queue state changes.
