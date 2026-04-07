---
ticket_id: TASK-0023
title: add harness engineering quickstart
phase: complete
status: done
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-07T04:27:36Z
updated_at: 2026-04-07T04:30:46Z
next_action: archived; use the new quickstart as the canonical starting point for future harness-tuning experiments
last_verification: manual review passed; verified the new spec, spec index, history writeback, and ticket with git diff --check clean on the changed files
linked_docs:
  - docs/specs/harness-engineering-quickstart.md
  - docs/specs/README.md
---

# TASK-0023: add harness engineering quickstart

## Summary
Add a durable quickstart that tells an agent which harness surfaces exist, what each one controls, and what to change first when trying to improve performance.

## Scope
- In: a practical canonical guide for harness tuning across `AGENTS.md`, hooks, subagents, skills, MCP/tooling, and review gates
- Out: new runtime machinery or a broad harness rewrite

## Plan

### Pitch
- `Req:` give agents a quickstart for autonomously tuning the harness
- `Bet:` a concrete map of harness levers plus a ranked experimentation loop will improve agent self-direction more than another abstract architecture note
- `Win:` agents can identify the next best harness variable to change without guessing

### B -> A
- `Before:` harness knowledge is spread across specs, prompts, hooks, and skills
- `After:` one canonical quickstart says what the levers are, what they affect, and how to run safe experiments
- `Outcome:` review-loop-first harness engineering becomes explicit and reusable

### Delta
- `Touch:` `docs/specs/README.md`, `docs/HISTORY.md`, new quickstart doc, and this ticket
- `Keep:` existing review-gates and spec-first execution model
- `Change:` discoverability and operator guidance for harness tuning
- `Delete/Avoid:` vague advice that does not map to repo surfaces

### Core Flow
```pseudo
inspect current harness surfaces and review-loop specs
read external harness references
write a canonical quickstart focused on practical tuning order
review the docs and write ticket evidence
archive the completed ticket
```

### Proof
- `P1:` the doc explicitly maps failure modes to concrete harness surfaces
- `P2:` the doc gives a ranked experimentation order with review loops first
- `Risk:` the guidance drifts into research-summary prose instead of an actionable quickstart
- `Rollback:` trim the doc back to operator checklists and repo-specific mappings

### Plan Review
- `Refs:` root `AGENTS.md`, `docs/specs/review-gates.md`, `docs/specs/spec-first-execution-loop.md`, linked external articles
- `Scope:` one canonical quickstart doc plus writeback only
- `Proof:` manual review of changed Markdown for correctness and consistency
- `Guardrails:` no speculative runtime work; no hidden control plane
- `Fixes:` keep recommendations tied to files already present in this repo

### Delegation
- `Need:` Not needed
- `Why:` bounded doc work with local context already gathered
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` finish the doc, run a review pass, then archive

### Ticket Move
- `Now:` `status: building`, `phase: building`
- `On approval:` n/a; direct user request already authorizes execution
- `Follow-ups:` none required if the doc is clear
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: a canonical doc explains the main harness levers in this repo and what each lever changes
- [x] AC-2: the doc gives an opinionated tuning order with review loops first
- [x] AC-3: the doc provides an experiment loop for autonomous harness improvement
- [x] AC-4: specs/history writeback makes the new guide discoverable

## Working Notes
- The document should read like an operator playbook, not like exploratory research.
- Keep the mental model compact: subagent, skill, hook, MCP, ticket, review gate.

## Implementation Notes
- Touched areas: `docs/specs/`, `docs/HISTORY.md`, `tickets/`
- Reused patterns: canonical spec style, review-gates language, ticket closeout shape
- Guardrails: no claims that the current repo already automates more than it does

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Validation details:
  - reviewed `docs/specs/harness-engineering-quickstart.md` for repo-surface accuracy against `AGENTS.md`, `hooks.json`, `bin/stop_hook.py`, `config.toml.example`, and the current orchestration/review specs
  - reviewed external references from Anthropic and Cursor to align the quickstart with planner/worker/evaluator lessons
  - ran `git diff --check -- docs/specs/harness-engineering-quickstart.md docs/specs/README.md docs/HISTORY.md tickets/archive/TASK-0023-harness-engineering-quickstart.md`
  - code-review pass: `work_type=planning`, `rubrics_used=[planning-rubric]`, `overall_score=94`, `verdict=pass`, `rerun_required=false`

## Blockers
- none

## Handoff
- Current state: the harness quickstart is now a canonical spec and the writeback is complete.
- Resume from: `docs/specs/harness-engineering-quickstart.md` if future harness experiments need a starting playbook.

## Writeback
- Update this ticket as work progresses.
- When the doc and review pass are complete, archive the ticket.
