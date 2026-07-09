---
title: Product Ticket Contracts
owner: ticket-opportunity-generator
status: active
kind: reference
created_at: 2026-07-06
---

# Product Ticket Contracts

Generated ticket specs must name the product lane, primary product skill,
artifact level, reward, review surface, and product-loop learning writeback.
The product skill owns workflow details; this reference owns the generator's
minimum ticket contract.

| Product | Product lane | Primary skill | Minimum artifact | Review question |
| --- | --- | --- | --- | --- |
| `experiments` | `metric_experiments` | `farplane-experiment-report` | experiment report with hypothesis, baseline, variant, metric, evidence, decision, limits | accept / revise / reject the experiment decision |
| `ablations` | `trust_ablations` | `farplane-ablation-proof` | with/without proof report with fair baseline and trust decision | accept / revise / reject the proof |
| `productization` | `productization` | `farplane-productization` | shipped harness delta or productization handoff with proof | accept / revise / reject the shipped behavior or plan |
| `distribution` | `trust_distribution` | `farplane-evidence-content` | script, storyboard, visual/demo brief, rendered clip, carousel/slides, publish-ready thread, or launch note grounded in accepted evidence | approve / revise / reject the artifact direction; publish remains gated |
| `market_learning` | `market_learning` | `farplane-market-learning` | decision-oriented learning brief with source quality, implication, and next action | accept / revise / reject the implication |

## Required Candidate Fields

```yaml
product: experiments | ablations | productization | distribution | market_learning
product_lane:
primary_product_skill:
workflow_id:
rewards:
  kpi:
    - accepted_harness_improvements
reward:
  kpi_rewards:
    - kpi_id:
      expected_reward:
      check_in_at:
      actual_result:
      reward_score:
      reward_score_reason:
  guard:
products_md_contribution:
icp_or_operator_audience:
trend_or_source_relevance:
state_of_art_pushback:
big_claim:
audience_tension:
surprise_factor:
baseline_or_contrast:
artifact_level:
review_surface:
prior_attempt_refs:
learning_writeback:
  target: farplane/products/<product>/progress.md
  fields:
    - selected_move
    - ticket_refs
    - artifact_refs
    - feedback_result
    - learning
    - next_lever
execution_plan_rationale:
human_gate:
```

## Learning Writeback

Tickets are execution attempts. Product-loop progress is the cross-ticket
learning memory. Each generated ticket must tell the worker or completing loop
which product-loop progress file should receive the compact learning entry.
