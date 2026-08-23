# Brainstorm Spine And Ensemble

Use this reference when a brainstorm asks for first-principles decomposition,
current-vs-ideal redesign, PRFAQ/working-backwards thinking, or a requested
ensemble view.

## Base Spine

```text
brainstorm_spine(prompt, objective?, context?)
  -> objective
   + current_reality
   + first_principles_contrast
   + candidate_directions
   + recommendation
   + next_owner
```

The direct path is compact. It should not become a ritual checklist for tiny
creative prompts; touch each field only as deeply as the request deserves.

## Optional Depth Lanes

Use lanes for targeted depth, not mandatory framework stacking.

```text
why_chain_lane(current_reality)
  -> inherited_assumptions + incentives + obsolete_constraints + root_causes
```

Use when the current process, habit, market standard, or organizational
incentive may explain the problem.

```text
customer_data_action_lane(problem)
  -> actor + decision + required_data + action + write_back + system_boundary
```

Use when the idea is an operational workflow, internal tool, triage surface, or
action loop. This lane corresponds to
[palantir-customer-data-action](palantir-customer-data-action.md).

```text
issue_tree_lane(problem)
  -> top_question + branches + sub_branches + evidence_needed + first_branch
```

Use when completeness, root cause, workstreams, or branch prioritization matter.
This lane corresponds to [mckinsey-issue-tree](mckinsey-issue-tree.md).

```text
working_backwards_lane(product_bet)
  -> customer + promise + press_release_claim + faq_objections + first_lovable_slice
```

Use when the brainstorm is really a product bet or launchable offer.

## Ensemble Modes

The direct path remains the default. If the operator asks for ensemble
coverage, load [../ensemble.yaml](../ensemble.yaml):

```text
ensemble: auto
  -> select exactly 3 relevant, diverse personas
   + independent first passes
   + synthesize into exploration_note

ensemble: max
  -> use every persona
   + independent first passes
   + synthesize into exploration_note
```

Choose personas by their stated focus, not by a fixed preset. Every synthesis
keeps the normal brainstorm output contract and preserves meaningful dissent;
it is not a majority vote. Do not propagate ensemble mode into child calls.

## Synthesis Rule

```text
synthesize_brainstorm(lane_outputs, output_contract)
  -> exploration_note with recommendation, dissent, evidence gaps,
     accepted tradeoff, and next owner
```

Choose the recommendation with the strongest argument, evidence fit, local
surface fit, and speed to useful learning.
