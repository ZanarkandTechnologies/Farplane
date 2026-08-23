---
name: brainstorm
version: 0.2.0
description: "Turn early ambiguous intent into option space, first-principles contrast, and candidate directions before requirements are committed."
tier: 2
source: local
capability:
  kind: shortcut
---

# Brainstorm

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] State whether this pass is loose divergence or structured decomposition.
- [ ] For meaningful brainstorms, run the base spine before recommending:
  `objective -> current reality -> first-principles contrast -> candidate
  directions -> recommendation -> next owner`.
- [ ] Use [spine-and-ensemble](references/spine-and-ensemble.md) when the request
  asks for first-principles decomposition, current-vs-ideal redesign,
  PRFAQ/working-backwards thinking, ensemble persona/council
  lanes, or unclear decomposition shape.
- [ ] Inspect supplied or local evidence directly when options need examples or
  a baseline; otherwise name the exact evidence handoff the operator must
  request.
- [ ] If the idea needs a full evidence brief rather than compact grounding,
  note the needed parity, competitor, or source-synthesis evidence for the
  operator.
- [ ] Compare the strongest 3 directions and name one recommended next bet.
- [ ] When `ensemble` is `auto` or `max`, preserve the exploration-note output
  contract and use complete personas from `ensemble.yaml`.
- [ ] Name the next owner in plain text: fuzzy directions need operator-led
  clarification; coherent directions name a requirements-artifact handoff.
- [ ] Do not create tickets or implement code from this skill.
- [ ] For meaningful changes to this shortcut, require an independent review
  before claiming readiness.
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
brainstorm(prompt, objective?, context?, ensemble?: auto | max) -> exploration_note

exploration_note:
  mode: loose_divergence | structured_decomposition
  objective:
  current_reality:
  first_principles_contrast:
  candidate_directions:
  strongest_tradeoffs:
  recommendation:
  chosen_lanes?:
  selected_personas?:
  next_owner: operator clarification | prd | research:* | none
  clarifications_needed:
```

When `ensemble` is present, `brainstorm` still returns `exploration_note`.
`auto` selects three relevant diverse personas and `max` selects all; the
owner skill synthesizes without changing its domain output.

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

- the user is ready to commit to one slice; stop for clarification or use `prd`
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
- load `references/spine-and-ensemble.md` when optional lane choice or
  complete persona prompts matter
- use optional depth lanes only when relevant:
  - why-chain for inherited processes, incentives, or obsolete constraints
  - customer/data/action for operational workflows
  - issue-tree for root causes, workstreams, blind spots, or evidence branches
  - PRFAQ/working-backwards for product bets
  - council critique for high-stakes, bias-prone, or ensemble brainstorms
- compare credible paths and recommend one best next direction
- if the result is still fuzzy after that, stop for operator clarification
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
- chosen lanes and selected personas when structured decomposition or ensemble
  mode is used
- recommended next intake skill
- what would need to be clarified next

## Handoff

- if the user chooses a direction but it is still fuzzy: operator clarification
- if the user chooses a direction and it is already coherent: `prd`
- if the missing piece is evidence: `research:*` with the exact method named
- if the user asks for implementation after a coherent plan: `impl-plan`

This skill should not create tickets or implement code itself.

## Reference Map

- [references/spine-and-ensemble.md](references/spine-and-ensemble.md) - load
  when first-principles decomposition, optional lane choice, or complete
  persona prompts matter.
- [references/palantir-customer-data-action.md](references/palantir-customer-data-action.md) -
  load when the selected optional lane is actor/data/action/write-back.
- [references/mckinsey-issue-tree.md](references/mckinsey-issue-tree.md) -
  load when the selected optional lane is issue-tree decomposition.
- [ensemble.yaml](ensemble.yaml) — load only for `ensemble: auto | max`.
