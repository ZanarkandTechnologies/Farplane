# Impl Plan Prompt

<!--
Unified ticket-planning prompt.
Keep the top of the ticket skimmable for a human reviewer and keep execution
detail lower for the implementing agent.
-->

0a. Study `@docs/prd.md`.
0b. Study `@docs/specs/*`, including any `Agent Testability Brief` when present.
0c. Study the active ticket in `@tickets/*`; if none exists, inspect
`@tickets/*`.
0d. Study `@docs/MEMORY.md`.
0e. Study `@docs/TROUBLES.md` if present.
0f. Search the codebase first.

Plan only. Target one selected ticket or one selected next-commit slice.

Rules:

1. First decide: `one commit` or `split`.
2. If split, stop and ask before planning deeper.
3. Keep one public planning artifact; do not create a second execution brief.
4. Write the plan in two lanes: `Human` first, `Agent` second.
5. The `Human` lane should let a reviewer approve or reject quickly.
6. The `Agent` lane should remove implementation ambiguity without bloating the
   top of the ticket.
7. If the user did not provide a take on a material choice, act like a
   consultant: compare real options and recommend one.
8. If `--consensus` is active, run Planner -> Architect -> Critic before final
   handoff.
9. Add appendix detail only if risk or novelty justifies it, but always include
   the options appendix for material choices.
10. Before final handoff, run a plan-quality pass and tighten the plan until it
    passes.
11. For material, cross-module, or architecture-facing work, lead with one
    Mermaid delta diagram and an optional numbered data-flow or zoom-in view.
12. Add a compact `Signature Sketch` near the top whenever interface shape,
    ownership boundaries, or changed handlers/files are important to trust.
13. When diagrams are used, follow `skills/diagramming/SKILL.md` plus
    `docs/specs/diagram-first-conventions.md` for compactness, delta coloring,
    inline signatures, and anti-bloat rules.
14. If an `Agent Testability Brief` exists, preserve its proof/testability
    surfaces instead of re-deriving them ad hoc.
15. If the plan still depends on invented entities, storage ownership, or
    runtime boundaries, stop and use `deep-system-design` first.

Output shape:

- `Human`
  - `Decision`
    - `Req`
    - `Best`
    - `Why`
    - `Tradeoff accepted`
    - `Not chosen`
  - `Diagram`
    - `Tier 1` top-level delta diagram
    - `Legend`
    - optional `Tier 2` zoom-in or numbered data flow
  - `Signature Sketch`
  - `B -> A`
  - `Proof`
  - `Ask`
- `Agent`
  - `Delta`
  - `Execution Plan`
  - `Risk / Rollback`
  - `Plan Review`
  - `Delegation`
  - `Ticket Move`
  - optional narrative sections only when the applicability rule requires them
  - `Options Appendix` for material choices

Requirements:

- `Human` must come first.
- `Decision` must name the chosen path directly and mention the rejected viable
  paths briefly.
- `Diagram` is required for material or cross-module work.
- Use one legend-backed delta diagram instead of separate before/after diagrams
  unless the split is clearly simpler.
- Follow `diagramming` for compact node labels, color/legend use, and
  inline-signature practice.
- `Signature Sketch` should usually contain 3-7 real seams in the form
  `module / symbol(input): output`.
- `B -> A` must appear near the top.
- Proof must use concrete checks, not generic test categories.
- `Execution Plan` should prefer a compact numbered Mermaid data-flow diagram
  for material work and use short steps or pseudocode only when that is clearer.
- Narrative sections must be concrete and distinct from `Summary` and `Scope`.
- If the work is a trivial localized fix, the narrative sections may be
  intentionally short or omitted.
- `Options Appendix` must show 3 viable options for material choices, each with
  pros, cons, and `Why not chosen`.
- `Plan Review` must state:
  - which references were actually used,
  - whether scope is still one commit,
  - whether proof/risk/rollback are concrete enough,
  - whether the recommendation is actually justified against the listed
    options,
  - whether the diagram-first approval surface is actually useful,
  - whether the signature sketch is actually useful,
  - whether the top approval surface stayed concise,
  - any fixes made before handoff.
- `Delegation: Not needed` unless justified.
- If delegation is used, include:
  - exact ticket file path
  - delegated agent/skill
  - short task note
  - expected artifact
  - required write-back section in the ticket
- End with `Ready: yes/no`.
- Include `Ticket Move`:
  - which `status` / `phase` the ticket should have after planning,
  - whether any follow-up tickets should be spawned,
  - whether the ticket stays in `status: review` or is ready for
    `status: building`.

Do not implement.
