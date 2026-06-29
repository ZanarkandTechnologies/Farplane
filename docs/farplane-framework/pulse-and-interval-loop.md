---
title: "Pulse And Interval Loop"
status: active
owner: farplane-framework
created_at: 2026-06-29
updated_at: 2026-06-29
framework_template_version: "0.2.0"
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
  -> ready ticket execution + planning request? + decision state

interval_update(project_root, interval_id, review_window, planning_window,
                context_refs?, report_workflows?, planning_policy?,
                write_policy?, now?)
  -> dated interval report + next-window plan + Pulse guidance
```

Pulse is the fast executor loop. It reads the static harness charter, current
goals, dynamic products, recent interval guidance, ticket state, execution
policy, rewards, and ledgers. It admits ready tickets, executes parallelizable
work up to policy cap, writes planning requests when no executable work exists,
writes a dated Pulse report, and updates decision/reward state.

Daily Interval reviews the last 24 hours and plans the next 24 hours. Weekly
Interval reviews the last week, checks drift against `farplane/harness.md` and
`farplane/goals.md`, and plans the next week. Both call `interval-update`,
write dated reports under `.farplane/reports/interval/`, and give Pulse
guidance.

The important design choice is that Pulse does not become long-horizon
strategy, and interval automations do not become fast execution dispatchers.
They share files, not hidden transcript memory.

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
  outcomes, or writes a planning request when the board lacks executable work.

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
execution bet goes to `goal-advisor`; small ticket deltas go to the board for
Pulse execution. The next daily and weekly intervals read the resulting
reports and reward signals.

The weekly report should reason over scores rather than pretending scores are
objective telemetry too early. Each selected bet should name:

```text
loss_term -> lever -> evidence -> expected_reward_signal
          -> owner_skill -> proof_route -> accept | continue | kill | resize
```

For Farplane itself, the main self-evolution metric is:

```text
validated meaningful improvement cycles per human intervention hour
```

Supporting signals are accepted output, accepted agent-hours, false-completion
incidents, context-isolation failures, source-gap rate, proof-closure rate, and
skill-backpropagation events. These are not a single blind score; the weekly
interval summarizes them as evidence and uses the score only to guide the
reasoned choice of 1-3 bets.

Urgent leverage escalation is a narrow bypass, not a second scheduler. It is
allowed only for high-confidence signals that would lose meaningful value
before the next weekly interval and that include an evidence ref, loss term,
review-by date, and next owner route.
