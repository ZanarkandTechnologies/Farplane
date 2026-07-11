---
skill: ticket-opportunity-generator
date: 2026-07-10
change_type: behavior
owner: skill-maintenance
status: accepted
review_route: reviewer
before_ref: skills/ticket-opportunity-generator/SKILL.md@794-lines-product-idea-compiler
after_ref: skills/ticket-opportunity-generator/SKILL.md@182-lines-plan-next-wave
reasoning_basis: reviewer
proof_artifacts:
  - tickets/TASK-0318/artifacts/review/plan-review.md
  - tickets/TASK-0318/artifacts/qa/work-pulse-proof.md
eval_required: yes
---

# Ticket Opportunity Generator Skill Audit

## Change

- Before: a 794-line product-specific idea compiler scanned product lanes,
  scored 14 dimensions, required product rewards/progress writeback, carried
  domain artifact rules, and returned large product ticket schemas.
- After: a 182-line pure `plan_next_wave` planner turns program, objective,
  ticket history, and current context into `0..wave_size` executable specs.
- Why: one generic planner is enough for the Work Pulse kernel; capability
  skills own domain workflow quality.
- Tradeoff accepted: content-specific ambition and market gates no longer live
  in the generic planner.

## First-Principles Reasoning

- Objective: produce the smallest useful executable backlog without side effects.
- Placement logic: planner owns selection/specification; Pulse owns materialization;
  capability skills own execution procedure; Interval owns dated evidence.
- Expected behavior delta: no product controller, lane, skill, progress, or
  learning-writeback input is required.
- Proof needed: QA gates, query-spoiler check, two focused evals, registry sync,
  and reviewer TAS-A.

## First-Load Review

```text
first_load_review:
  line_count_before: 794
  line_count_after: 182
  kept_in_skill:
    - input binding, context snapshot, leverage/dedupe selection, executable spec, proof, authority, and pure return gates
  moved_to_reference:
    - material ticket-spec reviewer handoff remains conditional
  deleted_as_duplicate_or_rationale:
    - fixed product lane catalog and portfolio scoring matrix
    - product-specific artifact levels and content examples
    - product-backed reward and learning-writeback requirements
    - product loop validator and product ticket contract reference
    - repeated caveats for valid-but-boring product tickets
    - long example ticket specs and scout schema
  extra_sections_kept_with_reason:
    - Phase Boundary: side-effect ownership is the defining v-next contract
    - Ticket Spec Contract: caller needs a compact return schema
  remaining_sections_over_budget: none
  proof_surface_fit: deterministic QA/query checks plus behavior evals and reviewer
  task_case_quality: four distinct planner boundaries with natural queries
  anti_cheat_case_design: query-spoiler validator passed before eval run
  qa_preflight_loaded: planner loads target checklist before acceptance
  qa_finish_independence: completion reviewer required
  qa_gotcha_deduplication: concise gotchas only
  project_specific_context_isolation: pass
  low_value_prose_scan: product philosophy, catalogs, and repeated caveats deleted
  verdict: pass pending completion reviewer
```

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, todo, phase boundary, schema, gates, and refs are first load. |
| `reference_load_precision` | pass | Reviewer handoff is loaded only for material candidates. |
| `missing_context_rate` | pass | Objective, evidence, dedupe, proof, capability, authority, and purity remain. |
| `noisy_context_rate` | pass | Product catalogs, scoring matrices, and examples removed. |
| `duplicated_instruction_count` | pass | QA owns detailed gates; capability skills own procedures. |
| `prompt_size_tokens` | pass | 182 lines, down from 794. |
| `task_success_rate` | pass | Focused planner run passed 2/2 at TAS-A. |
| `review_tas_rate` | pass | Completion reviewer passed all seven families at TAS-A. |
| `maintenance_locality` | pass | Planner selection/specification has one owner. |
| `composition_clarity` | pass | Pure reads/outputs and Pulse handoff are explicit. |

## Proof Artifacts

- Skill-local evals: `skills/ticket-opportunity-generator/eval_task.json`
- Runtime checklist: `skills/ticket-opportunity-generator/qa_checklist.md`
- Query-spoiler check: passed before eval run
- Behavior eval: `.farplane/evals/runs/20260710-134210-task-0318-plan-next-wave-gpt55` (2/2 TAS-A)
- Reviewer receipt: `tickets/TASK-0318/artifacts/review/completion-review.md`
- Validator: `check_skills.py --write` passed before final rerun
- Evidence gaps: none for Workstream 1

## Followups

- Rename the package only if later usage proves the existing name causes real
  routing failures; v-next explicitly prefers reuse over conceptual renaming.
