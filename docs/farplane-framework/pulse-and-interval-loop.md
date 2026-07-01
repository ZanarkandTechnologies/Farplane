---
title: "Pulse And Interval Loop"
status: active
owner: farplane-framework
created_at: 2026-06-29
updated_at: 2026-07-01
framework_template_version: "0.2.2"
tags:
  - farplane
  - lifecycle
  - automations
  - pulse
  - intervals
refs:
  - docs/farplane-framework/README.md
  - docs/farplane-framework/lifecycle.md
  - docs/farplane-framework/ticket-execution-loop.md
  - docs/features/FEAT-0065-pulse-and-interval-automation.md
  - docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md
  - docs/MEMORY.md
---

# Pulse And Interval Loop

Farplane autonomous operation uses explicit Codex automation loops:

```text
pulse_update(project_root, extensions?, pulse_policy?)
  -> ready ticket execution + tactical next-wave tickets? + planning request? + decision state

interval_update(project_root, interval_id, review_window, planning_window,
                context_refs?, report_workflows?, planning_policy?,
                write_policy?, now?)
  -> dated interval report + ops-memory delta? + next-window plan + Pulse guidance
```

Pulse is the fast execution bus. It reads the static harness charter, current
goals, dynamic products, active ops memory, product lane weights, recent
Weekly/Daily strategy inputs, ticket state, execution policy, rewards, and
ledgers. It admits ready tickets, executes parallelizable work up to policy
cap, creates a small tactical next wave when the board is empty and fresh
strategy is available, writes planning requests when no safe tactical work
exists, writes a dated Pulse report, and updates decision/reward state.

Daily Interval reviews the last 24 hours and recalibrates the next 24 hours.
Weekly Interval reviews the last week, checks drift against
`farplane/harness.md` and `farplane/goals.md`, reviews budget/runway for active
projects, and sets next-week bets. Both call `interval-update`, write dated reports under
`.farplane/reports/interval/`, and give Pulse strategy inputs.

`farplane/ops-memory.md` is the active operating memory between reports and
tickets. It is the compact, mutable second brain for current focus, active
projects, critical paths, next frontier, constraints, parking lot, and recent
operating decisions. It may hold multiple active projects, but those projects
remain Markdown sections, not a roadmap registry, project schema, database, or
second scheduler.

The important design choice is that Pulse does not become long-horizon
strategy, and interval automations do not become fast execution dispatchers.
Weekly and Daily alter the inputs to the tactical planner; Pulse owns the
current board scan, next-wave slicing, execution admission, and outcome
writeback. They share files, not hidden transcript memory.

## Memory Split

Use the smallest owner for each kind of state:

| State | Owner | Changes when |
| --- | --- | --- |
| Stable thesis and guardrails | `farplane/harness.md` | explicit human-approved harness delta |
| North star, value function, goal axes, inline SMART goals, durable bets | `farplane/goals.md` | horizon/goal delta with evidence and approval when material |
| Metric labels, units, chart behavior, pinned status, kind, and refresh prompts | `farplane/bindings.md` | metric recipe delta with source-gap proof |
| Product lanes, workflows, lane weights | `farplane/products.md` | product-boundary update with evidence |
| Active focus, active projects, critical paths, next frontier | `farplane/ops-memory.md` | Daily/Weekly refresh or Pulse frontier writeback |
| Executable work | `tickets/TASK-*/ticket.md` | ticket creation, execution, review, closeout |
| Ticket-level spend justification | ticket `Reward` block | ticket creation or planning update |
| Active project runway decisions | Weekly Interval report and `farplane/ops-memory.md` | weekly review or material evidence change |
| Receipts and ledgers | `.farplane/reports/**`, `.farplane/automation/*.jsonl` | Pulse/Interval/worker outcomes |
| Caps and cadence | `.farplane/automation/heartbeat-policy.json`, `farplane/automations.md` | explicit automation/policy update |

This keeps flexible planning in one place without turning every roadmap idea
into a new artifact family. Caps such as `maxChildThreadsPerBeat` remain policy
state; ops memory may mention where caps live, but it must not duplicate them
as mutable planning state.

## Strategy Inputs And Next-Wave Planning

Weekly and Daily reports expose compact strategy inputs and may refresh
ops-memory:

```text
StrategyInput := focus + bets + prefer + avoid + blocked + reward
OpsMemoryDelta := current_focus + active_projects + next_frontier
               + constraints + parking_lot + recent_decisions
```

`farplane/products.md` work-lane weights are the default allocation prior for
Pulse next-wave planning. They bias selection when several safe slices are
available; they are not hard quotas. Daily strategy, blockers, source
freshness, proof urgency, or a Weekly bet may override the weights, but the
Pulse report should record the reason.

