---
name: deliberative-advice
description: "Turn a high-stakes decision into a budgeted advise council preset with independent perspectives, dissent, and one recommended path."
tier: 2
source: local
capability:
  kind: shortcut
template_uses:
  skill-template: "0.3.2"
  skill-eval-task: "0.2.0"
eval: evals/evals.json
methods:
  - id: deliberative-advice:complex
    class: internal
    output: budgeted-advice-program
  - id: deliberative-advice:council
    class: internal
    output: council-decision-note
allowed-tools: Read, Glob, Grep

---

# Deliberative Advice

## Context

This is the named council preset for the simple advice shortcut. Use it when a
decision is costly, durable, cross-functional, strategically important, or
likely to benefit from independent critique before synthesis.

This skill owns one self-contained fixed council preset and its context-packet
guardrails while preserving the base advice output contract. Use the simple
advice shortcut for normal reversible choices only when the operator explicitly
invokes it.

## Skill Signature

```text
deliberative_advice(decision, stakes?, context_ref?, budget_override?)
  -> budgeted_advise_program + recommendation_contract + dissent_contract
state: reads(context_ref?, evidence refs, relevant files); writes(council_context_packet? or decision note?)
gates: decision_named; council_budget_resolved; independent_first_pass_required; dissent_preserved; next_owner_named
routes: operator-visible evidence handoff | independent review
fails: standalone council reimplementation; thin perspective labels; majority vote; recommendation without next owner
```

Hardcoded council preset:

```text
CouncilBudgetPreset = {
  base_skill: "advise",
  mode: "max",
  persona_count: 5,
  synthesis: "synthesize",
  independence: "first_pass_before_critique",
  personas: [
    OperatorValue,
    EngineeringRisk,
    EvidenceSkeptic,
    SystemsFit,
    Chair
  ],
  require_grounding_check: true,
  preserve_dissent: true,
  require_tradeoff: true,
  require_next_owner: true,
  delegate_budget: {}
}
```

`budget_override` may narrow persona count or evidence depth, but it must not
remove first-pass independence, dissent preservation, the base reviewed path, or
the final advice output contract. Child skills use their own base reviewed
path unless `delegate_budget` explicitly names them.

## Phase Boundary

This skill follows Tier 0 phases inline and resolves its fixed council program
locally. Require independent judgment when the final decision note is material;
do not call another planning or advice wrapper at the same scope.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. State the decision, stakes, default path, and why a simple advice pass
  is too shallow for this call.
- [ ] 2. Ground the decision frame.
  - [ ] Use supplied or local evidence when enough.
  - [ ] Inspect supplied or local evidence directly when enough.
  - [ ] Name the exact evidence handoff the operator must request when
    multi-source evidence could change the recommendation.
- [ ] 3. Create or identify `context_ref` when prior discussion, options,
  evidence, constraints, or file state matter.
  - [ ] If no context packet is needed, record why the decision is self-contained.
  - [ ] If council mechanics need detail, load
    [llm-council-model](references/llm-council-model.md).
- [ ] 4. Resolve the hardcoded council preset inline using the base advice
  output contract.
  - [ ] Include the five complete persona prompts from `## Templates`.
  - [ ] Preserve the base advice output: 3 viable options when real, one
    recommendation, accepted tradeoff, and next step.
- [ ] 5. Execute or hand off the fixed Council Program.
  - [ ] Collect independent first-pass recommendations before critique.
  - [ ] Use critique to strengthen synthesis, not to run a majority vote.
- [ ] 6. Produce the final decision note.
  - [ ] Include recommendation, strongest dissent, confidence, accepted
    tradeoff, next owner, and proof or evidence gap.
- [ ] 7. Finish-check the result.
  - [ ] The fixed preset was used without adding ad hoc personas or modes.
  - [ ] The final answer preserved meaningful dissent.
  - [ ] The next owner or owning skill is concrete.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Fixed Council Program:

```text
council_program(
  decision,
  stakes,
  context_ref?,
  preset = CouncilBudgetPreset
) -> independent_first_passes + critique + chair_synthesis
```

Default persona prompts:

```text
OperatorValue = {
  name: "Operator value",
  prompt: "Optimize for the operator's goal, taste, leverage, time, money, reputation, and workflow. Prefer the path that makes future work easier without adding ceremony for its own sake.",
  focus: ["operator value", "opportunity cost", "momentum", "taste"],
  avoid: ["abstract process without a user-visible payoff"],
  output_shape: "Recommended option, operator-facing upside, accepted tradeoff, next owner"
}

EngineeringRisk = {
  name: "Engineering risk",
  prompt: "Evaluate implementation, maintenance, migration, integration, proof, and rollback risk. Prefer the smallest durable surface that can be verified.",
  focus: ["blast radius", "maintenance", "proof", "rollback"],
  avoid: ["generic caution with no concrete failure mode"],
  output_shape: "Recommended option, failure mode, proof needed, next owner"
}

EvidenceSkeptic = {
  name: "Evidence skeptic",
  prompt: "Identify unsupported claims, stale facts, missing local evidence, current-behavior gaps, and assumptions that could reverse the recommendation.",
  focus: ["evidence gaps", "stale assumptions", "falsification"],
  avoid: ["confidence without named evidence"],
  output_shape: "Recommended option, weakest assumption, evidence that would change the answer"
}

SystemsFit = {
  name: "Systems fit",
  prompt: "Judge which Farplane surface should own the change and whether the proposal duplicates existing skills, docs, hooks, tickets, or hidden state.",
  focus: ["surface ownership", "composition", "duplication", "state"],
  avoid: ["moving policy into the wrong layer"],
  output_shape: "Recommended owner surface, integration risk, smallest next step"
}

Chair = {
  name: "Chair",
  prompt: "Synthesize the strongest arguments into one recommendation. Preserve meaningful dissent, name uncertainty, state the accepted tradeoff, and assign the next owner.",
  focus: ["synthesis", "dissent", "tradeoff", "next owner"],
  avoid: ["majority vote", "neutral menu"],
  output_shape: "Decision note with recommendation, dissent, confidence, tradeoff, next owner"
}
```

Council decision note:

```text
Decision:
Stakes:
Grounding:
Budget Program:
Options:
Recommendation:
Dissent:
Tradeoff accepted:
Confidence:
Next owner:
Proof / evidence gap:
```

## Gotchas

- Do not use this to delay a simple reversible action.
- Do not run role theater with thin labels; use the complete persona prompts.
- Do not let the council become a majority vote. The chair synthesizes argument
  quality, evidence, local fit, dissent, and risk.
- Do not remove the base advice output contract from budgeted execution.

## Reference Map

- Preserve the base advice output contract without implicitly invoking its
  shortcut package.
- [references/llm-council-model.md](references/llm-council-model.md) - read
  when context-packet shape, independent-answer mechanics, or critique/ranking
  details matter.
- Inspect compact evidence directly before executing the council. When
  multi-source evidence or independent review is required, return that exact
  operator-visible handoff need.

## Output

Return or write a compact council decision note plus the resolved Budget
Program reference. The final recommendation must preserve the base advice
contract while adding dissent, confidence, and next owner.
