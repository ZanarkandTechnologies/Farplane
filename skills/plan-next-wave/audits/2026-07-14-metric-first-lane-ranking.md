---
skill: plan-next-wave
date: 2026-07-14
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/plan-next-wave/SKILL.md@586-lines
after_ref: skills/plan-next-wave/SKILL.md
reasoning_basis: advise
proof_artifacts:
  - skills/plan-next-wave/scripts/test_validate_ticket_specs.py
  - skills/plan-next-wave/evals/evals.json#planner_metric_first_lanes_choose_global_top_n
  - tickets/TASK-0358/artifacts/qa/metric-first-lane-ranking.md
  - tickets/TASK-0358/ticket.md
eval_required: yes
---

# Metric-First Candidate-Lane Ranking Audit

## Change

- Before: areas and trajectory factors were present, but objective pace and
  candidate-lane coverage were not inspectable planner receipts.
- After: every pass records target/pace-aware objective progress, enumerates
  five candidate lanes without quotas, and requires every admitted spec to
  carry a metric priority trace before one global top-N ranking.
- Why: recent planning produced useful artifacts without reliably exposing why
  they outranked autonomous ablation, experimentation, rollout, or direct
  creator work.
- Tradeoff accepted: larger planner receipts and first-load contract in return
  for auditable priority decisions.

## First-Principles Reasoning

- Objective: maximize verified movement on selected metrics under guards,
  authority, evidence, and portfolio-interference constraints.
- Placement logic: candidate generation and admission belong in
  `plan-next-wave`; Pulse remains the materializer/dispatcher and project metric
  targets remain caller-owned data.
- Expected behavior delta: lanes widen search while objective priority, target
  gap/pace, expected delta, confidence, timeframe, risk, and interference choose
  the winning portfolio.
- Proof needed: deterministic schema rejection plus a behavior case where two
  candidates from one lane correctly beat weaker cross-lane candidates.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Lane, objective-progress, formula trace, gates, and output fields remain in `SKILL.md`. |
| `reference_load_precision` | pass | No new deferred reference is required for normal execution. |
| `missing_context_rate` | pass | Missing targets become explicit `unknown`; they are not inferred from UI state. |
| `noisy_context_rate` | unknown | Behavior is mandatory, but the target skill was already above the normal first-load budget. |
| `duplicated_instruction_count` | pass | Contract, todo, QA, validator, and eval each own schema, execution, judgment, mechanical proof, and variable-behavior proof respectively. |
| `prompt_size_tokens` | fail | Line count increased from 586 to 672; broader contract compaction is outside this ticket and needs separate behavior-preserving work. |
| `task_success_rate` | pass | Ticket-scoped representative proof admits two delivery winners, one ablation, and rejects gated rollout/operations candidates. |
| `review_tas_rate` | pass | Initial TAS-B findings were repaired; completion re-review returned TAS-A with no hard-gate failures. |
| `maintenance_locality` | pass | Planner behavior remains owner-local in `skills/plan-next-wave/`. |
| `composition_clarity` | pass | Inputs, receipts, spec fields, purity boundary, and Pulse handoff are explicit. |

## First-Load Review

```text
first_load_review:
  line_count_before: 586
  line_count_after: 672
  kept_in_skill: mandatory lane, objective-progress, priority-trace, gate, and output contracts
  moved_to_reference: none
  deleted_as_duplicate_or_rationale: one accidental duplicated protocol phrase
  extra_sections_kept_with_reason: required response and ticket-spec contracts are consumed on every planner call
  remaining_sections_over_budget: full skill; pre-existing complex planner contract
  proof_surface_fit: deterministic validator plus behavior eval and reviewer
  task_case_quality: hardcase distinguishes search coverage from lane allocation
  anti_cheat_case_design: prompt supplies business state and candidates without naming the desired lane allocation
  qa_preflight_loaded: pass
  qa_finish_independence: pending reviewer
  qa_gotcha_deduplication: pass
  project_specific_context_isolation: pass; fixture uses generic objective names
  low_value_prose_scan: not_run; behavior change, not compaction
  verdict: pass; representative behavior proof and TAS-A completion review
```

## Proof Artifacts

- Skill-local eval: `planner_metric_first_lanes_choose_global_top_n`.
- Deterministic validator: canonical lane, objective priority, progress trace,
  metric source, rank reason, and human-load checks.
- Representative planner proof:
  `tickets/TASK-0358/artifacts/qa/metric-first-lane-ranking.md`.
- Initial reviewer receipt:
  `tickets/TASK-0358/artifacts/review/2026-07-14-initial-review.md`.
- Final reviewer receipt:
  `tickets/TASK-0358/artifacts/review/2026-07-14-final-review.md`.
- Validator repair: directional progress now rejects unknown or unconfigured
  target value, target date, or target gap; focused suite passes 23 tests.
- Evidence gap: no live scheduled Pulse run has consumed the new contract yet.

## Before Behavior

- Candidate categories were implicit levers and artifact kinds.
- Current readings could be listed without target distance or pace status.
- Nothing forced a receipt proving ablation, experiment, rollout, and
  operations were considered before ranking.

## After Behavior

- Five canonical lanes are enumerated in one context.
- Lanes receive no quotas, reservations, or independent rankings.
- Each admitted spec records the configured metric priority and current/target
  evidence or explicit unknowns alongside its risk-adjusted trajectory.
- The global top-N portfolio may contain multiple winners from one lane.

## Followups

- Run a separate behavior-preserving compaction ticket only if the planner's
  first-load size causes observed context or execution failures.
- Shared generated registry files currently contain unrelated worktree changes;
  they validate as a whole but their full diffs are not TASK-0358-owned proof.
