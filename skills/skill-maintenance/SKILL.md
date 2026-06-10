---
name: skill-maintenance
description: "Maintain Farplane skill packages in bulk: classify tiers, add or audit todos, manage source ownership, sync the generated registry, and plan consolidation without bloating the global system prompt."
tier: 3
group: skills
source: local
skill_template_version: "0.1.0"
feature_refs:
  - FEAT-0037
  - FEAT-0040
  - FEAT-0044
---

# Skill Maintenance

## Context

Skill maintenance is the owner for bulk Farplane skill upkeep: template
onboarding, tier/source metadata, generated registry sync, todo-list shape,
link hygiene, source ownership, and consolidation planning. Use this skill to
make skill-system work repeatable instead of hiding rollout state in chat.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Load the current skill-system baseline before editing.
   - [ ] Read `docs/skills/system.md`, `docs/skills/README.md`,
     `docs/skills/best-practices.md`, `docs/skills/registry.jsonl`, active
     tickets, and the target skill files.
- [ ] 2. Classify the maintenance operation for each target skill.
   - [ ] 1. Template onboarding or version audit.
   - [ ] 2. Todo-list or reference cleanup.
   - [ ] 3. Tier, source, group, feature-ref, method, or common-chain metadata
     update.
   - [ ] 4. Consolidation, split, or external-source ownership change.
