---
name: update-memory
description: "Turn project history, memory, README, docs, lessons, troubles, and recent progress into consolidated project context and doc deltas."
tier: 3
group: project-ops
source: local
template_uses:
  skill-template: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash

---

# Update Memory

## Context

Use this as the generic project context refresh primitive. It is called by a PM
heartbeat when a project needs its durable memory and documentation state
consolidated for future agents or humans.

This skill updates project memory and docs surfaces; it does not own skill
hardening. Fresh lesson/trouble rows that should become evals or gotchas route
to `skill-maintenance(mode: harden_skill)`.

Do not split docs consolidation into a separate recurring job by default.
Route substantial prose cleanup through `documentation`, but keep the weekly PM
job as one context upkeep pass unless the docs have become large enough to need
a dedicated ticket or cadence.

## Automation Presets

`update-memory.project_context @7d -> reports.update_memory`

Use when a project PM heartbeat needs durable memory, README, docs, history,
lesson, and trouble consolidation. The automation manifest supplies cadence,
freshness, reports, gates, and project-local extensions; this skill owns default
source reads, candidate classification, hardening handoffs, output fields, and
review routing.

Eval surface: missing-source labeling, one-off observation rejection,
skill-hardening handoff routing, and append-only ledger preservation.

## Skill Signature

```text
update_memory(project_root?, readme?, docs?, memory?, history?, lessons?, troubles?, recent_progress?)
  -> memory_delta
   + readme_delta
   + docs_delta
   + docs_consolidation_plan?
   + history_candidates
   + lesson_or_trouble_promotions
   + stale_context_notes
state: reads(README, docs/**/*.md, docs/MEMORY.md, docs/HISTORY.md, docs/LESSONS.md, docs/TROUBLES.md, tickets/progress/PM reports); writes docs only when an owning project path and approval are explicit
gates: source_files_read; docs_owner_identified; no_raw_transcripts; promotion_threshold_named; stale_context_labeled; skill_hardening_routed_out
routes: documentation | skill-maintenance:harden_skill | review | ticket/spec owner
fails: dumps chat memory into docs; promotes one-off observations; edits skill evals/gotchas directly; rewrites append-only ledgers
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the project memory surfaces.
  - [ ] Resolve project root and read README plus `docs/MEMORY.md`,
    `docs/HISTORY.md`, `docs/LESSONS.md`, and `docs/TROUBLES.md` when present.
  - [ ] Inspect relevant `docs/**/*.md` owners when recent progress implies a
    durable documentation change.
  - [ ] Read recent progress, PM reports, ticket progress, or supplied context.
  - [ ] Label missing files instead of inventing project state.
- [ ] 2. Classify candidate updates.
  - [ ] `README` gets current high-level project shape, commands, and entry
    points that humans or agents need soon.
  - [ ] Topic docs under `docs/` get durable explanations, specs, runbooks, or
    framework guidance that would be too detailed for README or MEMORY.
  - [ ] `MEMORY` gets durable invariants and constraints.
  - [ ] `HISTORY` gets meaningful timeline events, not routine code deltas.
  - [ ] `LESSONS` gets distilled prevention lessons after proof or correction.
  - [ ] `TROUBLES` remains raw repeated misses or correction pain, not a
    cleanup target.
- [ ] 3. Route skill-hardening material out.
  - [ ] If a lesson/trouble should become evals, gotchas, QA guardrails, or
    skill-package changes, produce a `skill-maintenance(mode: harden_skill)`
    handoff rather than editing those surfaces here.
- [ ] 4. Produce compact deltas.
  - [ ] Prefer precise patch-sized deltas over large rewritten docs.
  - [ ] Use [documentation](../documentation/SKILL.md) for substantial prose
    cleanup, duplicate-doc consolidation, or docs-folder rewrites.
  - [ ] Create a docs consolidation ticket when the docs need a larger merge,
    split, archive, or owner decision.
  - [ ] Preserve append-only ledgers unless the project contract explicitly
    allows consolidation.
  - [ ] Remove or flag stale context only when evidence shows it is stale.
- [ ] 5. Finish with proof and next route.
  - [ ] Report files read, proposed deltas, skipped promotions, stale notes,
    and routed hardening handoffs.
  - [ ] Use [documentation](../documentation/SKILL.md) for substantial prose
    cleanup and [review](../review/SKILL.md) for material memory changes.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

```text
Memory Update
- project:
- source files:
- recent progress refs:
- README delta:
- docs delta:
- docs consolidation plan:
- MEMORY delta:
- HISTORY candidates:
- LESSON/TROUBLE promotions:
- skill hardening handoffs:
- stale context notes:
- skipped items:
- next route:
```

## Gotchas

- Do not turn memory refresh into strategy planning; use `update-strategy` for
  bets, priorities, experiments, and tickets.
- Do not create a separate docs heartbeat by default; route substantial docs
  work through `documentation` inside this context update or create a focused
  ticket when it is too large.
- Do not promote one-off observations into durable memory.
- Do not rewrite append-only logs to mark processing complete; use processed
  state or handoff records.
- Do not edit skill evals or gotchas directly from memory upkeep; route to
  `skill-maintenance(mode: harden_skill)`.

## Reference Map

- [../documentation/SKILL.md](../documentation/SKILL.md) - use for substantial
  doc-quality rewriting.
- [../skill-maintenance/SKILL.md](../skill-maintenance/SKILL.md) - route
  lesson/trouble-derived evals, gotchas, or skill-package changes.
- [../review/SKILL.md](../review/SKILL.md) - use for material memory or
  evidence-quality judgment.
- [../../docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md](../../docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md)
  - shared project harness and PM heartbeat vocabulary.

## Output

- `memory_delta`
- `readme_delta`
- `docs_delta`
- `docs_consolidation_plan`
- `history_candidates`
- `lesson_or_trouble_promotions`
- `stale_context_notes`
- `skill_hardening_handoffs`
