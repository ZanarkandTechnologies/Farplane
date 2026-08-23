---
name: leverage-advisor
description: "Turn a capability, evidence, and optional lever catalog into a ranked compounding roadmap, next wave, and first proof step."
tier: 2
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.2.0"
  skill-qa-checklist: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Glob, Grep

---

# Leverage Advisor

## Context

Use this when the operator points at an existing feature, capability, workflow,
artifact, tool, or bounded improvement campaign and asks what move or next wave
will create the most compounding value.

This is a conditional comparison workflow, not the default owner of every Goal
turn and not an execution or continuation loop. Invoke it when several
plausible moves need judgment; skip it when one next move is mechanically
implied. It
generates or consumes candidate levers, ranks short contingent trajectories,
chooses the next wave and first proof, and states when later evidence should
cause replanning. Domain entrypoints execute the move. Goal Advisor compiles a
material campaign. The ticket and `program.md` own scope and policy,
`hypothesis-tree.json` owns current experiment-search state when enabled, and
`progress.md` owns chronological receipts.

## Skill Signature

```text
advise_leverage(subject_ref, objective?, evidence_refs?, constraints?,
                lever_catalog?, hypothesis_tree_ref?, progress_ref?,
                remaining_budget?)
  -> leverage_plan + ranked_frontier + next_wave + first_proof
   + replan_conditions + source_gap?
state: reads(subject docs, registries, tickets/specs, optional lever catalog,
             optional hypothesis tree, program policy, progress observations,
             experiment receipts, prior proof, constraints and remaining
             budget);
       writes(leverage plan or ticket seed only when the caller owns a path)
gates: subject_grounded; objective_named; catalog_resolved_or_source_gap;
       diagnosis_and_policy_named; pre_outcome_bet_recorded;
       decision_changing_test_named; eligible_frontier_ranked; next_wave_earned;
       first_proof_named; replan_conditions_named
routes: reference-grounding | research:parity |
  research:source-synthesis | best-of-worlds | prototyping | metric-advisor |
  impl-plan | goal-advisor | harness-advisor | leverage-rollout
fails: generic strategy; invented capability or candidate; fixed ladder that
  ignores progress; fake-precision score; roadmap without proof or replan;
  pairwise tournament; persistent rank ownership; execution, Goal compilation,
  or ticket-per-experiment ownership
```

When `subject_ref` is underspecified, resolve it from local files, active
tickets, registries, recent decision artifacts, or one narrow question if the
subject cannot be identified safely.

## Phase Boundary

Keep evidence gathering and recommendation inline when the feature is already
locally grounded. Use a separate research, planning, or Goal skill only when
the chosen next step needs its own artifact, budget, or proof surface.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the feature and ambition.
   - [ ] Identify the feature, capability, workflow, artifact, or bounded
     campaign being maximized and name its objective.
   - [ ] Bind supplied constraints, remaining budget, program policy, optional
     hypothesis tree, catalog, and `progress.md` or experiment evidence when
     this is a replan checkpoint.
   - [ ] A campaign replan requires the actual program policy, eligible tree
     leaves, relevant progress/receipts, and remaining budget. If any are
     absent, return a source gap. A provisional diagnostic frontier may compare
     only moves supported by supplied evidence across bottleneck fit,
     information, unlocks, proof speed, cost, risk, and outside options, but it
     must be labeled conditional and not selected until missing state arrives.
   - [ ] Set the default objective to "compound leverage from existing
     capability" only when the caller does not provide a more concrete one.
   - [ ] Set default constraints to low operator effort, fast proof, reusable
     gain, and bounded rollout risk.
- [ ] 2. Ground the current capability.
   - [ ] Read the smallest relevant feature docs, registry rows, tickets,
     specs, skill contracts, or proof artifacts.
   - [ ] Use [reference-grounding](../reference-grounding/SKILL.md) when the
     recommendation depends on evidence not already loaded.
   - [ ] State what the subject already does, what progress has established or
     falsified, what remains uncertain, and what local assets can be reused.
