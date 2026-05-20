---
name: skill-maintenance
description: "Maintain Codexter skill packages in bulk: classify tiers, add or audit todos, manage source ownership, sync the generated registry, and plan consolidation without bloating the global system prompt."
tier: 3
group: skills
source: local
---

# Skill Maintenance

Use this when working on the skill system itself: tier metadata, `todos.md`,
source ownership, registry sync, link hygiene, or consolidation planning.

## Job

1. Read the relevant rollout/spec/docs surfaces.
2. Classify the skills being touched by tier, source, group, and method owner.
3. Add or update skill instructions without duplicating lower-tier logic.
4. Keep external skills refreshable by moving local wrapper policy into local
   caller skills.
5. Regenerate and validate the skill registry.
6. Record durable rules only when the change creates a reusable invariant.

## Core Rules

- Tier 1 primitives are base obligations for Tier 2.
- Tier 2 surfaces may link Tier 1 primitives.
- Tier 3 application skills may link Tier 2 surfaces and peer Tier 3 handoffs
  when the domain flow requires them.
- External skills should carry `source: external` and usually `upstream_url`;
  local Codexter policy belongs in local callers.
- Router-style todos choose methods conditionally. They do not run every method
  in sequence.

## Workflow

1. Read `docs/specs/skill-tier-rollout-plan.md`,
   `docs/skills/README.md`, `docs/skills/registry.jsonl`, and the target
   skill files.
2. Use [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
   when comparing external skill examples or upstream instructions.
3. Use [plan](../plan/SKILL.md) when tier/source/consolidation choices have
   real tradeoffs.
4. Update `SKILL.md` frontmatter only for manual fields: `tier`, `source`,
   Tier 3 `group`, optional `methods`, optional `common_chains`, and optional
   `upstream_url`.
5. Write `todos.md` as an anti-forgetting checklist:
   - project/docs context first
   - useful skill references second
   - proof/writeback last
6. Run the standard skill-system check:

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

This command regenerates the registry, verifies registry metadata, checks
`todos.md` tier edges, compiles the registry/check scripts, and prints a compact
summary. Use the lower-level commands only when debugging a specific failure:

```bash
python3 bin/sync_skill_registry.py --write
python3 bin/sync_skill_registry.py --check
python3 bin/check_skill_todo_tiers.py --allow-peer-tier3
```

7. Use [execute](../execute/SKILL.md) for final proof, docs writeback, and
   ticket evidence after skill changes.

## Outcome Contract

- Skill frontmatter remains minimal and valid.
- `todos.md` files obey the tier loading invariant.
- `docs/skills/registry.jsonl` is regenerated, not hand-edited.
- External-source skills remain easy to refresh.
- Consolidation candidates are ticketed or documented before hard migration.
- `python3 skills/skill-maintenance/scripts/check_skills.py --write` passes
  before completion is claimed.
