# Research Maintenance

## Scope

- `SKILL.md`
- `SKILL.md` Todo List
- `README.md`
- `AGENTS.md`

## Boundaries

- Keep this as the Tier 2 evidence workflow.
- Keep `reference-grounding` as the Tier 1 primitive that research uses for
  baseline, source confidence, and local impact.
- Keep `research:parity` focused on peer norms and convergence.
- Keep `research:gap` focused on local current state versus production
  expectation.
- Keep `research:source-synthesis` evidence-focused; use `best-of-worlds` for
  adopt/adapt/reject/defer synthesis.
- Keep `research:code-patterns` as the only public code-pattern entrypoint and
  preserve its conditional discovery/deep-dive contract in
  `references/code-patterns.md`.

## Do Not

- Recreate public `parity-research`, `gap-analysis`, or `external-patterns`
  wrapper packages.
- Turn this into a brainstorm surface.
- Turn methods into nested routers.

## Checks

- Each public method name appears in `SKILL.md`.
- `SKILL.md` Todo List links to method anchors and dependency skills using Markdown.
- Live docs reference `research:method` names rather than retired package names.
