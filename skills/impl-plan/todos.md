# Todos

- [ ] Read the active ticket first, then read the relevant PRD, specs, memory, troubles, and nearby code.
- [ ] Treat this skill as `PlanTicket<CodingTicket>` inside the
  [project-lifecycle](../deep-init-project/references/project-lifecycle.md).
- [ ] Use the generic [plan](../plan/SKILL.md) interface as the Tier 2 contract,
  but keep `impl-plan` coding-specific.
- [ ] Use the relevant [research](../research/SKILL.md) method when expected
  behavior depends on local baseline, official behavior, examples, or peer
  norms.
- [ ] Use [research:gap](../research/SKILL.md#researchgap) when missing or
  partial code work needs current-state gap and production expectation.
- [ ] Use [research:parity](../research/SKILL.md#researchparity) when external
  peer norms need to be established before local scope.
- [ ] Preserve the
  [first-principles-planning](../../docs/specs/first-principles-planning.md)
  basis for material work: objective, need, assumptions, root cause,
  constraints, first viable slice, proof/falsification, tradeoffs, and
  non-goals.
- [ ] Decide whether the whole selected ticket can stay whole or whether a
  real boundary forces a split first.
- [ ] If an `Agent Testability Brief` exists, carry its surfaces into the proof and execution plan.
- [ ] Write or refine the ticket `Proof Contract`: metrics or `none mechanical`, review rubric gates, hard gates, required evidence, and optional autoresearch session path.
- [ ] Compare 3 viable options and recommend one clearly.
- [ ] Keep the output in the canonical ticket-body shape instead of inventing a `Human` / `Agent` split.
- [ ] Make the `Plan` section carry callable seams in `Signature delta` and typed data seams in `Type Sketch`.
- [ ] Add one `Typed flow example` for material, stateful, interface-heavy, or cross-boundary work when it improves trust.
- [ ] Add `Execution steps` whenever the build has more than one non-trivial step.
- [ ] Use decisive action language in the recommendation and ordered steps.
- [ ] Make proof concrete and observable rather than generic.
- [ ] Keep metrics and rubrics distinct: metrics are mechanical signals; rubrics are review judgment frames.
- [ ] If the change is high-risk or contentious, run the `--consensus` version of this skill.
- [ ] Run the [plan](../plan/SKILL.md) challenge/review shape before claiming
  the plan is ready.
- [ ] Pitch the full-ticket plan to the user for approval and revise it before
  build starts.
- [ ] Keep planning separate from implementation and leave the ticket in `review` until approval exists.
