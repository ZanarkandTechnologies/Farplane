---
name: deep-interview
version: 0.1.0
description: "Ambiguity-gated requirements interview before PRD/spec writing."
---

# Deep Interview

Use this when the user has a real goal but the requirements are still too vague for good specs or tickets.

## Job

1. Interview the user one question at a time.
2. Collapse ambiguity into explicit constraints, scope, risks, and first-slice boundaries.
3. Produce a compact, execution-relevant requirements artifact.
4. Stop before implementation.

## Use When

- the user has a messy client transcript, call notes, or broad product idea
- the request has multiple possible scopes or product directions
- acceptance criteria are unclear
- you can feel that jumping straight to `prd` would bake in bad assumptions

## Do Not Use When

- the request is already specific enough for `prd`
- the user wants open-ended ideation without commitment pressure; use `brainstorm`
- the user wants implementation now; use `ralphplan` or `ralph` after specs are ready

## Process

- Ask one high-signal question at a time.
- Prefer questions that change the first SLC slice, acceptance criteria, or technical constraints.
- Keep the interview grounded in product decisions, not generic curiosity.
- Stop once the first slice is clear enough for PRD/spec writing.

Suggested question themes:

- audience / JTBD
- non-goals
- first lovable slice
- trust/safety constraints
- data sources / integrations
- acceptance criteria
- edge cases that would change architecture

## Output

- update `docs/prd.md` if the answers are already coherent enough, or
- write a temporary summary in the current ticket / working notes and hand off to `prd`

The output should contain:

- user / audience
- JTBD
- first SLC slice
- non-goals
- constraints
- open questions that still matter

## Handoff

After the interview:

- run `prd` if the idea is now coherent
- then run `spec-to-ticket`

This skill should not create tickets or implement code itself.
