# Impl Plan Prompt

<!-- Unified ticket-planning prompt. -->

0a. Study `@docs/prd.md`.
0b. Study `@docs/specs/*`, including any `Agent Testability Brief` when present.
0c. Study the active ticket in `@tickets/*`; if none exists, inspect
`@tickets/*`.
0d. Study `@docs/MEMORY.md`.
0e. Study `@docs/TROUBLES.md` if present.
0f. Search the codebase first.

Plan only. Target one selected ticket or one selected capability-sized execution slice.

Rules:

1. First decide whether the selected ticket should stay whole or whether a real boundary justifies a split.
2. If split, name the boundary explicitly: proof surface, reusable foundation, risky migration, external blocker, or real runtime/service boundary.
3. Do not force a split just because the work will span multiple commits.
4. Keep one public planning artifact aligned with the canonical ticket body.
5. Make the ticket skim quickly from the top without inventing a parallel reviewer-versus-implementer document.
6. Keep deeper detail inside the single `Plan` section rather than creating a second execution brief.
7. If the user did not provide a take on a material choice, act like a consultant: compare real options and recommend one.
8. If `--consensus` is active, run Planner -> Architect -> Critic before final handoff.
9. Add appendix detail only if risk or novelty justifies it.
10. Before final handoff, run a plan-quality pass and tighten the plan until it passes.
11. For material, cross-module, or architecture-facing work, add one Mermaid
    delta diagram and an optional numbered data-flow or zoom-in view when the
    file map alone is not enough to make flow, ownership, or typed data path
    legible.
12. Require compact callable seams in `Signature delta` whenever interface shape, ownership boundaries, or changed handlers/files are important to trust.
13. Require `Type Sketch` plus one `Typed flow example` whenever structs, objects, payloads, or stateful data evolve across boundaries and the data path matters to trust.
14. When diagrams are used, follow `skills/diagramming/SKILL.md` plus `docs/specs/diagram-first-conventions.md` for compactness, delta coloring, inline signatures, and anti-bloat rules.
15. If an `Agent Testability Brief` exists, preserve its proof/testability surfaces instead of re-deriving them ad hoc.
16. If the plan still depends on invented entities, storage ownership, or runtime boundaries, stop and use `deep-system-design` first.

Output shape:

- `Summary`
- `Scope`
- `Plan`
  - `Change`
  - `Why`
  - `Before -> After`
  - `Touch`
  - `Inspect`
  - `Signature delta`
  - `Type Sketch`
  - `Typed flow example`
  - `Recommendation`
  - `Options considered`
  - `Blast radius`
  - `Risks`
- optional `Gap Analysis`
- optional `Diagram`
- `Acceptance Criteria`
- `Verification`
- optional `Refs`
- `Evidence`
- `Blockers`

Requirements:

- The ticket body must stay one compact artifact, not `Human` / `Agent`
  sections.
- The recommendation must name the chosen path directly and mention the
  rejected viable paths briefly when a material choice exists.
- `Diagram` is expected for material or cross-module work when the flow,
  ownership, or typed data path is not obvious from the file map alone.
- Use one legend-backed delta diagram instead of separate before/after diagrams
  unless the split is clearly simpler.
- Follow `diagramming` for compact node labels, color/legend use, and
  inline-signature practice.
- `Signature delta` should usually contain 3-7 real seams in the form
  `module / symbol(input): output`.
- `Type Sketch` should name the key structs, records, DTOs, or payload shapes
  using only the fields that matter to the plan.
- `Typed flow example` should walk one representative payload or object through
  the main path using the named types from `Type Sketch`.
- Proof must use concrete checks, not generic test categories.
- If the work is a trivial localized fix, `Type Sketch`, `Typed flow example`,
  and other deeper detail may be intentionally short or omitted.
- `Options considered` must show 3 viable options for material choices, each
  with compact pros, cons, and why it lost.
- `Evidence` should carry plan-review notes:
  - which references were actually used,
  - whether scope is still one coherent build-and-proof loop,
  - whether any proposed split names a real boundary,
  - whether proof/risk are concrete enough,
  - whether the recommendation is actually justified against the listed
    options,
  - whether the diagram-first approval surface is actually useful,
  - whether the signature and type sketches are actually useful,
  - whether the top approval surface stayed concise,
  - any fixes made before handoff.
- End with `Ready: yes/no` in `Evidence` or the result summary.

Do not implement.