- [ ] 3. Route non-mechanical choices before editing.
   - [ ] Use [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
     when upstream or external skill examples should change the local contract.
   - [ ] Use [plan](../plan/SKILL.md) when tier, source, group, method ownership,
     or consolidation choices have real tradeoffs.
- [ ] 4. Record the edit boundary for each target skill.
   - [ ] Identify source ownership, related skills, adopted `FEAT-####`
     records, first-load dependencies, proof surfaces, and files that may
     change.
- [ ] 5. Prototype broad rewrites on a representative sample before scaling.
   - [ ] Include a mix of Tier 1, Tier 2, and complex Tier 3 packages when the
     migration will affect many skills.
- [ ] 6. Edit each target `SKILL.md` so first-load work is executable.
   - [ ] Put required actions in the marker-delimited `## Todo List`.
   - [ ] Keep every-invocation rules in `SKILL.md`.
   - [ ] Move conditional branches, examples, templates, long rubric detail,
     model maps, delegated prompts, and rare-path recipes into references.
   - [ ] Move actor identity, subagent spawning, caller routing, tool-use policy,
     and artifact writeback out of reusable skills unless the skill is explicitly
     an orchestration skill.
- [ ] 7. Verify template structure before marking a skill onboarded.
   - [ ] Check the actual `SKILL.md` headings and todo shape against the current
     template before setting or keeping `skill_template_version`.
   - [ ] Prune redundant `todos.md` once direct todo-list content matches.
- [ ] 8. Validate the skill system with `python3 scripts/check_skills.py --write`
   from this skill package.
- [ ] 9. Reinstall touched local skills and inspect the live copy before judging
   Codex behavior.
   - [ ] Use `bash ../../install.sh --skills-only --skills <names> --target ~/.codex`
     from this skill package when the user is checking installed behavior.
   - [ ] Re-read `~/.codex/skills/<name>/SKILL.md` for at least one touched skill
     before claiming the visible checklist changed.
- [ ] 10. Review readiness before completion.
   - [ ] For material skill-system changes, delegate final review to the native
     `reviewer` subagent with a reviewer handoff.
   - [ ] Use [execute](../execute/SKILL.md) for final proof, docs writeback, and
     ticket evidence when the pass needs durable closeout.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this when working on the skill system itself: tier metadata, direct todo
lists, legacy `todos.md` cleanup, source ownership, registry sync, link
hygiene, or consolidation planning.

## Core Rules

- Follow `docs/skills/system.md` for the tier model, source ownership,
  frontmatter contract, template versioning, feature tracking, and todo-link
  rules.
- Follow `docs/skills/best-practices.md` for first-load todo-list shape,
  reference placement, repeatability, and review gates.
- `SKILL.md` is the first-load source of truth. Required todo items belong in a
  direct marker-delimited `## Todo List` section.
- Keep logic in `SKILL.md` when it affects every invocation: trigger boundary,
  required order, decision routing, escalation, stop conditions, hard gates,
  output contract, and high-risk guardrails.
- Use `references/*` for conditional branches, examples, templates, long rubric
  detail, model maps, delegated prompts, and rare-path recipes.
- If a reference must be read every time, promote the needed logic into
  `SKILL.md`.
- Treat `todos.md` as a legacy/transitional input only. Delete it once it
  matches the direct `SKILL.md` todo list; reconcile divergent duplicates
  manually.
- External skills should carry `source: external` and usually `upstream_url`;
  local Farplane policy belongs in local callers.
- Router-style todos choose methods conditionally. They do not run every method
  in sequence.
- Complex Tier 3 pipeline skills should expose their domain as
  `Model + MethodRegistry + TodoRecipe + Templates + Proof` when that makes the
  workflow easier to scan. Keep the algebra in `SKILL.md` or a targeted
  `references/model.md`; do not add per-skill `README.md` files for this.

## Workflow

1. Read `docs/skills/system.md`, `docs/skills/README.md`,
   `docs/skills/best-practices.md`, `docs/skills/registry.jsonl`, and the
   target skill files.
2. Use [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
   when comparing external skill examples or upstream instructions.
3. Use [plan](../plan/SKILL.md) when tier/source/consolidation choices have
   real tradeoffs.
4. For broad migrations such as todo-list embedding or reference pruning, use
   [prototyping](../prototyping/SKILL.md) on a small representative set before
   running bulk commands.
5. Update `SKILL.md` frontmatter only for manual fields: `tier`, `source`,
   optional `skill_template_version`, optional `feature_refs`, Tier 3 `group`,
   optional `methods`, optional `common_chains`, and optional `upstream_url`.
   Use `feature_refs` only for compact `FEAT-####` handles already present in
   `docs/features/registry.jsonl`. Use `skill_template_version` only when the
   skill has been onboarded to a known structural template baseline; absence
   means not onboarded yet.
6. Put the anti-forgetting todo list directly in `SKILL.md` under
   `## Todo List`:
   - project/docs context first
   - required workflow and branch checks second
   - proof/writeback last
   - keep optional detail in references with clear read conditions
   - keep or create `todos.md` only as a temporary migration input
7. Run the standard skill-system check:

```bash
python3 scripts/check_skills.py --write
```

This command normalizes direct `## Todo List` sections, prunes
redundant `todos.md` files, regenerates the registry, verifies registry
metadata, checks todo-list tier edges, compiles the registry/check scripts, and
prints a compact summary. Use the lower-level commands only when debugging a
specific failure:

```bash
python3 scripts/sync_skill_checklists.py --write
python3 ../../bin/sync_skill_registry.py --write
python3 ../../bin/sync_skill_registry.py --check
python3 ../../bin/check_skill_todo_tiers.py --allow-peer-tier3
```

8. Use [execute](../execute/SKILL.md) for final proof, docs writeback, and
   ticket evidence after skill changes.

## Outcome Contract

- Skill frontmatter remains minimal and valid. Skills may carry `feature_refs`
  for adopted harness feature handles. Onboarded skills may carry
  `skill_template_version`; missing values remain visible in the generated
  registry and `check_skills.py --template-version <version>` report.
  Versioned skills fail the check when their structure no longer matches the
  template promise.
- Broad skill migrations include a representative `Prototype Note` before full
  batch application.
- `SKILL.md` contains the required first-load todo list and high-signal logic.
- Transitional `todos.md` files are removed when redundant or left only when a
  human must reconcile divergent content.
- Complex Tier 3 skills keep any algebraic project/component/method model
  concise, discoverable, and subordinate to the `SKILL.md` first-load contract.
- `docs/skills/registry.jsonl` is regenerated, not hand-edited.
- External-source skills remain easy to refresh.
- Consolidation candidates are ticketed or documented before hard migration.
- `python3 scripts/check_skills.py --write` passes
  before completion is claimed.

## Templates

Use `skills/skill-creator/references/SKILL_TEMPLATE.md` as the structural
baseline when onboarding a skill to `skill_template_version: "0.1.0"`.

## Gotchas

- Do not mark a skill as onboarded to a template version unless its structure
  actually follows that template.
- Do not bypass the template-structure validator by treating
  `skill_template_version` as metadata-only.
- Do not let generated registry rows become a hand-edited source of truth.
- Do not bulk-edit every skill before proving the pattern on a representative
  sample.
- Do not move Farplane wrapper behavior into external-source skills.

## Reference Map

- [docs/skills/system.md](../../docs/skills/system.md) - tier model, source
  ownership, frontmatter contract, template versioning, feature tracking, and
  todo-link rules.
- [docs/skills/README.md](../../docs/skills/README.md) - human skill selection
  guide, generated registry surface, and maintenance commands.
- [docs/skills/best-practices.md](../../docs/skills/best-practices.md) -
  first-load shape, reference placement, repeatability, and review gates.
- [../skill-creator/references/SKILL_TEMPLATE.md](../skill-creator/references/SKILL_TEMPLATE.md)
  - current baseline skill template.
- [scripts/check_skills.py](scripts/check_skills.py) - standard validation and
  template-version report.

## Output

- Updated `skills/*/SKILL.md` files.
- Regenerated `docs/skills/registry.jsonl`.
- A passing `python3 scripts/check_skills.py --write`
  result, or an explicit blocker with the exact failing command.
