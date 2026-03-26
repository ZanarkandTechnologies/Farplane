---
name: prd
version: 1.0.0
description: "Phase-1 Ralph skill for requirements gathering and PRD authoring."
---

# PRD Skill

Use this as the first session in the Ralph workflow.

## Job

1. Gather requirements through focused conversation.
2. Produce a detailed PRD with JTBD and constraints.
3. Save/update `docs/prd.md`.
4. Stop after PRD authoring. Do not create tickets here.

## Process

- Ask 6-10 high-signal questions (audience, JTBD, slice, non-goals, constraints, risks).
- Keep questions tied to implementation decisions.
- Confirm the first SLC slice boundary.
- Before handoff, read `references/review.md` and tighten the PRD until it passes those checks.

## Output

- Primary file: `docs/prd.md`
- Use template: `references/prd-template.md`
- Discovery guide: `references/requirements-discovery.md`
- Review guide: `references/review.md`

## Handoff

After PRD is accepted, run `spec-to-ticket` for slice decomposition into raw ticket files under `tickets/todo/`.
