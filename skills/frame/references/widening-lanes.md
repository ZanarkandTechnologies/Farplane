# Widening Lanes And Ensemble

Load this in `frame` N2 when the option space is unclear and one lane would cut
the specific uncertainty, or when the operator asks for `ensemble: auto | max`.
Touch each field only as deeply as the request deserves; tiny creative prompts
need the base contrast, not a lane.

## Base Contrast

```text
widen(frame) -> objective + current_reality + first_principles_rebuild
              + 2-4 candidate_directions + strongest_tradeoffs
```

## Optional Lanes

Pick at most the one lane that matches the uncertainty.

```text
why_chain(current_reality)
  -> inherited_assumptions + incentives + obsolete_constraints + root_causes
```

Use when a habit, market standard, or incentive may explain the problem.

```text
customer_data_action(problem)
  -> actor -> decision -> required_data -> action -> write_back + system_boundary
```

Use for operational workflows, internal tools, and triage or alert loops.
Warning sign: if the result reads as a list of components instead of that
chain, the lane is not being used.

```text
issue_tree(problem)
  -> top_question + 2-5 branches + sub_branches + evidence_needed + first_branch
```

Use when root cause, workstreams, or branch priority matter. Branches share one
organizing logic and do not overlap; a tree that mixes users, components,
solutions, and symptoms is not ready.

```text
working_backwards(product_bet)
  -> customer + promise + press_release_claim + faq_objections + first_lovable_slice
```

Use when the idea is a product bet or launchable offer. It stays a direction,
not a PRD.

## Ensemble Modes

The direct path is the default. Only when the operator asks, load
[../ensemble.yaml](../ensemble.yaml):

```text
ensemble: auto -> exactly 3 relevant, diverse personas -> independent first passes -> chair synthesis
ensemble: max  -> every persona                       -> independent first passes -> chair synthesis
```

Choose personas by their stated focus, not a preset. Personas are behavioral
archetypes; a request to think like a named public figure maps to the closest
archetype, never imitation. The chair keeps the normal `frame` output shape,
preserves meaningful dissent, and does not take a majority vote. Ensemble mode
never propagates into child calls.

Synthesis picks the direction with the strongest argument, evidence fit, local
fit, and speed to useful learning.
