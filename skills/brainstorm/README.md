# Brainstorm

## Purpose

Guide agents through lightweight option exploration and route them to a more
structured branch when loose ideation is no longer enough, without forcing the
user to switch to a second public intake skill.

## Public API / Entrypoints

- `SKILL.md`: main brainstorm workflow
- `AGENTS.md`: maintenance rules
- `references/palantir-customer-data-action.md`: customer/data/action decomposition lens
- `references/mckinsey-issue-tree.md`: structured issue-tree lens

## Minimal Example

1. Compare 2-4 viable directions.
2. If the problem needs structure, switch into decomposition mode inside `brainstorm`.
3. Apply the best-fit lens.
4. Recommend one best next bet or decomposition shape.
5. Hand off to `deep-interview` or `prd`.

## How To Test

- confirm the skill still compares options when divergence is needed
- confirm it can also handle structured customer/data/system decomposition inside the same public surface
- confirm it ends with one recommended next skill or artifact
