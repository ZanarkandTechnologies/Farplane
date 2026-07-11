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
next_wave_qa(candidate, program, objective_contract, ticket_history)
  -> pass | reject + failed_gates
```

## Hard Gates

1. `objective_contribution`
   - Names the objective or bottleneck and the expected contribution.
   - Uses an existing metric/review signal or states `none mechanical`.

2. `bau_boundary`
   - The primary outcome advances the project's product, customer, operations,
     reliability, deliverable, or user-facing capability.
   - The candidate is not primarily a Farplane harness, planner, skill-system,
     framework-automation, doctrine/docs, hook/validator, registry, or
     self-evaluation improvement.
   - Product docs and operational automation are not rejected merely because
     their artifact types resemble framework surfaces.

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
   - Compounding value reinforces direct BAU progress and does not smuggle in
     speculative infrastructure.
   - Plausible losing candidates have a deprioritization reason.

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

## Finish Gate

```text
accept(candidate)
  -> pass only when all gates pass
  -> reject when duplicate, vague, unsafe, blocked, ungrounded, or low leverage
```
