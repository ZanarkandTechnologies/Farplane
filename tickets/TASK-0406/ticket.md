---
template_id: ticket-template
template_version: "0.2.3"
feature_refs:
  - FEAT-0007
  - FEAT-0063
  - FEAT-0067
  - FEAT-0071
ticket_id: TASK-0406
title: "Simplify the metric-to-ticket control loop"
status: awaiting_review
priority: high
created_at: 2026-07-24T00:00:00+08:00
updated_at: 2026-07-24T00:00:00+08:00
---

# TASK-0406: Simplify the metric-to-ticket control loop

## Summary

Make Farplane's mutable strategy equal to its ticket board. Every quantitative
metric gets direction-normalized movement; Daily and Weekly Interval use the
same first-principles problem-to-ticket review over different evidence windows;
known work is admitted immediately after the report; and Plan Next Wave remains
the lean refill planner only when evidence has not already produced executable
work.

Retire the duplicate project strategy surfaces: `harness.yaml#goals`,
`identity.product_bets`, and the uncalled `update-strategy` skill. Add one
optional timezone-bearing ticket `due_at`, and preserve native ticket Goal
Packets as the execution mechanism rather than confusing them with the removed
project-level goal array.

## Scope

- In:
  - require `maximize` or `minimize` direction for every quantitative metric
    definition
  - derive raw delta, elapsed time, raw velocity, direction-normalized progress
    delta/velocity, and improving/flat/worsening momentum from consecutive
    available observations
  - make the derived movement available in Core metric cards without requiring
    separately declared growth metrics
  - make Daily and Weekly Interval run the same full first-principles review,
    with cadence changing evidence coverage rather than decision quality
  - identify stalled or worsening movement, distinguish symptom from root
    cause, select the dominant bottleneck, rebuild the simplest correct path,
    and compare compounding interventions
  - create, update, reprioritize, date, or reject stale `todo` tickets when the
    problem and next intervention are sufficiently grounded
  - admit an investigation ticket only when its output is decision-changing
    evidence: reproduced cause, ruled-out alternatives, selected correction,
    and proof artifact
  - require every admitted ticket to produce a concrete artifact, behavior,
    experiment result, or outcome; planning-only tickets are invalid
  - remove arbitrary Interval ticket-count caps in favor of materiality,
    executability, concrete proof, dedupe, authority, and coherence gates
  - add optional timezone-bearing `due_at` to ticket metadata, board adapters,
    Core projections, planner materialization, and Pulse ordering
  - order executable tickets by priority, then earliest `due_at` with missing
    dates last, then ticket ID
  - remove `harness.yaml#goals`, its validation, planner inputs, goal-state
    diagnosis, deadline fingerprinting, templates, examples, tests, and docs
  - remove `identity.product_bets` and replace live planner/capability bindings
    with stable problem, area, objective metric, system, and feature context
  - delete the uncalled `update-strategy` package and redirect its remaining
    active references to Interval or Plan Next Wave
  - update canonical feature/system/framework docs and regenerate inventories
- Out:
  - changing native Codex Goal mode, `goal-advisor`, ticket Goal Packets,
    `program.md`, or `progress.md`
  - physically deleting ticket history; Interval retires stale work through the
    existing rejected state and a reason
  - letting Interval execute tickets, run workers, mutate terminal evidence, or
    perform external/destructive actions
  - replacing objective metrics, guards, areas, configured planning skills, or
    stable identity problems
  - creating a new war-room skill, strategy report, campaign ledger, momentum
    metric definition, scheduler, or hidden orchestration state
  - treating raw ticket count, raw agent hours, or activity volume as success
  - removing ordinary uses of the word “goal,” including user goals,
    non-goals, metric targets owned by guard definitions, or ticket execution
    Goals

## Delta

```text
overall_before:
  - Metrics expose current values and a raw daily_diff, but movement is not normalized by the configured optimize direction and no comparable velocity contract exists.
  - Interval is intentionally restricted to BAU reporting and capped direct maintenance; uncertain interventions and new directional thinking wait for planner refill.
  - Project strategy is duplicated across identity.product_bets, harness goals, update-strategy, planner inputs, reports, and tickets.
  - Tickets have priority but no delivery deadline; Pulse breaks priority ties by ticket ID.
overall_after:
  - One metric definition produces value plus derived movement and direction-normalized momentum for every observation pair.
  - Every Daily and Weekly Interval performs the same evidence-to-bottleneck-to-ticket review, differing only in evidence window and recurrence coverage.
  - Stable intent lives in identity problems, areas, metrics, and configured skills; all mutable strategy is represented by ticket additions, updates, reprioritization, dating, or rejection.
  - Plan Next Wave refills a weak board but never delays a grounded ticket; Pulse orders same-priority work by due_at before ticket ID.
why_now:
  - The current separate strategy and goal inputs add latency and naming confusion even though execution and proof already converge on tickets.
problems:
  - before: Each metric can require a second manually declared growth metric or cadence-specific interpretation.
    after: Core derives comparable movement from consecutive observations and the metric's maximize/minimize direction.
    why_now: Interval needs a uniform signal for acceleration, stall, and regression without multiplying metric definitions.
  - before: Interval can observe a material problem yet defer a known or testable intervention to a later low-watermark refill.
    after: The same Interval run writes the report and then mutates the board when admission gates pass.
    why_now: Known work should not wait for a separate planner.
  - before: update-strategy sounds like the Interval strategy owner but has no live automation caller.
    after: Its useful first-principles moves belong directly to Interval; the unused package and active references are removed.
    why_now: One review owner is easier to invoke, test, and understand.
  - before: Product bets and dated project goals duplicate solution and urgency state outside tickets.
    after: Stable problems/objectives constrain planning; tickets carry chosen interventions, priority, due date, dependencies, and proof.
    why_now: The board becomes the inspectable strategy instead of one projection of several competing strategy stores.
  - before: Same-priority tickets cannot express delivery order except through ticket IDs.
    after: Optional due_at supplies an honest deadline without conflating strategic importance, delivery need, or Reward evaluation time.
    why_now: Deadline-aware kanban routing is a minimum scheduling contract.
first_principles_basis:
  objective: Convert observed movement and problems into the strongest proofable work with the least duplicated planning state.
  need: Agents must detect whether the system is improving, find the current constraint, and act without waiting for another strategy wrapper.
  assumptions:
    - Stable mission, problems, areas, configured skills, and objective metrics are sufficient context for refill planning.
    - Every quantitative metric can honestly declare maximize or minimize.
    - Ticket priority, due_at, dependencies, proof, and Reward are enough to represent current intervention strategy.
    - A dated Interval report should remain the audit snapshot before same-run ticket mutation.
  root_cause: Farplane split one feedback loop across report-only Interval, an uncalled strategy skill, mutable project targets, solution portfolios, and low-watermark planning.
  constraints:
    - Preserve one canonical ticket lifecycle and native Goal execution.
    - Preserve source-gap honesty and never calculate momentum across unavailable or incomparable observations.
    - Preserve configured kanban provider and authority boundaries.
    - Do not overwrite active, review, waiting-signal, or terminal ticket contracts during Interval.
    - Existing dirty changes on overlapping files must be merged, never reverted.
  first_viable_slice: Core movement projection, one consolidated Interval admission path, due_at routing, removal of duplicate strategy inputs, and contract/eval/doc proof.
  proof_or_falsification: Reject the design if it needs another strategy state file, creates planning-only tickets, calculates favorable momentum with missing/zero-time evidence, delays a grounded ticket until refill, or removes native ticket Goal execution.
  tradeoff: Remove product-bet portfolio validation and target/date goal urgency in exchange for one stable intent layer plus a directly inspectable ticket strategy.
  non_goals:
    - Optimizing for activity volume.
    - Predicting business outcomes from velocity alone.
    - Letting every observation automatically create work.
    - Making deadlines mandatory.
```

