---
name: consolidate
description: "Compress artifacts into their minimal owner-correct form when material value must be preserved while duplication, fluff, or sprawl is removed."
tier: 1
source: local
template_uses:
  skill-template: "0.3.5"
  skill-eval-task: "0.1.0"
eval: eval_task.json
allowed-tools: Read, Glob, Grep, Bash
---

# Consolidate

## Context

`consolidate` is a Tier 1 primitive for value-preserving compression. Use it
when an artifact or entity set needs to become smaller, clearer, or more
owner-correct without losing required behavior, proof, IDs, decisions, or future
actionability.

Consolidation is not summarization. Summarization can reduce detail for a
reader; consolidation rebuilds the target into the smallest shape that still
satisfies its owning template, schema, workflow contract, or first-principles
purpose.

## Skill Signature

```text
consolidate(target, structure?, template?, constraints?, value_function?, proof?)
  -> inventory
   + unit_decisions
   + minimal_artifact_or_patch
   + loss_check
   + handoff_or_blocker

state:
  reads(target artifact(s), owning template/schema/docs?, consumers?,
        local proof or usage evidence?)
  writes(updated artifact? or patch/handoff?; audit note? when material)
gates:
  target_bound; owner_or_template_identified; units_inventory_complete;
  value_function_named; hard_constraints_preserved; loss_check_passed
routes:
  documentation | skill-maintenance | update-memory | knowledge-tidier |
  metric-advisor | eval | review | direct-edit
fails:
  summarizes instead of consolidating; violates hard constraints; deletes
  required IDs/proof/gates; optimizes word count over value; hides losses;
  moves material to a wrong owner; invents a template when an existing one owns it
```

Input contract:

```text
structure = file | directory | registry | skill | eval_suite | gotchas |
            checklist | docs_tree | memory | other
unit = section | file | row | bullet | eval_case | checklist_item |
       gotcha | metric | template_slot | other
constraints = {
  max_words?: int,
  max_files?: int,
  max_sections?: int,
  preserve_ids?: bool,
  preserve_evidence?: bool,
  preserve_required_sections?: bool,
  no_delete?: bool,
  owner_boundary?: string
}
action = keep | merge | rewrite | move | delete | promote | demote | defer
```

Default value function:

```text
value(unit) =
  execution_value
+ proof_value
+ routing_value
+ reuse_value
+ memory_value
+ user_value
- fluff
- duplication
- stale_risk
- wrong_owner_risk
```

Hard constraints beat the value function. The value function decides how to use
scarce space only after required IDs, evidence, gates, safety constraints, and
owner boundaries are preserved.

Required response frame:

```text
1. Bound target:
2. Owning template or contract: <exact path/name; for local skills use docs/skills/templates/SKILL_TEMPLATE.md>
3. Hard constraints:
4. Value function: execution_value + proof_value + routing_value + reuse_value + memory_value + user_value - fluff - duplication - stale_risk - wrong_owner_risk
5. Unit inventory:
6. Unit decisions:
7. Minimal artifact, patch, or handoff:
8. Loss check:
9. Proof: <for material skill edits, include skill-maintenance validation and review route>
```

Fill this frame even for advice-only calls. Do not paraphrase the value function
in a way that drops proof, routing, reuse, memory, or user value. If the raw
target content is missing, say which frame fields are provisional and return the
smallest safe patch plan or blocker instead of pretending category-level guesses
are a unit inventory.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the target and hard constraints.
  - [ ] Resolve `target` and `structure`.
  - [ ] Bind explicit limits such as word count, file count, preserved IDs,
    required sections, no-delete policy, or owner boundary.
  - [ ] If constraints conflict, name the tradeoff and ask only when the
    conflict would force data loss or wrong ownership.
- [ ] 2. Find the owning template or infer the minimal contract.
  - [ ] Load the existing template, schema, section contract, registry contract,
    skill template, ticket template, or consumer docs when present.
  - [ ] Name the exact template or contract in the output, such as
    `docs/skills/templates/SKILL_TEMPLATE.md` for local skill `SKILL.md`
    consolidation.
  - [ ] If no template exists, infer the minimum contract from first principles:
    purpose, reader/user, owner, required decisions, required evidence, and
    finish proof.
  - [ ] Do not invent a new durable template unless the caller explicitly asks
    for template design or no existing owner can carry the result.
