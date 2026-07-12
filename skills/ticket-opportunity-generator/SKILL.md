---
name: ticket-opportunity-generator
description: "Plan the next ticket wave when Work Pulse finds no unclaimed executable work, using areas, KPI/guard state, adaptive history, dedupe, and global ranking to return complete specs or an explicit empty wave."
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

This skill is Farplane's one pure next-wave planner. Work Pulse calls it when
no unclaimed executable ticket or due check-in exists, even when human-active
tickets remain on the board. It converts planning areas, project objectives,
metric state, adaptive ticket history, and current context into at most
`wave_size` executable ticket specs.

The planner stays in one agent context. It reads the latest `N` compact ticket
rows across all areas first, then progressively filters by AI-planned origin,
area, KPI, status, Reward outcome, or a wider history window only when the
global sample is insufficient. It never spawns one planner per area.

The package keeps its existing name to reuse the current owner surface. Its
callable contract is `plan_next_wave(...)`.

Questions such as “what enters the next wave?”, “the board is empty; what
next?”, or “how should Work Pulse gather history?” are direct calls to this
contract even when the caller does not name the skill. Return the decision
protocol and ticket-spec shape; do not replace it with a generic options/advice
answer.

This skill owns ticket-wave admission over `advise`. Comparing candidates may
use option reasoning internally, but the response must still end in the
planner contract below. When `wave_size` is omitted, use `1`.

## Required Response Contract

Every planner response must use these top-level keys, in this order:

```yaml
global_query_receipt: {}  # or source_gap when no history input exists
diagnosis: {}
progressive_queries: []
candidate_comparison:
  - candidate:
    expected_delta:
    confidence:
    duration:
    signal_delay:
    cost:
    risk:
    reversibility:
    information_gain:
    compounding_value:
    interference:
    prerequisites: []
    human_load:
    ranking_result:
decision:
  admitted_specs: []
  duplicate_rejections: []
  deprioritized_candidates: []
  source_gaps: []
  human_request: null
  unused_capacity_reason: null
```

Rules that override the instinct to keep the board busy:

1. A stale or unknown hard guard blocks every ordinary delivery spec. A safe
   bounded observation-restoration spec may enter alone; delivery is not queued
   inside the same wave.
2. Rejecting a duplicate does not authorize adjacent adoption, proof, docs,
   rollout, or integration work. Admit such work only when independent evidence
   names a distinct unresolved bottleneck. Otherwise return `admitted_specs: []`
   and `unused_capacity_reason: recent_duplicate_no_distinct_move`.
3. A selected candidate is not admitted until its complete
   `executable_ticket_spec` is present. A recommendation, sequence, “track,” or
   ticket title is not a spec.
4. `candidate_comparison` must explicitly cover expected delta, confidence,
   duration, signal delay, cost, risk, reversibility, information gain,
   compounding value, interference, prerequisites, and human load for every
   plausible move. Do not compress these into generic pros/cons.
5. Say explicitly that one planner owns global-first retrieval and ranking; do
   not imply area planners, parallel planning lanes, or per-area admission.

The planner does not write tickets, claim work, spawn workers, send review
requests, or mutate goals, metrics, automations, reports, or external systems.
`pulse-update` owns those state changes. `interval-update` may supply dated
findings and suggestions as context, but it is not a wrapper around this skill.

Capability skills own domain workflows. A planned ticket may name the best
capability skill and its input/output contract; the planner must not copy that
skill's procedure into the ticket.

## Non-Negotiable Decision Protocol

For every call, return evidence for these five steps in order:

1. `global_query_receipt`: latest 20 compact rows with no area/origin filter.
2. `diagnosis`: objective/guard state, area attention distribution, AI origin,
   KPI movement, terminal Reward outcomes, and the named bottleneck.
3. `progressive_queries`: only the conditional filters or wider window actually
   needed, each with its receipt; use `[]` when the global sample is sufficient.
4. `candidate_comparison`: compare every plausible move on expected delta,
   confidence, duration, signal delay, cost, risk, reversibility, information
   gain, compounding value, interference, prerequisites, and human load.
5. `decision`: complete executable specs or an empty wave plus exact duplicate,
   guard, source-gap, authority, or low-leverage reason.