## Objective Contribution

```yaml
objective_contribution:
  ultimate_kpi_id: evidence_distribution_reach
  contribution_type: enabler
  kpi_or_guard_id: auto_completion_rate
  causal_mechanism: >-
    A single evidence-to-ticket control loop reduces planning latency and
    duplicate strategy state, allowing more grounded work to reach execution
    and proof without operator intervention.
  expected_change: >-
    Faster, more consistent conversion of material metric regressions and
    bottlenecks into accepted executable tickets.
  forecast_basis:
    kind: source_gap
    source_gap: >-
      No current observation isolates planning latency or autonomous completion
      changes caused by the duplicate strategy surfaces.
  metric_provider: local_project_metrics
  signal_horizon: first two completed Daily and Weekly Interval cycles after rollout
  check_in_at: unscheduled
```

## Reward

```yaml
kpi_rewards:
  - reward_id: task-0406-auto-completion-control-loop
    kpi_id: auto_completion_rate
    projection_type: enabler_result
    expected_reward: >-
      Faster, more consistent conversion of material metric regressions and
      bottlenecks into accepted executable tickets.
    check_in_at: unscheduled
    actual_result:
    decision:
    evaluated_at:
    evaluation_key:
    supersedes_evaluation_key:
    evidence_refs: []
guard: "do not reward ticket volume; count only accepted end-to-end behavior and honest metric movement"
```

## Change Plan

```text
architecture_signatures:
  module_level:
    - bin/core/farplane_project_snapshot.py / derive_metric_movement(direction, previous_point, current_point): movement | source_gap
    - skills/interval-update / analyze_control_loop(metric_movement, evidence, board): bottleneck + intervention_candidates
    - skills/interval-update / admit_ticket_delta(problem, intervention, board, authority): create | update | reject | candidate
    - skills/pulse-update/scripts/list_pulse_board.py / ticket_sort_key(priority, due_at, ticket_id): tuple
    - skills/plan-next-wave / plan_next_wave(planning_skill_refs, problems, metric_state, ticket_history_query, areas?, current_context?, world_memory?, preference_memory?, wave_size=1): proposed_skill_calls + admitted_call_ids
  main_flow:
    - metric observations -> directional movement -> Interval bottleneck review -> report -> ticket deltas -> Pulse dispatch
    - weak ready supply without grounded Interval work -> Plan Next Wave -> Pulse materialization -> ticket
  data_flow:
    - farplane/metrics.yaml#metrics.*.direction + observation[n-1:n] -> metric_card.series[].movement + metric_card.momentum
    - interval evidence + current board -> ticket frontmatter priority/due_at/status + ticket body proof contract
    - ticket frontmatter due_at -> WorkItem.dueAt + Core ticket projection + Pulse execution order
    - harness identity.problems + metric_refs + areas + planning.skill_refs -> Plan Next Wave input; no goals or product_bets
  builder_freeform_boundary:
    - Implementation below this level is builder-owned unless it changes canonical field names, strategy ownership, ticket admission gates, ordering semantics, native Goal boundaries, evidence behavior, or proof/reviewability.
```

### Change 1: Derive direction-normalized movement for every metric

