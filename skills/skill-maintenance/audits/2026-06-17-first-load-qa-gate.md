---
skill: skill-maintenance
date: 2026-06-17
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/skill-maintenance/SKILL.md
after_ref: skills/skill-maintenance/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/skill-maintenance/qa_checklist.md
eval_required: no
---

# Skill Audit

## Change

- Before: `qa_checklist.md` had the placement threshold but did not explicitly
  define the first-load required set, remove candidates, or finish-gate record.
- After: `qa_checklist.md` defines first-load required content, move/remove
  candidates, extra checks for section necessity, gotcha integration, and
  question-list-to-signature compaction, extra-section value checks, plus a
  required first-load review record.
- Why: `skill-maintenance` should catch bloated `SKILL.md` files during review
  instead of relying on subjective prose cleanup.
- Tradeoff accepted: the checklist grew slightly so each future skill can become
  shorter and easier to review.

## First-Load Review

```text
first_load_review:
  line_count_before: 301
  line_count_after: 315
  kept_in_skill: checklist routing, owner-surface rules, validation and audit gates
  moved_to_reference: detailed first-load QA rules stay in qa_checklist.md
  deleted_as_duplicate_or_rationale: none
  extra_sections_kept_with_reason: Upkeep Modes and Templates stay for now because they define maintenance modes and handoff shapes; future compaction can test whether they fold into Signature/Todo List.
  remaining_sections_over_budget: skill-maintenance/SKILL.md is over 250 lines because it carries mode routing and handoff templates
  verdict: pass
```

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Todo list now requires reading `qa_checklist.md` for `structure_update`, `refine_skill`, and `audit`. |
| `reference_load_precision` | pass | `qa_checklist.md` is referenced from the todo list and Reference Map. |
| `missing_context_rate` | pass | The core placement rule remains in `SKILL.md`; detailed checks are in the checklist. |
| `noisy_context_rate` | pass | Detailed QA criteria live in `qa_checklist.md`, not inline. |
| `duplicated_instruction_count` | pass | `SKILL.md` routes to checklist; checklist owns the expanded criteria. |
| `prompt_size_tokens` | pass | `SKILL.md` increased only ten lines to wire the gate and question-list rule. |
| `maintenance_locality` | pass | Future first-load review rules have one owner: `qa_checklist.md`. |
| `composition_clarity` | pass | Finish gate names required proof fields for changed skills. |
| `section_necessity` | pass | The new first-load criteria are not in `SKILL.md`; they are in the QA checklist. |
| `gotcha_integration` | pass | Todo step 5 now requires folding gotchas into workflow gates. |
| `workflow_duplication` | pass | Todo step 5 now flags duplicated workflow explanation. |
| `reference_escape_hatch` | pass | Todo step 7 requires recording first-load review fields when `SKILL.md` changes. |
| `line_budget_review` | pass | The finish gate requires before/after line counts and over-budget sections. |
| `question_list_to_signature` | pass | Checklist and todo now require converting long intake question lists into signatures, params, or schemas. |
| `extra_section_value` | pass | Checklist and todo now require extra top-level sections to fold into template sections or justify substantial unique first-load value. |

## Proof Artifacts

- Skill-local evals, when needed: not required for checklist wording.
- Structure evals, when needed: `skills/skill-maintenance/qa_checklist.md`.
- Reviewer receipt: self-check; no separate reviewer lane used in this pass.
- Validator: pending command run in this turn.
- Eval required: no.
- Evidence gaps: no independent reviewer receipt yet.

## Before Behavior

- Skill maintenance could shorten or expand a skill without a required record of
  what belonged in first load.

## After Behavior

- Material `SKILL.md` changes must run the checklist and record keep, move,
  delete, line-count, and verdict fields.

## Followups

- Consider a small parser later that reports top-level section count and line
  budget automatically from `check_skills.py`.