- [ ] 3. Inventory and slice the artifact.
  - [ ] Split the target into natural units: sections, files, rows, bullets,
    eval cases, checklist items, gotchas, metrics, or template slots.
  - [ ] Record consumers, backlinks, IDs, required proof, and owner surfaces
    before proposing deletions or moves.
  - [ ] For directories or registries, sample enough units to find duplicates
    before editing all of them.
- [ ] 4. Score units with the value function.
  - [ ] Name the value function used; start from the default and adapt it only
    when the target has a clearer domain value function.
  - [ ] When adapting the default, still account for proof, routing, reuse,
    memory, and user value unless you explicitly explain why a component is not
    relevant.
  - [ ] Classify each unit as `keep`, `merge`, `rewrite`, `move`, `delete`,
    `promote`, `demote`, or `defer`.
  - [ ] Treat redundant, outdated, trivial, wrong-owner, and low-proof material
    as consolidation candidates, not automatic deletion candidates.
- [ ] 5. Rebuild the minimal owner-correct artifact.
  - [ ] Fill the owning template or inferred contract section by section.
  - [ ] Merge duplicates into one stronger unit.
  - [ ] Rewrite verbose units into executable rules, decisions, proof gates, or
    examples only when their value survives.
  - [ ] Move branch-specific, rare, or deep material to the right owner surface
    only when the first-load or primary artifact remains sufficient.
  - [ ] When moving examples or rare detail, name the destination path or owner,
    such as `references/examples.md`, and explain how future readers find it.
- [ ] 6. Run the loss check.
  - [ ] Check whether any required behavior, evidence, ID, route, owner
    boundary, safety condition, metric, or future action was lost.
  - [ ] Restore, move, or explicitly block when the loss is material.
  - [ ] Verify that the result is not merely shorter; it must be more
    owner-correct and at least as useful for its purpose.
- [ ] 7. Finish with proof and handoff.
  - [ ] For direct edits, run the relevant validator, link check, eval, test,
    or review surface for the owner.
  - [ ] For advice-only consolidation, return the unit-decision table and the
    proposed patch/handoff instead of silently editing.
  - [ ] For material changes, include before/after size or shape, decisions by
    action, loss-check result, proof run, and remaining risks.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Examples

Skill gotchas:

```text
consolidate(target = skills/*/references/gotchas.md, structure = gotchas)
  -> repeated runtime failures promoted to qa_checklist.md or eval_task.json
   + stale one-off warnings deleted
   + examples moved to references only when branch-specific
```

Feature registry rows:

```text
consolidate(target = docs/features/registry.jsonl, structure = registry,
            constraints = { preserve_ids: true })
  -> canonical spec metadata retained
   + generated compatibility output preserved
   + stale rows retired only with validator proof
```

## Gotchas

- Do not use word count as the primary metric. Word count is a constraint;
  value preservation is the objective.
- Do not collapse different owners into one convenient file. If the target
  belongs in multiple owner surfaces, consolidate each surface separately and
  link them.
- Do not delete rare-but-critical proof, IDs, rollback notes, eval hard cases,
  or safety constraints just because they are low frequency.
- Do not move required first-load behavior into references unless the default
  artifact remains executable without hidden context.
- Do not skip the required response frame. Missing raw content can block a
  concrete edit, but it does not remove the obligation to name the template,
  constraints, value function, unit inventory status, loss check, and proof
  route.
- Do not self-approve material skill edits. If `structure = skill` or the
  target is `skills/*/SKILL.md`, route final edits through `skill-maintenance`
  validation and material review.
- Do not call category buckets a complete unit inventory. For gotchas, evals,
  registry rows, checklist items, and metrics, inspect or request the individual
  units before deleting, merging, or promoting them.

## Reference Map

- `docs/skills/system.md` - Tier 1 primitive contract and skill-system source
  ownership.
- `docs/skills/best-practices.md#structure-optimization` - structure metrics
  for skill consolidation and placement.
- `skills/skill-maintenance/qa_checklist.md` - skill-specific structure review
  when consolidating skill packages.
- `tickets/TASK-0231/ticket.md` - completed generated-registry consolidation
  exemplar.
- `tickets/TASK-0232/ticket.md` - planned skill consolidation workflow and
  metrics exemplar.

## Output

- `inventory`: units inspected plus required IDs, consumers, owners, and proof.
- `unit_decisions`: table or bullets with `keep | merge | rewrite | move |
  delete | promote | demote | defer`.
- `minimal_artifact_or_patch`: edited artifact, patch plan, or handoff.
- `loss_check`: preserved value, detected losses, restored material, and risks.
- `proof`: validator, eval, review, or explicit blocker.
