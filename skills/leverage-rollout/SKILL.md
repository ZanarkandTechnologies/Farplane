---
name: leverage-rollout
description: "Turn a selected leverage play into exemplar proof, extracted rollout pattern, and optional Goal-backed staged rollout."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash

---

# Leverage Rollout

## Context

Use this after a feature or capability has a plausible leverage play and the
operator wants the agent to turn that play into practical compounding value.

This skill owns the "do things that do not scale first" layer. It should prove
one to three excellent examples, extract the pattern, and only then use
`goal-advisor` rollout mode for scaling across a target set.

## Skill Signature

```text
roll_out_leverage(feature_ref, selected_play?, target_set?, ambition?, proof_need?) -> exemplar_packet + sample_proof + rollout_recommendation + optional_rollout_packet
state: reads(leverage plan, feature refs, tickets, specs, registries, current repo state, existing proof); writes(ticket.md? program.md? progress.md? artifacts? rollout child tickets?)
gates: selected_play_exists; exemplar_selected; sample_proof_created; pattern_extracted; rollout_readiness_decided; goal_advisor_rollout_used_when_scaling
routes: leverage-advisor | metric-advisor | goal-advisor | impl-plan | review | eval | optimize-with-human
fails: scales before exemplar proof; treats generic advice as sample proof; creates rollout Goal without target set; hides learning outside progress or artifacts
```

## Phase Contract

```text
leverage_rollout_phase(task, bound_inputs, state)
  -> grounded_play
   + exemplar_plan
   + exemplar_goal_or_direct_proof
   + pattern_extraction
   + rollout_readiness_decision
   + optional_goal_advisor_rollout
```

## Phase Boundary

This skill may create or recommend Goal Packets, but it does not replace
`goal-advisor`. Use `goal-advisor` for native Goal architecture, heartbeat,
rollout, batch, or final prompt compilation after an exemplar pattern exists.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the rollout inputs.
   - [ ] Identify the feature or capability.
   - [ ] Load an existing leverage plan when supplied.
   - [ ] Use [leverage-advisor](../leverage-advisor/SKILL.md) first when the
     selected leverage play is missing or weak.
   - [ ] Identify or propose a target set, but do not scale to it yet.
- [ ] 2. Choose one to three exemplar cases.
   - [ ] Prefer cases with high learning value, low setup friction, real
     enough failure exposure, and standalone value even if rollout stops.
   - [ ] State why each exemplar is representative.
   - [ ] Define what would prove, falsify, or pause the rollout idea.
- [ ] 3. Create or prepare the exemplar execution surface.
   - [ ] Use direct action for tiny exemplar proof.
   - [ ] Use [impl-plan](../impl-plan/SKILL.md) when the exemplar is a coding
     ticket that needs an approval-ready build plan.
   - [ ] Derive a metric card before any repeated metric-based exemplar.
   - [ ] Use [goal-advisor](../goal-advisor/SKILL.md) when the exemplar needs
     ticket.md, program.md, progress.md, budget, metric, or drift policy.
- [ ] 4. Capture sample proof and extract the rollout pattern.
   - [ ] Record the sample result or expected evidence path.
   - [ ] Extract reusable steps, failure modes, proof requirements, target
     filters, rollback or hold conditions, and operator feedback points.
   - [ ] Keep learning in the ticket, progress log, or artifacts instead of
     chat-only memory.
- [ ] 5. Decide rollout readiness.
   - [ ] Stop if the exemplar is weak, generic, or not worth repeating.
   - [ ] Run a second exemplar when the first result is promising but the
     pattern is not yet stable.
   - [ ] Promote to `goal-advisor` rollout only when a pattern, sample proof,
     and explicit target set exist.
- [ ] 6. Use Goal Advisor for scaling when ready.
   - [ ] Pass the extracted pattern, sample proof, target set, budget, metric,
     and hold/rollback conditions to [goal-advisor](../goal-advisor/SKILL.md).
   - [ ] Preserve the Goal Advisor rollout contract:
     `rollout_goal(pattern, sample_proof, target_set) -> staged_batches +
     child_tickets? + rollout_progress`.
   - [ ] Require one proof row per staged target or child ticket.
- [ ] 7. Finish with a rollout decision and review path.
   - [ ] Use [review](../review/SKILL.md) when the rollout recommendation,
     proof quality, or completion claim is judgment-heavy.
   - [ ] Use [eval](../eval/SKILL.md) when the behavior should be scored across
     repeatable cases.
   - [ ] State the next concrete owner: stop, second exemplar, Goal Packet,
     staged rollout, or skill promotion.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Program

```text
vars:
  feature = feature_ref
  selected_play = selected_play? or leverage_advisor(feature).recommended_play
  target_set = target_set? or discover_likely_targets(feature, selected_play)
  exemplar_count = 1..3

program:
  load_or_create_leverage_plan(feature, selected_play) -> leverage_plan

  choose_exemplar(leverage_plan, target_set) -> exemplar_case
    criteria = [
      high_learning_value,
      low_setup_friction,
      real_failure_exposure,
      standalone_value_if_not_scaled
    ]

  create_or_prepare_exemplar(exemplar_case) ->
    direct_proof | impl_plan | goal_packet

  run_or_handoff_exemplar(exemplar_execution) -> sample_proof

  extract_pattern(sample_proof) ->
    reusable_steps
    + failure_modes
    + proof_requirements
    + rollout_constraints
    + hold_or_rollback_conditions

  decide_rollout_readiness(pattern, sample_proof) ->
    stop | run_second_exemplar | promote_to_rollout

  if promote_to_rollout:
    goal_advisor.rollout(pattern, sample_proof, target_set) ->
      staged_batches + child_tickets? + rollout_progress

  output(rollout_decision)
```

## Templates

Short positive example:

```text
Input:
  feature_ref = "autonomous scale improvement"
  selected_play = "use it to find underused high-leverage Farplane features"

Output:
  Exemplar: run the play on one underused feature registry row and produce a
  concrete next-action plan. Sample proof: compare whether the output names a
  useful first ticket, proof path, and next owner. Rollout decision: run a
  second exemplar before using goal-advisor rollout across ten features.
```

## Gotchas

- Do not skip the exemplar phase. `goal-advisor` rollout starts after sample
  proof, not before it.
- Do not treat a nice idea as `sample_proof`. Sample proof must come from a
  concrete case, artifact, run, ticket, or evaluated output.
- Do not create a broad Goal with no target set. Rollout needs explicit targets
  and staged proof.
- Do not promote the rollout procedure into a reusable skill until repeated use
  proves the trigger and workflow are stable.

## Reference Map

- [../leverage-advisor/SKILL.md](../leverage-advisor/SKILL.md) - use when the
  selected leverage play is missing or needs recommendation.
- [../metric-advisor/SKILL.md](../metric-advisor/SKILL.md) - use when exemplar
  proof needs an honest metric card before repeated measurement.
- [../goal-advisor/SKILL.md](../goal-advisor/SKILL.md) - use for Goal Packet,
  heartbeat, rollout, batch, and native `/goal` prompt architecture.
- [../goal-advisor/references/goal-shapes.md](../goal-advisor/references/goal-shapes.md) -
  load when rollout, batch, heartbeat, or portfolio shape needs more detail.
- [../../docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md](../../docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md) -
  load when the rollout contract itself needs spec-level grounding.

## Output

Return this shape in chat or write it to the requested artifact:

- `Leverage Plan`
- `Exemplar Case`
- `Sample Proof`
- `Extracted Pattern`
- `Rollout Readiness`
- `Goal Advisor Handoff`
- `Next Owner`
