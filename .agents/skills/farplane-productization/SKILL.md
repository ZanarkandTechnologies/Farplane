---
name: farplane-productization
description: "Turn an accepted Farplane experiment or proof into durable harness behavior."
tier: 3
source: local
group: capability
template_uses:
  skill-template: "0.3.2"
---

# Farplane Productization

## Context

Use this project-local capability when an accepted experiment, ablation,
operator request, review finding, or interval report has enough evidence to
become durable harness behavior. The historical skill name describes rollout;
it is not a product controller, planning lane, or independent Pulse.

The capability may update skills, specs, validators, hooks, templates,
automations, UI handoffs, or docs. It preserves the static charter in
`farplane/harness.md` and routes material execution through tickets.

## Skill Signature

```text
farplane_productization(accepted_result, owner_surface, ticket?, proof_refs?)
  -> rollout_plan + shipped_delta_or_goal_handoff + proof
state: reads(accepted report, farplane/harness.md, farplane/goals.yaml, owner surface, tickets); writes(ticket, bounded owner-surface delta, ticket proof)
gates: owner_surface_named; evidence_refs_present; scoped_ticket_or_goal; proof_before_done
routes: root skill `harness-advisor` | root skill `impl-plan` | root skill `goal-advisor` | root skill `review`
fails: ships broad refactor without accepted evidence; changes charter silently; completes without proof
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read the accepted result and name its proof refs.
- [ ] 2. Confirm the smallest durable owner surface; use `harness-advisor` when unclear.
- [ ] 3. Bind an existing ticket or create one only for material execution.
- [ ] 4. Implement only the accepted bounded delta.
- [ ] 5. Run the narrowest validator, eval, QA, and review that proves rollout.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- Ticket-local rollout plan or handoff.
- Shipped delta summary.
- Proof command and artifact path.
