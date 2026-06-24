---
title: Skill Structure Checklist
owner: skill-maintenance
status: active
kind: qa-checklist
created_at: 2026-06-13
updated_at: 2026-06-17
feature_refs:
  - FEAT-0057
applies_to:
  - skills
---

# Skill Structure QA Checklist

This is the first-class skill-local QA checklist for skill structure changes.
Use it before creating or materially restructuring a skill as preflight
guardrails, then use it again before claiming the change is ready. Use the
target skill's own `qa_checklist.md` when a skill has domain-specific runtime
checks. Run each check against the actual changed files. Do not treat the
checklist as a passive reminder; write down violations, then fix or explicitly
defer them in the skill-local audit or final proof notes.

```text
skill_qa_checklist(skill_package, changed_files, claim, budget?)
  -> checklist_verdicts + fixes_or_deferrals + evidence_note
```

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

## First-Load Required Set

Keep a detail in `SKILL.md` only when it is needed to choose, execute, stop, or
prove the normal path:

- trigger/context boundary
- skill signature, inputs, outputs, state reads/writes, gates, routes, and fails
- numbered todo list with the normal workflow
- hard gates, stop conditions, and human handoff points
- reference map with precise load conditions
- final result/proof contract, usually in the signature or todo list
- short command examples that are normally run

## Checklist Placement

For skills with domain-specific runtime guardrails, prefer one discoverable
checklist file at the skill package root:

```text
skill_invocation_with_checklist(skill_package, task)
  -> read(SKILL.md)
   + read(qa_checklist.md when present)
   + execute_with_preflight_guardrails
   + final_checklist_verdict
   + independent_review_when_material
```

Use this placement rule:

- Put a short warning in `SKILL.md` only when the agent is likely to fail unless
  it knows the warning before execution.
- Put detailed, reusable checks in `qa_checklist.md` when they should be read
  at skill start and applied to the finished work.
- Keep rare examples, long rubrics, and branch-specific checklists in
  `references/*` only when `SKILL.md` states exactly when to load them.
- Do not mirror all checklist items into `## Gotchas`; duplicate truth creates
  stale prevention rules.

The baseline `SKILL.md` section set comes from
`../../docs/skills/templates/SKILL_TEMPLATE.md`. Extra top-level sections are
allowed only when they add substantial unique first-load value that cannot be
folded cleanly into `Context`, `Skill Signature`, `Phase Boundary`, `Todo List`,
`Templates`, `Gotchas`, `Reference Map`, or the signature/todo result contract.

## Move Or Remove Candidates

Move these to references, docs, audits, or templates unless the todo list proves
they are needed on every invocation:

- rationale sections such as `Why This Structure`
- historical notes, philosophy, or tutorial prose
- long gotcha catalogs that can become todo gates
- detailed manual setup steps when a script owns the path
- rare branches, migration guides, and extended examples
- full template inventories duplicated by the filesystem
- repeated rules already owned by project docs or system docs
- long question lists that can become a function signature with params
- `Output` sections that duplicate the signature and todo finish step
- extra top-level sections that duplicate or lightly rename a core template
  section

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

9. `section_necessity`
   - Question: Does each top-level section satisfy the First-Load Required Set?
   - Violation: A section exists mainly to explain history, rationale, philosophy,
     or optional background.

10. `gotcha_integration`
    - Question: Are gotchas folded into todos, gates, fails, or concise stop
      conditions where possible?
    - Violation: `SKILL.md` carries a long gotcha section that the workflow does
      not operationalize.

11. `workflow_duplication`
    - Question: Does prose duplicate the numbered todo list or a bootstrap script?
    - Violation: The skill explains the same workflow twice instead of keeping
      the executable path in one place.

12. `reference_escape_hatch`
    - Question: When detail moves out of first load, does `SKILL.md` say when to
      load the new reference?
    - Violation: Detail is hidden in a reference with no branch condition.

13. `line_budget_review`
    - Question: Did the maintainer actively inspect length after the edit?
    - Violation: If `SKILL.md` exceeds roughly 250 lines, the audit lacks the top
      removable sections. If it exceeds roughly 400 lines, treat it as a failure
      unless mandatory first-load contracts justify the size.

14. `question_list_to_signature`
    - Question: Can a long list of intake questions become a compact function
      signature, parameter list, or schema?
    - Violation: The skill lists many fixed questions even though normal agent
      behavior can infer and ask only for missing parameters.

