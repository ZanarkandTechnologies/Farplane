---
ticket_id: TASK-0152
title: run final skill registry audit and regenerate registry
phase: complete
status: done
owner: codex
claimed_by:
priority: medium
depends_on: ["TASK-0151"]
blocked_by: []
ready: false
approval_required: false
requires_qa: false
requires_demo: false
created_at: 2026-05-19T15:35:00+08:00
updated_at: 2026-05-19T14:59:00+08:00
next_action: complete; registry is regenerated and audited after TASK-0151
last_verification: `python3 bin/sync_skill_registry.py --check`; `python3 bin/check_skill_todo_tiers.py --allow-peer-tier3`; local missing todos summary; `python3 tickets/scripts/check_ticket_metadata.py`
---

# TASK-0152: run final skill registry audit and regenerate registry

## Summary
Run the mechanical final skill-system audit after the Phase 3 consolidation
batch: prove all local skills have `todos.md`, external missing todos are
intentional, tier todo edges are valid, and `docs/skills/registry.jsonl` is
freshly regenerated.

## Scope
- `In:`
  - run the canonical skill-maintenance validation commands
  - regenerate `docs/skills/registry.jsonl`
  - prove every `source: local` skill has `todos.md`
  - prove only intentionally external skills may omit local todos
  - prove no Tier 3 -> Tier 1 checklist direct-link violations
  - record row counts, tier counts, source counts, and missing-todos list
- `Out:`
  - changing skill behavior beyond mechanical audit fixes
  - adding todos to upstream-owned external skills
  - building graph visualization UI; that belongs to `TASK-0153`

## Plan
- `Change:` make the final registry/todos audit an explicit ticket instead of
  an informal terminal check.
- `Why:` after consolidation, the registry is the source of truth for the next
  graph and batch-work surfaces. We need one clean mechanical pass before
  building visual tooling on top.
- `Before -> After:`
  - Before: checks pass during individual migrations, but there is no final
    all-skill audit artifact for the phase.
  - After: one ticket records the final skill count, tier count, todos coverage,
    missing external todos, and validator outputs.
- `Touch:`
  - `docs/skills/registry.jsonl`
  - `tickets/TASK-0152/ticket.md`
  - maybe `docs/specs/skill-tier-rollout-plan.md` if counts change after
    `TASK-0151`
- `Inspect:`
  - `docs/skills/README.md`
  - `docs/skills/registry.jsonl`
  - `skills/skill-maintenance/SKILL.md`
  - `skills/skill-maintenance/scripts/check_skills.py`
  - `bin/sync_skill_registry.py`
  - `bin/check_skill_todo_tiers.py`
- `Signature delta:`
  - `skills/skill-maintenance/scripts/check_skills.py / main(--write): summary`
  - `bin/sync_skill_registry.py / write_registry(): registry.jsonl`
  - `bin/check_skill_todo_tiers.py / audit(): violations[]`
  - `tickets/TASK-0152/ticket.md / Evidence: audit summary`
- `Type Sketch:`
  - `SkillAuditSummary`: `rows`, `tiers`, `sources`, `todos`, `missing_todos`
  - `MissingTodo`: `name`, `source`, `tier`, `upstream_url?`, `intentional`
  - `TierViolation`: `from_skill`, `from_tier`, `to_skill`, `to_tier`, `file`
- `Typed flow example:`
  - Run `check_skills.py --write` -> registry rewrites -> summary says local
    skills have todos and only external skills are missing -> ticket evidence
    stores exact counts -> graph ticket consumes the fresh registry.
- `Execution steps:`
  1. Run `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
  2. Run `python3 bin/sync_skill_registry.py --check`.
  3. Run `python3 bin/check_skill_todo_tiers.py --allow-peer-tier3`.
  4. Run a small local/externals todos summary from `docs/skills/registry.jsonl`.
  5. Run `python3 tickets/scripts/check_ticket_metadata.py`.
  6. Run `git diff --check`.
  7. Update this ticket with counts and command outputs.
  8. Review the audit result before closing.
- `Recommendation:` run this immediately after `TASK-0151`; make `TASK-0153`
  depend on the audited registry.
- `Options considered:`
  - `Fold into TASK-0151:` too easy to lose the all-skill proof inside a
    migration ticket.
  - `Separate audit ticket:` best because it produces a clean graph input.
  - `Skip because validators already pass:` weak, because the user explicitly
    asked for a final check.
- `Blast radius:` generated registry, rollout counts, and downstream graph
  tooling.
- `Risks:` stale ignored ticket files, external skills misclassified as local,
  or check output being summarized without exact counts.

## Acceptance Criteria
- [x] `docs/skills/registry.jsonl` regenerated.
- [x] All `source: local` skills have `todos.md`.
- [x] Missing todos list contains only intentional `source: external` skills.
- [x] Tier todo checker passes.
- [x] Ticket records row counts, tier counts, source counts, and missing-todos
      entries.

## Verification
- `Tests:`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 bin/sync_skill_registry.py --check`
  - `python3 bin/check_skill_todo_tiers.py --allow-peer-tier3`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `git diff --check`
- `Manual checks:`
  - inspect generated summary for local/external todo classification
- `Evidence required:`
  - command output summary
  - registry count summary
  - review artifact

## Proof Contract
- `Metrics:`
  - `Primary metric:` local skills missing todos
  - `Direction:` zero
  - `Verify:` parse `docs/skills/registry.jsonl` for `source == local` and
    `has_todos == false`
  - `Guard:` skill-maintenance validator and tier checker
  - `Autoresearch warranted:` no
  - `Autoresearch session:` none
- `Review Rubrics:`
  - `evidence-quality >= 4.0`
  - `integration-readiness >= 4.0`
- `Required Evidence:`
  - validator outputs
  - count summary
  - review result

## Refs
- `docs/skills/README.md`
- `docs/skills/registry.jsonl`
- `skills/skill-maintenance/SKILL.md`

## Evidence
- `Artifacts:`
  - `tickets/TASK-0152/artifacts/review/2026-05-19-plan-review.json`
- `Commands:`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 bin/sync_skill_registry.py --check`
  - `python3 bin/check_skill_todo_tiers.py --allow-peer-tier3`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - local registry summary script
- `Result summary:`
  - `rows`: 70
  - `sources`: `local=67`, `external=3`
  - `tiers`: `tier1=3`, `tier2=27`, `tier3=40`
  - `todos`: `has=67`, `missing=3`
  - `missing_todos`: `agent-browser`, `convex`,
    `vercel-react-best-practices`
  - `local_missing_todos`: none

## Blockers
- none
