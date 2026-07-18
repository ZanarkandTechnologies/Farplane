---
name: skill-creator
description: "Turn a reusable workflow or capability idea into a Farplane skill package with frontmatter, todo path, references, and proof surfaces."
tier: 3
group: skills
source: local
eval: evals/evals.json
template_uses:
  skill-template: "0.3.2"
  skill-qa-checklist: "0.1.0"
  skill-surface-budget: "0.1.0"
qa_checklist: qa_checklist.md
license: Complete terms in LICENSE.txt
allowed-tools: mcp__sequential-thinking__sequentialthinking, Read, Write, Grep, Glob
---

# Skill Creator

## Context

Use this skill to create or update a stable reusable workflow. Read
`qa_checklist.md`, the target package, its registry row, and the relevant parts
of [skill system](../../docs/skills/system.md) and
[skill best practices](../../docs/skills/best-practices.md) before editing.
Update an existing owner instead of creating a duplicate skill.

Every staged hand-authored text file under `skills/` must be at most 200 lines.
Split conditional detail by branch or responsibility; do not hide default-path
behavior merely to meet the limit. Generated graphs, dependency locks, and
media assets are excluded by the commit gate.

## Skill Signature

```text
create_or_update_skill(request, existing_surface?, proof_need?)
  -> skill_package_change + validation_result
state: reads(skill docs, registry, target, template, QA); writes(owner-local package, registry?)
gates: trigger_stable; first_load_executable; each_authored_file_lines<=200;
       template_truthful; proof_named; review_ready
routes: gap-analysis | skill-maintenance | research:source-synthesis |
  self-improve | goal-advisor | review
fails: duplicate skill; hidden default workflow; oversized staged skill file;
  stale template claim; missing proof
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Ground the request and bind the owner.
   - [ ] Read `qa_checklist.md`, the target `SKILL.md`, target-local QA/evals,
     registry row, nearby docs, and the relevant template/best-practice section.
   - [ ] Create a skill only for a stable reusable trigger; otherwise update the
     existing skill, reference, script, template, eval, or validator owner.
   - [ ] Use `harness-advisor` when ownership crosses Farplane surfaces.
- [ ] 2. Name the behavior delta, trigger boundary, inputs, outputs, state,
  gates, failure modes, proof need, and non-goals before drafting.
- [ ] 3. Ground domain behavior when external practice could change the design.
   - [ ] Use `research:parity` or `research:source-synthesis` for comparison.
   - [ ] For book or longform inputs, load
     [book-to-skill extraction](references/book-to-skill.md).
   - [ ] Use the advice/proof routing in skill best practices before changing
     shared standards, meta skills, templates, eval, or reviewer policy.
- [ ] 4. Draft the minimum executable first-load contract.
   - [ ] Keep trigger/context, signature, numbered todo path, branches, hard
     gates, stop conditions, proof, reference routing, and output visible.
   - [ ] Write a one-sentence frontmatter description under 220 characters.
   - [ ] Apply the domain-specificity rubric from `qa_checklist.md`; include a
     domain workflow move, judgment gate, and positive example when quality is
     human-judged.
   - [ ] Apply the
     [Skill Structure QA Checklist](../skill-maintenance/qa_checklist.md).
- [ ] 5. Place supporting detail and enforce the file cap.
   - [ ] Keep every-invocation behavior in `SKILL.md`; move conditional branches,
     long examples, templates, rubrics, provider maps, and rare recipes to
     precisely linked supporting files.
   - [ ] Use the
     [method reference template](../../docs/skills/templates/METHOD_REFERENCE_TEMPLATE.md)
     and declare `skill-method-reference` for reusable method workflows.
   - [ ] Run the staged line-limit check before completion; split every included
     authored text file over 200 lines without weakening first-load behavior.
- [ ] 6. Run `python3 ../skill-maintenance/scripts/check_skills.py --write`,
  focused script/JSON/eval checks, and the staged line-limit validator.
- [ ] 7. Finish with proof and review.
   - [ ] Apply both QA checklists again and record pass, violation,
     not-applicable, or deferred for changed surfaces.
   - [ ] For material structural work, create a dated skill-local audit from
     [skill audit template](../skill-maintenance/templates/skill-audit.md); for a
     mechanical edit, record the skip reason.
   - [ ] Add or run representative behavior proof for behavior-sensitive work,
     or name the stronger owner and blocker.
   - [ ] Use the native reviewer for material or precedent-setting changes.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Use [skill package template](../../docs/skills/templates/SKILL_TEMPLATE.md) for
new skills and the method reference template linked above for reusable methods.
Standalone package helpers remain available under `scripts/` when a concrete
non-Farplane package artifact is required.

## Gotchas

- Do not create skills for generic knowledge, one-off notes, raw library docs,
  or behavior better owned by a script, ticket, prompt, or existing skill.
- Do not meet 200 lines by hiding required routing, gates, proof, or output.
- Do not split one coherent function mechanically; split by branch, provider,
  responsibility, or artifact type and keep precise load conditions.
- Do not duplicate rules across `SKILL.md`, references, templates, prompts, and
  docs, or put actor identity and delegation policy in a reusable skill.
- Do not call QA complete with “looks good”; name verdicts and evidence paths.

## Reference Map

- [skill system](../../docs/skills/system.md) — metadata, tiers, registry, and
  todo-link contracts; read for every structural update.
- [skill best practices](../../docs/skills/best-practices.md) — placement,
  repeatability, examples, and review; read the relevant anchored section.
- [creator QA](qa_checklist.md) — preflight and final authoring guardrails.
- [structure QA](../skill-maintenance/qa_checklist.md) — apply to every create
  or update invocation.
- [workflows](references/workflows.md) — load when todo branches need shaping.
- [architecture](references/architecture.md) — load when ownership between
  first load, references, scripts, prompts, and assets is unclear.
- [output patterns](references/output-patterns.md) — load when a template,
  example, validator, or structured output needs calibration.
- [tier-3 pipeline model](references/tier3-pipeline-model.md) — load only for a
  complex Tier 3 pipeline.

## Output

Return changed owner-local files, proof commands/results, QA verdicts, registry
status, audit or skip reason, and reviewer result or blocker. Confirm each
staged authored skill text file is at most 200 lines.
