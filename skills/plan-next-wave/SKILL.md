---
name: plan-next-wave
description: "Select and bind the strongest configured project-skill calls without writing tickets."
tier: 3
group: operations
source: local
template_uses:
  skill-template: "0.3.9"
  skill-eval-task: "0.2.0"
  skill-surface-budget: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Glob, Grep, Bash
---

# Plan Next Wave

## Context

Plan Next Wave is Farplane's pure work selector. It does not invent ticket
types or workflows. It chooses only from `farplane/harness.yaml#planning.skill_refs`,
reads each selected skill's `planner_contract` and signature, binds its
arguments from current evidence, ranks the resulting calls, and returns
`0..wave_size` call IDs. Work Pulse alone materializes tickets.

Areas are passive ICP and metric context. Lanes, proposal types, archetype
registries, and specialized ticket templates are not planning inputs.

This workflow runs only at the portfolio boundary when the executable board
needs refill. It never participates in `choose_next` inside an active Goal;
Goal Advisor compiles a selected leaf and the domain Goal owns its decisions.

## Skill Signature

```text
plan_next_wave(planning_skill_refs, problems, areas, metric_objectives, metric_state,
               ticket_history_query, current_context?, world_memory?,
               preference_memory?, wave_size = 1)
  -> input_receipts + proposed_skill_calls[] + admitted_call_ids[]
   + rejections[] + source_gaps[] + validation_receipt

state:
  reads(farplane/harness.yaml planning skill allowlist, stable problems, and passive areas,
        docs/systems and docs/features registries,
        allowed skill SKILL.md signatures and planner_contracts,
        farplane/metrics.yaml and observations, global-first ticket history,
        World Memory for outward calls, terminal preference evidence,
        optional dated Dogfood context, qa_checklist.md and golden)
  writes(no durable project state; ignored validator scratch only)

gates:
  fresh_hard_guards; configured_skill_only; required_arguments_bound;
  strategic_system_bound; evidence_stage_correct;
  global_history_first; evidence_grounded; canonical_icp_when_relevant;
  understandable_call; direct_artifact; honest_objective_contribution;
  rationale_consistent; falsifier; dedupe; authority_safe; non_interference;
  wave_size_respected

routes: pulse-update | configured project capability skill | review

fails:
  invents_workflow; invents_lane_or_proposal_type; writes_ticket; materializes;
  copies_skill_procedure; admits_unconfigured_skill; maintenance_as_value;
  random_feature_work; generic_market_report; skips_evidence_stage;
  contradictory_call; duplicates_recent_call; repeats_full_call_or_forecast;
  fake_ultimate_outcome
```

## Decision Loop

1. Read `planning.skill_refs`, then read each allowed skill's `SKILL.md` and
   `planner_contract`. Missing or unresolved skills are source gaps, never
   substituted workflows.
2. Check fresh hard guards. On stale, missing, or failing guards, return an
   empty wave and the caller-owned source gap; never create a refresh ticket.
3. Read the latest 20 tickets globally, then query deeper only for dedupe or
   terminal preference evidence. Read World Memory before outward-facing calls.
4. Bind each market-learning, ablation, or content call to one configured
   stable problem plus canonical `system_ref` and coherent `feature_refs`.
   Reject random features and work that cannot address a configured problem.
5. Select the missing evidence stage without copying its workflow:
   - no current ICP pain evidence -> `farplane-market-learning`;
   - current pain evidence but no comparative proof -> `farplane-ablation-proof`;
   - accepted proof -> `farplane-content-creation`;
   - accepted product delta -> `farplane-productization` using its own existing
     accepted-result contract.
   A configured skill may be skipped when its prerequisite evidence is absent.
6. Generate only bound invocations of allowed skills. The skill identity is the
   work type; its signature owns the workflow. Bind exactly the declared
   `required_arguments`; Pulse separately owns ticket creation and context.
   When a planner contract declares `admission_contract`, inspect that
   workstream first and attach an `admit` receipt. Return `hold`,
   `preempt_request`, or `reject` as a rejection, never as a proposed call.
7. Reject calls that are maintenance-only, duplicate, vague, unsafe, blocked,
   unsupported, internally contradictory, or whose value exists only in setup,
   reports, tests, schemas, or proof receipts. A call's arguments, evidence,
   why-now rationale, objective contribution, and falsifier must describe one
   consistent premise. Self-improvement requires reproduced failure evidence.
8. Rank the remaining calls once by objective impact, evidence, time to signal,
   risk, cost, reversibility, interference, and human load. Return fewer than
   `wave_size` rather than fill capacity.
9. Follow [the compact skill-call contract](references/skill-call-contract.md)
   and [response contract](references/response-contract.md). Run
   `scripts/validate_wave_response.py` against the exact final JSON.
10. Return exactly one JSON object with no prose. Record that Plan wrote and
   materialized nothing and Pulse is the sole materialization owner.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read configured planning skills, their signatures and planner contracts,
      stable problems and canonical system/feature refs, metric movement/guards,
      passive area ICP context, World Memory when relevant,
      current context, and global-first history/preference evidence.
- [ ] 2. Stop with an empty wave on an unhealthy hard guard or unresolved skill.
- [ ] 3. Select the missing evidence stage; bind problem, system, and feature
      refs when the selected `planner_contract` declares them; enforce any
      admission contract; then produce only compact configured-skill calls with
      exactly the required arguments bound.
- [ ] 4. Reject maintenance, workflow invention, duplicates, vague calls,
      unsupported impact, unsafe authority, and self-improvement without a
      reproduced failure.
- [ ] 5. Rank all valid calls once; admit only the best compatible
      `0..wave_size` call IDs.
- [ ] 6. Run the validator on the exact final object, reapply `qa_checklist.md`,
      and return JSON with a no-materialization receipt.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [Golden skill call](examples/golden/compelling-proposal.md) — calibration only.
- [Skill-call contract](references/skill-call-contract.md) — canonical call shape.
- [Response contract](references/response-contract.md) — exact decision envelope.

## Gotchas

- A configured skill is permission to call that workflow, not evidence that a
  particular call is valuable.
- Areas may supply ICP and metrics but never generate or reserve work.
- Stable problems constrain refill; system and feature registries keep proposed
  solution evidence coherent without storing mutable solution bets in the harness.
- Plan Next Wave performs only the bounded comparison needed to admit configured
  skill calls. It does not invoke `leverage-advisor` during refill; use that
  separate operator-facing workflow for a capability roadmap or contingent
  compounding campaign.
- A validator proves contract integrity, not human interest; human preference
  remains delayed bootstrap evidence.

## Output

One validated JSON decision with input/skill receipts, canonical proposed skill
calls, admitted call IDs, rejections/gaps, and a no-materialization receipt.
