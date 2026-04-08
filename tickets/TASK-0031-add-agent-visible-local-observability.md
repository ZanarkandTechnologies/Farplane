---
ticket_id: TASK-0031
title: add agent visible local observability
phase: planning
status: review
owner: codex
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: true
created_at: 2026-04-08T01:54:29Z
updated_at: 2026-04-08T01:54:29Z
next_action: review and approve the observability slice before implementation starts
last_verification: backlog ticket created from cross-source harness gap analysis
linked_docs:
  - docs/specs/harness-techniques.md
  - skills/runtime-debugging/SKILL.md
  - docs/specs/ralph-v2-direction.md
---

# TASK-0031: add agent visible local observability

## Summary
Extend agent legibility beyond browser/UI evidence by exposing a small local observability surface for runtime debugging, reliability, and performance tasks.

## Scope
- In: one lightweight log/metric/trace feedback path that agents can read during work and verification
- Out: a production-grade monitoring stack or hosted telemetry platform

## Plan

### Pitch
- `Req:` fix the weakness where agents can see UI/browser state well but still lack equivalent feedback for runtime and performance work
- `Bet:` expose one local observability path instead of building a large telemetry system
- `Win:` better debugging loops and better grounding for non-UI tickets

### B -> A
- `Before:` UI evidence is strong, but runtime evidence is still comparatively thin
- `After:` agents can inspect one local observability surface during debugging or verification
- `Outcome:` better root-cause analysis and fewer blind fixes

### Delta
- `Touch:` runtime-debugging workflow, one local observability artifact path, maybe ticket evidence expectations for backend/runtime work
- `Keep:` lightweight repo posture and local-first execution
- `Change:` make logs/metrics/traces legible to the agent for one bounded class of tasks
- `Delete/Avoid:` jumping straight to a heavyweight monitoring platform

### Core Flow
```pseudo
run the target task or repro
capture local log or metric artifacts in a standard place
let the agent read and reason over that artifact
use the same surface during verification
```

### Proof
- `P1:` at least one runtime or perf task can use the new observability surface during debugging
- `P2:` the artifacts are easy for agents to find and interpret
- `Risk:` build a lot of telemetry without improving real debugging
- `Rollback:` keep the first slice to one local observability path only

### Plan Review
- `Refs:` OpenAI agent-legibility framing, Anthropic observability gaps, `runtime-debugging` skill, `harness-techniques.md`, `ralph-v2-direction.md`
- `Scope:` local observability only
- `Proof:` one debugging or perf replay case
- `Guardrails:` no hosted infra requirement and no broad telemetry platform
- `Fixes:` choose the smallest surface with clear signal

### Delegation
- `Need:` Not needed
- `Why:` planning slice only
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` move to building and implement the first local observability surface

### Ticket Move
- `Now:` `status: review`, `phase: planning`
- `On approval:` set `status: building` and implement the local observability slice
- `Follow-ups:` may split logging, metrics, and trace surfaces if needed
- `Blocked in building?:` no

## Acceptance Criteria
- [ ] AC-1: one local observability artifact path is standardized for agent use
- [ ] AC-2: runtime-debugging or verification workflows can consume that artifact directly
- [ ] AC-3: one replayable runtime/perf case demonstrates improved debugging signal

## Working Notes
- Main weakness: agent legibility is much stronger for UI than for runtime behavior.
- Blog technique mapping: OpenAI’s application legibility emphasis plus Anthropic’s observability gap analysis.

## Implementation Notes
- Touched areas: runtime-debugging workflow, artifact conventions, maybe backend evidence expectations
- Reused patterns: local artifact writeback and ticket evidence
- Guardrails: stay local and lightweight

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [ ] QA / manual verification

## Review Packet
- `reviewed_at:` 2026-04-08 01:54 +0100
- `rubrics_used:` implementation-plan,evidence-quality
- `overall_score:` 90
- `overall_verdict:` pass
- `rerun_required:` false
- `blocking_findings:` none
- `next_action:` hold in review until approved for implementation

## Blockers
- none

## Handoff
- Current state: planning ticket created for the first local observability slice.
- Resume from: `docs/specs/harness-techniques.md` and `skills/runtime-debugging/SKILL.md`

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