When no ready ticket can advance, Pulse may use:

```text
plan_next_wave_when_empty(ops_memory, weekly_strategy, daily_strategy,
                          board_state, product_lane_weights)
  -> 1..N tactical tickets + admission decision
```

Generated tactical tickets must be small, local, approval-free, and tied to a
current focus, active project, frontier step, bet, lane, bottleneck, or reward
signal. Each generated ticket must include:

```yaml
Reward:
  kpi_rewards:
    - kpi_id: accepted_harness_improvements
      expected_reward: "one proof-backed shipped harness improvement"
  guard: "stop before expanding scope or counting unproved intent"
```

`Reward` is also the ticket-level budget justification. `kpi_rewards` names the
KPI IDs the ticket is expected to move and the expected reward text; `guard`
names the stop, resize, or non-expansion boundary. Do not add another ticket
field for budget reason unless a future ticket proves `Reward` is insufficient.

Pulse still writes `request_planning` when the strategy inputs are stale,
missing, unsafe, or require material product, KPI, goal, publishing, spend,
account, customer-contact, or authority decisions.

Before:

```text
latest interval report -> one safe tactical ticket -> maybe execution
```

After:

```text
goals/products + ops-memory + latest interval reports
  -> active frontier + needed metric readings
  -> bounded tactical tickets
  -> execution up to heartbeat-policy cap
```

Daily and Weekly should read goal-axis SMART goals semantically. For each
active SMART goal, use its `kpis` to find metric recipes in
`farplane/bindings.md`; each recipe gives the interval agent a prompt-only
`refresh` instruction for today's reading. Do not parse
`farplane/ops-memory.md` as a deterministic database; use it as flexible agent
memory for active initiatives, tracked content, and next ticket candidates.
Missing credentials, missing API fields, missing files, or missing feedback
mechanisms become source gaps and instrumentation-ticket candidates. After
writing `.farplane/metrics/daily/<date>.json`, run
`farplane metrics compile` to refresh `.farplane/metrics/ui/latest.json`.

Maintenance work should compete against the active frontier. It is selected
only when it unblocks the focus, protects proof, or has a clearer reward signal
than the current project work.

## Budget And Runway

Fast AI-worker loops still need protected runway. Quarterly goals protect
compounding bets from daily noise; weekly intervals decide whether each active
project deserves another planning window.

Weekly Interval should write a Budget / Runway Review before the next-window
plan. It should cite active projects from `farplane/ops-memory.md`, ticket
`Reward` blocks, metric snapshots, source gaps, interval reports, and visible
operator feedback. For autonomy claims, prefer the daily `autonomy_time_feedback`
readings over subjective intervention labels: human prompt count, estimated
human attention minutes, autonomous worker elapsed minutes, auto-time ratio, and
output per human prompt. Each active project receives one decision:

```text
continue | narrow | pause | instrument | stop | escalate_to_revenue
```

Rough spend or attention notes are enough until exact cost accounting changes
decisions. Work without weekly evidence should be paused, narrowed, or turned
into an instrumentation ticket. The runway decision constrains planning; it
does not authorize paid services, publishing, customer contact, deploys, or
product-boundary changes.

## Self-Update Loop

Weekly Interval is the default self-update loop. It reviews the last week,
compares work against goals, scores compounding leverage opportunities, chooses
1-3 next-week bets, and writes proposals before any durable strategy mutation.
Signals come from existing artifacts: reports, tickets, lessons, troubles,
skill/feature registry changes, evals, feedback, metrics, opportunity refs, or
supplied external source refs. Weekly Interval owns clustering, rejection,
selection, and decision logging inside the dated interval report.

Static charter changes are different from product or goals deltas. Weekly
Interval may propose a harness delta when evidence challenges the human thesis,
durable leverage commitments, non-tradeoffs, or agent authority, but applying
that delta requires explicit human approval.

```text
weekly_interval_report
  -> goals_delta_candidates
   + lever_inventory
   + next_week_bets
   + pulse_guidance
   + goal_advisor_handoffs
   + reward_signals_to_check_next_week
```

Goals deltas have three outcomes:

- `auto_apply`: small evidence-backed updates such as source refs, stale
  labels, current-signal notes, or minor milestone wording when policy allows.
- `approval_required`: north star, KPI, strategy axis, project priority, hold,
  stop condition, quarterly/yearly goal, or durable milestone changes. These
  stay in the weekly report until the operator accepts them or asks
  `horizon-advisor` to apply the strategy delta.
