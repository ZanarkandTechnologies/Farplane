---
name: skill-creator
description: Create or update Farplane skills when a user wants a reusable workflow, domain playbook, prompt/harness capability, or bundled scripts/templates that extend Codex behavior.
tier: 3
group: skills
source: local
skill_template_version: "0.1.0"
feature_refs:
  - FEAT-0048
license: Complete terms in LICENSE.txt
allowed-tools: mcp__sequential-thinking__sequentialthinking, Read, Write, Grep, Glob
---

# Skill Creator

## Context

Skill creation is part of the Farplane skill system. Read
[docs/skills/system.md](../../docs/skills/system.md) for the tier model,
source ownership, frontmatter contract, template versioning, feature tracking,
and todo-link rules before changing a skill's shape. Use
[docs/skills/best-practices.md](../../docs/skills/best-practices.md)
for first-load todo shape, reference placement, actor-prompt boundaries,
duplication control, repeatability, and review gates.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read the request, related skills, registry row, nearby project docs,
   [docs/skills/system.md](../../docs/skills/system.md),
   [docs/skills/README.md](../../docs/skills/README.md), and
   [docs/skills/best-practices.md](../../docs/skills/best-practices.md).
- [ ] 2. Decide the owning surface and write the decision into the edit.
   - [ ] 1. Create a new skill only when the capability has a stable trigger and
     reusable workflow.
   - [ ] 2. Update an existing skill when the request is a branch, method,
     todo-list fix, reference, script, or prompt inside an existing contract.
   - [ ] 3. Hand unclear ownership to [plan](../plan/SKILL.md).
- [ ] 3. Ground the skill design before drafting when external examples or peer
   skills could change the contract.
   - [ ] Use [research:parity](../research/SKILL.md#researchparity) or
     [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
     when source comparison is required.
- [ ] 4. Draft or revise `SKILL.md` so the first-load path is executable without
   hidden chat context.
   - [ ] Include trigger boundary, context, ordered `## Todo List`, branches,
     hard gates, proof command, and output contract.
- [ ] 5. Move non-first-load material to the right supporting surface.
   - [ ] Keep every-invocation rules in `SKILL.md`.
   - [ ] Move conditional branches, examples, templates, long rubrics, model
     maps, delegated prompts, and rare-path recipes into references.
   - [ ] Keep actor identity, delegation routing, tool-use policy, and artifact
     writeback in the owning agent prompt or caller skill.
   - [ ] Promote reference logic back into `SKILL.md` when it must be read every
     time; delete or merge empty, thin, or duplicated reference files.
- [ ] 6. Run `python3 ../skill-maintenance/scripts/check_skills.py --write`
   and fix any reported skill-system drift.
- [ ] 7. Review the finished skill contract before completion.
   - [ ] Repeatability from files alone.
   - [ ] No duplicated first-load logic.
   - [ ] Actor-prompt versus skill-contract boundaries are clean.
   - [ ] Explicit proof commands or blockers are recorded.
   - [ ] Native `reviewer` subagent used for material skill-system changes when
     available.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Minimal `SKILL.md` shape:

```markdown
## Context

TODO: add the marker-delimited `## Todo List` section from
`references/SKILL_TEMPLATE.md`.

- [ ] 1. ...
- [ ] 2. Choose the branch.
   - [ ] 1. Default branch.
   - [ ] 2. Repair branch.
- [ ] 3. Review before completion.
   - [ ] Repeatability from files alone.
   - [ ] No duplicated first-load logic.

## Templates
## Gotchas
## Reference Map
## Output
```

Use [references/SKILL_TEMPLATE.md](references/SKILL_TEMPLATE.md) for the full
starter file.

## Gotchas

- Do not create a skill for generic model knowledge, raw library
  documentation, one-off notes, or behavior better expressed as a prompt,
  script, ticket, or existing skill update.
- Do not hide the default workflow in references. If skipping all references
  makes the skill fail, `SKILL.md` is too thin.
- Do not teach the whole domain in `SKILL.md`. If it reads like onboarding,
  move the material to references.
- Do not duplicate the same rule across `SKILL.md`, references, templates,
  prompts, and README-style docs.
- Do not put actor identity, delegation routing, tool-use policy, or artifact
  writeback in a reusable skill contract.

## Reference Map

- [docs/skills/system.md](../../docs/skills/system.md) - tier model, source
  ownership, frontmatter contract, template versioning, feature tracking, and
  todo-link rules.
- [docs/skills/README.md](../../docs/skills/README.md) - human skill selection
  guide, generated registry surface, and maintenance commands.
- [docs/skills/best-practices.md](../../docs/skills/best-practices.md) -
  first-load todo shape, reference placement, actor-prompt boundaries,
  duplication control, repeatability, and review gates.
- [references/SKILL_TEMPLATE.md](references/SKILL_TEMPLATE.md) - minimal starter
  template for new skill packages.
- [references/workflows.md](references/workflows.md) - branch and
  outcome-contract patterns when the todo list needs shaping help.
- [references/architecture.md](references/architecture.md) - boundary between
  first-load contract, references, scripts, prompts, and assets.
- [references/judgement-questions.md](references/judgement-questions.md) -
  advise-style skill decisions.
- [references/output-patterns.md](references/output-patterns.md) - prompt,
  template, example, and validation output patterns.
- [references/tier3-pipeline-model.md](references/tier3-pipeline-model.md) -
  optional model for complex Tier 3 pipeline skills.
- [references/gotchas.md](references/gotchas.md) - extra review negatives.

## Output

Paths here are relative to the `skill-creator` package.

```bash
python3 ../skill-maintenance/scripts/check_skills.py --write
```

When creating or packaging a non-Farplane standalone skill, use the local
helper scripts:

```bash
python3 scripts/init_skill.py <skill-name> --path ..
python3 scripts/package_skill.py ../<skill-name>
```

Run added or changed scripts directly before claiming they work.

After this skill runs:

- The target skill has valid frontmatter and a direct marker-delimited
  `## Todo List`.
- `SKILL.md` contains the minimum first-load contract without tutorial bloat.
- References are linked directly from `SKILL.md` and used only for conditional
  detail.
- Scripts, prompts, assets, and templates exist only when they support repeated
  execution.
- Registry validation passes, or the remaining blocker is recorded with the
  exact failing command.
