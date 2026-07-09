---
kind: product-loop
id: productization
label: Harness improvements
status: active
created_at: 2026-07-08
updated_at: 2026-07-08
sort_order: 30
lane: productization
lane_purpose: ship accepted wins
default_weight: 20
audience: Farplane users and projects
output: skill, spec, eval, validator, hook, automation, or UI handoff
reward: reviewed shipped behavior
owner_skill: farplane-productization
skill_ref: farplane/products/productization/skill.md
progress_ref: farplane/products/productization/progress.md
worker_budget_min: 2
max_tickets_in_review: 3
review_channel: telegram through worker-artifact-review-request
human_gates:
  - publish
  - spend
  - deploy
  - account_mutation
  - destructive_cleanup
kpis:
  primary:
    - accepted_harness_improvements
  supporting:
    - latest_eval_pass_rate
  guardrail:
    - rejected_ai_ticket_count
supporting_skills:
  - impl-plan
  - goal-advisor
  - qa
  - demo
  - close-ticket
  - skill-maintenance
  - harness-advisor
goals:
  - id: accepted_improvement_loop
    scope: product
    target: Convert accepted evidence into reviewed shipped harness behavior without weakening proof quality.
    kpis:
      - accepted_harness_improvements
      - latest_eval_pass_rate
    interpretation: Productization is working when accepted evidence becomes durable behavior and proof/eval quality remains high.
artifact_workflows:
  - id: productization_handoff
    lane: productization
    owner: farplane-productization
    planning_artifact: productization bet and user-facing delta
    execution_artifact: shipped-behavior proposal or handoff
    feedback_question: accept / revise / reject the productization move
notes: Converts accepted evidence into shipped harness behavior, with ticket proof and reviewer gates.
---

# Harness Improvements

This product loop turns accepted learning into durable Farplane behavior. It
should not productize a claim that experiments or ablations have not earned.

## Current Strategy

```yaml
strategy:
  owner: interval-update
  cadence: daily evidence refresh, weekly strategy review
  horizon: current week
  status: active
  focus: turn accepted evidence into reviewed shipped harness behavior
  current_hypothesis: productization should follow accepted proof, not speculative cleanup
  allocation_hint: 20
  next_moves:
    - choose one accepted result with a clear owner surface
    - create or resume one bounded implementation ticket below the review cap
    - prove the shipped behavior before promoting it as durable doctrine
  last_interval_ref:
  next_review: next daily or weekly interval
```

Intervals may update this strategy block and nearby prose after reading all
products, product progress logs, tickets, metrics, reports, and registry state.
`product.md` is the tracked product loop program. Generated `products.json` must be regenerated only when frontmatter changes.

## Loop Contract

- `primary_output:` reviewed shipped harness behavior from accepted evidence:
  skill, spec, eval, validator, hook, automation, UI handoff, or docs delta.
- `primary_metric:` reviewed shipped behavior.
- `worker_budget:` derive from `default_weight`; default minimum `2`.
- `max_tickets_in_review:` `3`.
- `review_channel:` `telegram` through `worker-artifact-review-request` when a
  productization plan, proof bundle, or reviewable shipped delta is ready.
- `human_gates:` deploy, spend, destructive cleanup, account mutation,
  publishing.
- `runtime_progress:` `progress.md` is local ignored runtime learning. Do not
  promote or install it as product skill doctrine.

## Product Loop

1. Read accepted experiments/proofs, productization tickets, review outcomes,
   and product-loop progress.
2. Rank implementation levers by accepted proof strength, compounding value,
   local scope, and rollback simplicity.
3. Create or resume one bounded productization ticket when tickets in review
   are below `max_tickets_in_review`.
4. Judge shipped behavior from checks, QA, reviewer verdict, and Kenji feedback.
5. Record accepted or rejected productization learning plus the next lever in
   `progress.md`.

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
