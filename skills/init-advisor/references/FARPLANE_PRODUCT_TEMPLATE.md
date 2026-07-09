---
kind: product-loop
id: core
label: Core product
status: draft
created_at: "{{DATE}}"
updated_at: "{{DATE}}"
sort_order: 10
lane: primary_product
lane_purpose: create or improve the main product output
default_weight: 40
audience: TODO audience
output: TODO shipped artifact or service
reward: TODO accepted value signal
owner_skill: project-core-product
skill_ref: farplane/products/core/skill.md
progress_ref: farplane/products/core/progress.md
worker_budget_min: 1
max_tickets_in_review: 3
review_channel: telegram through worker-artifact-review-request
human_gates:
  - publish
  - spend
  - deploy
  - external_contact
  - account_mutation
  - destructive_cleanup
kpis:
  primary:
    - TODO_metric_name
  supporting: []
  guardrail: []
supporting_skills: []
goals:
  - id: first_core_product_goal
    scope: product
    target: TODO stable desired outcome for the core product loop.
    kpis:
      - TODO_metric_name
    interpretation: TODO explain how the product goal should guide ticket selection.
artifact_workflows:
  - id: core_output_review
    lane: primary_product
    owner: project-core-product
    planning_artifact: TODO concept or plan
    execution_artifact: TODO draft, demo, artifact, or shipped change
    feedback_question: keep / revise / reject the direction
notes: TODO describe how this product loop creates value.
---

# Core Product Loop

This file is the canonical product-loop definition. Keep product identity,
lane, KPI membership, gates, artifact workflows, stable product-level goals,
current strategy, loop contract, and progress-entry shape here.

Do not put metric refresh mechanics here; those belong in
`farplane/bindings.yaml`. Intervals may update the strategy section after
reviewing all products, progress logs, tickets, reports, metrics, and source
gaps. Runtime attempts and learning belong in ignored product `progress.md`.

## Current Strategy

```yaml
strategy:
  owner: interval-update
  cadence: daily evidence refresh, weekly strategy review
  horizon: current week
  status: active
  focus: TODO current product focus
  current_hypothesis: TODO current strategic hypothesis
  allocation_hint: 40
  next_moves:
    - TODO next product-shaped move
  last_interval_ref:
  next_review: next daily or weekly interval
```

## Loop Contract

- `primary_output:` TODO reviewable product output.
- `primary_metric:` TODO primary reward or decision signal.
- `worker_budget:` derive from `default_weight`; default minimum `1`.
- `max_tickets_in_review:` `3`.
- `review_channel:` `telegram` through `worker-artifact-review-request` when an
  artifact is ready for review.
- `human_gates:` publish, spend, deploy, external contact, account mutation,
  destructive cleanup.
- `runtime_progress:` `progress.md` is local ignored runtime learning. Do not
  promote or install it as product skill doctrine.

## Product Loop

1. Read current product strategy, recent tickets, metrics, reports, and
   product-loop progress.
2. Rank candidate moves by expected reward, evidence strength, reviewability,
   and autonomy safety.
3. Create or resume one bounded product ticket when tickets in review are below
   `max_tickets_in_review`.
4. Judge the artifact from proof, metrics, reviewer verdict, and Kenji feedback.
5. Record learning and the next lever in `progress.md`.

## Progress Entry Shape

Append compact runtime entries to `progress.md` using this shape:

```markdown
## <YYYY-MM-DD HH:MM +TZ> - cycle <n>

- `metric:` <primary reward being optimized>
- `tickets_in_review:` <count or unknown>
- `workers:` <worker count/threads if known>
- `prior_attempt:` <recent ticket/artifact/learning refs>
- `candidate_moves:` <ranked ideas or pointer to artifact>
- `selected_move:` <chosen lever>
- `why:` <strategy/reward rationale>
- `ticket_refs:` <tickets created/resumed>
- `artifact_refs:` <outputs/proof/review refs>
- `feedback_result:` <accepted/rejected/revised/blocked/pending>
- `learning:` <what worked or missed>
- `next_lever:` <next highest-leverage move>
- `blocker:` <none or blocker>
```
