# Impl Plan Prompt

<!-- Unified ticket-planning prompt. -->

0a. Study `@docs/prd.md`.
0b. Study `@docs/features/FEAT-*.md`, including any `Agent Testability Brief` when present.
0c. Study the active ticket in `@tickets/*`; if none exists, inspect
`@tickets/*`.
0d. Study `@docs/MEMORY.md`.
0e. Study `@docs/TROUBLES.md` and `@docs/LESSONS.md` if present.
0f. Search the codebase first.
0g. Before drafting, identify missing objective, acceptance criteria,
constraints, target files, proof weight, permissions, human gates, and
destructive/deploy/spend boundaries. Ask up to 3 clarifying questions only when
the missing input is blocking or materially changes the plan or Goal Packet;
otherwise record the assumption and continue.

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
7. Organize the plan around brief before/after `Delta`, modular `Change Plan`,
   concrete `Done`, `QA Strategy`, `Docs Strategy`, `Links`, and sparse `Notes`.
8. If the user did not provide a take on a real material choice, act like a consultant: compare real options and recommend one decisively. Omit options when there is no real fork.
9. If `--consensus` is active, run Planner -> Architect -> Critic before final handoff.
10. Add appendix detail only if risk or novelty justifies it.
11. Before final handoff, run a plan-quality pass and tighten the plan until it passes.
11a. Run `skills/impl-plan/qa_checklist.md` for material plans. Revise or
     block when the plan fails minimal required version, reuse before new
     surface, least parameters, function/file necessity, split boundary, or
     architecture-signature, independent-review, or proof-route checks.
     Material plans must declare themselves the minimal implementation plan
     that satisfies the ticket, and every proposed new function, helper,
     service, or module must justify why it cannot live inside an existing
     owner surface.
11b. For Goal-backed work, make the ticket ready for `goal-advisor(ticket)`
     after approval. The human approves the ticket plan first; then
     `goal-advisor` creates or updates `program.md`, `progress.md`, and the
     native `/goal` prompt from the approved ticket.
11c. Include `Docs Strategy` near the end of material plans. Use
     `doc-advisor` to decide `update_docs` with targets and validation or
     `no_docs` with a concrete reason. Do not add `close_ticket` or
     `documentation_skill` fields.
12. Use `Change Plan` units as the merged program and file map. Split the
    section into one heading and one fenced block per coherent change. Each
    material unit should include `fixes`, local before/after, `read`, `write`,
    `operation`, local `signature_or_type_impact`, `routes`, `qa`, and
    real `failure_modes`.
13. For material plans, put compact `architecture_signatures` at the top of
    `Change Plan`: module-level seams, main-flow signatures, relevant typed
    data movement, and the builder-owned freeform boundary. Use
    `not_applicable` only for tiny localized fixes with a concrete reason.
14. Never put Mermaid diagrams inside `ticket.md`. After writing the canonical
    ticket plan, always create and link `tickets/TASK-XXXX/diagrams.md` using
    `skills/impl-plan/references/visual-companion-template.md`. Keep it
    non-blocking with `canonical_contract: ticket.md`; tiny fixes still receive
    a compact separate companion.
15. Put explicit local callable seams inside `signature_or_type_impact` when
    one change unit modifies interface shape, ownership boundaries, or changed
    handlers/files. Use `module / symbol(input): output`.
16. Put typed data movement in `signature_or_type_impact` only when that
    change unit evolves structs, objects, payloads, or state across boundaries.
    Keep it to the fields that matter.
17. Require a compact `Change Plan` whenever the implementation has more than
    one non-trivial step.
18. Use decisive action language. Do not hedge core execution steps or the recommendation with "maybe", "might", or "could".
19. For the required separate diagrams, follow `skills/diagramming/SKILL.md` for
    compactness, delta coloring, inline signatures, and anti-bloat rules.
19a. Do not finish impl-plan until `farplane validate ticket
     tickets/TASK-XXXX/ticket.md --phase planning` passes. The phase API checks
     the ticket and required `diagrams.md`; a link alone is not completion.
20. If an `Agent Testability Brief` exists, preserve its proof/testability surfaces instead of re-deriving them ad hoc.
21. For material tickets, write compact `Done` conditions plus a `QA Strategy`
    that separates proof weight, mechanical checks, manual checks, delegated
    lanes, caller-declared rubric families, required TAS gates, hard gates,
    required evidence, goal-advisor inputs, and residual risk. Use
    `none mechanical` rather than inventing fake metrics.
