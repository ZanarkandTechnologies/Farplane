# Diagramming Maintenance

## Scope

- `SKILL.md`
- `README.md`
- `SKILL.md` Todo List
- `references/patterns.md`
- `references/review.md`

## Boundaries

- Keep this skill about system-design diagrams, not visual illustration.
- Choose the semantic form before the rendering language: Mermaid is preferred
  for standalone system packs, compact ASCII for ticket contracts, and a table
  for mappings or comparisons.
- Keep the skill compact; detailed patterns belong in references.
- Treat `skills/diagramming/SKILL.md` as the owner of Farplane diagram-first
  conventions when updating the repo.

## Conventions

- Lead with the one form that answers the approval question; use a delta map
  only when old-to-new change is the question.
- Only add one second diagram unless the user explicitly asks for depth.
- Prefer inline signatures over detached signature lists when the interface is
  the point.
- Prefer one legend-backed delta diagram over separate before/after diagrams
  when a delta view is needed.

## Checks

- Trigger conditions, workflow, branches, guardrails, and outcome contract exist.
- `references/patterns.md` adds concrete shapes instead of duplicating `SKILL.md`.
- `references/review.md` can catch mismatched forms, diagram bloat, and
  decorative Mermaid.

## Testing

- Re-read `SKILL.md` once and confirm it is executable without opening refs.
- Confirm the references add pattern depth rather than a second conflicting
  workflow.
- Confirm the default output shape stays compact.
