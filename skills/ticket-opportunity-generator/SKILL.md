---
name: ticket-opportunity-generator
description: "Turn a project program, objective contract, ticket history, and current context into a ranked bounded wave of executable BAU ticket specs."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.3.7"
  skill-eval-task: "0.2.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Glob, Grep, Bash
---

# Ticket Opportunity Generator

## Context

This skill is Farplane's pure BAU next-wave planner. Work Pulse calls it when
no executable ticket or due check-in exists. It converts the stable project
program, objective contract, ticket history, and current context into at most
`wave_size` executable ticket specs that directly advance the project's work.

The package keeps its existing name to reuse the current owner surface. Its
callable contract is `plan_next_wave(...)`.

The planner does not write tickets, claim work, spawn workers, send review
requests, or mutate goals, metrics, automations, reports, or external systems.
`pulse-update` owns those state changes. `interval-update` may supply dated
findings and suggestions as context, but it is not a wrapper around this skill.

Capability skills own domain workflows. A planned ticket may name the best
capability skill and its input/output contract; the planner must not copy that
skill's procedure into the ticket.

## Skill Signature

```text
plan_next_wave(program, objective_contract, ticket_history,
               current_context?, wave_size = 1)
  -> ranked_bau_specs[0..wave_size]
   + duplicate_rejections[]
   + deprioritized_candidates[]
   + source_gaps[]
   + human_request?

state:
  reads(program or farplane/harness.md, objective contract or
        farplane/goals.yaml + farplane/metrics.yaml,
        active and archived ticket summaries,
        ticket outcomes/progress/proof, latest dated interval suggestions?,
        current provider context such as Feed Scout?, capability skill refs?)
  writes(none)

gates:
  objective_boundary_present; history_loaded; current_context_labeled;
  bau_boundary_passed; bottleneck_named; levers_enumerated;
  compounding_value_considered; candidates_ranked; depriorities_explained;
  candidate_moves_deduped; wave_size_respected; executable_now;
  exact_output_named; proof_and_stop_named; authority_safe;
  capability_ref_valid_or_omitted; honest_objective_contribution_named;
  qa_checklist_passed

routes:
  pulse-update | impl-plan | goal-advisor | review | feed-scout

fails:
  writes_ticket_or_spawns_worker; requires_product_controller;
  selects_harness_self_improvement; selects_planner_or_framework_maintenance;
  creates_ticket_to_plan_more_tickets; duplicates_active_or_recent_work;
  invents_metric_or_evidence; copies_domain_skill_workflow;
  returns_vague_or_human-gated_work_as_executable
```

## Phase Boundary

```text
Interval -> dated BAU problem reports and bounded known-maintenance tickets
planner  -> executable ticket specs only
Pulse    -> ticket files, admission, claims, dispatch, receipts, reports
worker   -> ticket/program/progress/proof execution
```

The first prototype refills only when no executable `status: todo` ticket or
due `waiting_signal` check-in exists. A
low-watermark refill is a later optimization and needs separate duplicate and
review-load proof.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the planning frame.
  - [ ] Resolve `program`, `objective_contract`, `ticket_history`, optional
        current context, and `wave_size`.
  - [ ] When loading project files directly, bind `program` from
        `farplane/harness.md` and the objective contract from
        `farplane/goals.yaml` plus `farplane/metrics.yaml`. Do not require
        provider bindings to rank BAU work unless a candidate's executability
        depends on them.
  - [ ] Read [qa_checklist.md](qa_checklist.md) before accepting specs.
  - [ ] Label missing, stale, or contradictory inputs as source gaps; do not
        fill them with assumptions that change value direction or authority.
- [ ] 2. Build one compact context snapshot.
  - [ ] Summarize active commitments, recent outcomes, failed or abandoned
        attempts, review backlog, current bottleneck, objective signals, and
        material external changes.
  - [ ] Treat dated Interval, Feed Scout, and provider reports as optional
        evidence, not planning authority. A missing report is a source gap only
        when its evidence is necessary for the decision.
