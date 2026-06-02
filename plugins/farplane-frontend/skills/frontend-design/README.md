# Frontend Design

## Purpose

Guide agents through app-UI implementation with shadcn, AI Elements, registries, and theming once the product workflow and visual direction are already chosen.

## Public API / Entrypoints

- `SKILL.md`: main visual implementation contract
- `references/*`: setup, theming, registries, AI Elements, tokens, and component state patterns
- `AGENTS.md`: maintenance rules

## Minimal Example

1. Use `frontend-craft` for end-to-end frontend implementation.
2. Use `functional-ui` first if workflow/IA is still open.
3. Use `visual-design` first if taste, typography, color, or layout rhythm is still open.
4. Capture stack facts: packages, Tailwind version, shadcn aliases, registries, and theme status.
5. Read `SKILL.md` for app-UI components, theme, registry, token, and state-matrix guidance.
6. Build the interface.

## How to Test

- Confirm workflow-first requests are routed to `functional-ui`.
- Confirm visual-direction requests are routed to `visual-design`.
- Confirm the skill still provides concrete shadcn/registry guidance.
- Confirm registry/theme guidance uses current shadcn CLI and MCP flows.
- Confirm reusable shared components have a component-state matrix path.
- Confirm end-to-end implementation requests point to `frontend-craft`.
