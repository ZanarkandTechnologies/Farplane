---
title: Agent Skills eval layout migration
owner: eval
status: complete
kind: skill-audit
created_at: 2026-07-12
refs:
  - https://agentskills.io/skill-creation/evaluating-skills
  - skills/eval/scripts/migrate_skill_evals.py
  - skills/eval/scripts/run_evals.py
  - skills/skill-creator/references/EVAL_TASK_TEMPLATE.json
---

# Agent Skills eval layout migration

## Delta

- Replaced skill-local `eval_task.json` lists with portable
  `evals/evals.json` objects.
- Mapped `query` to `prompt` and `reference_points` to `assertions` while
  preserving Farplane-only fields under `metadata.farplane`.
- Kept project harness and AGENTS eval task files runner-native because they
  are not portable skill packages.
- Updated runner discovery, query lint, eval-drain discovery, surface budgets,
  skill frontmatter, templates, registries, and active documentation.

## Proof

- Migration applied to 59 skill packages and 196 eval rows.
- No `skills/*/eval_task.json` files remain.
- Focused migration, runner, drain, registry, and surface-budget tests pass.
- `skills/skill-maintenance/scripts/check_skills.py --write` passes after
  registry regeneration.
- Registry validation rejects canonical eval files that lack frontmatter
  enrollment, and all 59 suites are present in the generated skill registry.
- Generated skill, docs, harness, and template-intelligence graphs contain no
  legacy eval paths.
- Non-empty portable `files` fail explicitly until runner-owned fixture
  staging is implemented; they are never silently ignored.

## Review

Independent reviewer verdict: pass after adding the reverse registry invariant,
enrolling four previously undiscoverable suites, and regenerating all graph
projections.
