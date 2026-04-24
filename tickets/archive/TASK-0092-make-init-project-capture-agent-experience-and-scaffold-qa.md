---
ticket_id: TASK-0092
title: make init project capture agent experience and scaffold qa
phase: complete
status: done
owner: codex
claimed_by:
priority: medium
depends_on: []
blocked_by: []
ready: true
approval_required: false
requires_qa: false
requires_demo: false
created_at: 2026-04-24T19:55:00Z
updated_at: 2026-04-24T20:10:00Z
next_action: archived; use init-project bootstrap plus qa/cookbook for future project-init agent-experience setup
last_verification: `bash -n skills/init-project/scripts/bootstrap.sh`; `bash skills/init-project/scripts/bootstrap.sh /tmp/codexter-init-6hlUdA`; `git diff --check`
linked_docs:
  - skills/init-project/SKILL.md
  - skills/init-project/README.md
  - docs/specs/agent-testability-surfaces.md
  - qa/README.md
---

# TASK-0092: make init project capture agent experience and scaffold qa

## Summary
Bootstrap should ask how the agent will move through the app efficiently and where those answers live. This ticket moves that concern into `init-project` by making agent experience/testability part of the bootstrap brief and by scaffolding the repo-level `qa/` cookbook surfaces during project initialization.

## Scope
- In:
  - add agent-experience/testability questions to the bootstrap brief and init-project docs
  - scaffold `qa/` docs and cookbook templates from `init-project`
  - align bootstrap checklists and templates with the new default
- Out:
  - changing `deep-interview` or `agent-testability-plan`
  - adding app-specific shortcuts or instrumentation to any target repo

## Plan
- `Change:` extend the bootstrap brief with agent-experience/testability prompts, add QA/cookbook templates under `skills/init-project/references/`, and update `bootstrap.sh` plus init-project docs to scaffold `qa/` by default
- `Why:` operator memory should not be the only thing that keeps agent UX/testability in scope; bootstrap should create the surface and ask the question early
- `Before -> After:`
  - `Before:` init-project bootstraps docs and tickets, but it does not ask explicitly how agents reach/test the app and it does not scaffold `qa/`
  - `After:` bootstrap includes an agent-experience section and new repos start with a visible `qa/` cookbook surface for shortcuts, deep links, seeds, probes, and debug helpers
- `Touch:` `skills/init-project/*`, new `skills/init-project/references/qa/*` templates, `docs/MEMORY.md`, `docs/HISTORY.md`, and root `README.md` if needed for discoverability
- `Inspect:` `skills/init-project/SKILL.md`, `skills/init-project/README.md`, `skills/init-project/AGENTS.md`, `skills/init-project/scripts/bootstrap.sh`, `skills/init-project/references/BOOTSTRAP_BRIEF_TEMPLATE.md`, root `qa/*`
- `Signature delta:` none
- `Type Sketch:` none
- `Typed flow example:` none
- `Recommendation:` keep the bootstrap interview responsibility in `init-project`, but make agent-experience/testability a required bootstrap brief section and scaffold the QA cookbook surface immediately
- `Blast radius:` new-project bootstrap docs, generated scaffold shape, and the operator’s bootstrap checklist
- `Risks:` template drift between the live repo `qa/` docs and the init-project scaffold copies; over-expanding bootstrap if the new section becomes too verbose

## Acceptance Criteria
- [x] AC-1: `init-project` docs and templates explicitly ask how agents will reach, inspect, stabilize, and verify the app efficiently
- [x] AC-2: `init-project` scaffolds a repo-level `qa/` surface with cookbook templates by default
- [x] AC-3: bootstrap checklists and guidance tell the operator to keep durable agent-experience answers in the bootstrap brief and QA cookbook rather than chat

## Verification
- `Tests:` `git diff --check`
- `Manual checks:` inspect the bootstrap brief template, bootstrap script, and init-project docs for a consistent agent-experience/testability story
- `Evidence required:` linked ticket plus review artifact covering the updated bootstrap docs and scaffold
- `Artifacts path:` `tickets/artifacts/TASK-0092/`

## Evidence
- `Artifacts:`
  - [review.md](/Users/kenjipcx/coding-harness/Codexter/tickets/artifacts/TASK-0092/review/2026-04-24_201000_bootstrap-review/review.md)
  - [review.json](/Users/kenjipcx/coding-harness/Codexter/tickets/artifacts/TASK-0092/review/2026-04-24_201000_bootstrap-review/review.json)
- `Commands:`
  - `bash -n skills/init-project/scripts/bootstrap.sh`
  - `bash skills/init-project/scripts/bootstrap.sh /tmp/codexter-init-6hlUdA`
  - `git diff --check`
- `Result summary:` moved agent-experience/testability into init-project bootstrap, added visible bootstrap brief prompts for it, scaffolded `qa/` cookbook surfaces by default, and passed a final review with no blocking findings

## Blockers
- none