Never invent filler after rejecting a duplicate. Never omit a required field to
fit `wave_size`; a partial spec is a rejection, not an admitted ticket. When an
unknown hard guard cannot be safely restored, return zero specs plus the exact
source gap or one human request.

## Skill Signature

```text
plan_next_wave(harness_areas, metric_objectives, metric_state, ticket_history_query,
               current_context?, wave_size = 1)
  -> ranked_ticket_specs[0..wave_size]
   + duplicate_rejections[]
   + deprioritized_candidates[]
   + source_gaps[]
   + human_request?

state:
  reads(harness or farplane/harness.yaml, selected metric refs plus metric definitions from
        farplane/metrics.yaml, current readings from .farplane/metrics/,
        latest N active and archived ticket summaries from query_ticket_history.py,
        progressively filtered ticket outcomes/progress/proof when needed,
        latest dated interval suggestions?,
        current provider context such as Feed Scout?, capability skill refs?)
  writes(none)

gates:
  objective_boundary_present; areas_loaded; metric_state_loaded;
  global_history_loaded_before_filters; current_context_labeled;
  project_value_boundary_passed; area_distribution_inspected; bottleneck_named; levers_enumerated;
  compounding_value_considered; proposal_trajectories_compared; candidates_ranked; depriorities_explained;
  candidate_moves_deduped; wave_size_respected; executable_now;
  exact_output_named; proof_and_stop_named; authority_safe;
  capability_ref_valid_or_omitted; honest_objective_contribution_named;
  qa_checklist_passed

routes:
  pulse-update | impl-plan | goal-advisor | review | feed-scout

fails:
  writes_ticket_or_spawns_worker; requires_product_controller;
  spawns_area_planners; filters_before_global_history; treats_ticket_count_as_value;
  selects_speculative_harness_self_improvement;
  creates_ticket_to_plan_more_tickets; duplicates_active_or_recent_work;
  invents_metric_or_evidence; copies_domain_skill_workflow;
  returns_vague_or_human-gated_work_as_executable
```

## Phase Boundary

