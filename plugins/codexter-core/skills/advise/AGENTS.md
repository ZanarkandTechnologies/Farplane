# Advise Maintenance

## Scope

- `SKILL.md`
- `README.md`
- `AGENTS.md`
- `todos.md`

## Boundaries

- Keep this skill about judgment and recommendation framing, not implementation detail.
- Default to 3 viable options.
- Keep the recommendation explicit and above the fold.

## Conventions

- Treat missing user preference as a guidance gap.
- Compare real options, not cosmetic variants.
- Ground fact-dependent choices through `reference-grounding` or `research:*`.
- End with a direct next step, not an upsell.

## Checks

- Trigger conditions, workflow, guardrails, and output contract exist.
- The skill requires 3 options with pros/cons.
- The skill requires a named recommendation and accepted tradeoff.
- `todos.md` links dependency skills with Markdown links.

## Testing

- Re-read `SKILL.md` once and confirm the contract is usable without other files.
- Confirm the skill never asks the agent to stay neutral when guidance is needed.
