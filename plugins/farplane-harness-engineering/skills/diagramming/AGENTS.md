# Diagramming Maintenance

## Scope

- `SKILL.md`
- `README.md`
- `SKILL.md` Important Checklist
- `references/patterns.md`
- `references/review.md`

## Boundaries

- Keep this skill about system-design diagrams, not visual illustration.
- Keep Mermaid-first output as the default.
- Keep the skill compact; detailed patterns belong in references.
- Align with `docs/specs/diagram-first-conventions.md` when updating the repo.

## Conventions

- Lead with one top-level delta map.
- Only add one second diagram unless the user explicitly asks for depth.
- Prefer inline signatures over detached signature lists when the interface is
  the point.
- Prefer one legend-backed delta diagram over separate before/after diagrams.

## Checks

- Trigger conditions, workflow, branches, guardrails, and outcome contract exist.
- `references/patterns.md` adds concrete shapes instead of duplicating `SKILL.md`.
- `references/review.md` can catch diagram bloat and decorative Mermaid.

## Testing

- Re-read `SKILL.md` once and confirm it is executable without opening refs.
- Confirm the references add pattern depth rather than a second conflicting
  workflow.
- Confirm the default output shape stays compact.
