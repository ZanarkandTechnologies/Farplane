---
name: self-improve
description: "Turn an existing improvement goal into immediate or delayed measured experiments, evals, Goal context, memory, and promotion evidence."
tier: 3
group: self-improvement
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.2.0"
eval: evals/evals.json

---

# Self Improve

## Context

Use this when a target skill, prompt, or harness surface needs measured
optimization against a metric. This skill owns experiment context, evals,
baselines, candidate comparison, skill-local memory, and promotion rules. It is
not a generic implementation planner and should not mutate a target before the
metric card and proof path are clear.

Current mental model:

```text
Goal mode = durable loop runner
goal-advisor = writes the Goal contract
self-improve/ = target skill memory, evals, prompt candidates, and results
skill-maintenance = accepted writeback into SKILL.md/references/source copies
```

## Skill Signature

```text
self_improve(target, metric, feedback_class, ticket,
             program?, progress?, search_space?, eval_suite?)
  -> immediate_result | waiting_signal
   + evidence
   + promotion_decision?

state:
  reads(target package, evals, metric, prior runs, candidate constraints,
        ticket Reward.kpi_rewards[], Goal Packet program/progress)
  writes(evals?, results?, target-local memory?, accepted change?,
         original ticket Reward rows?, original progress log?)

gates:
  feedback_classified; metric_named; baseline_recorded;
  candidate_or_intervention_bounded; promotion_rule_named;
  immediate_result_measured_in_window_or_delayed_checkin_program_executable

routes: metric-advisor | eval | goal-advisor | skill-maintenance | review |
        pulse-update

fails:
  optimizes_by_taste; mutates_before_baseline; promotes_unmeasured_change;
  creates_checkin_ticket; invents_experiment_metadata;
  leaves_delayed_checkin_implicit; adds_delayed_checkin_debt_to_immediate_work;
  bloats_target_skill
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read the target skill package or harness surface: `SKILL.md`, direct todo list, references,
  scripts, and existing `self-improve/` memory.
- [ ] 2. Clarify the improvement target, eval boundary, or editable scope with
  the native planning phase when any of them is unclear.
- [ ] 3. Ground external examples or prior variants with
  [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
  when comparison is required.
- [ ] 4. Define the quality rubric and convert it into binary assertions before
  optimizing.
- [ ] 5. If the metric is unclear, derive a metric card first; then establish a
  baseline score or baseline judgment before mutating the target skill.
- [ ] 6. Classify feedback timing before choosing the execution route.
  - [ ] Use `immediate` only when baseline, intervention, result, and keep/kill
        decision can be observed inside the current execution window. Run it
        through native Goal without manufacturing a future check-in; keep the
        Goal Program `Check-In Program` as compact `mode: not_applicable`.
  - [ ] Use `delayed` when elapsed time, exposure, external action, or later
        human feedback is required. Encode the wait in the original ticket's
        `Reward.kpi_rewards[]` and compile an executable `Check-In Program` in
        its `program.md` through Goal Advisor.
  - [ ] Give every delayed row a stable `reward_id`. Treat only evidence-backed
        `accept` or `kill` as terminal; `monitor` updates the same row and wait.
- [ ] 7. For durable iterative work, prefer native Goal mode as the loop runner;
  use this skill as the eval, prompt-profile, and skill-memory context surface.
- [ ] 8. Promote only durable lessons, evals, and accepted changes into the target
  skill package, normally through [skill-maintenance](../skill-maintenance/SKILL.md).
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Execution Routes

Give native Goal mode the smallest measured-search context it needs; do not
build a parallel loop runner. Use `goal-advisor` when a durable Goal must be
compiled and `metric-advisor` when the metric provider or guards are unclear.

- `immediate`: baseline, intervention, result, and keep/kill decision are
  observable inside the current Goal window. Measure and decide in-window; do
  not manufacture a future check-in or fill delayed check-in procedure fields.
- `delayed`: the real signal requires elapsed time, exposure, an external
  event, or later human feedback. Persist the wait in the original ticket's
  Reward rows, and use Goal Advisor to fill the experiment-specific
  `program.md` `Check-In Program`. Work Pulse resumes the same packet and its
  worker executes that program when a row matures.

Immediate execution and ticket-local delayed check-in are execution timing
routes, not extra portfolio learners. Weekly Dogfood is the only aggregation
horizon and reads terminal Reward decisions without rescoring them. Do not add
an independent plan-quality loop; join Pulse admission receipts to eventual
Reward decisions when portfolio attribution is needed.

Load [workflows](references/workflows.md) for the full eval sequence, exact
Reward/Goal fields, due-row rule, and `accept | kill | monitor` decisions.
Iteration remains same-packet work, not another Reward state. Load [skill
evals](references/skill-evals.md) before designing cases
and [skill memory](references/skill-memory.md) before creating a target-local
`program.md`, run folders, or prompt-profile harness.

## Gotchas

1. Do not leak the intended answer into eval prompts.
2. Do not use judge-only subjective scores as the primary keep/discard metric.
3. Do not mutate the user's target skill until baseline evals exist.
4. Do not promote experimental evals into the skill package until they catch at
   least one real failure mode.
5. Do not optimize a skill that should be split into smaller skills first.
6. Do not fill target skill packages with bulky raw logs; store durable
  summaries, accepted evals, and reusable lessons.

## Reference Map

- [references/architecture.md](references/architecture.md) - self-improvement
  boundary and ownership model.
- [references/workflows.md](references/workflows.md) - eval and optimization
  phases.
- [references/gotchas.md](references/gotchas.md) - eval leakage and
  overfitting risks.
- [references/skill-evals.md](references/skill-evals.md) - case and assertion
  design.
- [references/skill-memory.md](references/skill-memory.md) - target-skill
  `program.md` and run history.
- [metric-advisor](../metric-advisor/SKILL.md) - metric card, guard metrics,
  anti-metrics, and no-metric rationale before variant search.
- [eval](../eval/SKILL.md) - proof and hardcase-marked eval cases.
- [skill-maintenance](../skill-maintenance/SKILL.md) - accepted writeback to
  skill source files.

## Templates

Experiment spine:

```text
target + metric + search_space + eval_suite -> baseline -> candidates -> comparison -> promotion
```

Promotion note:

```text
Target:
Metric:
Baseline:
Candidates:
Best candidate:
Promotion rule:
Accepted writeback:
Residual risk:
```

## Output

A self-improvement pass should leave:

- eval cases and assertions for the target skill
- deterministic eval runner/results when the prompt profile is used
- baseline score and changed-score logs
- Goal-readable context in `program.md`, latest results, failure analysis, and
  prompt/eval files
- updated `self-improve/program.md` when the user wants durable skill memory
- a concise before/after debrief
- only measured, reversible target skill edits
