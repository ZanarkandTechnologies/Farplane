---
name: brainstorm
version: 0.1.0
description: "Early-stage option exploration before requirements commitment."
---

# Brainstorm

Use this when the user wants to explore possibilities before locking a product direction.

## Job

1. Expand the space of plausible directions.
2. Compare a few strong options.
3. Expose tradeoffs, not implementation details.
4. Stop before pretending the idea is ready for tickets.

## Use When

- the user wants options, not commitment
- the product direction is still fuzzy
- multiple valid first-slice shapes exist
- the user wants to think before writing a PRD

## Do Not Use When

- the user is ready to commit to one slice; use `deep-interview` or `prd`
- the request is already concrete enough for ticket planning
- the user wants code now

## Process

- propose 2-4 distinct directions
- compare them on:
  - user value
  - implementation risk
  - speed to first lovable slice
  - dependency cost
- recommend one best next direction
- if the user converges, hand off to `deep-interview` or `prd`

## Output

Produce a short exploration note with:

- candidate directions
- strongest tradeoffs
- recommended first bet
- what would need to be clarified next

## Handoff

- if the user chooses a direction but it is still fuzzy: `deep-interview`
- if the user chooses a direction and it is already coherent: `prd`

This skill should not create tickets or implement code itself.
