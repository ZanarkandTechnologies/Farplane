---
title: Ticket Opportunity Generator QA Checklist
owner: ticket-opportunity-generator
status: active
kind: qa-checklist
created_at: 2026-07-06
updated_at: 2026-07-10
applies_to:
  - generated-ticket-specs
---

# Ticket Opportunity Generator QA Checklist

Apply this before returning any `plan_next_wave` spec. Every accepted spec must
pass all hard gates; `wave_size` never forces a weak ticket.

```text
next_wave_qa(candidate, harness_areas, metric_objectives, metric_state, ticket_history_queries)
  -> pass | reject + failed_gates
```

## Hard Gates

1. `objective_contribution`
   - Names an existing KPI or selected guard, causal mechanism, expected
     change, metric provider, signal horizon, delayed `check_in_at` when
     applicable, expected Reward, and proof route.
   - Rejects a proactive spec when no honest KPI/guard binding exists; never
     uses `none mechanical`.
   - Rejects ordinary admission when a hard guard reading is missing or stale;
     only bounded observation-restoration work may pass that condition.

2. `project_value_boundary`
   - The primary outcome advances a project objective, preserves a selected
     guard, fulfills a direct obligation, or tests an evidenced process change.
   - Self-improvement cites an observed failure, Reward outcome, guard
     regression, or toy/eval proof; speculative framework work fails.
   - Internal plans, summaries, recommendations, ticket volume, and other
     activity artifacts do not count as independent value.

3. `executable_now`
   - A worker can start from named inputs and produce the named output.
   - The ticket does not ask the worker to discover the idea or plan more
     tickets.

4. `evidence_and_source_gaps`
   - Claims and priority use current cited evidence.
   - Missing or stale evidence is labeled rather than invented.

5. `dedupe`
   - Compares intended outcome, artifact, target surface, and evidence against
     active and recent attempts.
   - Duplicate or already-completed work is rejected.
   - Planner read the latest global `N` rows before any area/origin filter and
     recorded the progressive query receipts used for deeper comparison.

6. `proof_and_stop`
   - Names checks, evidence artifact or review question, and a stop condition.
   - Proof is proportional to the claim.

7. `capability_boundary`
   - Names an existing capability skill when one owns the workflow.
   - Does not copy the capability procedure or invent a controller.

8. `authority_and_dependencies`
   - Human gates, dependencies, credentials, and external side effects are
     explicit.
   - A spec marked executable does not require unresolved authority or input.

9. `leverage_and_ranking`
   - Names the bottleneck, candidate lever, objective impact, bottleneck
     relief, urgency, proof speed, compounding value, cost/risk, and review
     load at useful qualitative resolution.
   - Compounding value reinforces direct project progress and does not smuggle in
     speculative infrastructure.
   - Plausible losing candidates have a deprioritization reason.
   - Ranking compares expected metric delta, confidence, duration,
     time-to-signal, cost, risk, reversibility, information gain, compounding
     value, interference, and prerequisites instead of greedily selecting the
     easiest immediate delta.
   - Area ticket counts inform attention only; outcome/metric movement and
     recent Reward evidence determine whether an area is actually under-moving.

10. `minimal_scope`
   - Contains one coherent result and the smallest work that can prove it.
   - Avoids speculative infrastructure, broad cleanup, and unrelated polish.

11. `lifecycle_contract`
   - Uses `status: todo`, no claim, satisfied dependencies, and a valid
     optional human gate.

12. `pure_planner_output`
    - The result is a spec plus gaps/rejections only.
   - No ticket write, worker spawn, review send, report write, or external
     mutation happened inside planning.

13. `single_adaptive_planner`
   - One planner owns global sampling, progressive retrieval, proposal
     generation, dedupe, and ranking.
   - No area planner subagents, area Pulses, quotas, or planning mode enum were
     introduced.

## Finish Gate

```text
accept(candidate)
  -> pass only when all gates pass
  -> reject when duplicate, vague, unsafe, blocked, ungrounded, or low leverage
```
