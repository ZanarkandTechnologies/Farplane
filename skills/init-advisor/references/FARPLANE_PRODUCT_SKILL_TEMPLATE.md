---
name: project-core-product
description: "Project-local workflow for producing the core product output."
tier: 3
source: local
group: product
---

# Project Core Product

## Context

Use this project-local skill when creating or improving the core product output.
Specialize this file after the project has a concrete operating model.

## Skill Signature

```text
project_core_product(product_goal, evidence_refs?, ticket?)
  -> product_artifact + proof_refs + next_action
state: reads(farplane/harness.md, farplane/products/core/product.md, farplane/goals.yaml, ticket context); writes(ticket artifact or product output)
gates: product_goal_named; kpi_ref_valid; proof_refs_named; final_actions_human_gated
routes: project-specific skills | goal-advisor | review
fails: creates generic busywork; changes product direction without evidence; performs publish/spend/deploy/contact actions without approval
```

## Output

- Product artifact, draft, demo, implementation delta, or handoff.
- Proof refs and next action.