- [ ] 3. Frame the decision before ranking.
   - [ ] Name the critical obstacle, a guiding policy that narrows the frontier,
     and the coherent next move it implies (Rumelt, *Good Strategy/Bad
     Strategy*).
   - [ ] Record the pre-outcome bet: what must be true, a calibrated confidence
     range when evidence supports one (otherwise `uncalibrated`), downside, and
     falsifier. Do not judge the decision solely from a later outcome (Duke,
     *Thinking in Bets*).
   - [ ] Specify the cheapest honest observation, then explicitly render
     `if positive -> next action` and `if negative -> next action`. Reject easy
     metrics that cannot change the ranking, spend, scope, or outside option
     (Hubbard, *How to Measure Anything*).
   - [ ] For deeper source method and the required decision-record fields, load
     [decision techniques](references/decision-techniques.md) when the choice
     is material, outcome uncertainty is high, or the evidence plan spends
     meaningful time, money, or attention.
- [ ] 4. Resolve the candidate frontier.
   - [ ] When an experiment-backed campaign supplies
     `hypothesis-tree.json`, treat eligible pending leaves as the current
     frontier. Derive leaves from parent and status; do not require stored
     ranks, child lists, depth, or a duplicate frontier.
   - [ ] Before the first mutation, use the supplied or project-local lever
     catalog, local failures, source-stage techniques, mechanisms, and variables
     to create intervention hypotheses with expected observations, falsifiers,
     expected rewards, and concise reward bases.
   - [ ] Otherwise generate candidates from grounded capability, failures,
     prior proof, and remaining constraints.
   - [ ] When credible candidates are missing, stale, or too weak to justify a
     choice, route bounded external research or multi-source synthesis through
     the owning workflow, then record `adopt | adapt | reject | defer`
     dispositions. Return a source gap rather than inventing candidates when
     the branch cannot run.
   - [ ] Filter prerequisites, conflicts, guards, exhausted branches, and moves
     that exceed the remaining budget before ranking.
- [ ] 5. Rank compounding moves and short trajectories.
   - [ ] When choosing among real plays, compare the viable options and state
     one recommendation with its accepted tradeoff.
   - [ ] Compare direct objective potential, bottleneck fit, information gain,
     downstream options unlocked, reusable assets, proof speed, cost, risk,
     reversibility, and interference. Use evidence-backed ordinal judgment
     unless calibrated numeric priors exist.
   - [ ] Include exactly three options when three viable options exist; do not
     invent a third weak option.
   - [ ] Make one ordinal comparison. Do not use a pairwise tournament, invent
     uncalibrated numeric lift, persist rank scores in the tree, or create a
     second selection algorithm.
- [ ] 6. Recommend the next wave and first proof.
   - [ ] Name the tradeoff accepted.
   - [ ] Choose one move by default. Admit multiple moves only when they are
     independently attributable, non-interfering, and budget-safe.
   - [ ] Make the first proof the decision-changing test from step 3 when it
     remains the cheapest honest falsifier of the strongest trajectory; do not
     collect an observation that leaves the recommendation unchanged.
   - [ ] Explicitly render and compare the best move with `report_now`,
     `request_feedback`, and `stop`; recommend spending more budget only when
     it wins. Do not leave this comparison implicit.
   - [ ] Use [prototyping](../prototyping/SKILL.md) when a 1 -> 10 -> 100
     proving path matters before scale.
- [ ] 7. State replan conditions and choose the next owner.
   - [ ] Define how positive, flat, negative, branch-specific, invalid, or
     budget evidence changes the frontier; do not return a fixed ladder.
   - [ ] Keep one stable objective, evaluator, and budget in one campaign
     ticket. Update current node state in `hypothesis-tree.json` and append the
     same selection/mutation receipt to `progress.md`; split only at a real
     ownership, proof, approval, spend, or objective boundary.
   - [ ] Add at most the program-bounded diagnostic children when a result is
     surprising, invalid, prerequisite-uncertain, or causally ambiguous.
     Expected negatives may close directly. After diagnosis, repair, reject,
     defer, or backtrack while preserving credible siblings.
   - [ ] Use [metric-advisor](../metric-advisor/SKILL.md) when the first proof
     depends on choosing a metric, reward signal, guard metric, or no-metric
     rationale.
   - [ ] Name `impl-plan` when the first proof is a coding ticket plan.
   - [ ] Name `goal-advisor` only when a durable Goal Packet is warranted.
   - [ ] Name `harness-advisor` when the main unresolved question is owner
     surface or harness lever.
   - [ ] Name `leverage-rollout` when the recommended play should be proven
     through exemplar runs before rollout.
