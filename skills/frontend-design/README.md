# Frontend Design

## Purpose

Guide agents to build distinctive production-grade app interfaces once the product workflow is already chosen.

## Public API / Entrypoints

- `SKILL.md`: main visual implementation contract
- `references/*`: setup, theming, registries, and AI Elements patterns
- `AGENTS.md`: maintenance rules

## Minimal Example

1. Use `functional-ui` first if workflow/IA is still open.
2. Read `SKILL.md`.
3. Choose the visual direction, theme, and component sources.
4. Build the interface.

## How to Test

- Confirm workflow-first requests are routed to `functional-ui`.
- Confirm the skill still provides concrete shadcn/registry guidance.
- Confirm the visual guidance stays distinctive.
