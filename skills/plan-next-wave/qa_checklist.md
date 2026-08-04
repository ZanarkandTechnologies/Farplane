---
title: Plan Next Wave QA Checklist
owner: plan-next-wave
status: active
kind: qa-checklist
updated_at: 2026-07-17
---

# Plan Next Wave QA Checklist

Apply before generation and again to the exact final JSON.

## Hard gates

1. `configured_skill_only`
   - Every proposed call uses one exact `farplane/harness.yaml#planning.skill_refs`
     entry and resolves to a skill package.
   - The planner reads the skill signature and `planner_contract`; it does not
     copy, paraphrase, or extend the workflow.

2. `arguments_bound`
   - `arguments` contains every `required_arguments` field with a concrete
     value and contains no undeclared fields.
   - Missing evidence rejects the call or remains an explicit source gap; it
     never becomes a planning task.
   - When the selected planner contract declares admission control, the call
     carries an `admit` receipt with the matching workstream/release condition
     and exact current open lifecycle refs below configured capacity. Holds and
     preemption requests are rejections, never proposed calls.

3. `strategic_stage_and_understandable_value`
   - Every market-learning, ablation, or content call names one configured
     stable problem plus canonical, coherent system/feature refs.
   - The selected skill matches the next missing evidence rung: current ICP
     pain, comparative proof, content from accepted proof, or productization
     from an accepted delta. Random features and generic research fail.
   - Without its title, the row makes the selected skill, finished artifact,
     ICP or operator, current alternative, why-now evidence, objective path,
     and falsifier obvious.
   - The primary artifact is usable, watchable, testable, or decision-changing;
     setup, schemas, tests, plans, and proof receipts do not count as value.

4. `history_preference_and_dedupe`
   - The planner queries global history before filters and compares skill,
     target/source, arguments, artifact, and intended outcome.
   - Recent terminal `kill` evidence requires a materially changed source,
     mechanism, or artifact. A renamed repeat fails.

5. `objective_authority_and_purity`
   - One authored objective contribution names an ultimate KPI plus honest
     `outcome | enabler | guard` attribution and a grounded forecast basis.
   - Enablers and guards cannot project realized revenue, reach, or subscriptions.
   - Human gates, dependencies, credentials, spend, publication, outreach, and
     external mutations are explicit; unresolved authority is not executable.
   - Plan writes no ticket, runs no worker, and materializes nothing.

6. `rationale_consistency`
   - The call's arguments, expected artifact, current alternative, why-now
     evidence, objective contribution, and falsifier support one premise.
   - Contradictory evidence, unsupported causal claims, or a falsifier for a
     different hypothesis rejects the call rather than being repaired by Pulse.

7. `lean_response`
   - Each proposed call appears exactly once. `decision.admitted_call_ids`
     references canonical rows instead of embedding them again.
   - No lanes, proposal types, Idea QA/TAS blocks, workflow steps, repeated
     forecasts, full ticket previews, or archetype registry appear.
   - `wave_size` is a maximum. Empty capacity needs no filler explanation beyond
     the exact rejection, conflict, authority, evidence, or leverage reason.

## Finish gate

```text
accept(call)
  -> configured skill + bound arguments + direct value + honest objective
   + consistent rationale + evidence + dedupe + authority + falsifier
```

An independent reviewer judges interest from compact calls plus held-out
context. The planner cannot self-certify desirability.
