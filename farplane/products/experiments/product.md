---
kind: product-loop
id: experiments
label: Experiment reports
status: active
created_at: 2026-07-08
updated_at: 2026-07-08
sort_order: 10
lane: metric_experiments
lane_purpose: improve measured harness behavior
default_weight: 30
audience: builders, researchers, Farplane operators
output: baseline, variant, measurement, decision
reward: validated improvement or rejected hypothesis
owner_skill: farplane-experiment-report
skill_ref: farplane/products/experiments/skill.md
progress_ref: farplane/products/experiments/progress.md
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
    - accepted_evidence_cycles
  supporting:
    - interesting_autonomy_results
  guardrail:
    - rejected_ai_ticket_count
supporting_skills:
  - metric-advisor
  - proof-advisor
  - eval
  - review
  - update-strategy
goals:
  - id: accepted_evidence_cycle_loop
    scope: product
    target: Turn high-uncertainty harness claims into accepted or rejected evidence cycles before productization.
    kpis:
      - accepted_evidence_cycles
    interpretation: Experiments are working when each completed cycle changes a productization, ablation, distribution, or strategy decision.
artifact_workflows:
  - id: experiment_report
    lane: metric_experiments
    owner: farplane-experiment-report
    planning_artifact: experiment decision angle
    execution_artifact: experiment report draft
    feedback_question: accept / revise / reject the decision
notes: Measures a harness hypothesis, records baseline/variant evidence, and turns the decision into rejection, iteration, or productization.
---

# Experiment Reports

This product loop turns unclear harness claims into explicit evidence cycles.
It should produce a decision, not a pile of observations.

## Current Strategy

```yaml
strategy:
  owner: interval-update
  cadence: daily evidence refresh, weekly strategy review
  horizon: current week
  status: active
  focus: turn unclear harness claims into measured keep/revise/reject decisions
  current_hypothesis: accepted evidence cycles are the cleanest path to compounding Farplane improvements
  allocation_hint: 30
  next_moves:
    - choose one high-uncertainty harness behavior with a visible baseline
    - create or resume one bounded experiment ticket below the review cap
    - route accepted evidence to productization or distribution
  last_interval_ref:
  next_review: next daily or weekly interval
```

Intervals may update this strategy block and nearby prose after reading all
products, product progress logs, tickets, metrics, reports, and registry state.
`product.md` is the tracked product loop program. Generated `products.json` must be regenerated only when frontmatter changes.

## Loop Contract

- `primary_output:` evidence-backed experiment report with baseline, variant,
  measurement, decision, limits, and follow-up.
- `primary_metric:` validated improvement or rejected hypothesis.
- `worker_budget:` derive from `default_weight`; default minimum `2`.
- `max_tickets_in_review:` `3`.
- `review_channel:` `telegram` through `worker-artifact-review-request` when a
  report or experiment packet is ready for Kenji.
- `human_gates:` external publishing, spend, deploy, account mutation,
  destructive cleanup.
- `runtime_progress:` `progress.md` is local ignored runtime learning. Do not
  promote or install it as product skill doctrine.

## Product Loop

1. Read current metrics, recent experiment tickets, rejected hypotheses, and
   product-loop progress.
2. Rank candidate moves by expected harness reward, evidence strength,
   baseline quality, and local autonomy.
3. Create or resume one bounded experiment ticket when tickets in review are
   below `max_tickets_in_review`.
4. Judge improvement from experiment evidence, reviewer verdict, and Kenji
   feedback.
5. Record the learning and next lever in `progress.md`.

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
