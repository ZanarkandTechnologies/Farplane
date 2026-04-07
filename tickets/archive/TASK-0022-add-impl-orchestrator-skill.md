---
ticket_id: TASK-0022
title: add impl orchestrator skill
phase: complete
status: done
owner: codex
priority: high
depends_on:
  - TASK-0006
  - TASK-0003
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-07T00:00:00Z
updated_at: 2026-04-07T00:00:00Z
next_action: archived; follow with TASK-0021 to simplify the remaining Ralph/bin runtime surface around the new $impl control plane
last_verification: added skills/impl/SKILL.md, updated the orchestration specs + README, and wired AGENTS.md so $impl is the explicit build-phase orchestrator surface
linked_docs:
  - docs/specs/spec-first-execution-loop.md
  - docs/specs/orchestrator-subagent-loop.md
  - skills/impl/SKILL.md
---

# TASK-0022: add impl orchestrator skill

## Summary
Create the user-facing `$impl` skill that acts as the orchestrator contract for the build phase, spawning ephemeral orchestration runs and worker panes without a permanent orchestrator pane.

## Scope
- In: the `$impl` skill contract, how it reads state and tickets, how it spawns builder/reviewer/QA/evidence-check workers, and the operator UX around panes/status
- Out: full dispatcher/runtime implementation in this ticket

## Acceptance Criteria
- [x] AC-1: a dedicated `$impl` skill exists as the orchestration entrypoint
- [x] AC-2: the contract explicitly says the orchestrator runs ephemerally and worker panes are the primary visible runtime surface
- [x] AC-3: the contract explains how Stop hook re-invokes the same orchestration behavior after worker completion

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Validation details:
  - confirmed no existing active ticket or spec already owned the dedicated `$impl` skill surface
  - reviewed `skills/impl/SKILL.md`
  - reviewed `docs/specs/spec-first-execution-loop.md`
  - reviewed `docs/specs/orchestrator-subagent-loop.md`
  - reviewed `AGENTS.md`
  - reviewed `README.md`

## Blockers
- none

## Handoff
- Current state: `$impl` is now the explicit public build-phase orchestration surface and the queue has been cleaned up to treat the older loop/spec tickets as completed contracts.
- Resume from: `skills/impl/SKILL.md`, `docs/specs/spec-first-execution-loop.md`, `docs/specs/orchestrator-subagent-loop.md`, and `TASK-0021`.

## Writeback
- Update this ticket as work progresses.
- Update `status` and `phase` in frontmatter when queue state changes.
