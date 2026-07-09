---
kind: product-loop
id: market_learning
label: Market learning
status: active
created_at: 2026-07-08
updated_at: 2026-07-08
sort_order: 50
lane: market_learning
lane_purpose: sharpen user and pain understanding
default_weight: 10
audience: Farplane strategy owners
output: interview, parity scan, opportunity brief
reward: sharper product or distribution bet
owner_skill: farplane-market-learning
skill_ref: farplane/products/market_learning/skill.md
progress_ref: farplane/products/market_learning/progress.md
worker_budget_min: 1
max_tickets_in_review: 3
review_channel: telegram through worker-artifact-review-request
human_gates:
  - external_contact
  - spend
  - publish
  - account_mutation
kpis:
  primary:
    - decision_changing_learning_briefs
  supporting:
    - interesting_autonomy_results
  guardrail: []
supporting_skills:
  - research
  - deep-interview
  - harness-scout
  - best-of-worlds
  - landing-page
  - social-content
  - update-strategy
goals:
  - id: decision_changing_learning_loop
    scope: product
    target: Produce learning briefs that change product, positioning, audience, or distribution decisions before execution spend grows.
    kpis:
      - decision_changing_learning_briefs
    interpretation: Market learning is working when research narrows a decision and creates a clearer next productization, distribution, or no-action move.
artifact_workflows:
  - id: offer_test
    lane: market_learning
    owner: landing-page
    planning_artifact: offer hypothesis variants
    execution_artifact: landing page section or offer test draft
    feedback_question: pick best / revise / reject the offer
  - id: learning_brief
    lane: market_learning
    owner: farplane-market-learning
    planning_artifact: decision question and source plan
    execution_artifact: market-learning brief
    feedback_question: accept / revise / reject the implication
notes: Sharpens audience, pain, offer, and distribution bets before product or content execution.
---

# Market Learning

This product loop turns research into decisions. It is not a generic reading
queue; a useful output changes what Farplane builds, says, sells, or stops.

## Current Strategy

```yaml
strategy:
  owner: interval-update
  cadence: daily evidence refresh, weekly strategy review
  horizon: current week
  status: active
  focus: produce learning briefs that change product, positioning, audience, or distribution decisions
  current_hypothesis: market learning is useful only when it narrows a decision before execution spend grows
  allocation_hint: 10
  next_moves:
    - choose one audience, offer, competitor, customer path, or adoption question
    - create or resume one bounded learning ticket below the review cap
    - route the implication to productization, distribution, or no-action
  last_interval_ref:
  next_review: next daily or weekly interval
```

Intervals may update this strategy block and nearby prose after reading all
products, product progress logs, tickets, metrics, reports, and registry state.
`product.md` is the tracked product loop program. Generated `products.json` must be regenerated only when frontmatter changes.

## Loop Contract

- `primary_output:` decision-oriented learning brief about users, pain,
  alternatives, positioning, distribution, or adoption.
- `primary_metric:` sharper product or distribution decision.
- `worker_budget:` derive from `default_weight`; default minimum `1`.
- `max_tickets_in_review:` `3`.
- `review_channel:` `telegram` through `worker-artifact-review-request` when a
  learning brief or decision implication needs Kenji judgment.
- `human_gates:` outreach, external contact, spend, publishing, account
  mutation.
- `runtime_progress:` `progress.md` is local ignored runtime learning. Do not
  promote or install it as product skill doctrine.

## Product Loop

1. Read current product questions, market-learning tickets, Feed Scout/source
   evidence, review decisions, and product-loop progress.
2. Rank learning moves by decision leverage, source quality, ICP relevance, and
   autonomy safety.
3. Create or resume one bounded learning ticket when tickets in review are
   below `max_tickets_in_review`.
4. Judge the learning by whether it changes a product, distribution, or
   positioning decision.
5. Record the implication and next product/distribution lever in `progress.md`.

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
