# Todos

- [ ] Read the chosen spec slice and confirm it is small enough for one planning pass.
- [ ] Start from the largest coherent self-contained feature ticket; do not split by schema/backend/UI layers just because those layers differ.
- [ ] Split only when a hard trigger applies: shared platform reuse, migration/backfill/rollout risk, external dependency/provisioning, or unresolved feasibility.
- [ ] Make acceptance criteria, evidence needs, and control fields concrete in each ticket.
- [ ] If a ticket includes UI, define the `Agent Contract`, `Evidence checklist`, and testability shape up front.
- [ ] If determinism or agent access looks weak, turn that into explicit instrumentation work now instead of hoping QA can improvise later.
- [ ] Write the raw tickets into `tickets/` with the correct state fields.
- [ ] Tighten the result against the [review guide](./references/review.md) before handoff.
- [ ] Stop after ticket creation and do not implement the slice here.