```text
Interval -> dated problem reports and grounded maintenance candidates
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
  - [ ] Resolve `harness`, `areas`, `metric_objectives`, `metric_state`, a
        `ticket_history_query` callable, optional
        current context, and `wave_size`.
  - [ ] When loading project files directly, bind identity, areas, objective
        priorities, and guard refs from `farplane/harness.yaml`; resolve each
        selected metric's direction, freshness, and guard rule from
        `farplane/metrics.yaml`. Load current readings from ignored metric
        observations or the project snapshot. Do not require
        provider bindings to rank project work unless a candidate's executability
        depends on them.
  - [ ] Read [qa_checklist.md](qa_checklist.md) before accepting specs.
  - [ ] Label missing, stale, or contradictory inputs as source gaps; do not
        fill them with assumptions that change value direction or authority.
  - [ ] Treat an unknown or stale hard guard as admission-blocking. Return only
        a bounded observation-restoration ticket when it can safely restore the
        guard; otherwise return a human request or no specs.
  - [ ] Omit unselected non-guard observations from ordinary planner context
        unless current evidence makes one necessary for a specific candidate.
- [ ] 2. Build one compact context snapshot.
  - [ ] First call
        `python3 skills/ticket-opportunity-generator/scripts/query_ticket_history.py --project-root <root> --limit <N>`
        with no area/origin filter. Default `N` is 20.
  - [ ] Inspect area distribution, AI-planned versus direct/unknown origin,
        recent outcomes, rejected/failed attempts, active commitments, review
        backlog, objective signals, and material external changes.
  - [ ] Treat ticket distribution as an attention diagnostic, not value. An
        area with few tickets warrants deeper retrieval only when its metric,
        obligation, or planner instruction indicates missing progress.
  - [ ] Progressively query `origin=ai_planned`, one area/KPI/status/Reward
        outcome, or a larger limit only when the first sample cannot support
        dedupe, attribution, or ranking. Record every query receipt.
  - [ ] Treat dated Interval, Feed Scout, and provider reports as optional
        evidence, not planning authority. A missing report is a source gap only
        when its evidence is necessary for the decision.
- [ ] 3. Enumerate area levers and candidate moves.
  - [ ] Name the current objective bottleneck before proposing tickets.
  - [ ] Enumerate relevant levers such as direct deliverables, customer or
        distribution work, product reliability, instrumentation, project
        operations, reusable assets, operational automation, and user-facing
        documentation.
  - [ ] Generate materially different moves across under-moving or
        bottleneck-relevant areas before
        ranking; do not turn every lever into a ticket.
  - [ ] Treat self-improvement as one area in the same global ranking. Admit a
        process/harness candidate only when an observed failure, terminal
        Reward outcome, guard regression, or toy/eval proof supports its causal
        change. Reject speculative cleanup and internal activity artifacts.
- [ ] 4. Rank the highest-leverage safe moves.
  - [ ] Prefer direct progress on the current objective or bottleneck over
        maintenance, meta-work, or speculative infrastructure.
  - [ ] Rank by objective impact, bottleneck relief, urgency, proof speed,
        compounding reuse, cost, risk, and human-review load. Compounding value
        strengthens a real project move; it does not justify speculative platform
        work by itself.
  - [ ] Compare each plausible move as a trajectory with expected metric
        delta, confidence, duration, time to signal, cost, risk, reversibility,
        information gain, compounding value, interference, and prerequisites.
  - [ ] Prefer a portfolio that preserves hard guards and contains
        non-interfering moves; do not select the easiest immediate metric delta
        when a slower prerequisite, probe, or compounding move has higher
        discounted expected value.
  - [ ] Compare against active and recent tickets by intended outcome,
        artifact, target surface, and evidence—not title alone.
  - [ ] Reject duplicates, already-completed work, and tickets whose only
        output is another plan or recommendation for what to ticket.
  - [ ] Return explicit deprioritization reasons for plausible moves that lost
        the ranking, especially when they are slower, less direct, duplicated,
        risky, or weakly evidenced self-improvement work.
- [ ] 5. Crystallize `0..wave_size` executable specs.
  - [ ] Name exact inputs, output artifact or state change, selected `area_id`,
        scope, capability skill when useful, KPI/guard contribution, causal
        mechanism, proof, stop condition, authority boundary, human gate, and
        dependency state.
  - [ ] Every proactive spec must bind an existing KPI or selected guard and
        include its metric provider, expected change, signal horizon,
        `check_in_at` when delayed, expected Reward, and proof route. Return no
        spec when no honest binding exists; never use `none mechanical` or
        invent a KPI.
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
  area_id:
  lifecycle:
    status: todo
    depends_on: []
    human_gate: none | [tag, reason]
  objective_contribution:
    kpi_or_guard_id:
    causal_mechanism:
    expected_change:
    metric_provider:
    signal_horizon:
    check_in_at: null
  reward:
    expected_reward:
    proof_route:
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
    planning_area:
    creation_reason:
    bottleneck:
    lever:
    objective_impact:
    bottleneck_relief:
    proof_speed:
    compounding_value:
    cost_risk_review_load:
    why_now:
  trajectory:
    expected_metric_delta:
    confidence:
    duration:
    time_to_signal:
    cost:
    risk:
    reversibility:
    information_gain:
    compounding_value:
    interference:
    prerequisites: []
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
- Planning areas are retrieval/ranking views, not ticket metadata, worker
  pools, quotas, controllers, or separate planning contexts.
- Self-improvement can win the global ranking, but only from concrete behavior
  evidence. Its presence as an area is not a standing quota.
- A capability skill is a callable workflow, not a reason to create a local
  controller, strategy file, or dedicated Pulse.

## Reference Map

- [qa_checklist.md](qa_checklist.md) - load before accepting candidate specs
  and apply again before return.
- [opportunity reviewer handoff](references/opportunity-reviewer-handoff.md) -
  use only when a material candidate needs independent ticket-spec review.
- [ticket template](../../tickets/templates/ticket.md) - current file contract
  used by Pulse when it materializes an accepted spec.
- [ticket history query](scripts/query_ticket_history.py) - compact global-first
  history with optional progressive filters.
