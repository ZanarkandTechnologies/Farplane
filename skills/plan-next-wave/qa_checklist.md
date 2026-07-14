---
title: Plan Next Wave QA Checklist
owner: plan-next-wave
status: active
kind: qa-checklist
created_at: 2026-07-06
updated_at: 2026-07-10
applies_to:
  - generated-ticket-specs
---

# Plan Next Wave QA Checklist

Apply this before returning any `plan_next_wave` spec. Every accepted spec must
pass all hard gates; `wave_size` never forces a weak ticket.

```text
next_wave_qa(candidate, harness_areas = harness.areas, metric_objectives,
             metric_goals?, metric_state, ticket_history_queries,
             review_pool_state?, world_memory?, taste_evidence?)
  -> pass | reject + failed_gates
```

## Hard Gates

0A. `objective_progress_contract`
   - Returns one progress row for every selected objective with configured
     priority, current value, freshness, confidence, and source plus target,
     target date, and gap when configured.
   - Uses `ahead`, `on_track`, or `behind` only when current evidence and a
     supplied target trajectory support the verdict. Otherwise uses `unknown`
     and names the missing reading, target, date, or pace input.
   - Never imports a target from a stale UI projection or invents numeric
     precision to force a ranking.
   - Loads optional `harness.goals`, derives completion from the current metric
     value and metric direction, and removes completed goals from urgency.
     Missing readings remain source gaps; no mutable goal status is invented.

0B. `candidate_lane_contract`
   - The same planner enumerates `delivery`, `ablation`, `experiment`,
     `rollout`, and `operations`; each returns `requested_count = wave_size`,
     `candidate_count`, `candidates[]`, and an exact shortfall reason when it
     produces fewer than requested.
   - Each lane searches for up to `wave_size` materially distinct moves before
     global ranking instead of stopping at its first plausible candidate.
   - Lanes widen candidate search only. They do not create quotas, reserved
     slots, separate planners, separate rankings, or guaranteed admission.
   - Every admitted spec names one canonical `ranking.lane`; multiple winners
     may share a lane when their metric-bound trajectories rank highest.

0. `area_instruction_contract`
   - Reads each scope-relevant complete area record from `farplane/harness.yaml`,
     including `description`, `icp`, `planner_instruction`, `skill_refs`, and
     `metric_refs`.
   - Global scope returns one instruction receipt for every objective-relevant
     configured area; reserved scope returns one for the caller-selected area.
   - Every admitted spec uses
     `ranking.area_instruction_ref = harness.areas.<area_id>.planner_instruction`
     and explains the applied instruction in
     `ranking.area_instruction_applied`.
   - Rejects caller-authored area-policy paraphrases, wrong-area refs, missing
     instructions, and area IDs or metric lists passed without their complete
     canonical area record.

0C. `icp_and_world_grounding`
   - Every admitted spec binds
     `audience_context.icp_ref = harness.areas.<area_id>.icp`, one concrete ICP
     job or pain, a named baseline/default, and the belief, implementation, or
     workflow change the artifact should cause.
   - Outward-facing delivery, research, ablation, experiment, sales, demo, and
     distribution specs cite at least one relevant entry in the configured
     Feed Scout Markdown memory plus its source evidence. A trend name or
     generic pain statement alone fails.
   - Self-improvement may use local ticket, Reward, eval, or run evidence when
     external context is irrelevant, but still binds the operator ICP and
     baseline. Memory remains evidence, never authority.
   - Stale or conflicting memory is labeled honestly; the candidate either
     proves the premise with a bounded research/experiment artifact or records
     a source gap instead of presenting it as current fact.

1. `objective_contribution`
   - Names an existing KPI or selected guard, causal mechanism, expected
     change, metric provider, signal horizon, delayed `check_in_at` when
     applicable, expected Reward, and proof route.
   - Rejects a proactive spec when no honest KPI/guard binding exists; never
     uses `none mechanical`.
   - Rejects ordinary admission when a hard guard reading is missing or stale;
     only bounded observation-restoration work may pass that condition.
   - Every unattended admitted spec uses `execution.operator_dependency: none`;
     later human-gated publish or use belongs in `lifecycle.human_gate` and
     `scope_out`, not in this field.
   - The final decision includes a deterministic `validation_receipt` covering
     every admitted spec; the receipt's `spec_count` matches the wave and every
     result has no errors.

Eval fixture preflight for the ICP/world-memory hardcase:

```bash
python3 skills/feed-scout/scripts/validate_memory.py \
  skills/plan-next-wave/evals/fixtures/icp-world-memory.md \
  --harness farplane/harness.yaml
```

