# Gap Analysis Skill Maintenance

## Scope

- `SKILL.md`
- `README.md`
- `AGENTS.md`

## Boundaries

- Keep `gap-analysis` focused on current repo state versus production
  expectation for one feature or ticket slice.
- Do not turn this into the general external-comparables skill; broader
  "what do peers include?" work belongs in `parity-research`.
- Keep runtime/root-cause investigation routed to `runtime-debugging`.
- Keep workflow/IA planning routed to `functional-ui` and architecture ambiguity
  routed to `deep-system-design`.

## Conventions

- Start from the user job and the observed repo limit before pulling in outside
  sources.
- Keep the output compact: `Current state`, `Production expectation`,
  `Missing gaps`, `Comparable implementations`, and `Recommendation`.
- Preserve the now-versus-later scope boundary instead of ending on a raw
  research dump.
- Keep the first-load contract self-sufficient; an agent should be able to run
  the core path from `SKILL.md` alone.

## Checks

- `SKILL.md` still includes triggers, workflow, decision branches, gotchas, and
  an outcome contract.
- The boundary with `parity-research`, `runtime-debugging`, and
  `deep-system-design` remains explicit.
- The README example still matches the actual workflow and output shape.

## Testing

- Re-read `SKILL.md` once and confirm an agent can execute it without opening
  other files.
- Confirm the README example starts from current repo state before external
  comparables.
- Confirm `gap-analysis` still ends by grounding `impl-plan`, not by replacing
  it.
