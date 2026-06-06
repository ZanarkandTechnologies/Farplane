# Advise Maintenance

## Scope

- `SKILL.md`
- `README.md`
- `AGENTS.md`
- `SKILL.md` Todo List

## Boundaries

- Keep this skill about judgment and recommendation framing, not implementation detail.
- Start recommendation work from first principles before comparing options.
  See `MEM-0119`.
- Default to 3 viable options.
- Keep the recommendation explicit and above the fold.

## Conventions

- Treat missing user preference as a guidance gap.
- Derive criteria and options from objective, need, root cause, constraints,
  assumptions, proof/falsification, tradeoffs, and non-goals.
- Compare real options, not cosmetic variants.
- Ground fact-dependent choices through `reference-grounding` or `research:*`.
- End with a direct next step, not an upsell.

## Checks

- Trigger conditions, workflow, guardrails, and output contract exist.
- The skill requires 3 options with pros/cons.
- The skill requires first-principles basis before option comparison.
- The skill requires a named recommendation and accepted tradeoff.
- `SKILL.md` Todo List links dependency skills with Markdown links.

## Testing

- Re-read `SKILL.md` once and confirm the contract is usable without other files.
- Confirm the skill never asks the agent to stay neutral when guidance is needed.