- `rejected_source_gap`: insufficient evidence. The interval should create an
  instrumentation, access, feedback, research, or ticket-delta proposal instead
  of rewriting strategy.

## Advisor Boundaries

- `horizon-advisor` owns long-horizon strategy: value function, KPI tree,
  strategy axes, current milestone, and material `farplane/goals.md` deltas.
- `leverage-advisor` scores how an existing feature, workflow, capability, or
  artifact can compound value.
- `harness-advisor` decides which harness surface should own a selected
  improvement: docs, skill, ticket contract, validator, hook, automation
  prompt, subagent, or template.
- `proof-advisor` owns proof selection and proof-case design. It decides
  whether a claim needs deterministic tests, validators, skill evals, policy
  evals, e2e workflow evals, QA, visual QA, agent QA, review, or a source-gap
  ticket before handing execution to the owning proof surface.
- `eval` executes runnable eval rows, judges, hardcases, and eval-run proof
  after `proof-advisor` or the caller has selected eval as the right surface.
- `skill-creator` creates or meaningfully reshapes a reusable skill only when
  the trigger is stable, the workflow should repeat, and no existing skill owns
  the behavior.
- `skill-maintenance` hardens or refines existing skills: eval-to-QA sync,
  lesson/trouble backpropagation, gotchas, checklist guardrails, registry sync,
  audits, and skill-package proof.
- `impl-plan` is the default coding-ticket planner when a selected bet needs a
  material implementation plan and proof contract before execution.
- `goal-advisor` compiles selected execution bets into ticket-backed Goal
  Packets or heartbeat prompts.
- `optimize-harness` is the umbrella improvement loop when the observed
  behavior gap itself is the task: diagnose the gap, place the lever, choose
  proof, route the change or experiment, and require review.
- `pulse-update` executes ready tickets up to policy cap, records immediate
  outcomes, creates bounded tactical next-wave tickets from fresh strategy when
  the board is empty, or writes a planning request when no safe tactical work
  exists.

Use this matrix when the weekly self-update report routes work:

| Question | Owner | Output |
| --- | --- | --- |
| Are we optimizing the right goal, KPI, frontier, or constraint? | `horizon-advisor` | goals delta or strategy packet |
| Which existing capability would compound fastest? | `leverage-advisor` | ranked leverage play and first proof step |
| Where should this harness change live? | `harness-advisor` | primary owner surface and rejected surfaces |
| How do we prove the behavior changed? | `proof-advisor` | proof plan, selected cases, proof-surface map, and execution handoff |
| Is this a new reusable skill? | `skill-creator` | new or reshaped skill package with proof |
| Does an existing skill need backpropagation? | `skill-maintenance` | skill hardening/refinement, eval/checklist sync |
| Does the bet need a coding plan? | `impl-plan` | ticket plan and proof contract |
| Is the selected frontier ready to run? | `goal-advisor` | Goal Packet, native Goal prompt, or heartbeat prompt |
| Is the whole harness behavior wrong? | `optimize-harness` | accepted change, experiment plan, or blocked report |

The weekly plan should not become a giant roadmap. It names a leverage table,
then selects a small number of bets:

```text
| Lever | Surface | Loss term | Evidence | Compounding value | Cost/risk | Experiment | Reward signal | Next owner |
```

After approval, a material strategy delta returns to `horizon-advisor`; an
execution bet goes to `goal-advisor`; small ticket deltas may go to the board
for Pulse execution. When the board is empty, Pulse may also create small
tactical tickets directly from the latest Weekly/Daily strategy and product
lane weights. The next daily and weekly intervals read the resulting reports
and reward signals.

The weekly report should reason over scores rather than pretending scores are
objective telemetry too early. Each selected bet should name:

```text
loss_term -> lever -> evidence -> expected_reward_signal
          -> owner_skill -> proof_route -> accept | continue | kill | resize
```

For Farplane itself, the main self-evolution metric is:

```text
validated meaningful improvement cycles per human attention hour
```

Supporting signals are accepted output, autonomous worker elapsed minutes,
human attention minutes, auto-time ratio, ticket intervention turns,
auto-completion rate, false-completion incidents, context-isolation failures,
source-gap rate, proof-closure rate, and skill-backpropagation events. These
are not a single blind score; the weekly interval summarizes them as evidence
and uses the score only to guide the reasoned choice of 1-3 bets.

Urgent leverage escalation is a narrow bypass, not a second scheduler. It is
allowed only for high-confidence signals that would lose meaningful value
before the next weekly interval and that include an evidence ref, loss term,
review-by date, and next owner route.
