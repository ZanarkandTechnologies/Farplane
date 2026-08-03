---
title: Skill Structure Checklist
owner: skill-maintenance
status: active
kind: qa-checklist
created_at: 2026-06-13
updated_at: 2026-07-18
feature_refs:
  - FEAT-0057
applies_to:
  - skills
---

# Skill Structure QA Checklist

Use this before creating or materially restructuring a skill, then apply it
again before completion. Check the actual changed files and record `pass`,
`violation`, `not_applicable`, or `deferred` with evidence and the smallest fix.
Also apply the target skill's own `qa_checklist.md` when it has domain-specific
runtime checks.

```text
skill_qa_checklist(skill_package, changed_files, claim)
  -> checklist_verdicts + fixes_or_deferrals + evidence_note
```

## Placement Contract

```text
place_skill_detail(detail)
  -> SKILL.md when defer_loading_risk > context_rot_risk + compaction_loss_risk
  -> reference when defer_loading_risk <= context_rot_risk + compaction_loss_risk
```

Keep in `SKILL.md` only what selects, executes, stops, or proves the normal path:
trigger/context; signature and state; numbered todo path; routing; hard gates;
human handoffs; precise reference load conditions; proof; output contract; and
short normally-run commands. Put branch-only examples, templates, rubrics,
provider maps, and rare recipes in references with explicit load conditions.

Treat file length as a diagnostic rather than a gate. Split by branch, provider,
responsibility, method, or artifact type only when the result has clearer
ownership and lower first-load cost; never hide required behavior to reduce a
count.

The baseline section set comes from
`../../docs/skills/templates/SKILL_TEMPLATE.md`. Extra top-level sections must
provide unique first-load value that cannot fold into `Context`, `Skill
Signature`, `Phase Boundary`, `Todo List`, `Templates`, `Gotchas`, `Reference
Map`, or `Output`.

## Checklist

1. `first_load_sufficiency` — normal execution needs no hidden chat or mandatory
   unloaded reference.
2. `reference_load_precision` — each reference has an explicit load condition
   and a descriptive link label.
3. `missing_context_rate` — compaction did not remove required gates, routing,
   proof, or output.
4. `noisy_context_rate` — first load excludes rare branches, long examples,
   tutorials, inventories, and rationale.
5. `duplicated_instruction_count` — one owner holds each operational rule.
6. `authored_file_structure` — authored files have coherent responsibility;
   any split improves ownership rather than only lowering a count.
7. `maintenance_locality` — a future maintainer can identify one owner surface.
8. `composition_clarity` — inputs, outputs, state reads/writes, evidence, routes,
   side effects, and failures are explicit.
9. `section_necessity` — each top-level section changes first-load behavior.
10. `gotcha_integration` — recurring gotchas become todos, gates, fails, or
    concise stop conditions instead of a detached catalog.
11. `workflow_duplication` — prose does not repeat the todo path or script.
12. `instruction_todo_alignment` — executable `load`, `run`, `apply`, `reject`,
    `must`, and `if/when` instructions live in or are routed by todos/gates.
13. `reference_escape_hatch` — moved detail is reachable through a precise
    branch condition.
14. `structure_budget_review` — split decisions name the ownership or loading
    improvement; raw size alone does not determine pass or fail.
15. `question_list_to_signature` — long fixed intake lists become parameters or
    schemas when missing values can be requested normally.
16. `extra_section_value` — kept extra sections name behavior lost by folding or
    reference placement.
17. `proof_surface_fit` — deterministic behavior uses tests/validators, variable
    AI behavior uses evals, tool workflows use agent QA, and judgment uses review.
18. `quality_signal_layer_fit` — QA, evals, metrics, review, and reward signals
    stay in their owning layers with repair context intact.
19. `task_case_quality` — tests/evals/examples are realistic, distinct,
    traceable, judgeable, and maintainable.
20. `anti_cheat_case_design` — user-facing eval prompts do not leak the skill,
    expected route, checklist, reference points, or desired answer.
21. `qa_preflight_loaded` — a skill with QA loads it before execution.
22. `qa_finish_independence` — material work reapplies QA and uses independent
    review or records why inline review is sufficient.
23. `qa_gotcha_deduplication` — QA contains evidence-oriented prevention rather
    than copying `## Gotchas`.
24. `project_specific_context_isolation` — reusable skills do not preload a
    private project, person, path, customer, or local workflow.
25. `low_value_prose_scan` — each first-load sentence changes execution,
    routing, proof, safety, ownership, or maintenance; otherwise classify it
    with [low-value prose scan](references/low-value-prose-scan.md).
26. `golden_calibration_independence` — planning may read the golden plus QA;
    review receives candidate, golden invariants, QA, and held-out context, not
    planner scratch reasoning or an answer key.
27. `lean_owner_reuse` — reuse the smallest owner; do not add parallel state,
    workflows, fields, public surfaces, or avoidable first-load context.

## Common Move Or Remove Candidates

- rationale, history, philosophy, tutorial prose, and generic quality claims
- long gotcha catalogs, setup prose already owned by scripts, and question lists
- rare branches, migration guides, extended examples, and template inventories
- duplicated shared rules and `Output` prose already expressed by signature/todo
- extra sections that lightly rename a core template section

## Finish Gate

```text
first_load_review:
  authored_file_structure:
  kept_in_skill:
  moved_to_reference:
  deleted_as_duplicate_or_rationale:
  extra_sections_kept_with_reason:
  proof_surface_fit:
  task_case_quality:
  anti_cheat_case_design:
  qa_preflight_loaded:
  qa_finish_independence:
  qa_gotcha_deduplication:
  project_specific_context_isolation:
  low_value_prose_scan:
  golden_calibration_independence:
  lean_owner_reuse:
  verdict: pass | fail | unknown
```

For behavior-affecting changes, also record:

```text
behavior_eval_review:
  suite:
  baseline_artifact:
  candidate_artifact:
  comparison_artifact:
  promotion_decision: accept | hold | rollback
  eval_skip_reason: # mechanical-only changes
```

## Reviewer Prompt

```text
Review the changed skill files against this checklist and the target skill's QA.
For every check return verdict, exact file/line evidence, and smallest fix. For
extra sections, decide fold, move, delete, or keep with unique first-load value.
Do not rewrite the skill or judge product quality. For golden-calibrated work, use only
candidate, invariants, QA, and held-out context; never planner scratch reasoning.
Return the highest-risk unresolved issue and TAS readiness verdict.
```
