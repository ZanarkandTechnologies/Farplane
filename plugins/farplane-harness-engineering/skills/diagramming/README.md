# Diagramming

## Purpose

Guide agents to turn text-heavy plans, specs, and code explanations into compact
Mermaid system-design diagrams.

## Public API / Entrypoints

- `SKILL.md`: main diagramming contract
- `SKILL.md` Important Checklist: compact anti-forgetting checklist
- [`references/patterns.md`](/Users/kenjipcx/coding-harness/Farplane/skills/diagramming/references/patterns.md)
- [`references/review.md`](/Users/kenjipcx/coding-harness/Farplane/skills/diagramming/references/review.md)
- `AGENTS.md`: maintenance notes

## Minimal Example

1. Read the active request or ticket.
2. Draw one top-level delta map.
3. Add one data-flow or zoom-in diagram only if needed.
4. Embed short signatures where interface shape matters.
5. Return the diagram pack with a short legend and short notes.

## How to Test

- Confirm the skill defaults to one top-level diagram, not many.
- Confirm it prefers one delta map over separate before/after views.
- Confirm inline signatures stay short and useful.
- Confirm the output can be understood before reading long prose.
