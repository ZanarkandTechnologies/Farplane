---
skill: init-advisor
date: 2026-06-25
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/deep-init-project/SKILL.md
after_ref: skills/init-advisor/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - "python3 -m json.tool skills/init-advisor/eval_task.json"
  - "python3 bin/validators/check_doc_refs.py"
  - "python3 bin/validators/check_farplane_project_files.py"
  - "python3 skills/skill-maintenance/scripts/check_skills.py --write"
  - "python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection skill-registry --check"
  - "python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection harness-reference --check"
  - "python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection farplane-framework-core --check"
  - "python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection farplane-lifecycle-core --check"
  - "python3 skills/skill-maintenance/scripts/test_generate_farplane_lifecycle_graph.py"
  - "python3 skills/skill-maintenance/scripts/test_generate_skill_graph.py"
  - "python3 bin/tests/test_farplane_adoption.py"
eval_required: no
---

# Init Advisor Rename Audit

## Change

- Before: public project bootstrap skill lived at `skills/deep-init-project/`
  with `deep_init_project(...)` naming, while `harness-creator` was the
  downstream operating-model phase.
- After: public setup entrypoint lives at `skills/init-advisor/` with
  `init_advisor(...)`; `harness-creator` remains the internal operating-model
  advisor called in `init_mode=full`.
- Why: the operator wanted the public setup surface renamed and the
  init-vs-operating-model responsibility split documented without legacy active
  compatibility.
- Tradeoff accepted: historical audit files moved with the package and keep
  their original dates; active docs and generated registries use the new name.

## First-Principles Reasoning

- Objective: make new Farplane project setup read as an advisor flow rather
  than a one-off "deep init" command, while preserving the existing substrate
  recipes and harness-creator handoff.
- Placement logic: rename the package because the public skill identity changed;
  keep implementation details in the same package because bootstrap templates,
  recipes, evals, and local docs already belonged together.
- Expected behavior delta: callers use `init-advisor`; full initialization
  routes operating-model work to `harness-creator`; active docs, graph sources,
  registries, and templates no longer point at `deep-init-project`.
- Proof needed: generated registries/graphs resolve `init-advisor`, doc refs
  pass, project-file checks pass, skill-maintenance checks pass, and active
  source scan finds no retired setup name outside historical experiments.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `skills/init-advisor/SKILL.md` retains context, signature, modes, todos, code recipes, gates, routes, and reference map. |
| `reference_load_precision` | pass | Reference Map in `skills/init-advisor/SKILL.md` names when to load project profiles, lifecycle, templates, QA refs, README, and prompt files. |
| `missing_context_rate` | pass | Full-mode handoff to `harness-creator`, automation activation handoff, and substrate/full end states remain in first load. |
| `noisy_context_rate` | pass | Rename did not add new prose; line count stayed flat. Existing code scaffold recipes remain because setup agents need them before choosing a stack branch. |
| `duplicated_instruction_count` | pass | Active docs point to `init-advisor`; `harness-creator` owns operating-model details; no active duplicate legacy setup name remains. |
| `prompt_size_tokens` | pass | 326 lines before and after; over the 250-line review threshold but under 400. Kept because bootstrap recipes and finish states are normal-path first-load material. |
| `task_success_rate` | unknown | No live init run was executed in this rename-only change. |
| `review_tas_rate` | unknown | No independent reviewer lane was run; self-check used because this was a structural rename with deterministic validators. |
| `maintenance_locality` | pass | Public setup files, templates, eval, README, AGENTS, and audits now live under `skills/init-advisor/`. |
| `composition_clarity` | pass | `init_advisor(...)` owns substrate/readiness/activation handoff; `project_harness_creator(...)` owns operating-model design. |

## Skill Structure Checklist Notes

```text
first_load_review:
  line_count_before: 326
  line_count_after: 326
  kept_in_skill: signature, phase boundary, todo list, setup outputs, code scaffold recipes, reference map
  moved_to_reference: package path moved from skills/deep-init-project to skills/init-advisor
  deleted_as_duplicate_or_rationale: no first-load text deleted; active legacy references removed from docs/config/scripts/graphs
  extra_sections_kept_with_reason:
    - What This Sets Up: normal-path setup result contract
    - Code Scaffold Recipes: normal-path stack-selection recipes for greenfield init
    - Optional Quality Tooling Slots: normal-path command-slot guidance for generated PROJECT_RULES
  remaining_sections_over_budget: Code Scaffold Recipes could later move to a reference if stack setup becomes a separate branch skill
  proof_surface_fit: deterministic validators and graph projection checks
  task_case_quality: existing eval rows renamed only; no new task cases added
  anti_cheat_case_design: unchanged existing init eval style; no new query leakage introduced beyond the rename
  qa_preflight_loaded: skill-maintenance qa_checklist.md loaded before edits
  qa_finish_independence: self-check used; deterministic validators passed
  qa_gotcha_deduplication: no target qa_checklist.md changes
  project_specific_context_isolation: pass; no project-specific/private refs added to reusable skill
  low_value_prose_scan: not run; no compaction or prose expansion in scope
  verdict: pass
```

## Proof Artifacts

- Skill-local evals, when needed: not run; eval JSON syntax and query lint
  passed through `check_skills.py --write`.
- Structure evals, when needed: `check_skills.py --write` passed.
- Reviewer receipt: not requested; self-check used for deterministic rename.
- Validator: doc refs, project files, graph projections, lifecycle graph tests,
  skill graph tests, and adoption tests passed.
- Eval required: no.
- Evidence gaps: no live project initialization was executed after the rename.

## Before Behavior

- Public setup skill was discoverable as `deep-init-project`.
- Active docs and graph sources pointed at `skills/deep-init-project`.
- Full setup already routed operating-model work to `harness-creator`, but the
  public setup API still carried older naming and depth language.

## After Behavior

- Public setup skill is discoverable as `init-advisor`.
- Active docs, registries, template registry, graph projections, tests, and
  adjacent skills point at `skills/init-advisor`.
- `init_mode=substrate|full` describes setup depth; full mode routes the
  operating model to `harness-creator`.

## Followups

- Consider a future compaction pass that moves code scaffold recipes into a
  branch-loaded reference only if agents can still select stack setup reliably.
