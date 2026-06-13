---
name: skill-creator
description: "Turn a reusable workflow or capability idea into a Farplane skill package with frontmatter, todo path, references, and proof surfaces."
tier: 3
group: skills
source: local
skill_template_version: "0.2.0"
feature_refs:
  - FEAT-0048
  - FEAT-0057
license: Complete terms in LICENSE.txt
allowed-tools: mcp__sequential-thinking__sequentialthinking, Read, Write, Grep, Glob
---

# Skill Creator

## Context

Skill creation is part of the Farplane skill system. Read
[docs/skills/system.md](../../docs/skills/system.md) for the tier model,
source ownership, frontmatter contract, template versioning, feature tracking,
and todo-link rules before changing a skill's shape. Use
[docs/skills/best-practices.md](../../docs/skills/best-practices.md) as the
skill-authoring standard. Prefer the specific anchored section needed for the
current edit; load the whole file only when shaping or reviewing the full skill
contract.

## Skill Signature

```text
create_or_update_skill(request, existing_surface?, proof_need?) -> skill_package_change + validation_result
state: reads(skill-system docs, registry, target skill, template); writes(SKILL.md, references?, scripts?, registry?)
gates: trigger_stable; template_structure_valid; proof_or_blocker_named; review_ready
routes: gap-analysis | skill-maintenance | research:source-synthesis | advise | deliberative-advice | review
fails: creates duplicate skills; hides required logic in references; omits proof; stamps stale template version
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read the request, related skills, registry row, nearby project docs,
   [docs/skills/system.md](../../docs/skills/system.md),
   [docs/skills/README.md](../../docs/skills/README.md), and
   the relevant anchored section of
   [docs/skills/best-practices.md](../../docs/skills/best-practices.md), and
   any target skill-local `qa_checklist.md` when updating an existing skill
   with runtime QA guardrails.
- [ ] 2. Decide the owning surface and write the decision into the edit.
   - [ ] 1. Create a new skill only when the capability has a stable trigger and
     reusable workflow.
   - [ ] 2. Update an existing skill when the request is a branch, method,
     todo-list fix, reference, script, or prompt inside an existing contract.
   - [ ] 3. Resolve unclear ownership through the native planning phase or
     `harness-advisor` when the placement affects Farplane surfaces.
- [ ] 3. Ground the skill design before drafting when external examples or peer
   skills could change the contract.
   - [ ] Use [research:parity](../research/SKILL.md#researchparity) or
     [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
     when source comparison is required.
   - [ ] Use
     [advice and proof routing](../../docs/skills/best-practices.md#advice-and-proof-routing)
     before changing shared standards, Tier 1 primitives, meta skills, `eval`,
     templates, reviewer rubrics, or cross-skill policy.
- [ ] 4. Draft or revise `SKILL.md` so the first-load path is executable without
   hidden chat context.
   - [ ] Write `description` as one sentence under 220 characters using
     `Verb input/context into output/artifact when call-condition`.
   - [ ] Include trigger boundary, context, `## Skill Signature` when useful,
     ordered `## Todo List`, branches, hard gates, proof command, and output
     contract.
   - [ ] Prefer first-load sufficiency over modular neatness: keep required
     every-invocation context and gates in `SKILL.md` even when they could be
     abstracted into a reference.
   - [ ] Use
     [docs/skills/best-practices.md#placement-boundaries](../../docs/skills/best-practices.md#placement-boundaries)
     to place content by whether it is needed now on first load or later
     through an explicit reference branch, plus owner scope, depth, and length.
   - [ ] Use the structure optimization metrics in
     [docs/skills/best-practices.md](../../docs/skills/best-practices.md#structure-optimization)
     to decide what belongs in first-load `SKILL.md` versus references,
     templates, evals, or review checks.
   - [ ] Load and run the
     [Skill Structure QA Checklist](../skill-maintenance/qa_checklist.md)
     when first-load size, progressive disclosure, or reference placement is
     material.
   - [ ] For quality-dependent skills, add or link one good positive example
     before optimizing checklist prose.
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
   - [ ] For material skill creation or structural edits, create
     `skills/<skill-name>/audits/YYYY-MM-DD-<short-change>.md` from
     [skill-maintenance/templates/skill-audit.md](../skill-maintenance/templates/skill-audit.md),
     or state why the change is mechanical enough to skip an audit record.
   - [ ] Repeatability from files alone.
   - [ ] Run each item in
     [Skill Structure QA Checklist](../skill-maintenance/qa_checklist.md)
     against the actual changed files; fix or record every violation before
     completion.
   - [ ] Review depth chosen with
     [docs/skills/best-practices.md](../../docs/skills/best-practices.md#structure-optimization):
     direct self-check for tiny mechanical edits, `advise` for normal recent
     skills, and `deliberative-advice` for Tier 1, meta, `eval`, stale,
     high-blast-radius, cross-skill, or precedent-setting structure changes.
   - [ ] No duplicated first-load logic.
   - [ ] Actor-prompt versus skill-contract boundaries are clean.
   - [ ] Explicit proof commands or blockers are recorded.
   - [ ] Quality-dependent skills have at least one transferable example, or an
     explicit blocker explains why the example cannot be produced yet.
   - [ ] Native `reviewer` subagent used for material skill-system changes when
     available.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Minimal `SKILL.md` shape:

```markdown
## Context

## Skill Signature

```text
skill_action(input_text, state?) -> primary_output + evidence?
state: reads(...); writes(...)
gates: proof_condition; review_condition
routes: next-skill | direct-answer
fails: known bad behavior
```

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
- Put content in `SKILL.md` when it is needed now on first load; put it in
  `references/*` when it is only needed later through an explicit branch,
  deeper rationale, optional detail, or rare mode.
- Do not teach the whole domain in `SKILL.md`. If it reads like onboarding,
  move the material to references.
- Do not use frontmatter `description` as a trigger catalog or mini manual. It
  is only the pre-load routing definition.
- Do not duplicate the same rule across `SKILL.md`, references, templates,
  prompts, and README-style docs.
- Do not put actor identity, delegation routing, tool-use policy, or artifact
  writeback in a reusable skill contract.
- Do not spend a full pass polishing structure for a quality-dependent skill
  that has no representative example; make the example first unless the skill
  is too broken to run.

## Reference Map

- [docs/skills/system.md](../../docs/skills/system.md) - tier model, source
  ownership, frontmatter contract, template versioning, feature tracking, and
  todo-link rules.
- [docs/skills/README.md](../../docs/skills/README.md) - human skill selection
  guide, generated registry surface, and maintenance commands.
- [docs/skills/best-practices.md](../../docs/skills/best-practices.md) -
  first-load todo shape, reference placement, actor-prompt boundaries,
  structure optimization metrics, duplication control, repeatability, and
  review gates.
- [../skill-maintenance/qa_checklist.md](../skill-maintenance/qa_checklist.md)
  - first-class skill-local QA checklist for first-load size, progressive
  disclosure, reference routing, and compaction risk.
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
- The target skill `description` is a one-sentence functional routing
  definition under 220 characters.
- `SKILL.md` contains the minimum first-load contract without tutorial bloat.
- References are linked directly from `SKILL.md` and used only for conditional
  detail.
- Scripts, prompts, assets, and templates exist only when they support repeated
  execution.
- Registry validation passes, or the remaining blocker is recorded with the
  exact failing command.
