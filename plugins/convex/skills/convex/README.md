# Convex Skill

## Purpose

Guide agents to build and review Convex backends using stable defaults, core safety rules, and focused deep-dive references.

## Public API / Entrypoints

- `SKILL.md`: main entrypoint loaded by the agent.
- `references/*.md`: optional deep references selected from `SKILL.md`.
- `scripts/setup-convex.ts`: applies Convex folder conventions after scaffold.

## Minimal Example

1. Read `SKILL.md` and execute the "Always-Load Core" checklist.
2. Select one deep reference based on task type (for example `references/multiplayer.md`).
3. Implement with Convex best practices and run tests before review.

## How to Test

- Validate that every file link in `SKILL.md` resolves.
- Confirm `SKILL.md` includes first-pass defaults (build order, testing, gotchas).
- Confirm merged references are canonical (no duplicate files for same topic).