22. For material plans, request a native reviewer lane before approval-ready
    handoff using `implementation-plan`, `architecture`, and
    `evidence-quality` unless the ticket declares a stronger route. Reconcile
    revise findings in the ticket; block on block/invalid.
23. Keep execution evidence out of the impl plan unless the user explicitly
    asks for audit detail. Evidence is stored in artifacts, `progress.md`, or
    concise ticket `Links` after execution.
24. Use citations inline or in a compact `Citations` line only when references
    ground a claim, decision, or external expectation.
25. If the plan still depends on invented entities, storage ownership, or runtime boundaries, stop and use `deep-system-design` first.

Output shape:

- `Summary`
- `Scope`
- `Delta`
  - `Before`
  - `After`
  - `Why now`
  - `First-principles basis` when material
- `Change Plan`
  - `architecture_signatures` for material plans, or concrete `not_applicable`
  - one heading and fenced block per change
  - `fixes`
  - `before`
  - `after`
  - `read`
  - `write`
  - `operation`
  - `signature_or_type_impact`
  - `routes`
  - `qa`
  - `failure_modes`
- `Done`
  - `done_when`
- `QA Strategy`
  - `proof_weight`
  - `checks`
  - `manual`
  - `delegated_lanes`
  - `review`
  - `evidence`
  - `goal_advisor_inputs`
  - `residual_risk`
- `Docs Strategy`
  - `outcome`
  - `doc_targets`
  - `no_docs_reason`
  - `validation`
- `Links`
  - `visual companion: tickets/TASK-XXXX/diagrams.md`
- `Notes`
  - risks, blast radius, rollback, follow-ups, citations, blockers only when real
- optional `Gap Analysis`
- optional `Agent Contract`
- optional `Run Hints`

Requirements:

- The ticket body must stay one artifact, not `Human` / `Agent`
  sections.
- The plan should solve the full selected ticket's acceptance criteria unless
  the ticket itself declares phased delivery or a real blocker forces narrower
  scope.
- `Change Plan` should give a builder an explicit ordered path, not just a list
  of topics, and should avoid forcing a reader to match files from another
  section.
- Do not use synthetic delta labels by default. Use `fixes:` in each change
  block; add stable anchors only when many-to-many traceability genuinely earns
  the extra notation.
- Goal-backed plans should leave enough ticket structure for
  `goal-advisor(ticket)` to compile `program.md`, `progress.md`, and native
  `/goal` prompt after approval without transcript memory.
- Material plans should include a final `Docs Strategy` so the Goal does not
  silently skip durable docs or invent closeout ceremony.
- The recommendation must name the chosen path directly when a real decision
  exists.
- The recommendation and build steps should use strong action language, not
  timid caveats.
- Every impl-plan output includes a separate, linked `diagrams.md`; diagrams
  never appear inside `ticket.md`.
- Use explicit legend-backed Before and After diagrams in the companion, with
  compact depth for small tickets.
- Follow `diagramming` for compact node labels, color/legend use, and
  inline-signature practice.
- Callable seams should appear in `signature_or_type_impact`, usually 3-7 real
  local seams in the form `module / symbol(input): output`; top-level seams
  belong in `architecture_signatures`.
- Typed data flow should appear in `architecture_signatures` or local
  `signature_or_type_impact` using only the fields that matter to the plan.
- QA Strategy must use concrete checks, not generic test categories.
- New files, functions, parameters, config knobs, routes, or abstractions must
  justify reuse checked, ownership, testability, or blast-radius reduction.
- Material plans must state that they are the minimal implementation plan for
  the selected ticket, and proposed new functions, helpers, services, or modules
  must prove why an existing owner surface cannot carry them.
- `Done` should be compact by default: done conditions only.
- `QA Strategy` should carry metric or `none mechanical`, optional metric-card
  rationale, review rubrics/TAS gates, hard gates, required evidence,
  proof route, final evidence, and final checkpoint.
- If the work is a trivial localized fix, typed flow, system maps, and other
  deeper detail may be intentionally short or omitted.
- `Options considered` must appear only for real material choices, with compact
  pros, cons, and why the chosen path won.
- End with a clear readiness call in `Notes`, not a full
  planning `Evidence` report.
- Include a compact `plan_qa` readiness note for material plans.
- Include reviewer handoff or receipt status for material plans; a planner
  self-check is not enough for approval-ready status.
