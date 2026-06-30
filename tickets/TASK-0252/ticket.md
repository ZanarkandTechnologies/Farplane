---
ticket_id: TASK-0252
title: Add skill baseline comparison to eval runner
phase: complete
status: done
owner: codex
claimed_by:
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: false
requires_qa: true
requires_demo: false
created_at: 2026-06-30T08:47:54Z
updated_at: 2026-06-30T08:50:10Z
next_action: done; run a live Codex profile comparison as follow-up when eval profiles exist
last_verification: "PASS: python3 skills/eval/tests/test_run_evals.py"
---

# TASK-0252: Add skill baseline comparison to eval runner

## Summary
Add the smallest useful Agent Skills-style comparison loop to Farplane's eval
runner without changing existing eval task JSON. Skill eval rows should run once
with the target skill available, record whether the skill triggered, and run a
baseline only when that trigger happened.

## Scope
- In: `skills/eval/scripts/run_evals.py`, runner tests, and eval README usage.
- Out: eval JSON backfill, dynamic description optimization, HTML report work,
  global mandatory baseline runs, and Codex CLI changes.

## Delta
```text
overall_before:
  - Skill-local evals judge one answer per row.
  - Skill context can be inlined, which proves forced instruction quality but not native skill triggering.
overall_after:
  - Compare mode runs a candidate native-skill eval, records skill_triggered, and conditionally runs a no-skill baseline.
  - Existing eval_task.json files remain valid and unchanged.
why_now:
  - Agent Skills' with-skill versus baseline pattern is valuable, but Farplane can express it as runner behavior over existing cases.
problems:
  - before: per-row evals can pass without showing whether the skill mattered.
    after: result JSON records trigger and candidate/baseline delta.
    why_now: this is the smallest proof upgrade before broader trigger-eval optimization.
first_principles_basis:
  objective: prove whether a skill triggers and improves outcomes for existing eval cases.
  need: compare candidate against the same task without the target skill.
  assumptions: Codex JSON events expose enough signal to detect skill loading; if not, record unknown instead of overclaiming.
  root_cause: eval task shape is sufficient; missing behavior is in runner orchestration and result schema.
  constraints: do not backfill JSON, do not mutate live Codex config, do not expand modes unnecessarily.
  first_viable_slice: one selected skill eval, candidate profile, baseline profile, trigger field, conditional baseline.
  proof_or_falsification: unit tests with fake JSON events plus eval runner test suite.
  tradeoff: skip baseline when skill does not trigger by default, favoring efficient trigger tuning over complete benchmark stats.
  non_goals: dynamic temporary CODEX_HOME generation and description candidate search.
```

## Change Plan
```text
architecture_signatures:
  module_level:
    - run_evals.py / command_run(args): eval run summary
    - run_task(task,args,...): task detail with optional comparison fields
  main_flow:
    - run_task -> run_candidate -> parse_skill_trigger -> maybe_run_baseline -> judge -> write detail
  data_flow:
    - EvalTask.query -> codex exec JSONL -> skill_triggered -> detail.candidate.skill_triggered
    - candidate.judge.pass + baseline.judge.pass -> comparison.delta
  builder_freeform_boundary:
    - Keep implementation local to run_evals.py helpers and tests unless proof shows a docs or template change is required.
```

### Change 1: Minimal compare-baseline runner path
```text
fixes:
  - Existing eval rows do not show whether the target skill triggered or mattered.
before:
  - One agent answer and one judge result per task.
after:
  - Compare mode writes candidate, optional baseline, and comparison objects.
read:
  - path: skills/eval/scripts/run_evals.py
    reason: current runner flow and Codex profile handling.
write:
  - path: skills/eval/scripts/run_evals.py
    change: add flags, event parsing, candidate/baseline task execution, and summary comparison counts.
operation:
  - Add `--compare-baseline` and `--baseline-agent-profile`.
  - Infer the target skill from the required single `--skill` selector.
  - Force native skill context in compare mode so `SKILL.md` is not inlined.
  - Run baseline only when candidate `skill_triggered` is true.
signature_or_type_impact:
  - CLI adds optional flags only; existing commands remain compatible.
routes:
  docs: update_docs
  qa: tests
  review: inline
qa:
  - Unit tests cover default compatibility and compare detail shape.
failure_modes:
  - Skill event parsing may be incomplete; record `unknown` rather than false certainty.
```

### Change 2: Minimal docs and tests
```text
fixes:
  - Users need one runnable example and tests need to prevent accidental JSON backfill requirements.
before:
  - README documents normal single-run eval commands only.
after:
  - README includes the minimal compare-baseline command and notes natural task prompts.
read:
  - path: skills/eval/tests/test_run_evals.py
    reason: existing fake CLI and runner assertions.
  - path: skills/eval/README.md
    reason: command documentation.
write:
  - path: skills/eval/tests/test_run_evals.py
    change: add fake skill-trigger event support and compare-mode assertions.
  - path: skills/eval/README.md
    change: add compact compare-baseline usage.
operation:
  - Keep docs short; do not introduce all proposed modes.
signature_or_type_impact:
  - none beyond CLI flags.
routes:
  docs: update_docs
  qa: tests
  review: inline
qa:
  - `python3 skills/eval/tests/test_run_evals.py`
failure_modes:
  - Fake CLI event shape may not match live Codex exactly; live proof remains a follow-up.
```

## Done
```text
done_when:
  - Existing eval runner tests pass.
  - Compare mode works over existing eval_task.json without requiring new fields.
  - Per-task output includes `candidate.skill_triggered`.
  - Baseline is skipped when the target skill does not trigger.
  - Summary includes trigger and baseline comparison counts.
```

## QA Strategy
```text
qa_strategy:
  proof_weight: tests
  checks:
    - python3 skills/eval/tests/test_run_evals.py
  manual:
    - inspect one generated compare-mode detail JSON from fake CLI test
  delegated_lanes:
    - none
  review:
    - rubric: inline localized runner review
      required_tas: none
  evidence:
    - test command output
  goal_advisor_inputs:
    proof_route: tests
    final_evidence: test output plus changed files
    final_checkpoint: runner compatibility check before final
  residual_risk:
    - live Codex event shape may need a follow-up parser refinement after first real compare run
```

## Docs Strategy
```text
docs_strategy:
  outcome: update_docs
  doc_targets:
    - skills/eval/README.md
  no_docs_reason:
  validation:
    - README command matches runner flags
```

## Links
- `program:` none
- `progress:` none
- `artifacts:`
- `review:`
- `refs:`
  - experiments/best-of-worlds/agent-skills-eval-comparison/handoff.md
  - skills/eval/scripts/run_evals.py

## Notes
- Keep this ticket intentionally narrow. Temporary `CODEX_HOME` synthesis and
  description optimization are follow-ups after this first comparison path works.
