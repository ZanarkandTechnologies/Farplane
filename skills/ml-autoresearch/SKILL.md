---
name: ml-autoresearch
description: "Optimize a measurable ML system through bounded Goal-backed experiments selected from roadmap and progress evidence."
tier: 3
group: self-improvement
source: local
template_uses:
  skill-template: "0.3.9"
  skill-eval-task: "0.2.0"
  skill-qa-checklist: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Glob, Grep, Bash
---

# ML Autoresearch

## Context

Use this when an ML training or inference system has a frozen evaluator, a
measurable objective, a bounded mutable surface, and enough compute authority
for repeated experiments. Use one campaign ticket for one stable objective,
evaluator, data boundary, and budget. Experiments are append-only progress
entries and evidence receipts, not tickets.

This adapts Karpathy's minimal Autoresearch loop—baseline, one code experiment,
evaluate, keep or discard, repeat—into Farplane's visible Goal Packet. Leverage
Advisor chooses every next experiment from the initial roadmap plus accumulated
`progress.md` learnings. Native Goal is the sole continuation engine. Goal
Advisor compiles the packet but does not choose ML techniques.

## Skill Signature

```text
ml_autoresearch(target_system, owning_ticket, mutable_surface,
                frozen_evaluator, primary_metric, guards?,
                technique_catalog?, budgets?)
  -> approved_goal_packet + best_verified_candidate + experiment_evidence

state:
  reads(target code/docs, immutable data/evaluator contract, owning ticket,
        program roadmap, progress.md learnings, experiment receipts,
        optional technique catalog, current compute/budget state)
  writes(ticket program.md, ticket progress.md, native Goal prompt,
         ticket-local experiment receipts, accepted mutable-surface change)

gates:
  target_exists; owning_ticket_exists; mutable_surface_bounded;
  evaluator_frozen; metric_and_direction_named; baseline_recorded;
  guards_and_budget_named; roadmap_bound; packet_approved

routes:
  leverage-advisor | goal-advisor | metric-advisor | research:parity |
  research:source-synthesis | best-of-worlds | eval | agent-qa-test | review

fails:
  evaluator_or_data_boundary_mutation; experiment_before_baseline;
  fixed_ladder_ignoring_progress; multiple_confounding_deltas;
  unbounded_compute_or_spend; result_cherry_pick; receipt_overwrite;
  ticket_per_attempt; second_runner_or_continuation_owner; self_approved_claim
```

## Mandatory Composition

Every campaign plan, policy, packet, and active-turn decision must make this
named composition explicit:

```text
leverage_advisor(local evidence + technique catalog?) -> initial roadmap
goal_advisor(ticket.md + program preset + progress.md) -> approved Goal Packet
leverage_advisor(program.md roadmap + progress.md learnings
                 + current receipts + remaining budget) -> next experiment
domain_executor(next experiment) -> receipt + progress.md append
native_goal(updated packet state) -> continue | replan | block | complete
```

The campaign Goal Packet always contains `ticket.md`, `program.md`, and
`progress.md`. `program.md` owns both the initial roadmap and the policy that
requires evidence-updated replanning before every experiment; `progress.md`
owns append-only observations, receipts, learnings, and decisions. Goal Advisor
is only the packet/native-Goal compiler. Leverage Advisor is the only
next-experiment selector. Do not replace either named owner with anonymous
equivalent logic, and do not select a technique directly before the Leverage
Advisor checkpoint.

## Phase Boundary

Keep setup and cheap local grounding inline. Route uncertain metrics to Metric
Advisor. Route a missing, stale, or evidence-thin technique frontier to bounded
research or Best Of Worlds before ranking. Use Agent QA or review when the
agent, evaluator integrity, leakage boundary, or final scientific claim needs
independent judgment. External compute, spend, uploads, or services still need
the authority named by the ticket.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the campaign contract.
  - [ ] Read the owning ticket, target code/docs, mutable surface, frozen
    evaluator and data boundary, primary metric and direction, guards, budget,
    and [QA checklist](qa_checklist.md).
  - [ ] Route an obvious deterministic bug to direct implementation instead of
    opening an experiment campaign.
- [ ] 2. Prove the baseline and evaluator boundary.
  - [ ] Hash or otherwise identify the frozen evaluator, data/split inputs,
    environment, and baseline candidate before mutation.
  - [ ] Run the baseline through the exact full evaluator; use smokes only for
    correctness, never promotion.
- [ ] 3. Build the initial compounding roadmap.
  - [ ] Use [Leverage Advisor](../leverage-advisor/SKILL.md) on local evidence
    and the optional technique catalog to produce the ranked frontier, first
    proof, rejected moves, and positive/flat/negative/invalid/budget branches.
  - [ ] When credible techniques are missing or stale, route bounded research
    or [Best Of Worlds](../best-of-worlds/SKILL.md); record source dispositions
    before a technique becomes eligible.
- [ ] 4. Use [Goal Advisor](../goal-advisor/SKILL.md) to instantiate
  [the ML Goal program preset](references/goal-program-template.md) into the
  owning ticket's `program.md`, create or update `progress.md`, compile the
  Files-listed native Goal prompt, and obtain required approval.
