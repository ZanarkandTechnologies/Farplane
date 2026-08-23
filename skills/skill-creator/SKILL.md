---
name: skill-creator
description: "Turn a new reusable workflow or capability idea into its first Farplane skill package with Golden Workflow Nodes, calibration, and proof."
tier: 3
group: operations
source: local
eval: evals/evals.json
template_uses:
  skill-template: "0.5.0"
  skill-surface-budget: "0.1.0"
allowed-tools: mcp__sequential-thinking__sequentialthinking, Read, Write, Grep, Glob
---

# Skill Creator

## Context

Use this skill to create a new stable reusable workflow. If a package or owner
already exists, route the change to `skill-maintenance`. Read the target owner
area, its registry neighbors, and the relevant parts
of [skill system](../../docs/skills/system.md) and
[skill best practices](../../docs/skills/best-practices.md) before editing.
Update an existing owner instead of creating a duplicate skill.

Keep every edited `skills/**/SKILL.md` at or below 200 physical lines. Split
conditional detail by branch or responsibility when doing so improves
ownership or first-load cost; do not hide default-path behavior merely to hit
the envelope.

## Skill Signature

```text
create_skill(request, proof_need?)
  -> skill_package_change + validation_result
reads: skill docs, registry, target package, template, QA, and evidence
does: creates the smallest owner-correct first skill contract
writes: owner-local skill files and generated registry data through validators
returns: changed files, validation evidence, and review result or blocker
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Admit the reusable workflow to its owner.**
  `request + registry context -> owner decision | maintenance | reject`

  Rule: Create only for a stable reusable trigger; existing packages route to
  `skill-maintenance` and cross-surface uncertainty to `harness-advisor`.

  Assert:
  - The owner and rejected alternatives are named.
- [ ] **N2 — Bind the behavior contract before drafting.**
  `accepted owner -> inputs + controls + output + proof + non-goals`

  Rule: Add only independently variable caller controls; keep fixed or derived
  behavior in the owning workflow.

  Assert:
  - The signature can be executed without transcript-only context.
- [ ] **N3 — Extract decision-changing domain workflow.**
  `sources -> workflow candidates | insufficient evidence | reject as summary`

  Rule: Retain source knowledge only when it changes a signal, decision,
  branch, output, or proof obligation.

  Assert:
  - Every retained insight maps to a node, golden, eval, guard, or validator.
- [ ] **N4 — Draft the executable first-load contract.**
  `behavior contract -> three-to-seven Golden Workflow Nodes | generic draft`

  Rule: Each top-level node must be one n8n-sized operation with inspectable
  state and a domain decision a generic agent would miss.

  Assert:
  - Important domain paths reach differentiated advantage.
- [ ] **N5 — Route conditional depth without hiding the normal path.**
  `first-load draft -> compact package + precise references | oversized contract`

  Rule: Keep every-invocation behavior in `SKILL.md`; move only conditional
  branches, long examples, templates, rubrics, or rare recipes.

  Assert:
  - Each reference has a named consumer and load condition.
- [ ] **N6 — Synchronize source and generated skill state.**
  `authored package -> registry-consistent validation evidence | repair`

  Rule: Run `python3 ../skill-maintenance/scripts/check_skills.py --write`
  plus focused script, JSON, and eval checks.

  Assert:
  - Template claims match actual structure and generated metadata.
- [ ] **N7 — Prove advantage and obtain an independent verdict.**
  `validated package -> reviewed readiness receipt | blocked`

  Rule: Behavior-sensitive skills require normal, hard, and boundary cases plus
  candidate/no-skill comparison; inspection-only dry runs cannot prove readiness.

  Assert:
  - Golden examples expose decisive node traces.
  - Material changes have a `skill-contract` reviewer verdict.
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
  runtime QA guard | new skill | reject | defer
copyright_boundary: no chapter-by-chapter or substitute-book summary
behavior_proof: concrete positive example or eval row, never book recall
```

## Gotchas

- Do not create skills for generic knowledge, one-off notes, raw library docs,
  or behavior better owned by a script, ticket, prompt, or existing skill.
- Do not hide required routing, gates, proof, or output to reduce file length.
- Do not expand signatures into state-machine catalogs. Put workflow rules in
  Todo List, failure examples in Gotchas, and consumed output schemas in Templates.
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
- [skill-contract rubric](../../docs/review/rubrics/skill-contract.md) — apply
  before readiness to node execution, edge, calibration, proof, and ownership.
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