```text
fixes:
  - Metrics currently expose raw daily_diff but not a universal direction-aware velocity or momentum contract.
before:
  - Only selected objective definitions must declare direction.
  - build_metric_card writes daily_diff from adjacent values regardless of elapsed time or optimize direction.
  - Missing, duplicate-date, and unavailable observations have no explicit movement contract.
after:
  - Every quantitative metric definition must declare direction: maximize or minimize.
  - Each available point after the first distinct prior observation carries raw_delta, elapsed_days, raw_velocity_per_day, progress_delta, progress_velocity_per_day, and momentum_state.
  - progress_delta and progress_velocity_per_day multiply the raw movement by +1 for maximize and -1 for minimize; positive means favorable for every metric.
  - momentum_state is improving, flat, or worsening from direction-normalized velocity; the first point, unavailable prior value, invalid date, or zero elapsed time yields unknown movement instead of an invented zero or infinity.
  - Metric cards expose latest movement as derived state; no separate ARR-growth, failure-momentum, or other duplicate metric definition is required.
read:
  - path: bin/core/farplane_project_snapshot.py
    reason: Existing observation, series, daily_diff, cumulative, target, and source-gap projection owner.
  - path: bin/validators/check_farplane_project_files.py
    reason: Existing metrics and selected-objective direction validation.
  - path: farplane/metrics.yaml
    reason: Migrate current definitions that do not yet declare direction.
  - path: skills/init-advisor/references/METRICS_TEMPLATE.yaml
    reason: Prevent new projects from recreating directionless metrics.
  - path: skills/metric-advisor/SKILL.md
    reason: Make direction and derived movement part of the advisory contract.
write:
  - path: bin/core/farplane_project_snapshot.py
    change: Add one local movement derivation seam and project movement into metric points/cards.
  - path: bin/tests/test_farplane_project_snapshot.py
    change: Cover maximize, minimize, ratio, daily flow, irregular elapsed days, first point, missing values, and duplicate-date/zero-time behavior.
  - path: bin/validators/check_farplane_project_files.py
    change: Require maximize/minimize on every quantitative metric definition, not only selected objectives.
  - path: bin/validators/test_check_farplane_project_files.py
    change: Prove directionless metrics fail and both directions pass.
  - path: bin/tests/test_farplane_project_file_validator.py
    change: Align object-level validator fixtures with the universal direction contract.
  - path: farplane/metrics.yaml
    change: Assign an honest direction to every existing metric definition.
  - path: skills/init-advisor/references/METRICS_TEMPLATE.yaml
    change: Require direction in generated metric examples.
  - path: skills/metric-advisor/SKILL.md
    change: Declare movement as derived output rather than a second authored metric.
operation:
  - Reuse build_metric_card and its ordered series; do not introduce a second metrics service or persisted movement ledger.
  - Preserve raw values and daily_diff for compatibility only if a current consumer still proves it is needed; otherwise replace daily_diff with the clearer movement object and update callers in the same change.
  - Compare distinct observation timestamps; never divide by zero or bridge a source gap as if it were a valid reading.
signature_or_type_impact:
  - metric_definition.direction becomes required for quantitative metrics.
  - metric_card.series[].movement and metric_card.momentum become derived projection fields.
routes:
  docs: doc-advisor
  qa: tests
  review: reviewer
qa:
  - A maximize move 10 -> 12 over two days yields raw_delta=2, raw_velocity_per_day=1, progress_velocity_per_day=1, improving.
  - A minimize move 10 -> 8 over two days yields raw_delta=-2, raw_velocity_per_day=-1, progress_velocity_per_day=1, improving.
  - A minimize move 8 -> 10 yields negative progress velocity and worsening.
  - Ratios and rates use the same arithmetic; no type-specific direction exception is added.
  - First, missing, stale, invalid-date, and same-timestamp cases never emit fake momentum.
failure_modes:
  - Treating percentage change as universally meaningful around zero.
  - Calculating movement from cumulative and raw values inconsistently.
  - Rewarding unfavorable movement because minimize direction was ignored.
  - Persisting derived momentum as another canonical metric.
```

### Change 2: Make Interval the first-principles review-to-ticket owner

```text
fixes:
  - Interval can see a material problem but is currently forbidden from completing the reasoning or admitting a testable uncertain correction.
  - update-strategy owns similar prose logic but has no live automation caller.
before:
  - Daily and Weekly are bounded BAU report profiles with maintenance-only, known-fix, capped recovery.
  - New direction, leverage comparison, and uncertain interventions wait for Plan Next Wave or another workflow.
  - maintenance_ticket_limit=1 can suppress a second independently material qualified correction.
after:
  - Daily and Weekly run one complete review algorithm over different evidence windows: read movement and outcomes, identify material stalls/regressions, select the dominant bottleneck, separate symptom/root cause, rebuild from the objective, compare compounding moves, and decide ticket deltas.
  - The report remains the immutable audit snapshot and is written before same-run board mutations.
  - Known problem + known intervention creates or updates a concrete solution ticket in the same Interval run.
  - Known problem + uncertain intervention creates an investigation/experiment ticket only when the required output is reproduced cause + ruled-out alternatives + selected correction + proof artifact.
  - Insufficiently grounded problems remain report candidates for later Plan Next Wave refill.
  - No numeric ticket cap remains; each ticket independently passes materiality, executability, artifact/proof, dedupe, authority, and largest-coherent-intervention gates.
  - Interval may reprioritize, add due_at, clarify, or reject stale todo tickets with reasons; it never rewrites active/review/waiting/terminal work or physically deletes history.
read:
  - path: skills/interval-update/SKILL.md
    reason: Runtime owner of Daily and Weekly review behavior.
  - path: skills/interval-update/references/interval-update.md
    reason: Cadence profiles, admission examples, and carry-forward rules.
  - path: skills/interval-update/templates/interval-report.md
    reason: Report must expose bottleneck reasoning and each admission decision without becoming another strategy store.
  - path: skills/interval-update/qa_checklist.md
    reason: Existing report/recovery guardrail must be replaced with the approved admission rule.
  - path: skills/update-strategy/SKILL.md
    reason: Source the useful root-cause, system-gap, experiment, and ticket-delta moves before deleting the duplicate owner.
  - path: tickets/TASK-0405/ticket.md
    reason: Preserve the accepted Interval highlight contract while changing the same report workflow.
  - path: tickets/TASK-0405/progress.md
    reason: Preserve current TASK-0405 decisions rather than relying on stale transcript context.
  - path: skills/interval-update/scripts/highlight_ledger.py
    reason: Keep report-finalized append ordering, sparse rows, idempotency, and the no-planning-input boundary intact.
  - path: skills/interval-update/scripts/test_highlight_ledger.py
    reason: Existing focused regression owner for TASK-0405 highlight persistence.
  - path: farplane/automations.toml
    reason: Daily/Weekly prompts must invoke the consolidated behavior directly.
write:
  - path: skills/interval-update/SKILL.md
    change: Replace maintenance-only/capped recovery with the full metric-to-bottleneck-to-ticket contract.
  - path: skills/interval-update/references/interval-update.md
    change: Define Daily versus Weekly evidence coverage and concrete create/update/reject/investigate examples.
  - path: skills/interval-update/templates/interval-report.md
    change: Add compact metric movement, dominant bottleneck, root-cause confidence, candidate comparison, and ticket-delta receipts.
  - path: skills/interval-update/qa_checklist.md
    change: Enforce material/executable/concrete/deduped admission and forbid planning-residue tickets.
  - path: skills/interval-update/evals/evals.json
    change: Replace report-only assumptions with known-fix, uncertain-cause, duplicate, stale-ticket, multiple-qualified-ticket, and no-grounded-work cases.
  - path: farplane/automations.toml
    change: Make both Interval prompts request the same full review with cadence-specific windows.
  - path: skills/update-strategy/
    change: Delete the package after its useful behavior and tests are represented in Interval.
  - path: skills/update-memory/SKILL.md
    change: Redirect strategy-planning guidance to Interval for evidence-driven review or Plan Next Wave for refill.
  - path: skills/harness-creator/SKILL.md
    change: Remove update-strategy routing and describe Interval/Pulse ownership.
operation:
  - Implement the approved admission predicate exactly: material problem AND executable next intervention AND concrete output/proof AND no active duplicate.
  - Prefer one largest coherent intervention per root problem; do not split analysis, design, implementation, and proof into planning-only tickets.
  - Keep source gaps and uncertain diagnosis visible rather than forcing admission.
  - Preserve the TASK-0405 post-report sequence: finalize the report, append independently selected sparse highlights without reading them as planning/correction input, then apply ticket deltas from report evidence and admission decisions.
  - Preserve report_complete_before_highlight_append, at-most-one win/failure per team, idempotent append, and Core highlight projection while rewriting Interval.
signature_or_type_impact:
  - Remove maintenance_ticket_limit from interval_update.
  - Replace maintenance_candidates/recovery_ticket_paths with candidate_interventions and ticket_deltas while preserving report and source-gap outputs.
routes:
  docs: doc-advisor
  qa: agent-qa-test
  review: reviewer
qa:
  - Behavior eval proves a same-run known correction creates/updates a ticket without Plan Next Wave.
  - Behavior eval proves an uncertain cause creates only the approved evidence-deliverable investigation ticket.
  - Behavior eval proves two independent material interventions may both be admitted without a fixed cap.
  - Behavior eval proves vague “plan strategy” work, duplicates, low-materiality chores, and artifact-free tickets are rejected.
  - Behavior eval proves active/review/terminal tickets are not silently rewritten.
  - Both Daily and Weekly invoke the same reasoning gates while reading different windows.
  - python3 skills/interval-update/scripts/test_highlight_ledger.py
  - Re-run the Interval highlight behavior eval and Core highlight projection tests from TASK-0405 after the consolidated Interval changes.
failure_modes:
  - Reintroducing a war-room wrapper or separate strategy report.
  - Treating more tickets as more momentum.
  - Letting Interval execute admitted work.
  - Rewriting ticket history or bypassing the configured board provider.
```

