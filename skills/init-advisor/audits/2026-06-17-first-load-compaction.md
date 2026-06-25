---
skill: init-advisor
date: 2026-06-17
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/init-advisor/SKILL.md
after_ref: skills/init-advisor/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/skill-maintenance/qa_checklist.md
eval_required: no
---

# Skill Audit

## Change

- Before: `SKILL.md` mixed init workflow with long rationale, planning
  philosophy, manual copy steps, duplicated template inventory, and a large
  gotcha catalog.
- After: `SKILL.md` keeps the executable init contract, code scaffold signature,
  stack recipes, stop conditions folded into todos, and reference routing.
- Why: first-load context should contain only the information needed to choose,
  execute, stop, and prove the normal init path.
- Tradeoff accepted: detailed manual setup stays in skill-local references;
  Farplane file rationale lives in `docs/farplane-framework/project-files.md`.

## First-Load Review

```text
first_load_review:
  line_count_before: 559
  line_count_after: 167
  kept_in_skill: signature, phase boundary, numbered todos, code scaffold signature, stack recipes, reference map
  moved_to_reference: detailed manual bootstrap via README/reference map; project file rationale via docs/farplane-framework/project-files.md
  deleted_as_duplicate_or_rationale: Why This Structure, Planning Philosophy, duplicated template inventory, long gotcha catalog, Bootstrap Workflow section, Output section
  remaining_sections_over_budget: none
  verdict: pass
```

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Todos still bind target, select stack, initialize substrate, optional scaffold, PRD handoff, and verify. |
| `reference_load_precision` | pass | Reference Map names when to load project profiles, lifecycle, templates, framework file spec, README, and prompts. |
| `missing_context_rate` | pass | Gates for preservation, manifest, human stops, secrets, hooks, and PRD boundary remain in first load. |
| `noisy_context_rate` | pass | Long rationale/manual sections were removed from first load. |
| `duplicated_instruction_count` | pass | Removed duplicate template inventory and repeated workflow prose. |
| `prompt_size_tokens` | pass | Reduced `SKILL.md` from 559 to 167 lines. |
| `maintenance_locality` | pass | Script owns bootstrap mechanics; `SKILL.md` owns routing and stop conditions. |
| `composition_clarity` | pass | Signature and todos define inputs, writes, proof, and handoff. |
| `section_necessity` | pass | Remaining sections support normal invocation. |
| `gotcha_integration` | pass | Standalone gotchas were folded into todo gates and stop conditions. |
| `workflow_duplication` | pass | Removed manual step-by-step copy list, Bootstrap Workflow, and Output from first load. |
| `reference_escape_hatch` | pass | Detailed manual path points to README; Farplane file rationale points to framework docs. |
| `line_budget_review` | pass | Under 250 lines after compaction. |
| `question_list_to_signature` | pass | Code scaffold intake is represented by `code_scaffold(...)` params instead of a question list. |

## Proof Artifacts

- Skill-local evals, when needed: not required for structure-only compaction.
- Structure evals, when needed: `skills/skill-maintenance/qa_checklist.md`.
- Reviewer receipt: self-check; no separate reviewer lane used in this pass.
- Validator: pending command run in this turn.
- Eval required: no.
- Evidence gaps: no agent behavior run yet against installed copy.

## Before Behavior

- Agents loaded broad rationale and long branch details before the init branch was
  selected.

## After Behavior

- Agents load a compact init workflow and only branch into references when the
  target project or user request needs extra detail.

## Followups

- Run a live installed-skill smoke after reinstall to confirm the copied skill
  preserves the compact first-load shape.
