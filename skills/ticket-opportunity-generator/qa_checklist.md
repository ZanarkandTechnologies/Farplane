---
title: Ticket Opportunity Generator QA Checklist
owner: ticket-opportunity-generator
status: active
kind: qa-checklist
created_at: 2026-07-06
applies_to:
  - generated-ticket-specs
  - product-loop-moves
---

# Ticket Opportunity Generator QA Checklist

Use this before Pulse or a product loop admits generated ticket specs. The
review posture is reject-first: find why the ticket is not worth a worker
cycle, then pass only when the move survives the gates.

```text
opportunity_qa(candidate_spec, product_loop_context, recent_attempts)
  -> pass | revise | reject + failed_checks
```

## Hard Gates

1. `product_loop_context`
   - Candidate names `product_lane`, `primary_product_skill`, and `workflow_id`
     when an artifact workflow applies.
   - Candidate is generated from one product-loop `product.md` strategy/loop
     contract and recent `progress.md` or clearly states why progress is
     unavailable.

2. `reward_trace`
   - Frontmatter `rewards.kpi` and body `Reward.kpi_rewards[]` agree.
   - Reward maps to `farplane/bindings.yaml` and a product output or artifact
     workflow in `farplane/products.json`.
   - `expected_reward` is concrete enough to know what would count.
   - `check_in_at` names when interval update should compare expectation to
     actual result.

3. `icp_resonance`
   - Candidate names the ICP or operator audience.
   - It states why the ICP would care now and what pain, curiosity, trust gap,
     or workflow tension the artifact answers.
   - Reviewer must list the strongest reason the ICP may still find it bland.

4. `trend_or_source_relevance`
   - Distribution and market-learning tickets cite recent Feed Scout/source
     evidence or explicitly name the source gap.
   - The ticket uses qualitative relevance, not fake scalar precision.

5. `state_of_art_pushback`
   - Candidate names the current/default/competitor-like baseline or normie
     workflow when audience-facing.
   - Reviewer must state why the idea may be below the bar of what the audience
     already sees, and either strengthen or reject it.

6. `artifact_ambition`
   - Artifact level matches the product lane: report, proof, shipped delta,
     script/storyboard/demo/visual/thread, or learning brief.
   - Notes, reminders, review receipts, and paperwork are not product
     throughput unless explicitly scoped as a planning card.

7. `execution_plan_rationale`
   - Ticket tells the worker what to build or measure; it does not ask the
     worker to discover whether the idea is worth doing.
   - The plan has clear input refs, output artifact, stop condition,
     validation, and final human gate.

8. `dedupe_and_learning`
   - Candidate lists prior attempt refs or says none found.
   - Candidate includes `learning_writeback` naming the target product-loop
     progress file and the learning fields to update after execution.

9. `review_surface`
   - Candidate names the artifact Kenji/reviewer should inspect.
   - Worker handoff requires `worker-artifact-review-request` unless the ticket
     explicitly says `review_notify: none` with a reason.

## Finish Gate

```text
accept(candidate)
  -> pass only when all hard gates pass
  -> revise when the idea is promising but weak in ICP, artifact ambition,
     baseline, execution rationale, or learning writeback
  -> reject when the ticket is generic, boring-but-valid, self-referential,
     maintenance-only, unsafe, or not product-backed
```
