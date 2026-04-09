# Frontend Design Maintenance

## Scope

- `SKILL.md`
- `README.md`
- `AGENTS.md`
- `references/*`

## Boundaries

- `functional-ui` owns user stories, comparable apps, and workflow recommendations.
- `frontend-design` owns visual execution, theming, component sourcing, and interaction polish after the workflow is chosen.
- `cinematic-landing` owns narrative landing pages.

## Conventions

- Route workflow-first product decisions to `functional-ui`.
- Keep the aesthetic guidance distinctive and implementation-oriented.
- Do not drift into generic UX strategy here.

## Checks

- The skill tells agents to use `functional-ui` when the workflow is unsettled.
- References still support implementation and theming.
- Related-skills boundaries stay explicit.

## Testing

- Re-read `SKILL.md` once and confirm the boundary with `functional-ui` is obvious.
- Confirm the quick-reference table points workflow/IA requests to `functional-ui`.