- [ ] 8. Return the leverage plan and apply [the QA checklist](qa_checklist.md).
   - [ ] Subject grounding and progress evidence are concrete.
   - [ ] Recommendation is not generic strategy.
   - [ ] Ranked frontier, next wave, first proof, rejected moves, and replan
     conditions are replayable from named evidence.
   - [ ] Reuse path, state owner, and next owner are explicit.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Program

```text
vars:
  subject = subject_ref
  objective = objective? or "compound leverage from existing capability"
  evidence = evidence_refs? + hypothesis_tree_ref? + progress_ref?
    + discover_nearest_context(subject)
  constraints = constraints? or [
    low_operator_effort,
    fast_proof,
    reusable_gain,
    bounded_rollout_risk
  ]

program:
  ground(subject, objective, evidence) -> current_state + learned_constraints

  frame_decision(current_state, objective) ->
    diagnosis + guiding_policy + coherent_move

  precommit_bet(coherent_move, evidence) ->
    thesis + confidence_range_or_uncalibrated + downside + falsifier

  resolve_candidates(
    hypothesis_tree_ref?, lever_catalog?, current_state, learned_constraints
  ) -> candidate_frontier | bounded_source_gap

  filter(candidate_frontier,
    prerequisites + conflicts + guards + remaining_budget
  ) -> eligible_frontier

  compare_short_trajectories(eligible_frontier,
    criteria = [
      direct_objective_potential,
      bottleneck_fit,
      information_gain,
      downstream_options_unlocked,
      reusable_assets,
      proof_speed,
      cost,
      risk,
      reversibility,
      interference
    ]
  ) -> ordinal_ranked_frontier

  compare_and_recommend(ordinal_ranked_frontier) -> next_wave + tradeoff_accepted

  compare_outside_options(next_wave,
    report_now + request_feedback + stop
  ) -> spend_decision

  design_decision_changing_test(next_wave, falsifier) ->
    first_proof + decision_if_positive + decision_if_negative

  define_replan_conditions(
    next_wave, ordinal_ranked_frontier
  ) -> positive + flat + negative + invalid + diagnostic + budget branches

  decide_execution_shape(next_wave) ->
    direct_action | metric_card | impl_plan | goal_packet | leverage_rollout

  output(leverage_plan)
```

## Templates

Short positive example:

```text
Input:
  subject_ref = "TASK-0055 ML research campaign"
  objective = "raise spatial discovery ranking under a fixed evaluator"
  progress_ref = "tickets/TASK-0055/progress.md"

Output:
  Next wave: run the cheap multiscale boosted-tree probe because it tests the
  current representation bottleneck and creates reusable neighbourhood inputs.
  Positive result: deepen representation or supervision. Flat result: inspect
  data/label limits before a neural model. Type-specific result: branch the
  next move by deposit system. Next owner: ML Autoresearch inside the existing
  campaign Goal Packet.
```

## Gotchas

- Do not confuse leverage advice with harness placement. Use `harness-advisor`
  when the primary question is which harness surface should own a behavior.
- Do not scale before proof. The first useful answer can be one excellent
  example, not a broad roadmap.
- Do not turn every good play into a Goal. Tiny direct actions should stay
  direct.
- Do not become a global registry, research engine, experiment executor, Goal
  compiler, ticket materializer, or second continuation owner.
- Do not become the hypothesis-tree state owner. Read the tree, return one
  selection and mutation expectation, and let the campaign update it.
- Do not rank technique names by novelty. Tie every move to the current
  bottleneck, evidence, cheapest falsifier, and result-dependent frontier
  update.
- Do not call an outcome proof of decision quality by itself. Compare it with
  the pre-outcome thesis, falsifier, and plausible luck or execution factors.
