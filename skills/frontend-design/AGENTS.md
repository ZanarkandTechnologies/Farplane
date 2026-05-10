# Frontend Design Maintenance

## Scope

- `SKILL.md`
- `README.md`
- `AGENTS.md`
- `references/*`

## Boundaries

- `frontend-craft` owns end-to-end frontend implementation orchestration.
- `functional-ui` owns user stories, comparable apps, current UI diagnosis, and workflow recommendations.
- `visual-design` owns taste, typography, color, layout rhythm, and visual-system choices.
- `frontend-design` owns app-UI implementation references, theming, component sourcing, and interaction polish after workflow and look are chosen.
- `landing-page` owns one-page marketing, launch, and scrolltelling surfaces.

## Conventions

- Route workflow-first product decisions to `functional-ui`.
- Route visual-system and taste decisions to `visual-design`.
- Route end-to-end implementation to `frontend-craft`.
- Keep the aesthetic guidance distinctive and implementation-oriented.
- Do not drift into generic UX strategy here.
- Keep shadcn guidance current with official CLI/MCP behavior, including
  registry index discovery, `search`, `view`, `docs`, `apply`, and `preset`.
- Reusable components need a component-state matrix when they become local
  primitives. See `MEM-0085`.

## Checks

- The skill tells agents to use `functional-ui` when the workflow is unsettled.
- The skill tells agents to use `visual-design` when the look is unsettled.
- References still support implementation and theming.
- References cover registry/theme discovery and component-state proof.
- Related-skills boundaries stay explicit.

## Testing

- Re-read `SKILL.md` once and confirm the boundary with `functional-ui` is obvious.
- Confirm the quick-reference table points workflow/IA requests to `functional-ui`, taste requests to `visual-design`, landing pages to `landing-page`, and end-to-end implementation to `frontend-craft`.
