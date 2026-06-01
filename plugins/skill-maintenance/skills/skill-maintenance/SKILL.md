---
name: skill-maintenance
description: "Maintain Codexter skill packages in bulk: classify tiers, add or audit todos, manage source ownership, sync the generated registry, and plan consolidation without bloating the global system prompt."
tier: 3
group: skills
source: local
---

# Skill Maintenance

<!-- BEGIN CODEXTER_IMPORTANT_CHECKLIST -->
## Important Checklist

Source: `SKILL.md`

- [ ] Read `docs/specs/skill-tier-rollout-plan.md`,
  `docs/skills/README.md`, `docs/skills/registry.jsonl`, active tickets, and
  the target skill files before editing.
- [ ] Use [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
  when upstream/external skill examples should inform local updates.
- [ ] Use [plan](../plan/SKILL.md) when tier, source, group, method ownership,
  or consolidation choices are not mechanical.
- [ ] For each target skill, identify project files, related skills, proof
  surfaces, and source ownership before editing the first-load contract.
- [ ] Use [plan](../plan/SKILL.md) before broad skill rewrites: update a
  representative sample across Tier 1, Tier 2, and complex Tier 3 packages,
  validate it, and scale only after the pattern is stable.
- [ ] Put required checklist items directly in `SKILL.md` under
  `## Important Checklist`; prune redundant `todos.md` once content matches.
- [ ] Keep every-invocation logic in `SKILL.md`; move only conditional
  branches, examples, templates, long rubric detail, model maps, delegated
  prompts, and rare-path recipes into references.
- [ ] Promote reference logic back into `SKILL.md` when it must be read every
  time.
- [ ] Keep Tier 2 todos linked to Tier 1 primitives; keep Tier 3 todos linked
  to Tier 2 surfaces plus intentional peer Tier 3 handoffs only.
- [ ] Keep external skill packages thin and move Codexter wrapper policy into
  local caller skills.
- [ ] Regenerate and validate the registry with
  `python3 skills/skill-maintenance/scripts/check_skills.py --write` after
  edits.
- [ ] Use [execute](../execute/SKILL.md) for final proof, docs writeback, and
  ticket evidence.
<!-- END CODEXTER_IMPORTANT_CHECKLIST -->

Use this when working on the skill system itself: tier metadata, direct
checklists, legacy `todos.md` cleanup, source ownership, registry sync, link
hygiene, or consolidation planning.

## Job

1. Read the relevant rollout/spec/docs surfaces.
2. Classify the skills being touched by tier, source, group, and method owner.
3. Add or update skill instructions without duplicating lower-tier logic.
4. Prototype broad migrations on a representative skill sample before scaling.
5. Keep external skills refreshable by moving local wrapper policy into local
   caller skills.
6. Regenerate and validate the skill registry.
7. Record durable rules only when the change creates a reusable invariant.

## Core Rules

- `SKILL.md` is the first-load source of truth. Required checklist items belong
  in a direct marker-delimited `## Important Checklist` section.
- Keep logic in `SKILL.md` when it affects every invocation: trigger boundary,
  required order, decision routing, escalation, stop conditions, hard gates,
  output contract, and high-risk guardrails.
- Use `references/*` for conditional branches, examples, templates, long rubric
  detail, model maps, delegated prompts, and rare-path recipes.
- If a reference must be read every time, promote the needed logic into
  `SKILL.md`.
- Treat `todos.md` as a legacy/transitional input only. Delete it once it
  matches the direct `SKILL.md` checklist; reconcile divergent duplicates
  manually.
- Tier 1 primitives are base obligations for Tier 2.
- Tier 2 surfaces may link Tier 1 primitives.
- Tier 3 application skills may link Tier 2 surfaces and peer Tier 3 handoffs
  when the domain flow requires them.
- External skills should carry `source: external` and usually `upstream_url`;
  local Codexter policy belongs in local callers.
- Router-style todos choose methods conditionally. They do not run every method
  in sequence.
- Complex Tier 3 pipeline skills should expose their domain as
  `Model + MethodRegistry + TodoRecipe + Templates + Proof` when that makes the
  workflow easier to scan. Keep the algebra in `SKILL.md` or a targeted
  `references/model.md`; do not add per-skill `README.md` files for this.

## Workflow

1. Read `docs/specs/skill-tier-rollout-plan.md`,
   `docs/skills/README.md`, `docs/skills/registry.jsonl`, and the target
   skill files.
2. Use [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
   when comparing external skill examples or upstream instructions.
3. Use [plan](../plan/SKILL.md) when tier/source/consolidation choices have
   real tradeoffs.
4. For broad migrations such as checklist embedding or reference pruning, use
   [prototyping](../prototyping/SKILL.md) on a small representative set before
   running bulk commands.
5. Update `SKILL.md` frontmatter only for manual fields: `tier`, `source`,
   Tier 3 `group`, optional `methods`, optional `common_chains`, and optional
   `upstream_url`.
6. Put the anti-forgetting checklist directly in `SKILL.md` under
   `## Important Checklist`:
   - project/docs context first
   - required workflow and branch checks second
   - proof/writeback last
   - keep optional detail in references with clear read conditions
   - keep or create `todos.md` only as a temporary migration input
7. Run the standard skill-system check:

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

This command normalizes direct `## Important Checklist` sections, prunes
redundant `todos.md` files, regenerates the registry, verifies registry
metadata, checks checklist tier edges, compiles the registry/check scripts, and
prints a compact summary. Use the lower-level commands only when debugging a
specific failure:

```bash
python3 skills/skill-maintenance/scripts/sync_skill_checklists.py --write
python3 bin/sync_skill_registry.py --write
python3 bin/sync_skill_registry.py --check
python3 bin/check_skill_todo_tiers.py --allow-peer-tier3
```

8. Use [execute](../execute/SKILL.md) for final proof, docs writeback, and
   ticket evidence after skill changes.

## Outcome Contract

- Skill frontmatter remains minimal and valid.
- Broad skill migrations include a representative `Prototype Note` before full
  batch application.
- `SKILL.md` contains the required first-load checklist and high-signal logic.
- Transitional `todos.md` files are removed when redundant or left only when a
  human must reconcile divergent content.
- Complex Tier 3 skills keep any algebraic project/component/method model
  concise, discoverable, and subordinate to the `SKILL.md` first-load contract.
- `docs/skills/registry.jsonl` is regenerated, not hand-edited.
- External-source skills remain easy to refresh.
- Consolidation candidates are ticketed or documented before hard migration.
- `python3 skills/skill-maintenance/scripts/check_skills.py --write` passes
  before completion is claimed.