- [ ] 5. Select the next experiment from current evidence.
  - [ ] Before every experiment, invoke Leverage Advisor on the `program.md`
    roadmap, `progress.md` learnings, current full-evaluator receipts, and
    remaining budget. Do not continue a fixed roadmap order.
  - [ ] Preregister one hypothesis, expected observation, observation horizon,
    named confidence, falsifier, surprise trigger, changed boundary, expected
    information, cost, guards, and keep/kill rule. Label `falsifier` and
    `surprise_trigger` separately; one failure threshold cannot silently stand
    in for both.
- [ ] 6. Execute and record one bounded experiment.
  - [ ] Modify only the allowed surface, run correctness smokes, then run the
    exact full frozen evaluator when valid.
  - [ ] Append the receipt link, learned constraint, keep/discard/repair-once
    decision, frontier update, and next action to ticket `progress.md`; include
    rejected alternatives or a budget checkpoint only when they materially
    affect the selection or a ceiling. Never overwrite a failed attempt.
  - [ ] When the observation materially misses its expectation or is
        implausibly strong, route the immutable receipt through
        `agent-qa-test:experiment` before rejecting the method or promoting the
        candidate. The domain executor owns every repair/rerun and must keep it
        inside the campaign's remaining time, compute, spend, and attempt budget.
- [ ] 7. Continue, replan, or stop mechanically.
  - [ ] Keep only candidates that improve the primary objective while every
    guard passes; prefer the simpler candidate when materially tied.
  - [ ] Replan after every valid full result. Stop on success, supported
    negative conclusion, exhausted useful frontier, stale packet, blocker, or
    budget before silently expanding scope.
  - [ ] In any negative-stop or surprise response, explicitly echo the
        preregistered `expected_observation`, `observation_horizon`,
        `confidence`, `falsifier`, and `surprise_trigger`; do not collapse them
        into one generic failure threshold. Explicitly say the domain executor
        owns any repair/rerun within the remaining campaign budget. Keep the
        Goal Packet active for an in-contract repair; mark it stale only when a
        frozen surface, scope, metric, data boundary, budget, or approval changes.
- [ ] 8. Finish with independent evidence review.
  - [ ] Re-run the full evaluator on the frozen best candidate, verify receipt
    and budget integrity, apply the QA checklist, obtain required QA/reviewer
    judgment, write residual risks, and close the owning ticket canonically.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Compact experiment receipt:

```yaml
experiment_id:
parent_candidate:
selected_from_roadmap:
progress_evidence_refs: []
hypothesis:
expected_observation:
observation_horizon:
confidence: low | medium | high
falsifier:
surprise_trigger:
changed_boundary:
config_code_data_evaluator_hashes: {}
command_environment:
smoke_result:
full_metrics: {}
guards: {}
runtime_compute_cost: {}
decision: keep | discard | repair_once | failed | defer
failure_or_learning:
frontier_update:
next_action:
```

## Gotchas

- Do not mistake search volume for research quality. Prefer the experiment that
  best distinguishes the current bottleneck or unlocks reusable capability.
- Do not let Leverage Advisor become an ML executor or state store. It returns
  a decision; the campaign ticket and receipts preserve state.
- Do not mutate the evaluator, split, primary metric, or prohibited inputs to
  manufacture improvement. Such changes stale the packet and require a new
  campaign decision.
- Do not make one ticket per trial. Split only for a changed objective or
  evaluator, independent owner/deliverable, separate approval/spend boundary,
  or genuinely parallel proof surface.

## Reference Map

- [ML Goal program preset](references/goal-program-template.md) — instantiate
  for every material campaign; it owns roadmap-plus-progress replanning.
- [Leverage Advisor](../leverage-advisor/SKILL.md) — initial roadmap and every
  next-experiment decision.
- [Goal Advisor](../goal-advisor/SKILL.md) — packet and native Goal compiler;
  never the technique selector.
- [Metric Advisor](../metric-advisor/SKILL.md) — use when the primary metric,
  direction, guard, or anti-metric is unclear.
- [Karpathy Autoresearch program](https://github.com/karpathy/autoresearch/blob/master/program.md)
  — source pattern only; Farplane's bounded local contract is authoritative.

## Output

- one approved campaign Goal Packet and compact native Goal prompt;
- baseline and append-only experiment receipts linked from `progress.md`;
- evidence-updated roadmap decisions with material selection rationale;
- best verified candidate or an evidence-backed no-improvement/blocked result;
- independent final evidence review and residual-risk statement.

For any requested loop policy, packet draft, or active turn, explicitly report:

```text
Packet: ticket.md + program.md + progress.md + Goal Advisor compilation state
Roadmap: program.md frontier + contingencies
Progress: progress.md learnings + current full-evaluator receipt refs
Selector: Leverage Advisor inputs + one selected move + material selection rationale
Experiment: hypothesis + falsifier + changed boundary + guards + cost
Expectation: expected observation + horizon + confidence + surprise trigger
Writeback: receipt ref + decision + learned constraint + frontier update + next action
```
