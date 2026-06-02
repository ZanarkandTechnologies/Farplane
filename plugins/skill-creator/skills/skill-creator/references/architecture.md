# Skill Creator Architecture

Skill creation is workflow design, not documentation dumping.

The durable structure is:

- `SKILL.md`: first-load execution contract
- `references/`: optional deeper guidance loaded on demand
- `scripts/`: deterministic helpers that should not be rewritten each time
- `prompts/`: reusable operator prompts
- `assets/`: output resources

## Core Boundary

Put the shortest successful path in `SKILL.md`. Move only variant-heavy,
verbose, or low-frequency detail into references.

## Stable Local Contracts

Farplane skills are stable local contracts. External skills, repos, blogs, and
command families are research inputs, not live dependencies. Use
`best-of-worlds` to review outside ideas, then import them as `adopt`, `adapt`,
`reject`, or `defer` decisions instead of auto-syncing upstream behavior.

This preserves local coherence while still letting skills learn from better
external implementations. See `MEM-0073`.

## Judgement Questions

Skills should declare judgement questions when the agent must make material
choices about user segment, metric, guard, scope, source credibility, or
adoption versus rejection. Those questions route naturally to `advise`.
