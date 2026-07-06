---
name: brainstorm
version: 0.2.0
description: "Turn early ambiguous intent into option space, first-principles contrast, and candidate directions before requirements are committed."
tier: 2
source: local
eval: eval_task.json
---

# Brainstorm

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] State whether this pass is loose divergence or structured decomposition.
- [ ] For meaningful brainstorms, run the base spine before recommending:
  `objective -> current reality -> first-principles contrast -> candidate
  directions -> recommendation -> next owner`.
- [ ] Use [spine-and-budget](references/spine-and-budget.md) when the request
  asks for first-principles decomposition, current-vs-ideal redesign,
  PRFAQ/working-backwards thinking, plus/max/deep budget, persona/council
  lanes, or unclear decomposition shape.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) when options
  need examples, local baseline, peer norms, or official behavior before they
  are useful.
- [ ] If the idea needs a full evidence brief rather than compact grounding,
  note the needed research method such as `research:parity`,
  `research:competitor`, or `research:source-synthesis` for the caller.
- [ ] Use [advise](../advise/SKILL.md) to compare the strongest 3 directions
  and name one recommended next bet.
- [ ] When a `budget` request is present, preserve the brainstorm output
  contract and use the complete `PersonaPrompt` objects in
  [spine-and-budget](references/spine-and-budget.md) for plus/max/persona
  programs.
- [ ] Name the next owner in plain text: fuzzy directions go to
  `deep-interview`; coherent requirements-ready directions go to `prd`.
- [ ] Do not create tickets or implement code from this skill.
- [ ] Run the [review protocol](../review/SKILL.md) after meaningful
  brainstorm-skill, intake-contract, or public-doc changes.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Context

Use this when the user wants to explore possibilities before locking a product
direction. The same public intake surface handles lightweight option
exploration and structured decomposition; do not split first-principles
decomposition into a second public skill.

`brainstorm` should not merely choose a named framework. For meaningful
brainstorms, it contrasts current reality with what would be rebuilt from first
principles, then recommends the most useful next direction or owner.

## Skill Signature

```text
brainstorm(prompt, objective?, context?, budget?) -> exploration_note

exploration_note:
  mode: loose_divergence | structured_decomposition
  objective:
  current_reality:
  first_principles_contrast:
  candidate_directions:
  strongest_tradeoffs:
  recommendation:
  chosen_lanes?:
  next_owner: deep-interview | prd | research:* | advise | none
  clarifications_needed:
```

When `budget` is present, `brainstorm` still returns `exploration_note`.
`budget-advisor` only resolves the base/plus/max execution program; it does not
own brainstorm's domain logic or output shape.

## Job

1. Expand plausible directions when the problem still needs divergence.
2. Run the base spine for meaningful brainstorms so inherited process and
   first-principles rebuild are both visible.
3. Add optional depth lanes only when they reduce uncertainty or expose useful
   contrast.
4. Expose tradeoffs, not implementation details.
5. Recommend the best next direction or owner.
6. Stop before pretending the idea is ready for tickets.

## Use When

- the user wants options, not commitment
- the product direction is still fuzzy
- multiple valid first-slice shapes exist
- the user wants to think before writing a PRD
- the user wants a current-vs-ideal, first-principles, or executive-style
  decomposition
- the user wants one public intake surface that can handle both loose ideation
  and structured decomposition

## Do Not Use When

- the user is ready to commit to one slice; use `deep-interview` or `prd`
- the request is already concrete enough for ticket planning
- the user wants code now

## Process

- identify whether the problem needs loose divergence or structured
  decomposition
- for meaningful brainstorms, run the base spine:
  - objective
  - current reality
  - first-principles contrast
  - candidate directions
  - recommendation
  - next owner
- propose 2-4 distinct directions unless the structure naturally produces one
  decisive recommendation
- use `reference-grounding` when useful options need examples, local baseline,
  peer norms, or official behavior before comparison
- use `research:parity`, `research:competitor`, or
  `research:source-synthesis` when compact grounding is not enough
- load `references/spine-and-budget.md` when optional lane choice, budget
  mapping, or complete persona prompts matter
- use optional depth lanes only when relevant:
  - why-chain for inherited processes, incentives, or obsolete constraints
  - customer/data/action for operational workflows
  - issue-tree for root causes, workstreams, blind spots, or evidence branches
  - PRFAQ/working-backwards for product bets
  - council critique for high-stakes, bias-prone, or budgeted brainstorms
- use `advise` to recommend one best next direction when there are multiple
  credible paths
- if the result is still fuzzy after that, hand off to `deep-interview`
- if the result is coherent enough for requirements writing, hand off to `prd`

## Output

Produce a short exploration note with:

- mode: loose divergence or structured decomposition
- objective
- current reality
- first-principles contrast
- candidate directions
- strongest tradeoffs
- recommended first bet or decomposition shape
- chosen lanes when structured decomposition or budget is used
- recommended next intake skill
- what would need to be clarified next

## Handoff

- if the user chooses a direction but it is still fuzzy: `deep-interview`
- if the user chooses a direction and it is already coherent: `prd`
- if the missing piece is evidence: `research:*` with the exact method named
- if the user asks for implementation after a coherent plan: `impl-plan`

This skill should not create tickets or implement code itself.

## Reference Map

- [references/spine-and-budget.md](references/spine-and-budget.md) - load when
  first-principles decomposition, optional lane choice, budget mapping, or
  complete persona prompts matter.
- [references/palantir-customer-data-action.md](references/palantir-customer-data-action.md) -
  load when the selected optional lane is actor/data/action/write-back.
- [references/mckinsey-issue-tree.md](references/mckinsey-issue-tree.md) -
  load when the selected optional lane is issue-tree decomposition.
- [../budget-advisor/SKILL.md](../budget-advisor/SKILL.md) - use when a
  caller supplies a concrete `budget` request and the brainstorm needs a
  base/plus/max program; budget-advisor resolves the program and does not own
  brainstorm's output contract.
