---
skill: deliberative-advice
date: 2026-06-24
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/deliberative-advice/SKILL.md@pre-change
after_ref: skills/deliberative-advice/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/deliberative-advice/SKILL.md
  - skills/deliberative-advice/eval_task.json
  - docs/skills/registry.jsonl
eval_required: yes
---

# Deliberative Advice Budget Preset Audit

## Change

- Before: `deliberative-advice` was a standalone 10-step council workflow with
  its own lane spawning, critique, synthesis, and context-packet procedure.
- After: `deliberative-advice` is a `skill-template` `0.3.2` council preset for
  budgeted `advise`; it hardcodes the five council personas and routes budget
  expansion through `budget-advisor`.
- Why: The reusable budget transformation belongs in `budget-advisor`, while
  this skill should only name the expensive advice pattern and provide its
  domain-specific defaults.
- Tradeoff accepted: First load grew from 183 to 213 lines to keep the complete
  persona prompts and budget preset executable without hidden context.

## First-Principles Reasoning

- Objective: preserve deliberative council behavior while removing duplicate
  orchestration from this skill.
- Placement logic: `advise` owns the base recommendation contract;
  `budget-advisor` owns effort-to-program transformation; `deliberative-advice`
  owns the named council preset and persona defaults.
- Expected behavior delta: callers should resolve a budgeted `advise` program
  instead of treating `deliberative-advice` as a separate advice engine.
- Proof needed: template-version validation, eval sync, registry sync, and
  first-load structure review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` includes signature, preset, persona prompts, todo path, gates, refs, and output. |
| `reference_load_precision` | pass | `llm-council-model` is loaded only when context-packet mechanics or critique/ranking details matter. |
| `missing_context_rate` | pass | Required budget preset and persona prompts remain in first load. |
| `noisy_context_rate` | pass | Standalone council process prose was replaced by budget route and compact todos. |
| `duplicated_instruction_count` | pass | Budget execution is routed to `budget-advisor` rather than duplicated. |
| `prompt_size_tokens` | pass | `SKILL.md` is 213 lines, under the 250-line review threshold. |
| `task_success_rate` | unknown | No runtime eval executed in this pass. |
| `review_tas_rate` | unknown | No external reviewer receipt. |
| `maintenance_locality` | pass | Budget defaults live here; transformation rules stay in `budget-advisor`; base advice stays in `advise`. |
| `composition_clarity` | pass | Signature names state, gates, routes, fails, Budget Program output, and final decision note. |

## First-Load Review

```text
first_load_review:
  line_count_before: 183
  line_count_after: 213
  kept_in_skill:
    - trigger boundary
    - skill signature
    - hardcoded CouncilBudgetPreset
    - complete default persona prompts
    - todo path and finish gates
    - output contract
  moved_to_reference:
    - detailed council mechanics remain in references/llm-council-model.md
  deleted_as_duplicate_or_rationale:
    - standalone lane-spawning implementation steps
    - repeated council-shape prose now represented as budget params and persona prompts
  extra_sections_kept_with_reason:
    - none beyond current template sections
  remaining_sections_over_budget: none
  proof_surface_fit: pass
  task_case_quality: pass
  anti_cheat_case_design: pass
  qa_preflight_loaded: not_applicable
  qa_finish_independence: self_check
  qa_gotcha_deduplication: pass
  project_specific_context_isolation: pass
  low_value_prose_scan: pass; behavior-bearing preset and persona prompts kept, duplicate council narration removed
  verdict: pass
```

## Proof Artifacts

- Skill-local evals, when needed: `skills/deliberative-advice/eval_task.json`
  updated to check budgeted `advise` preset behavior.
- Structure evals, when needed: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- Reviewer receipt: not run; self-check accepted for focused Tier 2 wrapper
  restructure.
- Validator: pass.
- Eval required: yes, eval task updated; runtime eval not executed.
- Evidence gaps: no child-agent council run was captured.

## Before Behavior

- The skill looked like a standalone council executor.
- The council defaults were procedural rather than encoded as budget params.

## After Behavior

- The skill is a named preset over `budget-advisor + advise`.
- The five council personas are first-load defaults.
- The final answer still preserves dissent, confidence, tradeoff, next owner,
  and the base `advise` output contract.

## Followups

- Consider adding a focused behavior eval run for `deliberative-advice` after
  the eval runner coverage for budgeted skill calls is refreshed.
