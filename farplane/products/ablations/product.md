---
kind: product-loop
id: ablations
label: Trust ablations
status: active
created_at: 2026-07-08
updated_at: 2026-07-08
sort_order: 20
lane: trust_ablations
lane_purpose: prove or reject trust claims
default_weight: 20
audience: skeptical operators and reviewers
output: with/without comparison, proof report, decision
reward: accepted or rejected trust claim
owner_skill: farplane-ablation-proof
skill_ref: farplane/products/ablations/skill.md
progress_ref: farplane/products/ablations/progress.md
worker_budget_min: 2
max_tickets_in_review: 3
review_channel: telegram through worker-artifact-review-request
human_gates:
  - publish
  - spend
  - deploy
  - external_contact
kpis:
  primary:
    - accepted_trust_ablations
  supporting:
    - accepted_evidence_cycles
  guardrail:
    - rejected_ai_ticket_count
supporting_skills:
  - proof-advisor
  - agent-qa-test
  - agent-behavior-test
  - eval
  - review
goals:
  - id: trust_claim_ablation_loop
    scope: product
    target: Prove or reject trust-critical surfaces before they become durable harness policy.
    kpis:
      - accepted_trust_ablations
    interpretation: Ablations are valuable when a with/without comparison changes whether a prompt, skill, validator, or review surface stays in the harness.
artifact_workflows:
  - id: ablation_proof
    lane: trust_ablations
    owner: farplane-ablation-proof
    planning_artifact: proof claim and contrast plan
    execution_artifact: ablation proof report
    feedback_question: accept / revise / reject the proof
notes: Proves whether a feature or workflow matters through with/without comparison and evidence review.
---

# Trust Ablations

This product loop protects Farplane from keeping ceremony just because it
sounds right. The output is a trust decision grounded in a fair comparison.

## Current Strategy

```yaml
strategy:
  owner: interval-update
  cadence: daily evidence refresh, weekly strategy review
  horizon: current week
  status: active
  focus: prove or reject trust-critical surfaces before they become durable policy
  current_hypothesis: with/without proof is the fastest way to separate useful ceremony from false confidence
  allocation_hint: 20
  next_moves:
    - choose one trust claim with a plausible baseline and variant
    - create or resume one bounded ablation ticket below the review cap
    - route accepted claims to productization and rejected claims to cleanup
  last_interval_ref:
  next_review: next daily or weekly interval
```

Intervals may update this strategy block and nearby prose after reading all
products, product progress logs, tickets, metrics, reports, and registry state.
`product.md` is the tracked product loop program. Generated `products.json` must be regenerated only when frontmatter changes.

## Loop Contract

- `primary_output:` trust ablation proof comparing with/without behavior,
  baseline, variant, evidence, decision, and residual risk.
- `primary_metric:` accepted or rejected trust claim.
- `worker_budget:` derive from `default_weight`; default minimum `2`.
- `max_tickets_in_review:` `3`.
- `review_channel:` `telegram` through `worker-artifact-review-request`.
- `human_gates:` publish, spend, deploy, external contact.
- `runtime_progress:` `progress.md` is local ignored runtime learning. Do not
  promote or install it as product skill doctrine.

## Product Loop

1. Read recent trust claims, ablation tickets, proof gaps, review feedback, and
   product-loop progress.
2. Rank claims by user-visible contrast, baseline strength, trust value, and
   local proofability.
3. Create or resume one bounded ablation ticket when tickets in review are
   below `max_tickets_in_review`.
4. Judge the claim from with/without evidence and reviewer/Kenji feedback.
5. Record accepted, rejected, or revised trust learning plus the next proof
   lever in `progress.md`.

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
