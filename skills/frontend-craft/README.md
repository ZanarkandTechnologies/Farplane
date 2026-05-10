# Frontend Craft

## Purpose

Main frontend implementation orchestrator for Codexter.

## Public API / Entrypoints

- `SKILL.md`: routing and implementation workflow
- `references/*`: motion, assets, experimental rendering, QA, and upstream-source map

## Minimal Example

1. Classify the frontend surface.
2. Use `functional-ui` when workflow or behavior is unsettled.
3. Use `visual-design` for the look and taste brief.
4. Use `landing-page` for marketing/scrolltelling pages.
5. Capture stack facts: packages, Tailwind, shadcn, registries, aliases, and theme status.
6. Build with the repo's implementation patterns and verify.

## How to Test

- Re-read `SKILL.md` and confirm it can route a dashboard, broken component, landing page, and generated-asset request.
- Run `python3 skills/skill-creator/scripts/quick_validate.py skills/frontend-craft`.