- Do not collect a convenient metric unless its positive and negative outcomes
  would alter the next action, spend, scope, or outside option.
- Do not turn a caller's relative timing (for example, "next month") into an
  unsupported calendar date.
- Do not invent current capability. If the feature is not grounded, say what
  evidence is missing and choose a grounding step.

## Reference Map

- Compare viable leverage plays inline when an explicit recommendation remains
  necessary.
- [../reference-grounding/SKILL.md](../reference-grounding/SKILL.md) - use
  when current capability or expected value needs evidence.
- [../research/SKILL.md](../research/SKILL.md) - use only when the candidate
  frontier is missing, stale, or evidence-thin enough to change the decision.
- [../best-of-worlds/SKILL.md](../best-of-worlds/SKILL.md) - use when several
  sources need scored `adopt | adapt | reject | defer` dispositions before
  entering the frontier.
- [../prototyping/SKILL.md](../prototyping/SKILL.md) - use when the proof path
  should start with one representative case before expansion.
- [../metric-advisor/SKILL.md](../metric-advisor/SKILL.md) - use when the
  first proof step needs an honest metric card before execution routing.
- [../leverage-rollout/SKILL.md](../leverage-rollout/SKILL.md) - use when the
  recommended play should become exemplar runs and staged rollout.
- [../goal-advisor/SKILL.md](../goal-advisor/SKILL.md) - use when a chosen play
  warrants a durable Goal Packet or rollout mode.
- [decision techniques](references/decision-techniques.md) - load for
  material, high-uncertainty, or meaningful-cost decisions requiring the named
  Rumelt, Duke, and Hubbard source methods.

## Output

For a source-gapped campaign replan, return a clearly conditional comparison
table with one row per supplied-evidence move and columns for objective fit,
bottleneck fit, information value, options unlocked, proof speed, cost, risk,
reversibility, and interference. Then compare separate rows for `report_now`,
`request_feedback`, and `stop`. Do not call a move selected until the missing
program/tree/progress/receipt/budget state is bound.

Return this shape in chat or write it to the requested artifact:

- `Feature Grounding`
- `Objective And Progress Grounding`
- `Hypothesis Tree Grounding`, when supplied
- `Decision Record`: `Diagnosis`, `Guiding Policy`, `Coherent Move`, `Bet
  Thesis`, `Confidence Range` or `Uncalibrated`, `Downside`, `Falsifier`, and
  `Decision-Changing Test` with `If Positive -> Next Action` and `If Negative
  -> Next Action`
- `Ranked Frontier And Rejected Moves`
- `Outside-Option Comparison`: `Next Wave`, `Report Now`, `Request Feedback`,
  and `Stop`, with an explicit spend decision
- `Next Wave`
- `Tradeoff Accepted`
- `Contingent Roadmap And Replan Conditions`
- `First Proof Step`
- `Source Gap`, when applicable
- `Next Owner`
- `Goal / Rollout Readiness`

For every material, non-source-gapped recommendation, render every `Decision
Record` field by name. Do not replace the bet thesis, downside, or falsifier
with an implied rationale; use `uncalibrated` rather than omitting confidence
when evidence does not support a calibrated range.

For a source gap, state the missing evidence and the bounded recovery route,
then make the candidate-admission gate explicit: every recovered candidate must
carry an `adopt`, `adapt`, `reject`, or `defer` disposition before it can enter
the frontier. Do not present that recovery step as a selected operating move.

For a source-stage request with sufficient inputs, do not return only a schema.
Render the extracted `Source refs`, `Techniques`, `Mechanisms`, and `Variables`,
then at least two concrete intervention candidates when credible alternatives
exist. Every candidate must include `hypothesis`, `mechanism`,
`expected_observation`, `falsifier`, `expected_reward`, `reward_basis`, and
`source_refs`. Finish with one ordinal selected candidate and its rationale. A
source gap is valid only when the supplied facts genuinely cannot support those
fields.

For an ambiguous-result request, render `Diagnostic children`, `Preserved
siblings`, `Outcome branches` (`repair | reject | defer | backtrack`), and
`Writeback order` (`hypothesis-tree.json` before `progress.md`).
