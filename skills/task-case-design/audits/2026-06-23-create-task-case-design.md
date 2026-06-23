---
title: Create Task Case Design Skill Audit
owner: skills/task-case-design
status: draft
created_at: 2026-06-23
---

# Create Task Case Design Skill Audit

## Change

Created `task-case-design` as a Tier 2 case-generation workflow shared by
software tests, evals, skill evals, agent QA, and validators.

## Source Basis

- OpenAI eval best practices: objective, data, metrics, run/iterate, logs, and
  human calibration.
- Anthropic agent eval guidance: task, trial, grader, multi-turn environment,
  and deterministic checks inside agent environments.
- Hamel/Shankar eval guidance: error analysis, trace review, dimensions,
  personas/scenarios, synthetic data only as gap fill.
- Pragmatic Engineer eval guide: code-based evals for deterministic failures,
  LLM-as-judge for subjective failures.
- Google ML Test Score: ML systems need data/model/infrastructure/monitoring
  tests beyond generic software unit tests.

## First-Load Review

```text
first_load_review:
  line_count_before: 0
  line_count_after: 186
  kept_in_skill: trigger boundary, signature, todo workflow, proof routing, templates, gotchas, reference map
  moved_to_reference: source synthesis, detailed task-case rubric
  deleted_as_duplicate_or_rationale: none
  extra_sections_kept_with_reason: none
  remaining_sections_over_budget: none
  verdict: pass
```

## Proof Plan

## Proof Run

```text
proof:
  - python3 -m json.tool skills/task-case-design/eval_task.json
  - python3 skills/eval/scripts/check_eval_queries.py --root .
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
result: pass
notes: check_skills refreshed generated registry, template registry, and skill-template intelligence artifacts.
```

## Checklist Notes

```text
task_case_qa:
  changed_files:
    - skills/task-case-design/SKILL.md
    - skills/task-case-design/references/source-ledger.md
    - skills/task-case-design/references/task-case-rubric.md
    - skills/task-case-design/qa_checklist.md
    - skills/task-case-design/eval_task.json
  reviewed_cases: 2
  verdict: pass
  fixes_applied: kept eval queries natural; put expected behavior in reference_points.
  deferrals: actual eval harness run not performed in this pass.
  remaining_risk: behavior proof is seeded but not yet run through a full eval harness trial.
```
