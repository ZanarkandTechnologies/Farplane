---
name: skill-creator
description: Create or update Farplane skills when a user wants a reusable workflow, domain playbook, prompt/harness capability, or bundled scripts/templates that extend Codex behavior.
tier: 3
group: skills
source: local
license: Complete terms in LICENSE.txt
allowed-tools: mcp__sequential-thinking__sequentialthinking, Read, Write, Grep, Glob
---

# Skill Creator

## Context

Skill creation is part of the Farplane skill system. Read
[docs/skills/README.md](../../docs/skills/README.md) for tier definitions,
source ownership, registry fields, and todo-link rules before changing a
skill's shape. Use [docs/skills/best-practices.md](../../docs/skills/best-practices.md)
for first-load todo shape, reference placement, actor-prompt boundaries,
duplication control, repeatability, and review gates.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

1. [ ] Read the request, related skills, registry row, nearby project docs,
   [docs/skills/README.md](../../docs/skills/README.md), and
   [docs/skills/best-practices.md](../../docs/skills/best-practices.md).
2. [ ] Choose the ownership branch.
   - New skill: use only when the capability has a stable trigger and reusable
     workflow.
   - Existing skill update: use when the behavior is a branch, method,
     todo-list fix, reference, script, or prompt inside an existing contract.
   - Unclear ownership: use [plan](../plan/SKILL.md).
3. [ ] Ground the design when needed.
   - Use [research:parity](../research/SKILL.md#researchparity) or
     [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
     when external skill examples should inform the design.
4. [ ] Draft or revise the minimum executable contract directly in `SKILL.md`:
   trigger boundary, job, numbered `## Todo List`, core branches,
   hard gates, judgement questions, proof commands, and outcome contract.
5. [ ] Place supporting material by load frequency.
   - Keep every-invocation logic in `SKILL.md`.
   - Move conditional branches, examples, templates, long rubrics, model maps,
     delegated prompts, and rare-path recipes into references.
   - Keep actor identity, delegation routing, tool-use policy, and artifact
     writeback in the owning agent prompt or caller skill.
   - Promote reference logic back into `SKILL.md` when it must be read every
     time; delete or merge empty, thin, or duplicated reference files.
6. [ ] Validate after edits:
   `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
7. [ ] Review readiness before completion.
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

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List
1. [ ] ...
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

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

- [docs/skills/README.md](../../docs/skills/README.md) - tier definitions,
  source ownership, registry fields, and todo-link rules.
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

Use these commands from the Farplane repo root:

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

When creating or packaging a non-Farplane standalone skill, use the local
helper scripts:

```bash
python3 skills/skill-creator/scripts/init_skill.py <skill-name> --path skills
python3 skills/skill-creator/scripts/package_skill.py skills/<skill-name>
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
