---
ticket_id: TASK-0093
title: strengthen shipped modularity doctrine in global agents contract
phase: complete
status: done
owner: codex
claimed_by: codex
priority: medium
depends_on: []
blocked_by: []
ready: true
approval_required: false
requires_qa: false
requires_demo: false
created_at: 2026-04-24T20:23:05Z
updated_at: 2026-04-24T20:26:33Z
next_action: archived
last_verification: review artifact written and `python3 tickets/scripts/check_ticket_metadata.py` passed before archive
linked_docs:
  - templates/global/AGENTS.md
  - docs/MEMORY.md
  - docs/HISTORY.md
---

# TASK-0093: strengthen shipped modularity doctrine in global agents contract

## Summary
Tighten the install-time global `AGENTS.md` so modularity is treated as an
explicit default, not a vague preference. The shipped contract should steer UI,
utilities, backend seams, planning, and delegation toward feature-first,
extractable modules.

## Scope
- In: global contract wording for modular design defaults, durable memory, and
  history writeback
- Out: repo-local orchestration changes, new validators, or workflow hooks

## Plan
- `Change:` add a stronger modularity doctrine to the shipped global contract
- `Why:` the current `modular by default` rule is too abstract and does not
  guide folder shape, backend seams, or planning boundaries clearly enough
- `Before -> After:` generic modularity preference -> explicit feature-first,
  extractable-module, service-ready, subagent-friendly guidance
- `Touch:` `templates/global/AGENTS.md`, `docs/MEMORY.md`, `docs/HISTORY.md`
- `Inspect:` `templates/global/AGENTS.md`, `docs/specs/harness-engineering-doctrine.md`, `docs/MEMORY.md`, `docs/HISTORY.md`, `tickets/templates/ticket.md`
- `Signature delta:` none
- `Type Sketch:` none
- `Typed flow example:` none
- `Recommendation:` update `templates/global/AGENTS.md` as the primary surface
  because this is a shipped cross-repo operating contract; log the invariant in
  `docs/MEMORY.md`; append `docs/HISTORY.md`
- `Blast radius:` future generated/global agent behavior across repos that use
  the shipped template
- `Risks:` wording that over-encourages premature abstraction; keep the rule
  framed as modular structure with small high-impact main-loop changes rather
  than speculative architecture

## Gap Analysis
- `Current state:` the global contract says `modular by default` and
  `modules should stay extractable`, but does not define preferred module
  boundaries or folder strategy
- `Production expectation:` a credible cross-repo contract should state that UI
  components, utilities, backend capabilities, and plans should bias toward
  feature-first, extractable modules with clear ownership seams
- `Missing gaps:` no explicit guidance for component directories, feature-first
  structure, microservice-ready backend seams, or subagent-sized ownership
- `Comparable implementations:` local harness doctrine only
- `Recommendation:` land the global wording now; defer mechanical enforcement to
  future tickets only if repeated failures justify validators or hook changes

## Acceptance Criteria
- [x] AC-1 global `AGENTS.md` explicitly defines modular structure expectations
- [x] AC-2 durable invariant logged in `docs/MEMORY.md`
- [x] AC-3 change appended to `docs/HISTORY.md`

## Verification
- `Tests:` `python3 tickets/scripts/check_ticket_metadata.py`
- `Manual checks:` review the diff for accurate placement, correct surface selection, and install-path consistency through `install.sh`
- `Evidence required:` diff plus final file state and a linked review artifact
- `Artifacts path:` `tickets/archive/TASK-0093/artifacts/`

## Evidence
- `Artifacts:` `tickets/archive/TASK-0093/artifacts/review-2026-04-24T202522Z.json`
- `Commands:` `git diff -- templates/global/AGENTS.md docs/MEMORY.md docs/HISTORY.md tickets/archive/TASK-0093/ticket.md`; `python3 tickets/scripts/check_ticket_metadata.py`
- `Result summary:` global modularity doctrine landed in the shipped template, durable docs were updated, and the review pass found no blocking drift. `install.sh` was checked to confirm the template is the live global link source.

## Blockers
- none