2. `project_value_boundary`
   - The primary outcome advances a project objective, preserves a selected
     guard, fulfills a direct obligation, or tests an evidenced process change.
   - Self-improvement cites an observed failure, Reward outcome, guard
     regression, or toy/eval proof; speculative framework work fails.
   - Internal plans, summaries, recommendations, ticket volume, and other
     activity artifacts do not count as independent value.
   - Names a concrete positive output or state change and the causal path from
     that output to the selected KPI/guard.
   - Historical cleanup counts as maintenance, not compounding leverage. A
     self-improvement spec must name a recurring failure, durable preventive
     mechanism, and proof on a future or reproduced run.

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
   - A blocked or awaiting-review ticket owns only its intended output, target
     surface, and unresolved prerequisite. It does not suppress independent
     artifacts merely because they share an area, KPI, audience, or objective.
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
   - When operator availability is missing or stale, uses unattended mode and
     rejects dirty cross-project mutation, publication, outreach, credential,
     destructive, or decision-dependent work from the executable wave.

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
   - Every admitted candidate carries an inspectable `priority_trace` with
     objective priority, current value, target/target date/gap or explicit
     unconfigured/unknown values, progress status, metric freshness/source, and
     the final rank reason. The trajectory separately carries expected delta,
     confidence, duration, time-to-signal, cost, risk, human load, information
     gain, compounding value, and interference.
   - The selected `0..wave_size` tickets are the highest-impact compatible
     portfolio after hard gates. Lane diversity and artifact count never
     displace a stronger risk-adjusted metric trajectory.
   - Area ticket counts inform attention only; outcome/metric movement and
     recent Reward evidence determine whether an area is actually under-moving.
   - When evidence supports them, compares immediate, near-term, and
     compounding horizons and considers direct BAU/customer/sales moves plus
     evidence-backed self-improvement. Fewer candidates require an exact
     evidence, authority, or dedupe reason; `wave_size` never requires filler.
   - When review pools are saturated or operator availability is absent,
     selection favors unattended-safe work with machine or delayed feedback
     and low immediate human load; saturation never suppresses planning.
   - Content/distribution hypotheses may cite Tasty Pack ingredients as
     optional taste evidence, but never create a separate content Pulse or
     bypass KPI, proof, authority, and artifact gates.

10. `minimal_scope`
   - Contains one coherent result and the smallest work that can prove it.
   - Avoids speculative infrastructure, broad cleanup, and unrelated polish.
   - Avoidable setup is bundled into the first independently useful exemplar;
     a setup-only ticket fails when that bundle is possible.

11. `artifact_output`
   - Every ordinary admitted spec names one or more structured `direct_value`
     output artifacts with a supported kind, concrete ref, independent value,
     and direct use path.
   - A plan, recommendation, configuration, schema, template, setup state, or
     proof/test receipt does not count and belongs in `setup_changes` or proof.
   - Non-empty `setup_changes` requires `setup_burden: bundled` plus a
     non-empty string `bundled_setup` and a `first_exemplar` exactly equal to
     one direct-value artifact ref; `setup_burden: none` must fail mechanically.
   - Compound outputs are preferred when a coherent ticket can create direct
     value plus reusable proof, demo, research, or distribution value.

12. `wave_shape`
   - Global scope covers every objective-relevant area before one global
     ranking. Explicit reserved-area scope records the caller allocation and
     covers every relevant lever inside that area after a global history query.
   - At most one ordinary admitted spec is setup-bearing; it consolidates the
     required setup and ships the first useful exemplar.
   - All other admitted specs are independently useful without another setup
     ticket. The wave maximizes artifact-producing specs only after all hard
     quality, objective, guard, authority, dedupe, and interference gates.
   - `lanes_considered` contains all five canonical lanes, but the admitted
     wave may contain any lane distribution, including several tickets from
     one lane or none from another.
   - A hard-guard observation-restoration wave remains the single-spec
     exception and may not queue ordinary delivery behind it. Its only output
     class is `guard_restoration` / `metric_observation`, its `guard_id` equals
     the configured guard bound by `objective_contribution`, and ordinary
     specs may not use that class.

13. `lifecycle_contract`
   - Uses `status: todo`, no claim, satisfied dependencies, and a valid
     optional human gate.

14. `pure_planner_output`
    - The result is a spec plus gaps/rejections only.
   - No ticket write, worker spawn, review send, report write, or external
     mutation happened inside planning.

15. `single_adaptive_planner`
   - One planner owns global sampling, progressive retrieval, proposal
     generation, dedupe, and ranking in both global and reserved-area scope.
   - No area planner subagents, area Pulses, or separate ranking implementation
     were introduced; reserved scope exists only from an explicit caller
     allocation.

## Finish Gate

```text
accept(candidate)
  -> pass only when all gates pass
  -> reject when duplicate, vague, unsafe, blocked, ungrounded, or low leverage
```
