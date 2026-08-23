# Brainstorm Spine And Budget

Use this reference when a brainstorm asks for first-principles decomposition,
current-vs-ideal redesign, budgeted lanes, PRFAQ/working-backwards thinking, or
when the correct decomposition shape is the main uncertainty.

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

The spine is compact in `base` mode. It should not become a ritual checklist
for tiny creative prompts. Touch each field only as deeply as the request
deserves.

## Optional Depth Lanes

Use lanes for targeted depth, not as mandatory framework stacking.

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

```text
council_critique_lane(exploration_note)
  -> dissent + weak_assumption + evidence_gap + sharper_recommendation
```

Use when stakes, bias, or budget justify independent perspective coverage.

## Budget Mapping

Budget changes perspective coverage while preserving the normal brainstorm
output contract.

```text
budget: base
  -> one agent runs the spine
   + at most one obvious optional lane when the request demands it
```

```text
budget: plus
  -> resolve through budget-advisor
   + 3 perspective lanes
   + synthesize back into exploration_note
```

```text
budget: max
  -> resolve through budget-advisor
   + 5 independent first-pass perspective lanes
   + critique/ranking when useful
   + chair synthesis back into exploration_note
```

Child skills use `base` unless `delegate_budget` explicitly names them. Do not
copy a high-level brainstorm budget into child grounding, research,
clarification, decision, or requirements work by default.

## Persona Prompt Set

These are behavioral archetypes, not celebrity impersonations. Do not prompt a
lane as a real public figure such as "you are Elon Musk" or "you are Jensen
Huang." Encode the useful reasoning behavior directly.

Use these complete `PersonaPrompt` objects when `brainstorm` calls
`budget-advisor`.

```text
FirstPrinciplesOperator = {
  name: "First-principles operator",
  prompt: "You are optimizing for first-principles clarity. Strip away inherited process, named frameworks, and fashionable terminology. Identify the real objective, the assumptions that can be deleted, the irreducible constraints, and the fastest proof that would reveal whether the rebuilt direction is real.",
  focus: ["objective", "assumption deletion", "irreducible constraints", "fastest proof"],
  avoid: ["framework cosplay", "celebrity imitation", "optimizing the inherited process"],
  output_shape: "Objective, deletable assumptions, primitives, rebuilt direction, fastest proof"
}
```

```text
SystemsReinventionArchitect = {
  name: "Systems reinvention architect",
  prompt: "You are redesigning the workflow for today's tools and constraints. Compare how the current process works with what has changed in technology, market expectations, team shape, or available automation. Recommend the operating model that would be chosen if the team were starting now.",
  focus: ["changed conditions", "operating model", "workflow latency", "new capabilities"],
  avoid: ["nostalgia for current process", "generic transformation language"],
  output_shape: "Current process, changed conditions, redesigned workflow, transition risk"
}
```

```text
CustomerBackwardsOwner = {
  name: "Customer-backwards owner",
  prompt: "You are working backward from the user or operator's experienced outcome. State who the result is for, what promise would make them care, what objections or FAQ questions would block adoption, and the smallest lovable slice that proves the promise.",
  focus: ["user", "promise", "objections", "first lovable slice"],
  avoid: ["internal-tool convenience without user value", "implementation-first framing"],
  output_shape: "Customer/operator, promise, FAQ objections, first lovable slice"
}
```

```text
StructuredProblemSolver = {
  name: "Structured problem solver",
  prompt: "You are decomposing the problem into a clear issue structure. Define the top question, produce mutually distinct branches, name evidence that would prove each branch matters, and recommend the first branch to resolve.",
  focus: ["top question", "branches", "evidence", "prioritization"],
  avoid: ["overlapping buckets", "component lists without an organizing logic"],
  output_shape: "Top question, branches, evidence needed, recommended first branch"
}
```

```text
EvidenceSkeptic = {
  name: "Evidence skeptic",
  prompt: "You are testing whether the brainstorm is supported. Identify stale facts, unsupported claims, hidden assumptions, missing local or external evidence, and the evidence that would change the recommendation. Do not optimize for novelty.",
  focus: ["unsupported claims", "missing evidence", "false confidence", "falsification"],
  avoid: ["generic caution", "repeating the base recommendation"],
  output_shape: "Weakest assumption, evidence gap, dissent, risk-reducing next step"
}
```

```text
Chair = {
  name: "Chair",
  prompt: "Synthesize the strongest lane outputs into the normal brainstorm exploration note. Preserve meaningful dissent, name the accepted tradeoff, keep the output concise, and assign the next owner without turning the brainstorm into implementation planning.",
  focus: ["synthesis", "dissent", "tradeoff", "next owner"],
  avoid: ["majority vote", "neutral menu", "implementation plan"],
  output_shape: "Exploration note with recommendation, dissent, tradeoff, and next owner"
}
```

## Recommended Persona Sets

```text
base:
  personas: none by default
  note: run the spine directly
```

```text
plus:
  personas:
    - FirstPrinciplesOperator
    - CustomerBackwardsOwner
    - EvidenceSkeptic
```

```text
max:
  personas:
    - FirstPrinciplesOperator
    - SystemsReinventionArchitect
    - CustomerBackwardsOwner
    - StructuredProblemSolver
    - Chair
```

If a max run is evidence-risky, replace `Chair` as an independent first-pass
lane with `EvidenceSkeptic`, then run chair synthesis after lane outputs are
collected.

## Synthesis Rule

```text
synthesize_brainstorm(lane_outputs, output_contract)
  -> exploration_note that preserves best ideas, dissent, evidence gaps,
     accepted tradeoff, recommendation, and next owner
```

Do not use majority vote. Choose the recommendation with the best argument
quality, evidence fit, local surface fit, and speed to useful learning.
