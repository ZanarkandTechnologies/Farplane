---
name: leverage-advisor
description: "Turn an existing feature or capability into ranked leverage plays, a rollout roadmap, and the next executable proof step."
tier: 2
source: local
skill_template_version: "0.2.0"
allowed-tools: Read, Glob, Grep
---

# Leverage Advisor

## Context

Use this when the operator points at an existing feature, capability, workflow,
artifact, or tool and asks how to get the most compounding value from it.

This is an advice workflow, not an execution loop. It chooses the best leverage
play and the first proof step. Use `leverage-rollout` when the selected play
should be turned into exemplar runs, Goal Packets, staged rollout, or repeated
execution.

## Skill Signature

```text
advise_leverage(feature_ref, context_refs?, ambition?, constraints?) -> leverage_plan + recommended_first_move
state: reads(feature docs, feature registry, tickets, specs, current repo state, related skills, prior proof); writes(leverage_plan.md? ticket_seed? autoresearch_seed? goal_recommendation?)
gates: feature_grounded; opportunities_ranked; recommendation_named; proof_path_named; next_action_executable
routes: reference-grounding | advise | prototyping | autoresearch-plan | impl-plan | goal-advisor | harness-advisor | leverage-rollout
fails: gives generic strategy; invents feature capability; recommends a roadmap with no first proof step; over-goalifies tiny moves
```

When `feature_ref` is underspecified, resolve it from local files, active
tickets, feature registry rows, recent discussion artifacts, or one narrow
question if the feature cannot be identified safely.

## Phase Boundary

Keep evidence gathering and recommendation inline when the feature is already
locally grounded. Use a separate research, planning, or Goal skill only when
the chosen next step needs its own artifact, budget, or proof surface.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the feature and ambition.
   - [ ] Identify the feature, capability, workflow, or artifact being
     maximized.
   - [ ] Set the default ambition to "compound leverage from existing
     capability" when the caller does not provide one.
   - [ ] Set default constraints to low operator effort, fast proof, reusable
     gain, and bounded rollout risk.
- [ ] 2. Ground the current capability.
   - [ ] Read the smallest relevant feature docs, registry rows, tickets,
     specs, skill contracts, or proof artifacts.
   - [ ] Use [reference-grounding](../reference-grounding/SKILL.md) when the
     recommendation depends on evidence not already loaded.
   - [ ] State what the feature already does, what it does not prove yet, and
     what local surfaces it can realistically affect.
- [ ] 3. Generate and score leverage plays.
   - [ ] Use [advise](../advise/SKILL.md) when choosing among real plays.
   - [ ] Score plays for compounding value, proof speed, reuse surface,
     operator-effort reduction, implementation friction, and rollout risk.
   - [ ] Include exactly three options when three viable options exist; do not
     invent a third weak option.
- [ ] 4. Recommend one play and the first proof step.
   - [ ] Name the tradeoff accepted.
   - [ ] Choose the smallest honest proof step before broader rollout.
   - [ ] Use [prototyping](../prototyping/SKILL.md) when a 1 -> 10 -> 100
     proving path matters before scale.
- [ ] 5. Choose the next owner.
   - [ ] Name `autoresearch-plan` when the first proof is metric-driven
     research.
   - [ ] Name `impl-plan` when the first proof is a coding ticket plan.
   - [ ] Name `goal-advisor` only when a durable Goal Packet is warranted.
   - [ ] Name `harness-advisor` when the main unresolved question is owner
     surface or harness lever.
   - [ ] Name `leverage-rollout` when the recommended play should be proven
     through exemplar runs before rollout.
- [ ] 6. Return the leverage plan and self-check it.
   - [ ] Feature grounding is concrete.
   - [ ] Recommendation is not generic strategy.
   - [ ] First proof step is executable.
   - [ ] Reuse path and next owner are explicit.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Program

```text
vars:
  feature = feature_ref
  context = context_refs? or discover_nearest_feature_context(feature)
  ambition = ambition? or "compound leverage from existing capability"
  constraints = constraints? or [
    low_operator_effort,
    fast_proof,
    reusable_gain,
    bounded_rollout_risk
  ]

program:
  ground(feature, context) -> current_capability

  identify_enabled_moves(current_capability, ambition) -> opportunity_list

  score(opportunity_list,
    criteria = [
      compounding_value,
      proof_speed,
      reuse_surface,
      operator_effort_reduction,
      implementation_friction,
      rollout_risk
    ]
  ) -> ranked_opportunities

  advise(ranked_opportunities) -> recommended_play + tradeoff_accepted

  design_first_test(recommended_play) -> experiment_or_ticket_seed

  decide_execution_shape(recommended_play) ->
    direct_action | autoresearch_plan | impl_plan | goal_packet | leverage_rollout

  output(leverage_plan)
```

## Templates

Short positive example:

```text
Input:
  feature_ref = "Goal Packets"
  ambition = "reduce operator effort and make useful work resume without chat memory"

Output:
  Recommendation: use Goal Packets first on one stalled high-value ticket where
  state recovery has been painful. First proof: create ticket.md, program.md,
  and progress.md, then resume from files alone once. Next owner:
  leverage-rollout if the exemplar works; goal-advisor if the packet is ready.
```

## Gotchas

- Do not confuse leverage advice with harness placement. Use `harness-advisor`
  when the primary question is which harness surface should own a behavior.
- Do not scale before proof. The first useful answer can be one excellent
  example, not a broad roadmap.
- Do not turn every good play into a Goal. Tiny direct actions should stay
  direct.
- Do not invent current capability. If the feature is not grounded, say what
  evidence is missing and choose a grounding step.

## Reference Map

- [../advise/SKILL.md](../advise/SKILL.md) - use when choosing among viable
  leverage plays.
- [../reference-grounding/SKILL.md](../reference-grounding/SKILL.md) - use
  when current capability or expected value needs evidence.
- [../prototyping/SKILL.md](../prototyping/SKILL.md) - use when the proof path
  should start with one representative case before expansion.
- [../leverage-rollout/SKILL.md](../leverage-rollout/SKILL.md) - use when the
  recommended play should become exemplar runs and staged rollout.
- [../goal-advisor/SKILL.md](../goal-advisor/SKILL.md) - use when a chosen play
  warrants a durable Goal Packet or rollout mode.

## Output

Return this shape in chat or write it to the requested artifact:

- `Feature Grounding`
- `Leverage Opportunities`
- `Recommendation`
- `Tradeoff Accepted`
- `Roadmap`
- `First Proof Step`
- `Next Owner`
- `Goal / Rollout Readiness`