### Change 3: Make the ticket board the only mutable strategy state

```text
fixes:
  - Dated metric goals, solution-level product bets, and update-strategy duplicate state that ultimately has to become tickets.
before:
  - harness.yaml stores identity.product_bets and an optional goals array.
  - Product-facing planner skills require product_bet_ref, system_ref, and feature_refs.
  - Pulse fingerprints goal deadline/urgency state and Plan Next Wave returns goal_state diagnosis.
after:
  - harness identity keeps mission, human thesis, north star, and stable problems; areas, objective metrics, guards, and configured planning skills remain.
  - identity.product_bets and harness goals are unsupported active fields and are removed from project/template data.
  - Product-facing planning skills bind a stable problem_ref plus the relevant system_ref/feature_refs when those refs are part of their actual public input.
  - Mutable solution choice, urgency, order, due date, and proof live only on tickets.
  - Native ticket Goal Packets remain the execution compiler/runtime context and are explicitly distinguished in docs.
read:
  - path: farplane/harness.yaml
    reason: Current product bets, goals, identity problems, metrics, areas, and skill allowlist.
  - path: skills/init-advisor/references/HARNESS_TEMPLATE.yaml
    reason: New-project source template.
  - path: bin/validators/check_farplane_project_files.py
    reason: Product-bet and goal validation owner.
  - path: .agents/skills/farplane-market-learning/SKILL.md
    reason: Current product_bet_ref planner contract.
  - path: .agents/skills/farplane-ablation-proof/SKILL.md
    reason: Current product_bet_ref planner contract.
  - path: .agents/skills/farplane-content-creation/SKILL.md
    reason: Current product_bet_ref planner contract.
write:
  - path: farplane/harness.yaml
    change: Remove identity.product_bets and goals; preserve stable problems, metrics, areas, and configured skills.
  - path: skills/init-advisor/references/HARNESS_TEMPLATE.yaml
    change: Generate the simplified harness shape.
  - path: bin/validators/check_farplane_project_files.py
    change: Remove product-bet and goal schema paths; reject them as unsupported rather than keeping compatibility parsing.
  - path: bin/validators/test_check_farplane_project_files.py
    change: Remove portfolio/goal acceptance tests and add lean harness plus rejection fixtures.
  - path: bin/tests/test_farplane_project_file_validator.py
    change: Remove goals fixtures and prove the simplified current project passes.
  - path: .agents/skills/farplane-market-learning/SKILL.md
    change: Replace product_bet_ref with problem_ref and retain decision-changing system/feature grounding.
  - path: .agents/skills/farplane-ablation-proof/SKILL.md
    change: Replace product_bet_ref with problem_ref and keep claim/surface/baseline proof.
  - path: .agents/skills/farplane-content-creation/SKILL.md
    change: Replace product_bet_ref with problem_ref and keep audience/evidence/content-goal grounding.
  - path: .agents/skills/farplane-*/evals/
    change: Update planner-contract and behavior fixtures affected by the public signature change.
operation:
  - Remove current active fields and callers in one migration; do not add aliases, fallback parsers, or dual contract support.
  - Validate problem_ref against identity.problems and validate system/feature coherence against canonical registries without a product-bet container.
  - Update the project-owned source skill packages and use the normal skill sync path; do not patch installed copies as source of truth.
signature_or_type_impact:
  - harness.identity.product_bets removed.
  - harness.goals removed.
  - farplane-market-learning, farplane-ablation-proof, and farplane-content-creation replace product_bet_ref with problem_ref.
routes:
  docs: doc-advisor
  qa: agent-qa-test
  review: reviewer
qa:
  - Current and generated harness fixtures validate without goals or product_bets.
  - Either retired field fails validation with a direct migration message.
  - Each affected planning skill rejects an unknown problem_ref and accepts a configured stable problem plus coherent system/feature refs.
  - Searches distinguish removed project-goals terminology from preserved native Goal execution.
failure_modes:
  - Broadly deleting every occurrence of goal or target.
  - Leaving one capability skill or template dependent on product_bet_ref.
  - Losing enough stable context that an empty-board refill can propose random work.
  - Editing generated registries by hand.
```

