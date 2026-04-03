---
ticket_id: TASK-0002
title: add notion-style ticket metadata foundation
phase: complete
status: complete
owner: codex
priority: high
depends_on:
  - TASK-0001
blocked_by: []
ready: false
approval_required: false
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-03T05:05:00Z
next_action: none; the v1 ticket metadata contract is locked and downstream runtime or autonomy work must stay outside this ticket unless a later ticket explicitly re-opens scope
last_verification: manual review of README, config example, installer, AGENTS, memory/history, and the ticket board after the v1 coherence pass
linked_docs:
  - docs/research/web-research/2026-04-02_run-artifacts-risk-analysis.md
  - docs/research/web-research/2026-04-02_codexter-change-proposal.md
---

# TASK-0002: add notion-style ticket metadata foundation

## Summary
Reconsider the earlier runtime-state direction and define a Notion-style ticket contract where frontmatter holds fixed machine-readable metadata, the Markdown body holds flexible task memory, folder placement acts as the Kanban view, and durable knowledge is promoted into docs on completion.

## Scope
- In: fixed frontmatter schema, constrained ticket-body sections, DAG/dependency fields, ownership rules between `tickets/` and `docs/`, completion/documentation lifecycle, and folder-level README guidance
- Out: separate runtime state files, `run_id`, per-run trees, hooks, automation, evaluator scoring, team runtime, external Kanban tools

## Plan

### Pitch
- `Req:` give Codexter one canonical active-task object that works for both humans and agents without introducing a second orchestration system
- `Bet:` use Notion-style tickets on disk: frontmatter for fixed metadata, Markdown body for flexible task memory, and folder placement for board state
- `Win:` active work stays visible in folders, machine-readable metadata stays typed and compact, and task-local memory stays attached to the task without extra state files

### B -> A
- `Before:` tickets, docs, and proposed runtime-state ideas are drifting toward multiple overlapping systems with unclear ownership
- `After:` each active ticket is the single task object: frontmatter is machine-readable metadata, the body is task-local working memory, and docs remain the durable post-completion record
- `Outcome:` Codexter gets Kanban visibility, DAG/task readiness, and agent-usable state without overengineering a separate runtime layer

### Delta
- `Touch:` ticket template, active ticket contract docs, active tickets, `tickets/INDEX.md`, and any planning docs that still assume separate runtime state
- `Keep:` `tickets/` as the active Kanban surface and `docs/` as the durable memory surface
- `Change:` move only non-lane machine-readable state into ticket frontmatter, keep folder placement as the Kanban source of truth, and formalize ticket-body sections as task-local memory/evidence/handoff space
- `Delete/Avoid:` avoid separate state files, `run_id`, parallel artifact trees, hidden automation, and any metadata that does not directly improve active-task routing or resume

### Core Flow
```pseudo
study current ticket/docs surfaces
define one fixed frontmatter schema for all active tickets
keep schema small and typed:
  identity, phase, status, owner, priority, depends_on, blocked_by,
  ready, approval_required, timestamps, next_action, last_verification,
  linked_docs
define constrained body sections for:
  summary, scope, plan, working notes, evidence, blockers, handoff
document ownership split:
  ticket frontmatter = machine-readable task metadata
  ticket body = task-local memory and execution notes
  folder placement = Kanban lane / lifecycle view
  folder README = local design rationale
  docs/* = durable post-completion memory
document lifecycle:
  todo -> review -> building -> documenting -> complete
  after documenting, archive/delete ticket and promote durable notes into docs
apply the canonical dialect to all active review/building tickets
```

### Proof
- `P1:` the repo defines one fixed frontmatter schema that is enough for active-task routing, readiness, and quick inspection without a separate state file or a duplicated `lane` field
- `P2:` a reviewer can open one ticket and see both machine-readable state and human-readable task memory without ambiguity about where truth lives
- `P3:` the lifecycle explains exactly when task-local memory stays in the ticket and when durable knowledge is promoted into docs
- `Risk:` frontmatter grows too large or ticket bodies become junk drawers instead of constrained task objects
- `Rollback:` revert the ticket schema changes and return to the looser current template until a smaller metadata set is agreed

### Plan Review
- `Refs:` `docs/research/web-research/2026-04-02_codexter-change-proposal.md`, `docs/research/web-research/2026-04-02_codexter-vs-omx-gap-analysis.md`, `docs/research/web-research/2026-04-02_run-artifacts-risk-analysis.md`, `docs/research/web-research/2026-04-02_anthropic-harness-comparison.md`, `tickets/templates/ticket.md`, `AGENTS.md`
- `Scope:` pass; narrowed further from runtime-state design to one ticket-contract redesign only
- `Proof:` pass; the slice is reviewable by inspecting the frontmatter schema, body conventions, ownership split, state matrix, and documentation lifecycle
- `Guardrails:` pass; keeps active Kanban visible, avoids second-system complexity, and preserves the no-hidden-continuation rule
- `Fixes:` replaced separate-state assumptions with ticket-frontmatter metadata, moved working memory into the ticket body, made doc promotion the completion boundary, and migrated active tickets to the canonical dialect

### Delegation
- `Need:` `Not needed`
- `Why:` small architecture/doc contract slice
- `Artifact:` none

### Ask
- `Ready: yes`
- `Next:` keep downstream tickets aligned with the ticket-metadata contract as later loops touch them

### Ticket Move
- `Now:` `tickets/building/`
- `On approval:` `approved`
- `Follow-ups:` `TASK-0003`, `TASK-0005`, `TASK-0006`, `TASK-0007`
- `Blocked in building?:` `no`

## Acceptance Criteria
- [x] AC-1: ticket frontmatter is documented as the canonical machine-readable metadata surface for active tasks
- [x] AC-2: the frontmatter schema is frozen to a minimal fixed field set that supports routing, DAG readiness, and quick resume without duplicating board-lane state
- [x] AC-3: ticket body section conventions are explicit and separate task-local memory from durable docs memory
- [x] AC-4: the contract explicitly rejects separate runtime state files, `run_id`, run trees, and hidden automation in v1
- [x] AC-5: the completion lifecycle makes documentation writeback a required phase before a ticket can be removed or archived

## Working Notes
- Refined v1 by removing `lane` from frontmatter so board state lives in exactly one place: the ticket's folder path.
- Kept the remaining fields because they still serve routing, readiness, resume, and passive metadata updates without adding a second state system.
- Locked the active board and todo backlog to one frontmatter dialect and made `tickets/INDEX.md` explicitly non-authoritative.

## Implementation Notes
- Touched areas: docs/contracts/templates, active tickets, and the ticket index
- Reused patterns: Codexter file-based tickets and durable docs
- Guardrails: no auto-continue, no hidden runtime behavior, no team complexity, no second orchestration system, no oversized frontmatter schema

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification

## Blockers
- none

## Handoff
- Current state: contract docs, template, index wording, active tickets, and the todo backlog now share one canonical ticket dialect, and assisted continuation is explicitly parked outside the v1 foundation.
- Resume from: downstream tickets such as `TASK-0005`, `TASK-0008`, and `TASK-0009` only if later loops need to keep post-foundation work aligned with this boundary.

## Writeback
- Update this ticket as work progresses.
- Move the ticket and update `tickets/INDEX.md` when its board state changes.
