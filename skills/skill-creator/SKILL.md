---
name: skill-creator
description: "Turn a reusable workflow or capability idea into a Farplane skill package with frontmatter, todo path, references, and proof surfaces."
tier: 3
group: operations
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

Treat file length as a diagnostic, not a gate. Split conditional detail by
branch or responsibility when doing so improves ownership or first-load cost;
do not hide default-path behavior merely to reduce a count.

## Skill Signature

```text
create_or_update_skill(request, existing_surface?, proof_need?)
  -> skill_package_change + validation_result
state: reads(skill docs, registry, target, template, QA); writes(owner-local package, registry?)
gates: trigger_stable; first_load_executable; structure_coherent;
       template_truthful; book_branch_explicit_when_applicable;
       book_sources_type_confidence_convergence_labeled;
       runnable_eval_rows_created_or_deferred; proof_named; review_ready
routes: gap-analysis | skill-maintenance | research:source-synthesis |
  eval | self-improve | goal-advisor | review
fails: duplicate skill; hidden default workflow; arbitrary line-count splitting;
  stale template claim; book request without named extraction branch/schema;
  book grounding without source convergence or copyright boundary;
  scenario-only eval plan; applicable self-improve without artifact or reason;
  missing proof
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
   - [ ] For book-summary grounding, search workflow-bearing videos, articles,
     blogs, apps/notes, and author interviews; label source type, confidence,
     and convergence instead of trusting one summary. Explicitly follow the
     `book-to-skill extraction` branch even when book or target inputs are
     missing, and never produce a chapter-by-chapter or substitute-book summary.
   - [ ] Convert takeaways into workflow candidates with trigger, inputs,
     steps, decisions, stop condition, output, and proof. Compare each candidate
     with the target skill before choosing `SKILL.md`, a reference,
     `evals/evals.json`, `qa_checklist.md`, a new skill, reject, or defer; test
     behavior rather than book recall. State this schema and placement set even
     when grounding must pause for missing inputs, and name at least one
     concrete positive example or eval row that proves the extracted workflow.
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
- [ ] 5. Place supporting detail by responsibility and load frequency.
   - [ ] Keep every-invocation behavior in `SKILL.md`; move conditional branches,
     long examples, templates, rubrics, provider maps, and rare recipes to
     precisely linked supporting files.
   - [ ] Use the
     [method reference template](../../docs/skills/templates/METHOD_REFERENCE_TEMPLATE.md)
     and declare `skill-method-reference` for reusable method workflows.
   - [ ] Split only when the result improves ownership or first-load behavior;
     raw line count is not a pass/fail condition.
- [ ] 6. Run `python3 ../skill-maintenance/scripts/check_skills.py --write`
  plus focused script, JSON, and eval checks.
- [ ] 7. Finish with proof and review.
   - [ ] Apply both QA checklists again and record pass, violation,
     not-applicable, or deferred for changed surfaces.
   - [ ] For material structural work, create a dated skill-local audit from
     [skill audit template](../skill-maintenance/templates/skill-audit.md); for a
     mechanical edit, record the skip reason.
   - [ ] For new behavior-sensitive skills, enable eval metadata, create
     executable `evals/evals.json` rows with natural prompts, expected outputs,
     and assertions, then hand execution and candidate/baseline comparison to
     [eval](../eval/SKILL.md). Record pass, fail, or an explicit deferred-proof
     blocker. Do not self-grade or substitute scenario titles for runnable
     cases. Treat failures as blockers or fixes and rerun the smallest case
     through `eval` before readiness.
     In a read-only/dry-run fixture, return explicit `eval_result: deferred`,
     `eval_blocker`, and `readiness: blocked` fields plus the smallest-failure
     rerun rule; never report readiness from inspection alone.
   - [ ] For artifact-creation skills that warrant continued optimization,
     route through `self-improve` with an owning ticket and canonical suite;
     Goal Advisor instantiates ticket `program.md` and `progress.md`, then the
     run records a real baseline. Otherwise record the exact
     `no_self_improve_reason` field before readiness. A dry run without a real
     baseline must use that field instead of claiming readiness.
   - [ ] Use the native reviewer for material or precedent-setting changes.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Use [skill package template](../../docs/skills/templates/SKILL_TEMPLATE.md) for
new skills and the method reference template linked above for reusable methods.
Standalone package helpers remain available under `scripts/` when a concrete
non-Farplane package artifact is required.

For every book-grounded request, return this branch contract even if inputs are
missing:

```text
branch: book-to-skill extraction
sources: videos + articles/blogs + app summaries/notes + author interviews
source_assessment: type + confidence + cross-source convergence
workflow_candidate: trigger + inputs + steps + decisions + stop + output + proof
placement_comparison: existing target -> SKILL.md | reference | evals/evals.json |
  qa_checklist.md | new skill | reject | defer
copyright_boundary: no chapter-by-chapter or substitute-book summary
behavior_proof: concrete positive example or eval row, never book recall
```

## Gotchas

- Do not create skills for generic knowledge, one-off notes, raw library docs,
  or behavior better owned by a script, ticket, prompt, or existing skill.
- Do not hide required routing, gates, proof, or output to reduce file length.
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
- [eval](../eval/SKILL.md) — run the initial skill suite, grade evidence, and
  compare a candidate with no-skill or previous-skill behavior before readiness.
- [workflows](references/workflows.md) — load when todo branches need shaping.
- [architecture](references/architecture.md) — load when ownership between
  first load, references, scripts, prompts, and assets is unclear.
- [output patterns](references/output-patterns.md) — load when a template,
  example, validator, or structured output needs calibration.
- [tier-3 pipeline model](references/tier3-pipeline-model.md) — load only for a
  complex Tier 3 pipeline.

## Output

Return changed owner-local files, proof commands/results, QA verdicts, registry
status, audit or skip reason, and reviewer result or blocker. For dry-run creation,
include the complete proposed eval JSON rows and explicit proof/self-improve
fields required by todo 7, including `rerun_rule: fix and rerun the smallest
failing eval before readiness`; a filename or scenario list is not enough.