- [ ] 3. Enumerate BAU levers and candidate moves.
  - [ ] Name the current objective bottleneck before proposing tickets.
  - [ ] Enumerate relevant levers such as direct deliverables, customer or
        distribution work, product reliability, instrumentation, project
        operations, reusable assets, operational automation, and user-facing
        documentation.
  - [ ] Generate materially different moves across the relevant levers before
        ranking; do not turn every lever into a ticket.
  - [ ] Reject candidates whose primary outcome is improving Farplane's own
        harness, planner policy, skill system, self-improvement machinery,
        framework automation, framework doctrine/docs, hooks/validators, or
        feature registries. Weekly Dogfood self-improvement owns those bets.
- [ ] 4. Rank the highest-leverage safe moves.
  - [ ] Prefer direct progress on the current objective or bottleneck over
        maintenance, meta-work, or speculative infrastructure.
  - [ ] Rank by objective impact, bottleneck relief, urgency, proof speed,
        compounding reuse, cost, risk, and human-review load. Compounding value
        strengthens a real BAU move; it does not justify speculative platform
        work by itself.
  - [ ] Compare against active and recent tickets by intended outcome,
        artifact, target surface, and evidence—not title alone.
  - [ ] Reject duplicates, already-completed work, and tickets whose only
        output is another plan or recommendation for what to ticket.
  - [ ] Return explicit deprioritization reasons for plausible moves that lost
        the ranking, especially when they are slower, less direct, duplicated,
        risky, or self-improvement work.
- [ ] 5. Crystallize `0..wave_size` executable specs.
  - [ ] Name exact inputs, output artifact or state change, scope, capability
        skill when useful, objective contribution, proof, stop condition,
        authority boundary, human gate, and dependency state.
  - [ ] Use an honest project metric/reward when the objective contract
        provides one. Otherwise use a reviewable contribution and state
        `none mechanical`; never invent a KPI.
  - [ ] Return no spec and one `human_request` when the next move requires an
        objective, authority, credential, destructive, deploy, spend,
        publish, account, or external-contact decision.
- [ ] 6. Apply ticket-quality gates.
  - [ ] Run [qa_checklist.md](qa_checklist.md) against each candidate.
  - [ ] For a material candidate whose safety or architecture cannot be made
        executable within current authority, return it as a review request or
        source gap—not an admitted ticket.
- [ ] 7. Return specs to the caller.
  - [ ] Include accepted specs, duplicate rejections, source gaps, and the
        reason fewer than `wave_size` tickets survived.
  - [ ] Do not write files, claim tickets, spawn workers, or perform the work.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Ticket Spec Contract

```yaml
executable_ticket_spec:
  title:
  lifecycle:
    status: todo
    depends_on: []
    human_gate: none | [tag, reason]
  objective_contribution:
    objective_ref:
    expected_change:
    metric_or_review: "<metric ref> | none mechanical"
  execution:
    inputs: []
    output:
    capability_skill:
    scope_in: []
    scope_out: []
    stop_condition:
  proof:
    checks: []
    evidence_artifact:
    review_question:
  dedupe:
    compared_against: []
    decision: novel | materially_distinct
  source_gaps: []
  ranking:
    bottleneck:
    lever:
    objective_impact:
    bottleneck_relief:
    proof_speed:
    compounding_value:
    cost_risk_review_load:
    why_now:
```

Use the current ticket template when Pulse materializes the spec. The spec may
omit optional fields that add no execution or proof value.

## Gotchas

- A specific ticket can still be low leverage; objective contribution is a
  gate, not decoration.
- `wave_size` is a maximum, not a quota. One strong ticket or no ticket is
  valid.
- Fresh external context can change priority without becoming durable program
  truth.
- BAU is defined by the candidate's primary outcome, not its file extension.
  Product documentation, customer-facing features, product code, operational
  automation that performs project work, and reliability fixes can be BAU.
  A ticket primarily changing Farplane's planner, agent harness, skills,
  framework automations, doctrine, or self-evaluation is self-improvement.
- In the Farplane repo itself, shipping a user-facing Farplane capability can
  be BAU; changing the internal harness that chooses or executes work is not.
- A capability skill is a callable workflow, not a reason to create a local
  controller, strategy file, or dedicated Pulse.

## Reference Map

- [qa_checklist.md](qa_checklist.md) - load before accepting candidate specs
  and apply again before return.
- [opportunity reviewer handoff](references/opportunity-reviewer-handoff.md) -
  use only when a material candidate needs independent ticket-spec review.
- [ticket template](../../tickets/templates/ticket.md) - current file contract
  used by Pulse when it materializes an accepted spec.
