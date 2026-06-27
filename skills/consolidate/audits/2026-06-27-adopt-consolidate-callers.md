---
skill: consolidate
date: 2026-06-27
change_type: adoption
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/*/SKILL.md
after_ref: skills/consolidate/SKILL.md
proof_artifacts:
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
---

# Adopt Consolidate Across Caller Skills

## Change

- Before: skill, eval, docs, memory, and interval workflows carried separate
  local consolidation wording.
- After: caller skills bind their target structure and constraints, then call
  `consolidate(...)` for unit inventory, value scoring, merge/move/delete
  decisions, and loss checks.
- Scope: `skill-maintenance`, `knowledge-tidier`, `update-memory`, `eval`,
  `interval-update`, `harness-creator`, and the artifact boundary in
  `code-review`.

## Unit Decisions

| Surface | Decision | Rationale |
| --- | --- | --- |
| `skill-maintenance` refinement | route to `consolidate(..., structure = skill)` | Skill-maintenance applies accepted edits and proof; consolidate owns compaction decisions. |
| `eval:consolidate` | route each changed eval file to `consolidate(..., structure = eval_suite)` | Eval keeps fixture/runner ownership while consolidate owns row decisions. |
| `knowledge-tidier` | adapt value function and call `consolidate(..., structure = memory | docs_tree | file)` | Knowledge-specific factuality/archive rules remain local. |
| `update-memory` | call `consolidate(..., structure = memory | docs_tree)` for broad keep/merge/move/delete decisions | Memory refresh keeps source routing and append-only constraints. |
| `interval-update` docs/skill refinement | route interval handoffs through `consolidate` before owner-specific edit skills | Interval stays a planner/router, not a second consolidation engine. |
| `harness-creator` default lanes | route older skill-surface compaction through `consolidate`, then `skill-maintenance` | Generated harnesses inherit the shared primitive. |
| `code-review` branch consolidation | add boundary note | Code-level duplication stays review/refactoring; artifact/entity-set consolidation routes to `consolidate`. |

## Proof

- `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
- Validator output included registry sync, template registry sync, template
  intelligence generation, todo tier check, Tier 0 phase protocol check, skill
  capability fixtures, eval query lint, doc refs, and Python compile.
- Note: the registry now reports 99 rows because an existing untracked
  `skills/infographic/` package is visible to registry generation. This audit
  did not edit that package.

## Remaining Risk

- Future caller skills may still describe domain dedupe that is not artifact
  consolidation. Leave operational dedupe local unless it is a value-preserving
  artifact/entity-set compression problem.
