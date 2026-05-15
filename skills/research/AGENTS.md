# Research Maintenance

## Scope

- `SKILL.md`
- `todos.md`
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

## Do Not

- Recreate public `parity-research` or `gap-analysis` wrapper packages.
- Turn this into a brainstorm surface.
- Turn methods into nested routers.

## Checks

- Each public method name appears in `SKILL.md`.
- `todos.md` links to method anchors and dependency skills using Markdown.
- Live docs reference `research:method` names rather than retired package names.
