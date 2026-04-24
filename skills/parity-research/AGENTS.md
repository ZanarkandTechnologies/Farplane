# Parity Research Skill Maintenance

## Scope

- `SKILL.md`
- `README.md`
- `AGENTS.md`

## Boundaries

- Keep `parity-research` focused on external comparables: products, standards,
  official docs, and open-source repos.
- Do not collapse local repo scoping into this skill; that belongs in
  `gap-analysis`.
- Do not absorb runtime investigation; root-cause work belongs in
  `runtime-debugging`.
- Route workflow-choice questions to `functional-ui` once parity evidence is
  collected.

## Conventions

- Start with a short local baseline so external research stays anchored.
- Search broad first, then deep-dive the best sources rather than wandering
  through many repos shallowly.
- Prefer literal implementation-pattern searches for code parity.
- Keep the final artifact compact and decision-oriented instead of ending on
  raw notes.
- When naming a parity target, separate shared must-haves from nice-to-have
  extras.

## Checks

- `SKILL.md` still includes trigger conditions, workflow, decision branches,
  gotchas, and an outcome contract.
- The boundary with `gap-analysis`, `runtime-debugging`, and `functional-ui`
  remains explicit.
- Tool guidance still prefers primary sources and real implementations.
- The README example still shows repo-first framing followed by external
  comparison.

## Testing

- Re-read `SKILL.md` and confirm an agent can execute it without opening other
  files.
- Confirm the workflow still ends with a parity boundary and recommended
  follow-up surface.
- Confirm the skill still avoids turning screenshots or marketing pages into
  evidence.
