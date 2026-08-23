---
name: metric-advisor
version: 0.1.1
description: "Turn objectives and evidence into honest metric cards, experiment expectations, guard metrics, anti-metrics, and route hints."
tier: 1
source: local
template_uses:
  skill-template: "0.3.2"
allowed-tools: Read, Glob, Grep
---

# Metric Advisor

## Context

Use this when an objective, eval result, ticket, Goal loop, strategy artifact,
or improvement idea needs an honest metric before work continues. The output is
a metric card: provider, primary signal, direction, guard metrics,
anti-metrics, minimum meaningful delta, measurement method, and route hint.
For causal, comparative, or uncertainty-reducing work, the same card also
preregisters the observation expected before the result is known.

This skill does not run evals, reviews, Goals, QA, or experiments. It gives the
caller the smallest trustworthy measurement contract and may write the
project-level `metrics.yaml` definition delta and `harness.yaml` selection
delta when explicitly requested. The caller keeps domain
ownership: `optimize-harness` coordinates recovery, `goal-advisor` compiles
Goal Packets, `self-improve` compares variants, `impl-plan` owns ticket proof,
and `review` judges evidence.

## Skill Signature

```text
metric_advice(objective, evidence?, proof_surface?, constraints?)
  -> metric_card + expectation? + derived_view_contract + route_hint + no_metric_reason?
state: reads(objective, farplane/harness.yaml?, farplane/metrics.yaml?, ticket/progress/eval/review artifacts, constraints);
       writes(none by default; optional farplane/metrics.yaml definition/direction/freshness/guard delta plus farplane/harness.yaml selection delta; caller writes ticket/program/progress/proof)
gates: objective_named; provider_truthful; metric_matches_objective;
       direction_named; guard_metric_named; anti_metric_named; measurement_method_named;
       experimental_work:expectation_preregistered; no_fake_precision
routes: optimize-harness | goal-advisor | self-improve | impl-plan |
  proof-advisor | agent-qa-test:experiment | gap-analysis | review
fails: fake numeric score; proxy gaming; missing guard metric; hidden
  subjective judgment; resurrecting retired autoresearch skill routes
```

Provider taxonomy:

```text
mechanical      command, script, validator, benchmark, parser, or artifact check
eval            runnable eval pass rate, tier distribution, or specific case count
review          TAS verdict, rubric family, or explicit reviewer judgment
agent_qa        adversarial tester evidence plus evidence-review critique
human_feedback  operator label, approval, ranking, or qualitative feedback
market          clicks, replies, sales, retention, usage, or other external result
hybrid          named combination of signals without pretending one fake number
none            no honest metric; use judgment questions and write "none mechanical"
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the objective and artifact being improved.
  - [ ] Name the desired behavior, loss term, or decision this metric will
        support.
  - [ ] Name the caller that will own execution after this advice.
- [ ] 2. Ground available evidence.
  - [ ] Read the supplied ticket, eval summary, review result, goal/program
        file, strategy artifact, or proof output before choosing a metric.
  - [ ] Mark missing evidence instead of inventing a measurable state.
- [ ] 3. Choose the primary provider and metric.
  - [ ] Prefer the most faithful mechanical or eval signal when it exists.
  - [ ] Use `review`, `agent_qa`, `human_feedback`, `market`, or `hybrid` when
        the honest signal is judgment-heavy or external.
  - [ ] Use `none` and `none mechanical` when no real metric exists.
  - [ ] Declare `maximize` or `minimize` for every quantitative metric so Core
        can derive a direction-normalized trend from raw observations.
  - [ ] Declare `type: flow` for additive period activity or `type: stock` for
        a point-in-time balance.
  - [ ] Do not author a second growth, period, or cumulative metric when Core
        can project those views from the primary metric.
- [ ] 4. Add guard metrics, anti-metrics, and minimum meaningful delta.
  - [ ] Guard against breaking correctness, quality, safety, proof, user
        value, or operator control while moving the primary signal.
  - [ ] For eval recovery, include guards for `A_count_not_lower`,
        `query_lint_pass`, and registry or skill validation passing unless a
        stronger local guard is named.
  - [ ] Name at least one anti-metric that would make the optimization a cheat.
  - [ ] Give the smallest delta that would justify action, or say
        `qualitative threshold`.
- [ ] 5. For experiment-like work, preregister the expected observation before
      reading the result.
  - [ ] Name the observation, direction or qualitative band, horizon,
        confidence (`low | medium | high`), falsifier, and material surprise
        trigger.
  - [ ] Include unexpectedly weak and implausibly strong results when leakage,
        contamination, evaluator bugs, or baseline mismatch are credible.
  - [ ] Omit this block for deterministic implementation or ordinary status
        reporting; do not invent a fake hypothesis. When asked why it is
        omitted, explicitly state: `The expectation block applies only to
        causal, comparative, or uncertainty-reducing work.`
- [ ] 6. Name measurement method and route hint.
  - [ ] Explain exactly how the caller measures or judges the metric.
  - [ ] Route direct repair when owner and fix are clear.
  - [ ] Route `self-improve` only when candidate search, baseline, and variant
        comparison are needed.
  - [ ] Route `goal-advisor` when the metric belongs inside a ticket-backed
        Goal Packet or heartbeat.
  - [ ] Route material causal surprise to `agent-qa-test:experiment`.
  - [ ] Route a delayed ticket Reward miss without a causal experiment to
        `gap-analysis`, then preserve the ticket check-in's
        `accept | kill | monitor` decision.
  - [ ] Do not route to retired autoresearch skill routes; choose the live
        owner instead.
- [ ] 7. Finish-check for fake precision and proxy gaming.
  - [ ] If the primary metric is a proxy, say what it misses and which guard
        catches that miss.
  - [ ] If the metric is qualitative, keep it qualitative and provide
        judgment questions instead of a fake score.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Metric card:

```text
Objective:
Loss term:
Provider:
Primary metric:
Direction:
Guard metrics:
Anti-metrics:
Minimum meaningful delta:
Measurement method:
Expectation: # optional; required only for experiment-like work
  Hypothesis:
  Expected observation:
  Observation horizon:
  Confidence: low | medium | high
  Falsifier:
  Surprise trigger:
  Surprise route:
