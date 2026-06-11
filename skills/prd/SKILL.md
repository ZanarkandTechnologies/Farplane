---
name: prd
version: 1.0.0
description: "Turn product intent into a Phase-1 Farplane PRD with requirements, scope, and handoff shape."
tier: 3
group: coding
source: local
common_chains:
  after: ["spec-to-ticket"]
---

# PRD Skill

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Read the current project surfaces before asking: `docs/prd.md`, active
  ticket, `docs/specs/`, `docs/MEMORY.md`, and `docs/LESSONS.md` when present.
- [ ] Use [research:user-grounding](../research/SKILL.md#researchuser-grounding)
  when audiences, jobs, user stories, contexts, friction, or success criteria
  are not already grounded.
- [ ] Use [research:parity](../research/SKILL.md#researchparity) or
  [research:competitor](../research/SKILL.md#researchcompetitor) when product
  expectations, peer workflows, or market examples should shape the PRD.
- [ ] Use
  [first-principles-planning](../../docs/specs/first-principles-planning.md)
  to reduce the request to objective, need, constraints, assumptions, root
  cause, first viable slice, proof/falsification, tradeoffs, and non-goals.
- [ ] Fill the PRD by section: audience, JTBD, user stories, constraints,
  non-goals, risks, first SLC slice, metric candidates, and autonomy readiness.
- [ ] If `docs/bootstrap-brief.md` has a project profile, load
  [project-profiles](../deep-init-project/references/project-profiles.md) and
  include component matrix, advice axes explored, selected directions,
  prototype gates, and pipeline handoff.
- [ ] Preserve the project lifecycle phase boundary from
  [project-lifecycle](../deep-init-project/references/project-lifecycle.md):
  PRD writes the project spec/brief and first SLC slice; it does not create
  tickets or implement.
- [ ] Keep metric candidates honest: mechanical when possible, `none
  mechanical` when the work is judgment-heavy.
- [ ] Use the PRD references already owned by this skill:
  `references/prd-template.md`, `references/requirements-discovery.md`, and
  `references/review.md`.
- [ ] Use [plan](../plan/SKILL.md) when several PRD shapes or first-slice
  boundaries are viable and the tradeoff needs to be explicit.
- [ ] Stop after PRD authoring and hand off to
  [spec-to-ticket](../spec-to-ticket/SKILL.md) only after the PRD is accepted.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this as the first session in the Farplane workflow.

## Job

1. Gather requirements through focused conversation.
2. Produce a detailed PRD with JTBD, constraints, metric candidates, and
   `Autonomy Readiness`.
3. When a project profile exists, capture component matrices, explored options,
   selected complete directions, prototype gates, and pipeline handoffs.
4. Save/update `docs/prd.md`.
5. Stop after PRD authoring. Do not create tickets here.

## Process

- Ask 6-10 high-signal questions (audience, JTBD, slice, non-goals, constraints, risks).
- Keep questions tied to implementation decisions.
- Use `docs/specs/first-principles-planning.md` to reduce the request to
  objective, user/system need, assumptions, root cause, constraints, first
  viable slice, proof/falsification, tradeoffs, and non-goals.
- Confirm the first SLC slice boundary.
- If `docs/bootstrap-brief.md` names a project profile, use
  `deep-init-project/references/project-profiles.md` to drive PRD questions and
  sections.
- Explore options across the profile's material advice axes, then synthesize
  complete directions before writing implementation-facing requirements.
- Define the smallest prototype or PoC needed to prove the highest-risk
  assumption before full production tickets.
- Define mechanically meaningful product, workflow, quality, or operational
  metric candidates when they exist. If the work is judgment-heavy, say no
  honest mechanical metric exists instead of inventing one.
- Ask what inputs, assets, credentials, compute, tools, QA surfaces, and human
  gates an agent would need before attempting long-running autonomous work.
- Before handoff, read `references/review.md` and tighten the PRD until it passes those checks.

## Output

- Primary file: `docs/prd.md`
- Use template: `references/prd-template.md`
- Discovery guide: `references/requirements-discovery.md`
- Review guide: `references/review.md`
- Downstream tickets should carry PRD metric candidates into their `Proof
  Contract` only when the metric is honest, mechanical, and useful for the
  selected slice.
- Downstream specs/tickets should carry selected component directions and
  prototype gates forward instead of re-running project discovery.

## Handoff

After PRD is accepted, run `spec-to-ticket` for slice decomposition into raw ticket files under `tickets/`.
