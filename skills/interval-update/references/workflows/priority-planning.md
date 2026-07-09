---
title: "Priority Planning Workflow"
status: active
owner: interval-update
kind: workflow-reference
template_uses:
  skill-template: "0.3.2"
---

# Priority Planning Workflow

## Context

Use this workflow when an interval update needs to turn review-window evidence
into strategy inputs, ranked priorities, and downstream guidance for the
configured planning window. This is the generic version of the old weekly PM
synthesis lane: it keeps the valuable parts of priority review,
deprioritization, proof checks, follow-up agenda, and Pulse guidance without
embedding one project’s context into the skill.

This workflow plans and routes. It does not execute leaf work. It also does not
need to fully pre-plan ticket inventory when the project enables Pulse
next-wave planning; instead it can emit product focus, current hypothesis, prefer/avoid rules,
blocked items, reward signals, lane distribution, constraints, and an
product strategy refresh that Pulse uses to slice tactical tickets when the
board is empty. Treat Pulse as a bold bounded tactical idea engine and the
interval as the evidence check that challenges product-local operating beliefs.
Do not add an idea ledger or second planning database; use the interval report
and product `product.md` strategy sections.

## Workflow Signature

```text
priority_planning(context_bundle, review_window, planning_window,
                  workflow_findings?, parent_context_refs?, planning_policy?)
  -> strategy_input + lane_distribution + priorities + depriorities
     + proof_checks + downstream_guidance + goals_delta_candidates
     + product_strategy_review? + product_strategy_delta? + source_gaps

state: reads(context_bundle, workflow_findings?, parent_context_refs?,
             planning_policy?);
       writes(parent_interval_update_report_section)
gates: report_evidence_available; planning_window_sized; proof_checks_named;
       selected_priorities_move_named_goal_or_bottleneck;
       strategy_input_named_when_pulse_next_wave_enabled;
       product_strategy_review_named_when_product_beliefs_change;
       product_strategy_delta_named_when_active_strategy_changes;
       leaf_work_routed_not_executed; material_goal_deltas_approval_gated
fails: writing a vague plan; mixing reporting and execution; hiding
       depriorities; filling time without a needle-moving rationale;
       embedding project-specific priorities in the workflow
```

## Source Contract

Default sources:

- the static human thesis, durable leverage commitments, non-tradeoffs, and
  allocation guardrails from the context bundle.
- product work lanes, default weight hints, product boundaries, current
  strategies, reward signals,
  and local product skill refs from `farplane/products.json` and
  `.agents/skills/` in the context bundle.
- parent context refs and goals from the context bundle.
- enabled workflow findings such as plan progress, goal drift, ticket board
  drift, feedback obligations, opportunity signals, attention drift, and
  metric snapshots.
- tickets, Pulse reports, interval reports, worker outcomes, and memory docs.
- product `## Current Strategy` sections from
  `farplane/products/<product>/product.md`. These capture product-local focus,
  current hypothesis, allocation hints, next moves, constraints, and review
  cadence. They are mutable working context, not a replacement for goals,
  generated product indexes, tickets, or dated interval reports.

Optional sources:

- `context_refs.workflow_refs.status_refs`: planning systems, Notion status
  views, project status docs, CRM/PM dashboards.
- `context_refs.workflow_refs.metric_refs`: KPI or feedback proof.
- `context_refs.workflow_refs.feedback_refs`: commitments and people-facing
  obligations.
- `context_refs.workflow_refs.opportunity_refs`: source-backed opportunities.

Do not fetch private planning systems by convention. They must be configured.

## Phase Boundary

Run inline for small intervals. Use a read-only subagent when multiple workflow
findings need independent synthesis or when the planning window is large enough
that a second read reduces self-confirmation.

## Todo List

- [ ] 1. Bind inputs.
  - [ ] Confirm `review_window`, `planning_window`, parent context refs, and
        enabled workflow findings.
  - [ ] Confirm the static charter boundary from the context bundle before
        ranking product, goal, or ticket changes.
  - [ ] Confirm product work lanes and default weight hints from the context
        bundle before creating or reprioritizing tickets.
  - [ ] Read planning policy for side-effect, goals-delta, or output-shape
        instructions.
- [ ] 2. Separate planning inputs.
  - [ ] Group inputs by goals, completed work, unfinished work, feedback,
        board hygiene, opportunity signals, metrics, and attention drift.
  - [ ] Convert changed insight into implication into action.
  - [ ] Identify current product beliefs from product strategy sections, recent
        Pulse reports, generated tickets, or interval strategy inputs when
        available.
