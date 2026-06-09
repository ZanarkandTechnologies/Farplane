# Impl Plan Prompt

<!-- Unified ticket-planning prompt. -->

0a. Study `@docs/prd.md`.
0b. Study `@docs/specs/*`, including any `Agent Testability Brief` when present.
0c. Study the active ticket in `@tickets/*`; if none exists, inspect
`@tickets/*`.
0d. Study `@docs/MEMORY.md`.
0e. Study `@docs/TROUBLES.md` and `@docs/LESSONS.md` if present.
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
7. Organize the plan around before/after `Delta`, visual `Map`, ordered `Build Plan`, and concrete `Verification`.
8. If the user did not provide a take on a real material choice, act like a consultant: compare real options and recommend one decisively. Omit options when there is no real fork.
9. If `--consensus` is active, run Planner -> Architect -> Critic before final handoff.
10. Add appendix detail only if risk or novelty justifies it.
11. Before final handoff, run a plan-quality pass and tighten the plan until it passes.
12. For material, cross-module, or architecture-facing work, add one Mermaid
    delta map when it makes flow, ownership, changed seams, or typed data path
    easier to understand visually.
13. Put explicit callable seams inside the `Map` when interface shape,
    ownership boundaries, or changed handlers/files matter to trust. Use
    `module / symbol(input): output` in nodes or edge labels where readable.
14. Put typed data movement inside the `Map` when structs, objects, payloads,
    or state evolve across boundaries. Use numbered edges or compact node
    labels instead of a separate prose example when possible.
15. Add separate `Signature delta`, `Type sketch`, or `Typed flow` fallback
    detail only when the map would become crowded or ambiguous without it.
16. Require `Build Plan` whenever the implementation has more than one non-trivial step.
17. Use decisive action language. Do not hedge core execution steps or the recommendation with "maybe", "might", or "could".
18. When diagrams are used, follow `skills/diagramming/SKILL.md` plus
    `docs/specs/diagram-first-conventions.md` for compactness, delta coloring,
    inline signatures, and anti-bloat rules.
19. If an `Agent Testability Brief` exists, preserve its proof/testability surfaces instead of re-deriving them ad hoc.
20. For material tickets, write a compact `Proof Contract` that separates
    mechanical metrics, caller-declared rubric families, required TAS gates,
    hard gates, and required proof. Use `Metrics: none mechanical` rather than
    inventing fake metrics.
21. Keep execution evidence out of the impl plan unless the user explicitly
    asks for audit detail. Evidence is stored in the ticket after execution.
22. Use citations inline or in a compact `Citations` line only when references
    ground a claim, decision, or external expectation.
23. If the plan still depends on invented entities, storage ownership, or runtime boundaries, stop and use `deep-system-design` first.

Output shape:

- `Summary`
- `Scope`
- `Delta`
  - `Before`
  - `After`
  - `Why now`
  - `First-principles basis` when material
- `Map`
  - Mermaid delta map when visually useful
  - `Touch` / `Inspect`
  - inline signatures when seams matter
  - numbered typed flow when data movement matters
  - optional fallback `Signature delta`, `Type sketch`, or `Typed flow`
- `Build Plan`
  - ordered implementation steps
  - optional `Recommendation`
  - optional `Options considered`
- `Verification`
- `Notes`
  - risks, blast radius, rollback, follow-ups, citations, blockers only when real
- optional `Gap Analysis`
- optional `Acceptance Criteria`
- optional compact `Proof Contract`
- optional `Autonomy Readiness`

Requirements:

- The ticket body must stay one artifact, not `Human` / `Agent`
  sections.
- The plan should solve the full selected ticket's acceptance criteria unless
  the ticket itself declares phased delivery or a real blocker forces narrower
  scope.
- `Build Plan` should give a builder an explicit ordered path, not just a list
  of topics.
- The recommendation must name the chosen path directly when a real decision
  exists.
- The recommendation and build steps should use strong action language, not
  timid caveats.
- `Map` is expected for material or cross-module work when it makes flow,
  ownership, changed seams, or typed data path easier to understand.
- Use one legend-backed delta map instead of separate before/after diagrams
  unless the split is clearly simpler.
- Follow `diagramming` for compact node labels, color/legend use, and
  inline-signature practice.
- Callable seams should appear in the map or a compact fallback list, usually
  3-7 real seams in the form `module / symbol(input): output`.
- Typed data flow should appear in the map or a compact fallback flow using
  only the fields that matter to the plan.
- Proof must use concrete checks, not generic test categories.
- `Proof Contract` should be compact by default: metric or `none mechanical`,
  review rubrics/TAS gates, hard gates, required proof, and optional
  autoresearch session path.
- If the work is a trivial localized fix, `Map`, typed flow, and other deeper
  detail may be intentionally short or omitted.
- `Options considered` must appear only for real material choices, with compact
  pros, cons, and why the chosen path won.
- End with a clear readiness call in `Verification` or `Notes`, not a full
  planning `Evidence` report.
