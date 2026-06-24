---
title: Create Task Case Design Skill Audit
owner: skills/proof-advisor
status: draft
created_at: 2026-06-23
---

# Create Task Case Design Skill Audit

## Change

Originally created `task-case-design` as a Tier 2 case-generation workflow
shared by software tests, evals, skill evals, agent QA, and validators. The
package was later renamed to `proof-advisor`; this audit remains as source
history, not a compatibility surface.

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
  moved_to_reference: source synthesis, detailed proof-case rubric
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
  - python3 .farplane/evals/run_evals.py run --harness codex --skill task-case-design --label task-case-design-smoke --limit 1
  - python3 .farplane/evals/run_evals.py run --harness codex --skill task-case-design --task-id task-case-design-critical-path --label task-case-design-critical-path
result: pass
notes: check_skills refreshed generated registry, template registry, and skill-template intelligence artifacts. The real Codex-backed eval smoke wrote `.farplane/evals/runs/20260623-082746-task-case-design-smoke` with pass_rate 1.0 and verdict A for `task-case-design-proof-surface-fit`. The critical-path eval wrote `.farplane/evals/runs/20260623-083155-task-case-design-critical-path` with pass_rate 1.0 and verdict A for `task-case-design-critical-path`.
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
  reviewed_cases: 7
  verdict: pass
  fixes_applied: expanded the suite to cover the critical path, source-first case mining, dimension-first generation, proof-surface routing, and maintenance-loop behavior.
  deferrals: two eval rows were run through the full harness in this pass; the remaining targeted rows still need a full-suite run when compute budget allows.
  remaining_risk: the expanded rows are linted and registered, but still need a full skill-local eval run when compute budget allows.
```