### Change 4: Keep Plan Next Wave as lean refill, not a gate before known work

```text
fixes:
  - Plan Next Wave currently consumes goals/product bets and can become an unnecessary hop for already-grounded work.
before:
  - Pulse low-watermark planning passes metric_goals, product_bets, goal urgency/deadline buckets, and goal_state.
  - Strategic argument validation assumes product_bet_ref.
after:
  - Interval-created or updated tickets enter the ordinary board immediately after the report; Plan Next Wave is not invoked for them.
  - Plan Next Wave runs only on low ready supply and selects configured skill calls from stable problems, areas, objective/guard movement, evidence, ticket history, World Memory, and preference memory.
  - The planner still produces only concrete configured-skill calls and never writes tickets; Pulse remains the refill materializer.
  - Goal-state and product-bet inputs/outputs disappear from fingerprints, response contracts, fixtures, and receipts.
read:
  - path: skills/plan-next-wave/SKILL.md
    reason: Pure refill planner contract and current product-bet/goal dependencies.
  - path: skills/plan-next-wave/scripts/validate_wave_response.py
    reason: Strategic argument and goal-state response validation.
  - path: skills/pulse-update/SKILL.md
    reason: Low-watermark input, semantic fingerprint, materialization, and dispatch owner.
  - path: skills/pulse-update/scripts/plan_wave_guard.py
    reason: Semantic input fingerprint and overlap guard.
write:
  - path: skills/plan-next-wave/SKILL.md
    change: Bind stable problems/areas/metric movement instead of product bets/goals and clarify refill-only ownership.
  - path: skills/plan-next-wave/references/skill-call-contract.md
    change: Add optional lifecycle due_at and remove assumptions tied to product_bet_ref.
  - path: skills/plan-next-wave/references/response-contract.md
    change: Remove goal_state and replace it with direct objective/problem/movement diagnosis already needed for ranking.
  - path: skills/plan-next-wave/scripts/validate_wave_response.py
    change: Validate problem refs and coherent system/feature refs without product bets; permit optional lifecycle.due_at only when the shared timezone-bearing ISO validator accepts it.
  - path: skills/plan-next-wave/scripts/test_validate_wave_response.py
    change: Cover the lean input, new binding errors, absent/valid due_at, and malformed or timezone-naive due_at rejection.
  - path: skills/plan-next-wave/evals/
    change: Update fixtures, assertions, and golden examples.
  - path: skills/pulse-update/SKILL.md
    change: Remove metric_goals and goal semantic-time state; keep low-watermark refill and ticket materialization.
  - path: skills/pulse-update/scripts/plan_wave_guard.py
    change: Fingerprint metric movement/freshness and other real semantic changes without goal deadline buckets.
  - path: skills/pulse-update/scripts/test_plan_wave_guard.py
    change: Prove movement/freshness changes replan and serialization-only churn does not.
  - path: skills/pulse-update/scripts/materialize_skill_call.py
    change: Materialize optional due_at from an admitted call without inventing one.
operation:
  - Keep the side-effect-free planner boundary and existing configured-skill allowlist.
  - Do not merge Plan Next Wave into Interval: Interval owns observed-problem conversion; refill owns candidate discovery when the board/evidence is weak.
  - Do not require a due date when evidence supplies none.
  - Reuse bin/core/farplane_ticket_reward.py:is_timezone_bearing_iso_datetime as the current timezone-bearing ISO parser for planner and ticket validation; do not introduce a second date grammar.
  - Materialize lifecycle.due_at only after validate_wave_response accepts it, and write no due_at key when it is absent.
signature_or_type_impact:
  - plan_next_wave drops product_bets and metric goals; problem context becomes the stable strategic binding.
  - Planner lifecycle may carry optional due_at.
  - Pulse planner receipts and semantic fingerprints drop goal_state/deadline fields.
routes:
  docs: doc-advisor
  qa: tests
  review: reviewer
qa:
  - Low-watermark refill still emits zero to wave_size validated configured-skill calls.
  - A ready ticket from Interval is selectable without any planner call.
  - Planner rejects unknown problem/system/feature refs and planning-only outputs.
  - Planner accepts an absent or timezone-bearing lifecycle.due_at, rejects date-only/timezone-naive/malformed values, and materializes an accepted value unchanged into ticket frontmatter.
  - Repeated unchanged inputs no-op; real metric movement, ticket state, freshness, Reward, preference, or operator availability changes re-open comparison.
failure_modes:
  - Turning Interval and Plan Next Wave into two implementations of the same planner.
  - Removing the planner's grounding so it invents random feature work.
  - Letting Plan Next Wave write or dispatch tickets.
```

### Change 5: Add a real ticket delivery deadline

