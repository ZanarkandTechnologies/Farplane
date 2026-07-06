# Brainstorm

## Purpose

Guide agents through lightweight option exploration or spine-first structured
decomposition without forcing the user to switch to a second public intake
skill.

## Public API / Entrypoints

- `SKILL.md`: main brainstorm workflow
- `AGENTS.md`: maintenance rules
- `SKILL.md` Todo List: Tier 2 intake checklist
- `references/spine-and-budget.md`: first-principles spine, optional depth
  lanes, budget mapping, and complete brainstorm persona prompts
- `references/palantir-customer-data-action.md`: customer/data/action decomposition lens
- `references/mckinsey-issue-tree.md`: structured issue-tree lens

## Minimal Example

1. Decide whether the request needs loose divergence or structured
   decomposition.
2. For meaningful brainstorms, run the base spine: objective, current reality,
   first-principles contrast, candidate directions, recommendation, and next
   owner.
3. Add optional lanes only when they reduce uncertainty: why-chain,
   customer/data/action, issue-tree, working-backwards, or council critique.
4. When `budget` is present, route plus/max persona programs through
   `budget-advisor` using `references/spine-and-budget.md`.
5. Recommend one best next bet or decomposition shape.
6. Hand off to `deep-interview`, `prd`, `research:*`, or `impl-plan` as
   appropriate.

## How To Test

- confirm the skill still compares options when divergence is needed
- confirm base mode runs the spine without unnecessary council machinery
- confirm example-dependent brainstorms ground options through
  `reference-grounding` or `research:*`
- confirm it can handle structured current-vs-ideal and first-principles
  decomposition inside the same public surface
- confirm plus/max budget routes preserve the brainstorm output contract and
  use complete behavioral persona prompts rather than public-figure cosplay
- confirm it ends with one recommended next skill or artifact