- [ ] 3. Rank priorities.
  - [ ] Choose a lane distribution for `planning_window`, using product lane
        hints as defaults and recent evidence to adjust them.
  - [ ] Treat product lane weights as allocation priors, not hard quotas.
        Explain any temporary Weekly/Daily override with evidence.
  - [ ] Check the distribution against static allocation guardrails.
  - [ ] Pick the top priorities sized to `planning_window`.
  - [ ] For each priority, include why-now, owner or next surface, expected
        output, and proof check.
  - [ ] For each selected lane or priority, name the goal, bottleneck, or
        reward signal it is expected to move; reject priorities that only fill
        capacity or sound useful without moving the plan.
  - [ ] When Pulse next-wave planning is enabled, emit compact per-product
        strategy input: product, focus, current hypothesis, prefer, avoid,
        blocked, reward, and any allocation hint.
  - [ ] Challenge current product beliefs before refreshing product strategy:
        name what worked, what failed, which belief to keep, revise, or drop,
        and the guard for any double-down.
  - [ ] When write policy allows product strategy edits, emit compact product
        strategy deltas: focus, current hypothesis, allocation hint, next
        moves, constraints, last interval ref, and next review. Keep material
        goals, KPI, product-boundary, publishing, spend, account, or
        customer-contact changes in their owning files or approval gates.
- [ ] 4. Name depriorities.
  - [ ] Identify drag, stale assumptions, weak fit, and opportunity cost.
  - [ ] Decide revisit, park, kill, or split.
- [ ] 5. Route downstream work.
  - [ ] Separate solo work, people-facing follow-ups, background-agent work,
        and approval-required decisions when the project has those lanes.
  - [ ] Convert executable work into proposed ticket deltas or Goal Advisor
        handoffs when the interval has enough evidence and the work deserves a
        durable ticket now. Include a `.agents/skills/<product-skill>/SKILL.md`
        ref when a local product skill owns the workflow.
  - [ ] Return Pulse constraints for the fast executor loop; Pulse should
        execute ready tickets, create bounded tactical next-wave tickets from
        fresh strategy when empty, or request more planning. Pulse must not
        create strategy.
  - [ ] Route product strategy refreshes as active-context writeback only. Do not
        create a roadmap registry, project schema, database, or second report
        archive from this workflow.
- [ ] 6. Gate strategy changes.
  - [ ] Mark material goals, KPI, strategy-axis, quarterly/yearly, or durable
        milestone changes as approval-required goals deltas.
  - [ ] Mark human thesis, static leverage commitment, non-tradeoff, or
        agent-authority changes as approval-required harness deltas.

## Templates

Read-only subagent handoff:

```text
Read <context_bundle> and enabled workflow findings. Run priority_planning for
<review_window> -> <planning_window>. Return ranked priorities, depriorities,
proof checks, downstream guidance, goals_delta_candidates, and source_gaps.
Do not mutate files, goals, tickets, or external systems.
```

Priority row:

```text
- priority:
  why_now:
  lane:
  owner_or_next_surface:
  expected_output:
  proof_check:
  route: ticket_delta | goal_advisor_handoff | pulse_constraint | human_decision
```

Strategy input row:

```text
product_strategy_review:
  product:
  product_belief_reviewed:
  what_worked:
  what_failed:
  belief_to_keep:
  belief_to_revise:
  belief_to_drop:
  double_down_guard:
  source_gap:
strategy_input:
  product:
  focus:
  current_hypothesis:
  prefer:
  avoid:
  blocked:
  reward:
  allocation_hint:
product_strategy_delta:
  product:
  focus:
  current_hypothesis:
  next_moves:
  constraints:
  last_interval_ref:
  next_review:
```

## Gotchas

- A plan without depriorities is usually just a wish list.
- Larger planning windows need stronger proof checks, not more vague bullets.
- Goal Advisor is for durable goal/ticket architecture, not every tiny Pulse
  decision.
- Product strategy should be edited in place and kept compact. If a product
  strategy is stale, narrow or park it instead of appending a new roadmap.
- Do not turn promising ideas into a separate ledger. Pulse can generate bold
  tactical ideas; intervals decide which operating beliefs deserve more runway.

## Reference Map

- Parent interval update loads this file only when
  `report_workflows.priority_planning` is enabled.

## Output

```text
priorities:
  - priority:
    lane:
    why_now:
    owner_or_next_surface:
    expected_output:
    proof_check:
product_strategy_review:
  product:
  product_belief_reviewed:
  what_worked:
  what_failed:
  belief_to_keep:
  belief_to_revise:
  belief_to_drop:
  double_down_guard:
  source_gap:
strategy_input:
  product:
  focus:
  current_hypothesis:
  prefer:
  avoid:
  blocked:
  reward:
  allocation_hint:
lane_distribution:
  - lane:
    planned_weight:
    ticket_budget:
    expected_reward:
    guardrail_check:
depriorities:
  - item:
    reason:
    revisit_or_kill:
proof_checks:
  - item:
    check:
downstream_guidance:
  pulse_constraints:
  ticket_deltas:
  goal_advisor_handoffs:
product_strategy_delta:
goals_delta_candidates:
  - delta:
    decision: auto_apply | approval_required | rejected_source_gap
    evidence:
source_gaps:
```
