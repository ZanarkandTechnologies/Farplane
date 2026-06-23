---
skill: eval
date: 2026-06-23
change_type: maintenance
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/eval/references/query-spoiler-qa-checklist.md
after_ref: skills/eval/qa_checklist.md
reasoning_basis: reviewer
proof_artifacts:
  - .farplane/evals/runs/eval-query-review-eval-skill.json
  - skills/eval/qa_checklist.md
eval_required: no
---

# Eval Query QA Checklist Audit

## Change

- Before: Query-spoiler review lived in a reference file, even though
  `skill-maintenance` standardizes domain runtime checks as
  `edited_skill/qa_checklist.md`.
- After: `eval` declares `qa_checklist: qa_checklist.md` and stores the
  query-spoiler review gate in `skills/eval/qa_checklist.md`.
- Why: Material eval-row edits need a discoverable skill-local QA surface that
  `skill-maintenance` can find during `eval_to_qa_sync`.
- Tradeoff accepted: The checklist is separate from `SKILL.md` first load; the
  todo names when to load it.

## First-Principles Reasoning

- Objective: Prevent eval queries from teaching the expected skill behavior
  while following the existing QA checklist convention.
- Placement logic: Query-spoiler review is a reusable runtime guardrail for
  eval authoring, so it belongs in `skills/eval/qa_checklist.md`.
- Expected behavior delta: Agents editing material skill-local eval rows run
  the eval QA checklist with independent judgment instead of relying on regex
  or adding another LLM-runner script.
- Proof needed: Metadata points to the checklist, links resolve, smoke lint and
  skill-system validation pass.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` says when to run `qa_checklist.md` after skill-local eval edits. |
| `reference_load_precision` | pass | The checklist is loaded only for new, material, high-risk, or proof-acceptance eval rows. |
| `missing_context_rate` | pass | The query-spoiler rule is discoverable through frontmatter and the todo list. |
| `noisy_context_rate` | pass | Detailed pass/revise/fail rubric moved out of first load. |
| `duplicated_instruction_count` | pass | The deleted reference no longer duplicates the QA checklist surface. |
| `prompt_size_tokens` | pass | `SKILL.md` keeps only the routing rule and link. |
| `task_success_rate` | unknown | No full Codex skill eval rerun was required for placement-only correction. |
| `review_tas_rate` | unknown | No separate reviewer receipt was requested for this small follow-up. |
| `maintenance_locality` | pass | Changes stay inside `skills/eval` plus generated registries. |
| `composition_clarity` | pass | `eval` owns task QA; `skill-maintenance` owns checklist sync mechanics. |

## Proof Artifacts

- Skill-local evals, when needed: not required; existing query rows were already
  rewritten and reviewed.
- Structure evals, when needed: not required.
- Reviewer receipt: `.farplane/evals/runs/eval-query-review-eval-skill.json`
  reports pass for current `skills/eval/eval_task.json` queries.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed.
- Eval required: no.
- Evidence gaps: no independent reviewer receipt for the final placement
  change.

## Before Behavior

- Query-spoiler QA existed, but under `references/`, making it easier for an
  agent to miss the skill-local QA checklist convention.

## After Behavior

- Query-spoiler QA is the `eval` skill's first-class `qa_checklist.md`.
- `eval` frontmatter advertises that checklist.
- The smoke script points maintainers to `skills/eval/qa_checklist.md`.

## Followups

- Consider a future skill-system check that warns when a local skill has
  runtime QA guidance in `references/*qa*` but no frontmatter
  `qa_checklist`.