Derived views: requested-window value, preceding equal-window absolute and
  percentage delta, direction-normalized improving/flat/worsening trend, and
  cumulative total for flows only; unknown when facts are missing, stale,
  conflicting, invalid, or not time-comparable.
Judgment questions:
Route hint:
No-metric reason:
```

Lifecycle eval recovery example:

```text
Objective: recover Farplane core lifecycle eval quality.
Loss term: repeated C-tier lifecycle behavior.
Provider: eval.
Primary metric: lifecycle_core_C_count.
Direction: lower.
Guard metrics: A_count_not_lower; query_lint_pass; skill_registry_validation_pass.
Anti-metrics: inflating reference points; hiding expected behavior in queries;
  broad prompt bloat; ignoring failed owner skills.
Minimum meaningful delta: at least one C -> B/A without lowering any A to B/C.
Measurement method: rerun the same lifecycle eval subset and compare summary.json.
Expectation:
  Hypothesis: the owner-local repair removes at least one repeated lifecycle
    failure without weakening passing behavior.
  Expected observation: C count falls by at least one while A count does not fall.
  Observation horizon: the next equal-budget selected-suite run.
  Confidence: medium.
  Falsifier: no C case improves, an A case regresses, or query lint fails.
  Surprise trigger: the observed delta is outside that band, including an
    implausible all-A jump suggesting leakage or grading drift.
  Surprise route: agent-qa-test:experiment.
Judgment questions: did the fix target the failing owner? did proof stay local?
Route hint: optimize-harness direct repair first; self-improve only if candidate
  search is needed after direct repair fails.
```

Judgment-heavy example:

```text
Objective: make a planning artifact easier for the operator to approve.
Loss term: unclear approval surface.
Provider: review or human_feedback.
Primary metric: reviewer TAS pass or operator approval with named objections closed.
Direction: pass/fail or accept/revise.
Guard metrics: ticket checks remain concrete; no scope creep; no fake metric.
Anti-metrics: long prose that hides decisions; numeric confidence theater.
Minimum meaningful delta: all blocking objections resolved.
Measurement method: reviewer handoff or explicit operator feedback file.
Route hint: review or goal-advisor.
```

Retired mechanical-loop example:

```text
Objective: reduce type errors across one editable package.
Provider: mechanical.
Primary metric: type_errors.
Direction: lower.
Guard metrics: tests_or_validators_pass; command_output_parseable.
Anti-metrics: editing the metric parser; weakening tests; narrowing scope
  dishonestly; suppressing diagnostics.
Measurement method: run the existing command and parse its output from the
  owning ticket, program, or eval artifact.
Route hint: goal-advisor or self-improve, not retired autoresearch skills.
```

## Gotchas

- Do not optimize by vibes. If there is no metric, say `none mechanical` and
  provide review or human-feedback questions.
- Do not reward proxy motion that can be gamed. Every primary metric needs a
  guard or anti-metric.
- Do not route to retired autoresearch skill routes.
- Do not turn this skill into the executor. It only returns the measurement
  contract and route hint.
- Do not confuse the immediate experiment expectation with
  `Reward.expected_reward`, which forecasts delayed realized value.
- Do not confuse an Eval expectation with its assertions or reference points;
  those grade behavior and stay outside the user-facing query.
- Store canonical raw observations only. Direction-aware movement is a Core
  projection, not a second persisted observation or hand-maintained metric.
- Keep the metric definition lean: `type`, `unit`, `direction`, and one
  `refresh_ref` or inline `refresh` are the semantic minimum. The projection
  request—not `metrics.yaml`—owns window bounds and timezone.

## Reference Map

- [../goal-advisor/SKILL.md](../goal-advisor/SKILL.md) - compiles selected
  metric providers into Goal Packets or heartbeats.
- [../optimize-harness/SKILL.md](../optimize-harness/SKILL.md) - coordinates
  observed-versus-expected recovery, placement, proof, and accept/hold/rollback.
- [../self-improve/SKILL.md](../self-improve/SKILL.md) - owns baseline,
  candidate comparison, experiment memory, and promotion rules.
- [../proof-advisor/SKILL.md](../proof-advisor/SKILL.md) - turns behavior
  claims into proof cases and proof surface choices.
- [../agent-qa-test/SKILL.md](../agent-qa-test/SKILL.md) - independently
  diagnoses material observation surprises.
- [../gap-analysis/SKILL.md](../gap-analysis/SKILL.md) - diagnoses delayed
  expected-versus-actual value gaps that are not scientific experiment claims.
- [../review/SKILL.md](../review/SKILL.md) - judges evidence when metric
  traceability or qualitative sufficiency needs independent review.

## Output

Return a compact metric card plus the optional expectation and route hint.
Include `Expectation` only for experiment-like work. Include `No-metric reason`
only when the provider is `none` or the honest route is review/human judgment
without a mechanical metric.
