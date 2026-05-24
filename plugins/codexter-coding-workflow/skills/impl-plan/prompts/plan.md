# Impl Plan Prompt

<!-- Unified ticket-planning prompt. -->

0a. Study `@docs/prd.md`.
0b. Study `@docs/specs/*`, including any `Agent Testability Brief` when present.
0c. Study the active ticket in `@tickets/*`; if none exists, inspect
`@tickets/*`.
0d. Study `@docs/MEMORY.md`.
0e. Study `@docs/TROUBLES.md` if present.
0f. Search the codebase first.

Plan only. Target one selected ticket.
If `spec-to-ticket` or equivalent planning already produced modular tickets,
assume the selected ticket is the planning boundary by default.

Rules:

1. First decide whether the selected ticket should stay whole or whether a real boundary justifies a split. Default to keeping the whole ticket.
2. If split, name the boundary explicitly: proof surface, reusable foundation, risky migration, external blocker, or real runtime/service boundary.
3. Do not force a split just because the work will span multiple commits, feels safer, or could be shipped incrementally.
4. Do not rewrite the selected ticket into a smaller "first slice" unless the ticket itself declares phased delivery or a real blocker forces it.
5. Keep one public planning artifact aligned with the canonical ticket body.
6. Make the ticket skim quickly from the top without inventing a parallel reviewer-versus-implementer document.
7. Keep deeper detail inside the single `Plan` section rather than creating a second execution brief.
8. If the user did not provide a take on a material choice, act like a consultant: compare real options and recommend one decisively.
9. If `--consensus` is active, run Planner -> Architect -> Critic before final handoff.
10. Add appendix detail only if risk or novelty justifies it.
11. Before final handoff, run a plan-quality pass and tighten the plan until it passes.
12. For material, cross-module, or architecture-facing work, add one Mermaid
    delta diagram and an optional numbered data-flow or zoom-in view when the
    file map alone is not enough to make flow, ownership, or typed data path
    legible.
13. Require explicit callable seams in `Signature delta` whenever interface shape, ownership boundaries, or changed handlers/files are important to trust.
14. Require `Type Sketch` plus one `Typed flow example` whenever structs, objects, payloads, or stateful data evolve across boundaries and the data path matters to trust.
15. Require `Execution steps` whenever the implementation has more than one non-trivial step.
16. Use decisive action language. Do not hedge core execution steps or the recommendation with "maybe", "might", or "could".
17. When diagrams are used, follow `skills/diagramming/SKILL.md` plus `docs/specs/diagram-first-conventions.md` for compactness, delta coloring, inline signatures, and anti-bloat rules.
18. If an `Agent Testability Brief` exists, preserve its proof/testability surfaces instead of re-deriving them ad hoc.
19. For material tickets, write a `Proof Contract` that separates mechanical
    metrics, review rubric gates, and required evidence. Use `Metrics: none
    mechanical` rather than inventing fake metrics.
20. If the plan still depends on invented entities, storage ownership, or runtime boundaries, stop and use `deep-system-design` first.

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
  - `Execution steps`
  - `Recommendation`
  - `Options considered`
  - `Blast radius`
  - `Risks`
- optional `Gap Analysis`
- optional `Diagram`
- `Acceptance Criteria`
- `Verification`
- `Proof Contract`
- optional `Refs`
- `Evidence`
- `Blockers`

Requirements:

- The ticket body must stay one artifact, not `Human` / `Agent`
  sections.
- The plan should solve the full selected ticket's acceptance criteria unless
  the ticket itself declares phased delivery or a real blocker forces narrower
  scope.
- `Execution steps` should give a builder an explicit ordered path, not just a
  list of topics.
- The recommendation must name the chosen path directly and mention the
  rejected viable paths briefly when a material choice exists.
- The recommendation and execution steps should use strong action language, not
  timid caveats.
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
- `Proof Contract` must name the metric or `none mechanical`, review rubrics
  and thresholds, hard gates, required evidence, and optional autoresearch
  session path.
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
  - whether the top surface stayed skimmable without becoming thin,
  - whether `Execution steps` are explicit enough to build from,
  - whether the tone is decisive and action-oriented,
  - any fixes made before handoff.
- End with `Ready: yes/no` in `Evidence` or the result summary.

Do not implement.
