# Functional UI Maintenance

## Scope

- `SKILL.md`
- `README.md`
- `AGENTS.md`
- `references/*`

## Boundaries

- Keep this skill about workflow, IA, current UI diagnosis, comparable examples, states, and interaction models.
- Leave visual styling and taste to `visual-design`.
- Leave ticket composition and implementation sequencing to `impl-plan`.
- Keep comparisons grounded in user stories and adjacent products.

## Conventions

- Lead with users and jobs-to-be-done.
- For broken UI requests, diagnose the current surface before proposing a redesign.
- Compare 3 viable UI options.
- Recommend one pattern clearly.

## Checks

- Trigger conditions, workflow, guardrails, and output contract exist.
- The workflow requires user stories, comparable apps, and a recommendation.
- The skill returns accepted UX context to `impl-plan`; it does not route or
  implement a frontend itself.

## Testing

- Re-read `SKILL.md` once and confirm it is actionable without extra files.
- Confirm the skill does not drift into aesthetics-first advice.
