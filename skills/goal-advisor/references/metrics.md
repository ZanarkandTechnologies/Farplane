# Metric Card

Load when a Goal, heartbeat, eval recovery, ticket proof, or strategy objective
needs an honest measurement contract before work continues, or when a caller
asks "what should we measure". It returns a card; it does not run the loop.
The caller keeps ownership: `goal-advisor` compiles the card into `program.md`,
`optimize-harness` coordinates recovery, `self-improve` compares variants,
`impl-plan` owns ticket Done / Proof wording, and `review` judges evidence. It
may write the project's `farplane/metrics.yaml` definition delta and
`farplane/harness.yaml` selection delta only when explicitly asked.

## Provider taxonomy

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

## Rules

1. Bind the objective (the behaviour, loss term, or decision the metric
   supports) and the caller that executes after the advice. Read the supplied
   ticket, eval summary, review, program, or proof before choosing; mark
   missing evidence instead of inventing a measurable state.
2. Prefer the most faithful mechanical or eval signal. Use `review`,
   `agent_qa`, `human_feedback`, `market`, or `hybrid` when the honest signal is
   judgment-heavy or external; use `none mechanical` when nothing real exists.
3. Every quantitative metric declares `maximize` or `minimize` and
   `type: flow` (additive period activity) or `type: stock` (a point-in-time
   balance). Core derives growth, period, cumulative, and trend views from raw
   observations; never author a second derived metric.
4. **Every primary metric needs a guard metric and at least one anti-metric**
   that would make the optimization a cheat. Eval recovery guards include
   `A_count_not_lower`, `query_lint_pass`, and registry/skill validation.
   Name the smallest delta that justifies action, or `qualitative threshold`.
5. **For causal, comparative, or uncertainty-reducing work, write the expected
   observation before the test runs:** observation, direction or band,
   horizon, confidence (`low | medium | high`), falsifier, and material surprise
   trigger, including implausibly strong results when leakage, contamination,
   evaluator bugs, or baseline mismatch are credible. Omit it for deterministic
   work and ordinary status reporting, and say: `The expectation block applies
   only to causal, comparative, or uncertainty-reducing work.`
6. Route direct repair when owner and fix are clear; `self-improve` only when
   candidate search and a baseline are needed; material causal surprise to
   `eval:experiment`; a delayed ticket Reward miss with no causal
   experiment back to its owning ticket, preserving the check-in's
   `accept | kill | monitor` decision.
7. Finish-check: when the primary metric is a proxy, say what it misses and
   which guard catches that miss; keep qualitative metrics qualitative with
   judgment questions instead of a fake score.

## Card

```text
Objective:
Loss term:
Provider:
Primary metric:          # with type: flow | stock
Direction:               # maximize | minimize
Guard metrics:
Anti-metrics:
Minimum meaningful delta:
Measurement method:
Expectation:             # experiment-like work only, written before the test
  Hypothesis:
  Expected observation:
  Observation horizon:
  Confidence: low | medium | high
  Falsifier:
  Surprise trigger:
  Surprise route:
Judgment questions:
Route hint:
No-metric reason:        # only for provider none or judgment-only routes
```

## Examples

Eval recovery: provider `eval`; primary `lifecycle_core_C_count`, minimize;
guards `A_count_not_lower`, `query_lint_pass`, `skill_registry_validation_pass`;
anti-metrics inflating reference points, hiding expected behaviour in queries,
broad prompt bloat; delta at least one C -> B/A with no A regressing; method
rerun the same subset and compare `summary.json`; expectation C count falls by
one or more within the next equal-budget run, surprise trigger an implausible
all-A jump; route `optimize-harness` direct repair first.

Judgment-heavy: "make plans easier to approve" has no command, so provider
`review` or `human_feedback`; primary reviewer pass or operator approval with
named objections closed; anti-metrics long prose that hides decisions and
numeric confidence theater; no expectation block.

## Gotchas

- The experiment expectation is not `Reward.expected_reward`, which forecasts
  delayed realized value, and not an eval's assertions or reference points.
- Store canonical raw observations only; direction-aware movement is a Core
  projection. The definition minimum is `type`, `unit`, `direction`, and one
  `refresh_ref` or inline `refresh`; the projection request owns windows.
