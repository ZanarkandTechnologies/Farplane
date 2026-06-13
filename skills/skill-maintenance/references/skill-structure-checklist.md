---
title: Skill Structure Checklist
owner: skill-maintenance
status: active
created_at: 2026-06-13
---

# Skill Structure Checklist

Use this checklist after creating or materially restructuring a skill. Run each
check against the actual changed files. Do not treat the checklist as a passive
reminder; write down violations, then fix or explicitly defer them in the
skill-local audit or final proof notes.

## Threshold

```text
place_skill_detail(detail)
  -> SKILL.md when defer_loading_risk > context_rot_risk + compaction_loss_risk
  -> reference when defer_loading_risk <= context_rot_risk + compaction_loss_risk
```

- `defer_loading_risk`: cost that the agent fails, asks, or drifts because
  detail was not loaded immediately.
- `context_rot_risk`: cost of loading detail before the branch is chosen,
  including distraction, stale assumptions, and duplicated instruction.
- `compaction_loss_risk`: cost that bulky first-load context causes chat
  compaction before task state, user corrections, or evidence are stable.

## Checks

1. `first_load_sufficiency`
   - Question: Can another agent execute the normal path from `SKILL.md`
     without hidden chat context?
   - Violation: Required trigger, state, routing, proof, or output contract is
     only in a reference.

2. `reference_load_precision`
   - Question: Does every reference have an explicit read condition in the todo
     list or Reference Map?
   - Violation: A reference is listed without saying when to load it.

3. `missing_context_rate`
   - Question: Are required gates, routing, proof, and output contracts still in
     first load?
   - Violation: The skill becomes shorter by hiding mandatory behavior.

4. `noisy_context_rate`
   - Question: Did the change leave long templates, examples, rare branches, or
     tutorial prose in first load when they only matter after a branch is chosen?
   - Violation: First load teaches a rare branch before the branch is selected.

5. `duplicated_instruction_count`
   - Question: Is the same rule copied across `SKILL.md`, references,
     templates, docs, and examples without distinct jobs?
   - Violation: Two surfaces own the same operational rule.

6. `prompt_size_tokens`
   - Question: Is `SKILL.md` short enough that agents can read and use it before
     task context compacts?
   - Violation: `SKILL.md` is over roughly 250 lines and most extra lines are
     not gates, routing, or output contract.

7. `maintenance_locality`
   - Question: Does future editing have one obvious owner surface?
   - Violation: A maintainer would not know whether to edit `SKILL.md`,
     reference, template, docs, eval, or audit.

8. `composition_clarity`
   - Question: Are inputs, outputs, state reads/writes, evidence, and routes
     explicit?
   - Violation: A caller cannot tell what the skill consumes, writes, proves, or
     hands off.

## Subagent Review Prompt

Use a reviewer or QA subagent when independent structure checking is worth the
coordination cost:

```text
Review the changed skill files against
skills/skill-maintenance/references/skill-structure-checklist.md.

For each checklist item, return:
- verdict: pass | violation | not_applicable
- evidence: exact file/path and short quote or line reference
- fix: smallest required edit, or "none"

Do not rewrite the skill. Do not judge product quality. Only report structure
checklist violations and the highest-risk unresolved issue.
```