```text
fixes:
  - Priority expresses importance but tickets cannot express when an artifact/outcome is needed.
before:
  - Canonical ticket metadata has priority, dependencies, claims, gates, and compute target but no due_at.
  - Pulse sorts executable tickets by priority and then ticket ID.
  - Reward.check_in_at can be mistaken for a work deadline even though it schedules outcome evaluation.
after:
  - Optional due_at is a timezone-bearing ISO-8601 delivery deadline.
  - priority remains strategic importance; due_at remains delivery need; Reward.check_in_at remains outcome-evaluation time.
  - Pulse sorts priority -> due_at ascending with missing last -> ticket_id.
  - Board adapters, Core ticket projections, planner materialization, templates, and docs expose the same field.
read:
  - path: tickets/README.md
    reason: Canonical metadata and field semantics.
  - path: tickets/templates/ticket.md
    reason: Authoring guidance for optional routing fields.
  - path: tickets/scripts/check_ticket_metadata.py
    reason: Allowed-field and validation owner.
  - path: skills/pulse-update/scripts/list_pulse_board.py
    reason: Executable board row and ordering owner.
  - path: bin/core/farplane_boards.py
    reason: Normalized WorkItem projection.
  - path: bin/core/farplane_project_snapshot.py
    reason: UI ticket projection.
write:
  - path: tickets/README.md
    change: Document due_at semantics, examples, and distinction from priority/check_in_at.
  - path: tickets/templates/ticket.md
    change: Add due_at to optional routing-field guidance.
  - path: tickets/scripts/check_ticket_metadata.py
    change: Allow due_at and require bin/core/farplane_ticket_reward.py:is_timezone_bearing_iso_datetime to accept it.
  - path: bin/tests/test_ticket_metadata.py
    change: Cover valid offset/Z, missing optional value, date-only, timezone-naive, malformed, and unknown-field behavior.
  - path: skills/pulse-update/scripts/list_pulse_board.py
    change: Normalize due_at into board rows and use the approved sort key.
  - path: skills/pulse-update/scripts/test_list_pulse_board.py
    change: Cover same-priority dated ordering, missing-last behavior, overdue ordering, cross-priority behavior, and deterministic ticket-ID ties.
  - path: skills/pulse-update/scripts/materialize_skill_call.py
    change: Write due_at only when the validated planner call supplies it.
  - path: bin/core/farplane_boards.py
    change: Add due_at/dueAt to WorkItem and public projection.
  - path: bin/tests/test_farplane_boards.py
    change: Cover normalized deadline projection.
  - path: bin/core/farplane_project_snapshot.py
    change: Add due_at to ticket refs consumed by the UI snapshot.
  - path: bin/tests/test_farplane_project_snapshot.py
    change: Cover ticket deadline projection.
operation:
  - Reuse bin/core/farplane_ticket_reward.py:is_timezone_bearing_iso_datetime from both ticket metadata and planner response validation; do not create competing date grammars.
  - Keep priority as the first sort dimension exactly as approved.
signature_or_type_impact:
  - TicketFrontmatter.due_at?: timezone-bearing ISO-8601 string.
  - WorkItem.due_at?: string; public dictionary key dueAt.
  - Planner lifecycle.due_at?: string.
routes:
  docs: doc-advisor
  qa: tests
  review: reviewer
qa:
  - urgent undated work stays ahead of high dated work.
  - Within one priority, overdue/earlier valid deadlines come first and missing deadlines come last.
  - Reward.check_in_at never affects ordinary ticket ordering.
  - Invalid or timezone-naive due_at fails ticket/planner validation rather than sorting lexically.
failure_modes:
  - Treating due_at as a second lifecycle state.
  - Letting a low-priority dated chore outrank urgent undated work.
  - Reusing Reward.check_in_at as the deadline.
  - Accepting local-time timestamps without an offset.
```

### Change 6: Consolidate the canonical docs and inventories

```text
fixes:
  - Current framework, feature, system, skill, and automation docs teach competing strategy owners.
before:
  - FEAT-0067 says Interval does not decide strategy or create uncertain experiment tickets.
  - FEAT-0071 documents goals/product bets as planner inputs.
  - Framework and system maps describe bounded candidate sources feeding a separate adaptive planner.
  - update-strategy remains discoverable despite having no live caller.
after:
  - FEAT-0067 owns the full evidence-to-ticket Interval behavior.
  - FEAT-0071 owns only refill selection, materialization, ordering, dispatch, and check-ins.
  - FEAT-0063/project-file docs explain direction-derived movement.
  - FEAT-0007/ticket docs explain due_at.
  - Horizon Loop shows metric movement -> Interval -> ticket -> Pulse, with Plan Next Wave as the low-supply fallback.
  - update-strategy and removed project goal/product-bet terms disappear from active inventories while native Goal docs remain.
read:
  - path: docs/features/FEAT-0067-daily-interval-review-reports.md
    reason: Interval feature owner.
  - path: docs/features/FEAT-0071-project-work-pulse.md
    reason: Pulse/refill feature owner.
  - path: docs/features/FEAT-0063-metric-advisor-cards.md
    reason: Metric direction and movement behavior.
  - path: docs/features/FEAT-0007-ticket-as-durable-task-memory.md
    reason: Ticket deadline contract.
  - path: docs/systems/horizon-loop.md
    reason: Cross-feature control-loop boundary.
  - path: docs/farplane-framework/project-files.md
    reason: Canonical harness/metrics/project-file contract.
  - path: docs/farplane-framework/pulse-and-interval-loop.md
    reason: Operator workflow and signatures.
  - path: docs/skills/README.md
    reason: Public skill discoverability and update-strategy row.
write:
  - path: docs/features/FEAT-0067-daily-interval-review-reports.md
    change: Rename/reframe as Daily and Weekly control-loop reviews and update behavior, limits, evidence, and history.
  - path: docs/features/FEAT-0071-project-work-pulse.md
    change: Remove goal/product-bet planning and document refill-only ownership plus due_at ordering.
  - path: docs/features/FEAT-0063-metric-advisor-cards.md
    change: Document required direction and derived movement without duplicate growth metrics.
  - path: docs/features/FEAT-0007-ticket-as-durable-task-memory.md
    change: Add due_at to the optional metadata contract.
  - path: docs/systems/horizon-loop.md
    change: Replace the multi-strategy flow with the consolidated control loop.
  - path: docs/farplane-framework/project-files.md
    change: Remove goals/product_bets and document stable intent plus derived metric movement.
  - path: docs/farplane-framework/pulse-and-interval-loop.md
    change: Update signatures, admission flow, refill boundary, and deadline semantics.
  - path: docs/farplane-framework/README.md
    change: Update the sparse project-model map.
  - path: README.md
    change: Remove project-goal/product-bet claims only where they describe active project strategy; preserve native Goal execution links.
  - path: ARCHITECTURE.md
    change: Update the whole-system map without shrinking it.
  - path: PROJECT_RULES.md
    change: Remove retired project goals from the tracked harness inventory.
  - path: docs/skills/README.md
    change: Remove update-strategy and point review/refill needs to the two surviving owners.
  - path: docs/features/registry.jsonl
    change: Regenerate from source feature docs.
  - path: docs/features/registry.md
    change: Regenerate from source feature docs.
  - path: docs/systems/registry.jsonl
    change: Regenerate after Horizon metadata/content changes.
  - path: docs/systems/registry.md
    change: Regenerate after Horizon metadata/content changes.
  - path: docs/skills/registry.jsonl
    change: Regenerate after skill deletion/signature changes.
  - path: skills/skill-maintenance/graph/
    change: Regenerate affected skill and lifecycle graph outputs.
operation:
  - Update canonical source docs first and regenerate outputs with repo-owned validators.
  - Search removed terms in active surfaces with narrow patterns so native Goal, user goal, non-goal, and historical archive references are not falsely purged.
  - Record one meaningful shipped consolidation in HISTORY only after implementation proof passes; add MEMORY only if the new ownership is not already fully represented by feature/system docs.
signature_or_type_impact:
  - Public documentation signatures match Changes 1-5.
routes:
  docs: doc-advisor
  qa: tests
  review: reviewer
qa:
  - Feature, system, doc-ref, skill-maintenance, project-file, and ticket validators pass.
  - Active search finds no harness.yaml#goals, identity.product_bets, product_bet_ref, or update-strategy references outside explicit historical/migration evidence.
  - Active docs still link native Goal Advisor and Goal Packet execution correctly.
failure_modes:
  - Hand-editing generated registries.
  - Deleting historical evidence or native Goal documentation.
  - Leaving the current project fixed while init templates recreate the retired model.
```

