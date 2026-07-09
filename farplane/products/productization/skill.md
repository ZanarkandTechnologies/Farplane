---
name: farplane-productization
description: "Turn an accepted Farplane experiment or proof into shipped harness behavior when a result should become product."
tier: 3
source: local
group: product
template_uses:
  skill-template: "0.3.2"
---

# Farplane Productization

## Context

Use this project-local skill when a Farplane experiment, ablation, operator
request, review finding, or interval report has enough evidence to become
shipped harness behavior.

Productization can update skills, specs, validators, hooks, templates,
automations, UI handoffs, or docs. It must preserve the static charter in
`farplane/harness.md` and route material execution through tickets.

## Skill Signature

```text
farplane_productization(accepted_result, owner_surface, ticket?, proof_refs?)
  -> productization_plan + shipped_delta_or_goal_handoff + proof
state: reads(accepted report, farplane/harness.md, farplane/goals.yaml, farplane/products/productization/product.md, owner surface, tickets); writes(ticket, skill/spec/validator/template/docs delta, proof artifact)
gates: owner_surface_named; evidence_refs_present; scoped_ticket_or_goal; proof_before_done
routes: root skill `harness-advisor` | root skill `impl-plan` | root skill `goal-advisor` | root skill `review`
fails: ships broad refactor without accepted evidence; changes charter silently; completes without proof
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the accepted result.
  - [ ] Read the accepted experiment, ablation, review, or operator request.
  - [ ] Name the intended owner surface and proof refs.
- [ ] 2. Confirm placement.
  - [ ] Use `harness-advisor` when ownership across skill, spec, validator,
    hook, template, automation, UI, or docs is unclear.
- [ ] 3. Create or bind the ticket.
  - [ ] Use an existing ticket when present.
  - [ ] Create a compact follow-up ticket when execution is material.
- [ ] 4. Implement the product delta.
  - [ ] Keep scope to the accepted result.
  - [ ] Preserve static charter boundaries unless a human-approved harness
    delta exists.
- [ ] 5. Prove and review.
  - [ ] Run the narrowest validator, eval, QA, or review that proves the
    shipped behavior.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- Productization plan or ticket handoff.
- Shipped delta summary.
- Proof command or artifact path.
