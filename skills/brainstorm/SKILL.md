---
name: brainstorm
version: 0.1.0
description: "Early-stage option exploration before requirements commitment."
---

# Brainstorm

Use this when the user wants to explore possibilities before locking a product direction, including cases where the same public intake surface should shift from lightweight option exploration into more structured decomposition.

## Job

1. Expand the space of plausible directions when the problem still needs divergence.
2. Switch into structured decomposition when the problem needs customer/data/workflow/system thinking.
3. Expose tradeoffs, not implementation details.
4. Recommend the best next direction or lens.
5. Stop before pretending the idea is ready for tickets.

## Use When

- the user wants options, not commitment
- the product direction is still fuzzy
- multiple valid first-slice shapes exist
- the user wants to think before writing a PRD
- the user wants one public intake surface that can handle both loose ideation and structured decomposition

## Do Not Use When

- the user is ready to commit to one slice; use `deep-interview` or `prd`
- the request is already concrete enough for ticket planning
- the user wants code now

## Process

- propose 2-4 distinct directions
- use `reference-grounding` when useful options need examples, local baseline,
  peer norms, or official behavior before comparison
- use `research:parity`, `research:competitor`, or
  `research:source-synthesis` when compact grounding is not enough
- identify whether the problem still needs divergence or whether to switch into structured decomposition mode
- compare them on:
  - user value
  - implementation risk
  - speed to first lovable slice
  - dependency cost
- use `advise` to recommend one best next direction when there are multiple
  credible paths
- when structure is needed, use one explicit lens inside `brainstorm`:
  - `palantir-customer-data-action` for user/data/action/write-back decomposition
  - `mckinsey-issue-tree` for driver / workstream / root-cause decomposition
- if the result is still fuzzy after that, hand off to `deep-interview`
- if the result is coherent enough for requirements writing, hand off to `prd`

## Output

Produce a short exploration note with:

- candidate directions
- strongest tradeoffs
- recommended first bet or decomposition shape
- chosen lens when structured decomposition is used
- recommended next intake skill
- what would need to be clarified next

## Handoff

- if the user chooses a direction but it is still fuzzy: `deep-interview`
- if the user chooses a direction and it is already coherent: `prd`

This skill should not create tickets or implement code itself.