## Done

```text
done_when:
  - Every quantitative metric definition declares maximize/minimize and Core proves honest direction-normalized movement across maximize, minimize, rate/ratio, missing, and zero-time cases.
  - Daily and Weekly Interval share one full first-principles review/admission contract and differ only by evidence window/coverage.
  - A grounded known intervention becomes a concrete ticket delta in the same Interval run; an uncertain intervention is admitted only with the approved decision-changing evidence output.
  - Ticket admission has no arbitrary count cap and rejects low-materiality, vague, duplicate, authority-unsafe, or planning-only work.
  - due_at validates as an optional timezone-bearing timestamp, projects through board/Core interfaces, and orders same-priority executable work earliest-first with missing last.
  - harness.yaml#goals, identity.product_bets, product_bet_ref, and update-strategy are removed from active source, templates, callers, validators, tests, skills, and generated inventories with no compatibility aliases.
  - Plan Next Wave still passes focused behavior/contract tests as a side-effect-free configured-skill refill planner using stable problems, areas, objective movement, evidence, and history.
  - Native Goal Advisor and ticket Goal Packet behavior remain present and correctly documented.
  - Canonical docs and generated registries describe one metric -> Interval -> ticket -> Pulse loop.
  - Integrated behavior proof follows a metric regression through Interval report, ticket admission with priority/due_at, Pulse ordering, and no Plan Next Wave call.
  - A second integrated behavior proof shows insufficiently grounded evidence produces no ticket and later low-watermark refill can still call Plan Next Wave.
  - TASK-0405 highlight selection, report-before-append ordering, append idempotency, and Core projection tests still pass after the Interval/Core rewrite.
  - Material QA evidence review and completion review both reach TAS-A before farplane ticket close.
```

## QA Strategy

```text
qa_strategy:
  proof_weight: agent_qa
  checks:
    - python3 -m unittest bin.tests.test_farplane_project_snapshot
    - python3 -m unittest bin.tests.test_ticket_metadata
    - python3 -m unittest bin.tests.test_farplane_boards
    - python3 skills/pulse-update/scripts/test_list_pulse_board.py
    - python3 skills/pulse-update/scripts/test_plan_wave_guard.py
    - python3 skills/plan-next-wave/scripts/test_validate_wave_response.py
    - python3 skills/plan-next-wave/scripts/test_eval_fixtures.py
    - python3 skills/interval-update/scripts/test_highlight_ledger.py
    - python3 tickets/scripts/check_ticket_metadata.py
    - python3 bin/validators/check_farplane_project_files.py
    - python3 docs/features/validate_features.py
    - python3 bin/validators/check_doc_refs.py
    - python3 skills/skill-maintenance/scripts/check_skills.py --write
  manual:
    - Inspect one maximize and one minimize card in .farplane/project/ui/latest.json and confirm favorable movement has positive progress velocity.
    - Inspect the executable board fixture and confirm priority dominates due_at, due_at dominates ticket ID within a priority, and missing dates sort last.
    - Inspect an Interval report and its ticket links for one direct correction, one decision-changing investigation, one duplicate rejection, and one ungrounded planner candidate.
    - Confirm the same Interval fixture finalizes its report before highlight append, does not read highlights as planning input, preserves the TASK-0405 sparse/idempotent highlight contract, and only then applies ticket deltas.
    - Search active surfaces for the removed project strategy terms while confirming goal-advisor and Goal Packet docs remain.
  delegated_lanes:
    - qa-tester runs the ordered unit/integration checks and captures the two end-to-end control-loop fixtures.
    - agent-qa-test adversarially tests Interval against ticket flooding, planning residue, fake momentum, missing evidence, duplicate ownership, and accidental execution.
    - reviewer performs implementation, evidence-bundle, documentation-quality, and completion review.
  review:
    - rubric: code-quality, skill-contract, integration-readiness, evidence-quality, documentation-quality
      required_tas: TAS-A
  evidence:
    - tickets/TASK-0406/artifacts/qa/test-results.txt
    - tickets/TASK-0406/artifacts/qa/control-loop-known-intervention.json
    - tickets/TASK-0406/artifacts/qa/control-loop-refill-fallback.json
    - tickets/TASK-0406/artifacts/qa/interval-agent-qa.md
    - tickets/TASK-0406/artifacts/qa/task-0405-highlight-regression.txt
    - tickets/TASK-0406/artifacts/review/evidence-review.md
    - tickets/TASK-0406/artifacts/review/completion-review.md
  goal_advisor_inputs:
    proof_route: tests -> qa-tester integration fixtures -> agent-qa-test -> evidence review -> completion review
    final_evidence: ticket Done checklist plus the strongest linked QA/review artifacts
    final_checkpoint: farplane ticket close TASK-0406 only after TAS-A evidence and completion reviews
  residual_risk:
    - The current worktree already contains uncommitted edits in snapshot, validators, metrics, harness-related skills, docs, registries, and automations; execution must reconcile rather than overwrite them.
    - TASK-0405 also changes Interval and Core snapshot surfaces; preserve its accepted highlight behavior and rerun both tickets' focused tests after merge.
    - Replacing product_bet_ref changes project-local skill public signatures and requires source-package sync plus behavior eval proof.
    - Direction choices for currently directionless observational metrics require human-readable rationale; do not assign maximize merely to satisfy validation.
```

