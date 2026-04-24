---
ticket_id: TASK-0092
title: make init-project use deep-interview-quality intake
phase: complete
status: done
owner: codex
claimed_by:
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: false
requires_qa: true
requires_demo: false
created_at: 2026-04-24T19:43:00+0100
updated_at: 2026-04-24T19:55:00+0100
next_action: none
last_verification: 2026-04-24 19:50 +0100 | ticket metadata OK; structural doc parity OK; harness invariants OK; bootstrap smoke OK; pre-push template smoke-tested at 501-line warn and 1001-line block thresholds; local review pass 4.3/5.0
linked_docs:
  - skills/init-project/SKILL.md
  - skills/deep-interview/SKILL.md
  - skills/init-project/README.md
---

# TASK-0092: make init-project use deep-interview-quality intake

## Summary
`init-project` should stop feeling like a shallow scaffold dump. It should use a
deep-interview-quality intake first, then scaffold bootstrap artifacts and
pre-push templates from that clarified brief.

## Scope
- In:
  - init-project intake-first workflow updates
  - deep-interview bootstrap-mode guidance
  - stronger pre-push template and hook docs
  - generated utility-sharing guidance in templates
- Out:
  - full monorepo or turborepo generators
  - automatic hook activation
  - hook-driven repo mutation or auto-refactor commits

## Plan
- `Change:` make `deep-interview` the canonical interview engine for bootstrap
  work and make `init-project` consume that shape instead of duplicating it;
  upgrade the generated `pre-push` contract with file-size checks, stack-aware
  validators, and soft optional heavy gates.
- `Why:` the current `init-project` skill already scaffolds hooks, but it does
  not capture the same intent/quality bar as `deep-interview`, and its
  generated `pre_push_check.sh` is still only a placeholder.
- `Before -> After:` before, bootstrap was mostly copy templates then fill them
  in manually; after, bootstrap starts with a clarified brief and generates a
  real pre-push policy surface with clear defaults.
- `Touch:` `skills/init-project/*`, `skills/deep-interview/SKILL.md`,
  `docs/HISTORY.md`, `docs/MEMORY.md`
- `Inspect:` current skill docs, bootstrap script, hook templates, and existing
  memory around `pre-push`/CodeRabbit placement
- `Signature delta:` `init-project / bootstrap flow: intake brief ->
  scaffolded files`; `pre_push_check.sh / staged checks(): warnings + blockers`;
  `deep-interview / init-project mode: bootstrap-specific dimensions`
- `Type Sketch:` `InitProjectBrief { projectShape, stack, topology,
  localChecks, heavyChecks, fileSizePolicy, utilityPolicy, defaultsChosen }`
- `Typed flow example:` `User idea -> bootstrap intake brief -> scaffolded
  templates -> repo-local pre-push contract`
- `Blast radius:` future initialized repos, hook docs, and bootstrap guidance
  will read differently; biggest risk is over-specifying generated policy while
  keeping it generic enough for different stacks
- `Risks:` utility-detection heuristics can get noisy, and the intake guidance
  must stay clearly reusable rather than becoming init-project-only logic inside
  deep-interview

## Acceptance Criteria
- [x] AC-1: `init-project` explicitly routes bootstrap work through a
      deep-interview-quality intake rather than implying a shallow scaffold-only
      flow
- [x] AC-2: the generated `pre_push_check.sh` template performs a real staged
      file-size and local-check flow instead of placeholder output
- [x] AC-3: generated templates include project guidance about shared utilities
      without making duplicate-helper detection a hard blocker
- [x] AC-4: docs, templates, and bootstrap script stay aligned on manual hook
      activation and optional CodeRabbit/desloppify behavior

## Verification
- `Tests:` `python3 bin/check_doc_parity.py`; `python3 bin/check_harness_invariants.py`; `python3 tickets/scripts/check_ticket_metadata.py`
- `Manual checks:` inspect generated template wording and run the pre-push
  template in dry-run style against the repo shell
- `Evidence required:` passing validators plus a fresh review artifact
- `Artifacts path:` `tickets/artifacts/TASK-0092/`

## Refs
- [skills/init-project/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/init-project/SKILL.md)
- [skills/deep-interview/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/deep-interview/SKILL.md)

## Evidence
- `Artifacts:` [review-2026-04-24-1950+0100.json](/Users/kenjipcx/coding-harness/Codexter/tickets/artifacts/TASK-0092/review-2026-04-24-1950+0100.json)
- `Commands:` `python3 tickets/scripts/check_ticket_metadata.py`; `python3 bin/check_doc_parity.py`; `python3 bin/check_harness_invariants.py`; temp-repo smoke test of `skills/init-project/scripts/bootstrap.sh`; temp-repo smoke test of `skills/init-project/references/PRE_PUSH_CHECK_TEMPLATE.sh` at `501` and `1001` lines
- `Result summary:` all three validators passed; the bootstrap script scaffolded `docs/bootstrap-brief.md`, `.githooks/pre-push`, and `scripts/pre_push_check.sh`; the generated pre-push template warned but passed for a tracked `501`-line file, and failed with the expected remediation message for a tracked `1001`-line helper file; the final review artifact passed at `4.3/5.0`

## Blockers
- none
