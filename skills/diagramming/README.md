# Diagramming

## Purpose

Guide agents to turn text-heavy plans, specs, and code explanations into compact
system-design diagrams selected by the reader's approval question.

## Public API / Entrypoints

- `SKILL.md`: main diagramming contract
- `SKILL.md` Todo List: compact anti-forgetting checklist
- [`references/patterns.md`](references/patterns.md)
- [`references/review.md`](references/review.md)
- `AGENTS.md`: maintenance notes

## Minimal Example

1. Read the active request or ticket.
2. Choose a flow, state, boundary/data, trace, wireflow, delta, or table form.
3. Draw one top-level form and add one distinct second view only if needed.
4. Embed short signatures where interface shape matters.
5. Return the diagram pack with a short legend and short notes.

## How to Test

- Confirm the selected form answers the approval question, not a generic default.
- Confirm the skill defaults to one top-level diagram, not many.
- Confirm it uses a delta map only for old-to-new questions.
- Confirm inline signatures stay short and useful.
- Confirm the output can be understood before reading long prose.
