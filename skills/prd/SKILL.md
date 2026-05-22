---
name: prd
version: 1.0.0
description: "Phase-1 Codexter skill for requirements gathering and PRD authoring."
tier: 3
group: coding
source: local
common_chains:
  after: ["spec-to-ticket"]
---

# PRD Skill

Use this as the first session in the Codexter workflow.

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