Critical path claimed:

1. A metric definition and two available observations produce an honest
   direction-normalized movement.
2. Daily or Weekly Interval consumes that movement and supporting evidence,
   identifies a material bottleneck, and writes the dated report.
3. The same run creates or updates one concrete ticket when the intervention
   passes admission, without invoking Plan Next Wave.
4. The ticket carries priority and optional `due_at`; Pulse places it in the
   approved order and can dispatch it through the existing worker/Goal route.
5. When Step 3 lacks grounded work, the board remains unchanged and a later
   low-watermark Pulse can call Plan Next Wave using stable problem/metric/area
   context.

Ordered sanity checks:

1. Prove the metric movement function in isolation.
2. Prove metric card projection and project validation.
3. Prove `due_at` parsing, projection, and sort behavior.
4. Prove Interval admission/rejection behavior with skill evals.
5. Prove Plan Next Wave and Pulse contracts after removed inputs.
6. Prove both integrated control-loop branches.
7. Run adversarial agent QA and independent review over the evidence bundle.

## Docs Strategy

```text
docs_strategy:
  outcome: update_docs
  doc_targets:
    - docs/features/FEAT-0067-daily-interval-review-reports.md
    - docs/features/FEAT-0071-project-work-pulse.md
    - docs/features/FEAT-0063-metric-advisor-cards.md
    - docs/features/FEAT-0007-ticket-as-durable-task-memory.md
    - docs/systems/horizon-loop.md
    - docs/farplane-framework/project-files.md
    - docs/farplane-framework/pulse-and-interval-loop.md
    - docs/farplane-framework/README.md
    - docs/skills/README.md
    - tickets/README.md
    - README.md
    - ARCHITECTURE.md
    - PROJECT_RULES.md
  no_docs_reason:
  validation:
    - Update canonical feature/system/framework sources before generated registries.
    - python3 docs/features/validate_features.py --write
    - python3 bin/validators/check_doc_refs.py
    - python3 bin/validators/check_doc_parity.py
    - python3 skills/skill-maintenance/scripts/check_skills.py --write
    - Verify removed project strategy terms are absent from active surfaces and preserved native Goal terms remain valid.
```

Doc placement decision:

- Feature docs own metric, Interval, Pulse, and ticket behavior.
- `docs/systems/horizon-loop.md` owns the cross-feature control-loop boundary.
- Framework docs own project-file and operator workflow contracts.
- Skill files own executable reasoning/admission procedures.
- This ticket owns migration detail and proof until it is distilled.
- No new strategy, war-room, or campaign document is created.

## Links

- `program:` created by goal-advisor after operator approval
- `progress:` created by goal-advisor after operator approval
- Visual companion: `tickets/TASK-0406/diagrams.md`
- `artifacts:` `tickets/TASK-0406/artifacts/`
- `review:` `tickets/TASK-0406/artifacts/review/plan-review.md`
- `refs:`
  - `skills/interval-update/SKILL.md`
  - `skills/update-strategy/SKILL.md`
  - `skills/plan-next-wave/SKILL.md`
  - `skills/pulse-update/SKILL.md`
  - `bin/core/farplane_project_snapshot.py`
  - `tickets/README.md`
  - `docs/systems/horizon-loop.md`

## Notes

- `Blast radius:` metric schema/projection, project harness schema, three
  project-local capability signatures, Interval behavior, planner/Pulse
  contracts, ticket metadata/ordering, init templates, docs, tests, and
  generated registries.
- `Risks / rollback:` Land as one schema migration with updated callers and no
  live compatibility paths. If behavior proof fails, keep the ticket open and
  revert the whole unaccepted migration rather than restoring parallel strategy
  owners. Preserve report-only behavior as the safe failure mode only during
  implementation, not as a shipped dual mode.
- `Minimal implementation plan:` This is the smallest coherent implementation
  that produces one end-to-end control loop. Splitting metric movement,
  Interval admission, strategy-input removal, and board deadlines would leave
  temporary competing owners or an unprovable partial workflow.
- `Existing service fit:` Movement extends the existing Core metric-card
  builder; ticket mutation extends Interval; refill stays Plan Next Wave;
  materialization/ordering stays Pulse; validation stays existing validators;
  no new service, state file, or strategy skill is introduced.
- `Grounding:` local-only. This is a Farplane-internal ownership/schema
  consolidation grounded in current source, tests, feature specs, system docs,
  memory, troubles, and lessons; no external API or peer-practice decision is
  required.
- `Overlap:` TASK-0405 is awaiting review and touches Interval/Core projection.
  Implementation must read its accepted delta and preserve it rather than
  reverting or duplicating its highlight path.

```text
plan_qa:
  minimal_required_version: pass
  reuse_before_new_surface: pass
  least_parameters: pass
  new_files_functions_justified: pass
  minimal_impl_plan_claim: pass
  existing_service_fit: pass
  goal_advisor_ready: pass
  clarifying_questions: pass
  architecture_signatures: pass
  change_plan_signature_linkage: pass
  change_plan_locality: pass
  qa_strategy_explicit: pass
  docs_strategy: pass
  independent_plan_review: pass
  visual_companion_boundary: pass
  visual_companion_colored_delta: pass
  grounding_evidence: local_only
  highest_risk: Public planner-skill signature migration across a dirty overlapping worktree.
  fix_or_deferral: Reconcile source changes first, preserve and rerun TASK-0405 highlight contracts, validate planner and ticket due_at through the shared parser, migrate all active callers in one pass, then regenerate inventories.
```
