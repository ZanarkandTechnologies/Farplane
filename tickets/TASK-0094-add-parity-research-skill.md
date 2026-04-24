---
ticket_id: TASK-0094
title: add parity research skill
phase: complete
status: done
owner: codex
claimed_by:
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: false
requires_qa: false
requires_demo: false
created_at: 2026-04-24T19:42:00+0100
updated_at: 2026-04-24T19:58:00+0100
next_action: archive the ticket after this change set lands cleanly
last_verification: 2026-04-24 19:58 +0100 | ticket metadata OK; structural doc parity OK; harness invariants OK; `git diff --check --cached` OK; fresh review pass (4.1/5.0)
linked_docs:
  - AGENTS.md
  - templates/global/AGENTS.md
  - docs/specs/harness-techniques.md
  - docs/MEMORY.md
  - docs/HISTORY.md
  - skills/gap-analysis/SKILL.md
  - skills/parity-research/SKILL.md
---

# TASK-0094: add parity research skill

## Summary
Ship a separate `parity-research` skill for external comparable-products,
standards, docs, and open-source repo analysis. Keep it distinct from
`gap-analysis`, which should stay focused on current repo state versus
production expectation for one feature or ticket slice.

## Scope
- In:
  - `skills/parity-research/` as a first-class skill package
  - a tighter `gap-analysis` boundary
  - missing module docs for `gap-analysis`
  - canonical router/docs updates for the new skill
  - durable memory/history writeback
- Out:
  - merging research, planning, and debugging into one umbrella skill
  - runtime-debugging changes
  - new hooks, subagents, or validators

## Plan
- `Change:` add a dedicated parity-comparison skill, then route broader external
  "what do others include?" questions to it while keeping `gap-analysis`
  responsible for local feature-gap scoping.
- `Why:` the repo already had a lightweight gap-analysis contract, but the user
  explicitly wanted a separate skill boundary for broader comparable-product and
  comparable-codebase research.
- `Before -> After:` before, `gap-analysis` implicitly covered parity-driven
  work and had no module docs; after, `parity-research` owns external parity
  comparison, `gap-analysis` stays narrower, and both modules are discoverable.
- `Touch:` `skills/parity-research/*`, `skills/gap-analysis/*`, `AGENTS.md`,
  `templates/global/AGENTS.md`,
  `docs/specs/harness-techniques.md`, `docs/MEMORY.md`, `docs/HISTORY.md`
- `Inspect:` `skills/gap-analysis/SKILL.md`,
  `skills/external-patterns/SKILL.md`, `skills/runtime-debugging/SKILL.md`,
  `docs/specs/harness-engineering-doctrine.md`, `tickets/README.md`
- `Signature delta:` `skills/parity-research/SKILL.md / parity_brief(capability,
  local_baseline): recommendation`; `skills/gap-analysis/SKILL.md /
  route(task): gap-analysis|parity-research|functional-ui|deep-system-design`
- `Type Sketch:` `ParityBrief { capability, localBaseline, comparables,
  commonSurfaces, repoDelta, recommendation }`
- `Typed flow example:` `Parity question -> comparable set -> parity brief ->
  gap-analysis or impl-plan`
- `Blast radius:` user routing docs, planning-skill boundaries, and future
  feature-scoping behavior
- `Risks:` the new skill could duplicate `gap-analysis` if the boundary is not
  explicit enough, or drift into debugging language if the examples stay too
  broad

## Acceptance Criteria
- [x] AC-1: `skills/parity-research/` exists with `SKILL.md`, `README.md`, and
      `AGENTS.md`
- [x] AC-2: the new skill explicitly owns external parity comparison against
      products, standards, docs, and open-source repos
- [x] AC-3: `gap-analysis` explicitly routes broader external-parity work to
      `parity-research`
- [x] AC-4: canonical router/docs surfaces mention the new skill as a shipped
      workflow
- [x] AC-5: durable history/memory writeback records the new boundary

## Verification
- `Tests:` `python3 tickets/scripts/check_ticket_metadata.py`; `python3 bin/check_doc_parity.py`; `python3 bin/check_harness_invariants.py`; `git diff --check`
- `Manual checks:` re-read the new skill and the tightened `gap-analysis`
  boundary to confirm the split is obvious from a cold read; confirm the
  existing `.gitignore` rule currently ignores new ticket markdown files
- `Evidence required:` passing validators plus a fresh review artifact
- `Artifacts path:` `tickets/artifacts/TASK-0094/`

## Evidence
- `Artifacts:` [review-2026-04-24-1952+0100.json](/Users/kenjipcx/coding-harness/Codexter/tickets/artifacts/TASK-0094/review-2026-04-24-1952+0100.json)
- `Commands:` `python3 tickets/scripts/check_ticket_metadata.py`; `python3 bin/check_doc_parity.py`; `python3 bin/check_harness_invariants.py`; `git diff --check`
- `Result summary:` the new `parity-research` package landed with explicit
  boundaries against `gap-analysis` and `runtime-debugging`, the committed
  router/docs surfaces were updated in sync, the closeout validators and staged
  diff check passed, and a fresh review scored the work `4.1/5.0` with no
  blocking findings; residual
  caveat: the existing `.gitignore` rule still ignores new `tickets/**/*.md` by
  default, so new tickets still need an ignore-rule change or force-add when
  they should be tracked in Git

## Blockers
- none
