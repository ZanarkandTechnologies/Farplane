# Todos

- [ ] Read the chosen spec slice and confirm it is small enough for one planning pass.
- [ ] Use the generic [plan](../plan/SKILL.md) interface as the Tier 2 contract,
  but keep `spec-to-ticket` coding-ticket specific.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) when ticket
  scope depends on local baseline, examples, official behavior, peer norms, or
  implementation patterns.
- [ ] Start from the largest coherent self-contained feature ticket; do not split by schema/backend/UI layers just because those layers differ.
- [ ] Keep CRUD and other narrow operator workflows in one ticket by default.
- [ ] Split only when a hard trigger applies: shared platform reuse, migration/backfill/rollout risk, external dependency/provisioning, unresolved feasibility, or a real service/runtime boundary.
- [ ] For complex systems, make the first ticket leave behind a minimal end-to-end happy path plus a reusable proof surface instead of empty scaffolding.
- [ ] Group later follow-up tickets by shared proof surface or adjacent operator value, not one internal pipeline stage per ticket.
- [ ] Make acceptance criteria, evidence needs, and control fields concrete in each ticket.
- [ ] If an `Agent Testability Brief` exists, carry its surfaces into the ticket contract instead of re-deriving them.
- [ ] If there is no richer testability brief yet but `docs/bootstrap-brief.md` has `Agent Experience / Testability`, use it as the fallback seed for the first UI-bearing or agentically hard ticket.
- [ ] If a ticket includes UI, define the `Agent Contract`, `Evidence checklist`, and testability shape up front.
- [ ] If the repo has `qa/cookbook/` and the slice is UI-bearing or agentically hard, seed or update the matching workflow entry.
- [ ] If determinism or agent access looks weak, turn that into explicit instrumentation work now instead of hoping QA can improvise later.
- [ ] Write the raw tickets into `tickets/` with the correct state fields.
- [ ] Tighten the result against the [review guide](./references/review.md) before handoff.
- [ ] Stop after ticket creation and do not implement the slice here.