15. `extra_section_value`
    - Question: For each top-level section not present in the current skill
      template, can it fold into a core section without losing behavior?
    - Violation: An extra section exists for organization, explanation, or a
      light rename of template content rather than substantial unique
      first-load value.
    - Evidence required when keeping it: name the section, why core sections are
      insufficient, what behavior would be lost by folding it, and why a
      reference file would create too much defer-loading risk.

16. `proof_surface_fit`
    - Question: Does the skill choose the right proof surface for its behavior:
      deterministic test or validator for mechanically checkable behavior,
      eval for variable AI behavior, agent QA or behavior capture for multi-turn
      tool/artifact proof, and manual/review only when judgment is explicit?
    - Violation: The skill calls every proof a unit test, routes parseable
      outputs to an LLM judge, skips evals for prompt-like behavior, or treats
      reviewer prose as behavior proof without a case, artifact, or command.

17. `task_case_quality`
    - Question: When a skill adds tests, evals, examples, or QA scenarios, are
      the cases realistic, distinct, traceable to a risk/source, judgeable, and
      small enough to maintain?
    - Violation: The skill adds happy-path-only examples, near-duplicate eval
      rows, synthetic cases with no stated coverage gap, or cases whose failure
      would not identify what to fix.

18. `anti_cheat_case_design`
    - Question: For skill evals and agent behavior cases, does the user-facing
      query avoid leaking the skill name, expected routing, checklist, reference
      points, or desired answer?
   - Violation: The test prompt teaches the behavior it claims to measure,
     making the case a memory test of the eval author's wording instead of a
     behavior test of the skill.

19. `qa_preflight_loaded`
   - Question: When a skill has `qa_checklist.md`, does `SKILL.md` tell the
     invoking agent to read it before execution as preflight guardrails?
   - Violation: The checklist is only mentioned as a final cleanup step, so the
     agent may discover the gotchas after making the mistake.

20. `qa_finish_independence`
   - Question: For material work, does the finish path apply the checklist
     again and route independent reviewer/subagent verification when useful?
   - Violation: The author self-certifies material checklist conformance without
     a reviewer lane or a recorded reason to keep review inline.

21. `qa_gotcha_deduplication`
   - Question: Are `## Gotchas` and `qa_checklist.md` separated by job rather
     than mirrored?
   - Violation: `SKILL.md` repeats the full checklist as gotchas, or
     `qa_checklist.md` merely copies gotchas without structured evidence,
     violation, fix, or deferral checks.

22. `project_specific_context_isolation`
   - Question: If the skill is reusable, does it avoid embedding a specific
     project, person, private path, customer, automation profile, or local
     workflow in `SKILL.md`, first-load refs, evals, templates, or generated
     registry-visible metadata?
   - Violation: A generic skill links to or names a project-specific profile,
     private path, personal workflow, or customer/source assumption that every
     caller would see. Move it to the Codex automation prompt, project docs,
     bindings, examples, or caller-supplied hook refs. Personal/project skills
     may keep specific context only when that specificity is the skill's stated
     purpose.

## Finish Gate

For material `SKILL.md` changes, record this in the audit or final proof notes:

```text
first_load_review:
  line_count_before:
  line_count_after:
  kept_in_skill:
  moved_to_reference:
  deleted_as_duplicate_or_rationale:
  extra_sections_kept_with_reason:
  remaining_sections_over_budget:
  proof_surface_fit:
  task_case_quality:
  anti_cheat_case_design:
  qa_preflight_loaded:
  qa_finish_independence:
  qa_gotcha_deduplication:
  project_specific_context_isolation:
  verdict: pass | fail | unknown
```

## Subagent Review Prompt

Use a reviewer or QA subagent when independent structure checking is worth the
coordination cost:

```text
Review the changed skill files against
skills/skill-maintenance/qa_checklist.md.

If the target skill has its own qa_checklist.md, read that file independently
too. Verify that the author used it as preflight prevention and final
verification, then apply it against the finished work.

For each checklist item, return:
- verdict: pass | violation | not_applicable
- evidence: exact file/path and short quote or line reference
- fix: smallest required edit, or "none"

For every top-level section not in
docs/skills/templates/SKILL_TEMPLATE.md, decide whether it should
fold into a core section, move to a reference, delete as duplicate/rationale, or
remain because it provides substantial unique first-load value.

Do not rewrite the skill. Do not judge product quality. Only report structure
checklist violations and the highest-risk unresolved issue.
```
