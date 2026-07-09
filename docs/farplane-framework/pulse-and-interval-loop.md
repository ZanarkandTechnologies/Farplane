---
title: "Pulse And Interval Loop"
status: active
owner: farplane-framework
created_at: 2026-06-29
updated_at: 2026-07-08
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
  -> ready ticket delegation + product-loop invocations? + planning request? + decision state

product_pulse(product_md, product_loop_progress?, products, tickets,
              metrics?, reviews?, strategy_inputs?)
  -> ranked moves + executable ticket specs? + worker handoffs? + learning writeback

interval_update(project_root, interval_id, review_window, planning_window,
                context_refs?, report_workflows?, planning_policy?,
                write_policy?, now?)
  -> dated interval report + product.md strategy deltas? + next-window plan + Pulse guidance
```

Pulse is the fast manager/delegation bus with founder-like ambition inside hard gates.
It reads the static harness charter, current goals, dynamic product strategies,
product lane weights, recent Weekly/Daily reports, ticket state,
execution policy, rewards, and ledgers. It admits ready
tickets, delegates parallelizable work under product-loop worker policy, invokes
eligible product loops when the board is empty and fresh strategy is available,
writes planning requests when no safe tactical work exists, writes a dated
Pulse report, and updates decision/reward state. Product loops generate bold
bounded tactical ideas as tests of their current product belief, frontier,
bottleneck, or reward signal.

Daily Interval reviews the last 24 hours and recalibrates the next 24 hours. It
acts as a short-horizon reality check: what worked, what failed, and which
product strategy should be kept, revised, dropped, or doubled down under a
guard. Weekly Interval reviews the last week, checks drift against
`farplane/harness.md` and `farplane/goals.yaml`, reviews budget/runway for active
products/projects, and sets next-week product strategy. It acts like a board review for runway and
belief quality. Both call `interval-update`, write dated reports under
`.farplane/reports/interval/`, and give Pulse strategy inputs by updating the
`## Current Strategy` sections in product `product.md` files when policy allows.

The important design choice is that Pulse does not become long-horizon strategy
or the all-product idea brain, and interval automations do not become fast
execution dispatchers. Weekly and Daily alter the inputs to product loops;
Pulse owns current board reconciliation, product-loop invocation, execution
admission, and outcome writeback. They share files, not hidden transcript
memory. Do not add a separate generic idea ledger in this slice: product-loop
`progress.md`, Pulse reports, interval reports, tickets, rewards, metrics, and
product `product.md` strategy sections are the existing evidence surfaces.

## Memory Split

Use the smallest owner for each kind of state:

| State | Owner | Changes when |
| --- | --- | --- |
| Stable thesis and guardrails | `farplane/harness.md` | explicit human-approved harness delta |
| North star, value function, goal axes, inline SMART goals, and durable goals | `farplane/goals.yaml` | horizon/goal delta with evidence and approval when material |
| Metric labels, units, chart behavior, pinned status, kind, and refresh prompts | `farplane/bindings.yaml` | metric recipe delta with source-gap proof |
| Product identity, lanes, workflows, KPI refs, goals, lane weights, current strategy, and loop contract | `farplane/products/<product>/product.md` | product-boundary or product-strategy update with evidence |
| Generated product registry | `farplane/products.json` | regenerated from product files |
| Product-loop learning | `farplane/products/<product>/progress.md` | local runtime hypothesis cycles, selected moves, feedback, learning, and next lever |
| Executable work | `tickets/TASK-*/ticket.md` | ticket creation, execution, review, closeout |
| Ticket-level spend justification | ticket `Reward` block | ticket creation or planning update |
| Active product/project runway decisions | Weekly Interval report and product `## Current Strategy` sections | weekly review or material evidence change |
| Receipts and ledgers | `.farplane/reports/**`, `.farplane/automation/*.jsonl` | Pulse/Interval/worker outcomes |
| Cadence and shared side-effect gates | `.farplane/automation/heartbeat-policy.json`, `farplane/automations.toml` | explicit automation/policy update |

This keeps flexible planning close to the product that learns from it without
turning every roadmap idea into a new global artifact family. Product worker
budgets, `max_tickets_in_review`, current strategy, loop contract, and
progress-entry shape live in `product.md`.

Products are goal-owned lanes, not independent mini-businesses. A product loop
deserves recurring Pulse attention only when it can name the global SMART goal,
product-local goal, KPI, guardrail, or interval strategy signal it is moving.
The generated product registry includes a goal-product matrix so Interval and
Pulse can cite the named goal instead of treating product existence as enough
reason to run.

Product `progress.md` is not an event stream. Do not write every Pulse skip,
worker reconciliation, reminder, archive receipt, no-op, or stale-strategy
finding into product progress. Those are Pulse report or automation-ledger
events. Product progress receives only product-loop learning: ranked candidate
moves, selected move, why, ticket and artifact refs, feedback result, learning,
next lever, blocker, and compact strategy-delta receipts when the learning
changes what the product should try next.

## Strategy Inputs And Next-Wave Planning

Weekly and Daily reports expose compact strategy inputs and may update
product strategy:

```text
ProductStrategyInput := product + focus + current_hypothesis + prefer + avoid
                      + blocked + expected_reward + allocation_hint
ProductStrategyChallenge := product_belief_reviewed + what_worked
                         + what_failed + keep + revise + drop
                         + double_down_guard + source_gap
ProductStrategyDelta := product + current_strategy_patch + source_report_ref
```

`farplane/products/<product>/product.md` `default_weight` values, rendered into
`farplane/products.json`, are the default allocation prior for product-loop
worker budgets. They bias how many workers each product loop gets; they are not
hard quotas. Daily strategy, blockers, source freshness, proof urgency, or a
Weekly strategy may override which product loop runs first, but the Pulse report
should record the reason.

Pulse's executable board is the reward-bearing AI-planned subset, not every
active ticket directory. Because tickets intentionally do not carry
`created_by`, Pulse discovers AI-planned work by parsing active ticket
frontmatter `rewards.kpi`. The body `Reward.kpi_rewards[]` block explains the
expected reward and guard, but the frontmatter marker is the board-classifier
input. `.farplane/automation/spawned-threads.jsonl` records worker/handoff
state, not ticket origin. Active operator/manual tickets without `rewards.kpi`
are diagnostics; they do not block refill and should not be repaired by Pulse
unless the operator explicitly opts them into AI planning with a valid
frontmatter marker plus matching body reward block.

When no reward-bearing AI-planned ready ticket can advance, Pulse may use:

```text
plan_next_wave_when_empty(product_strategies, weekly_strategy, daily_strategy,
                          ai_generated_board, manual_ticket_diagnostics,
                          product_md_files)
  -> eligible product-loop invocations + 0..N tactical tickets
   + worker handoffs + admission decision
```

Generated tactical tickets must be small, local, approval-free, and tied to a
current product-loop belief, active project, frontier step, strategy move, lane,
bottleneck, or reward signal. Each next-wave decision should name the product
loop and active belief being tested so Daily or Weekly can challenge it later.
Each generated ticket must include frontmatter:

```yaml
rewards.kpi:
  - accepted_harness_improvements
```

and a body `## Reward` block:

```yaml
kpi_rewards:
  - kpi_id: accepted_harness_improvements
    expected_reward: "one proof-backed shipped harness improvement"
    check_in_at: "2026-07-15T09:00:00+08:00"
    actual_result:
    reward_score:
    reward_score_reason:
guard: "stop before expanding scope or counting unproved intent"
```

`Reward` is also the ticket-level budget justification. `kpi_rewards` names the
KPI IDs the ticket is expected to move, the expected reward text, and the
check-in time when expected reward should be compared with observed reality.
`actual_result`, `reward_score`, and `reward_score_reason` are filled by the
interval reward-checkin analyzer. `reward_score` is a scalar from `-1` to `1`,
where `1` means the actual result strongly matched or exceeded the expectation,
`0` means unclear or weakly related, and `-1` means the actual contradicted the
expectation or created negative value. `guard` names the stop, resize, or
non-expansion boundary. Do not add another ticket field for budget reason unless
a future ticket proves `Reward` is insufficient.
Pulse autonomous selection is restricted to product-backed work. A ticket is
not proceedable for Pulse merely because it is ready; it must include
frontmatter `rewards.kpi` and parseable body `Reward.kpi_rewards[]` with at
least one KPI listed by a product `product.md` file and present in
`farplane/bindings.yaml`, and the ticket scope must produce that product output
or artifact workflow. Human-created tickets without `rewards.kpi` are
manual/operator work. Maintenance, Pulse, generator, metadata, or tooling
cleanup is only a repair arm when it directly unblocks an existing
product-backed ticket, not a primary next-wave worker ticket.

## Bold Reviewable Bet Pipeline

Product-loop next-wave planning should generate executable moves, not planner
tickets:

```text
generate_tickets(product_md, products_index, product_loop_progress,
                 goals.yaml, daily_report, weekly_report,
                 board_state, recent_evidence)
  -> product_loop_scan
  -> trend_tensions from last-7-day Feed Scout evidence
  -> leverage_moves from existing Farplane capabilities
  -> dedupe against recent tickets/artifacts/claims
  -> opportunity QA / reviewer requirements
  -> executable ticket specs with big claim + artifact level + reward + learning_writeback
  -> worker-thread handoffs with review notification instructions
```

The lean owner graph is:

```text
Pulse -> manager heartbeat, board admission, product-loop invocation, handoffs, receipts
product loops -> product-local next-move selection, worker budget, max_tickets_in_review, learning progress
ticket-opportunity-generator -> detailed executable ticket spec + opportunity QA contract
product skills -> workflow-specific artifact contracts and collocated product-loop files
goal-advisor -> approved ticket execution compilation
worker-artifact-review-request -> Telegram-first review exit gate
```

Pulse may summarize downstream gates, but should not duplicate the full
workflow doctrine for each owner. Its proof is operational: invoked/skipped
product loops, accepted/rejected specs, handoff rows, review receipts or
blockers, and decision/reward/report writeback.

Distribution and market-facing tickets use Feed Scout as attention evidence:
what changed, who cares, why people react now, and which Farplane claim can be
shown locally. Self-improvement, experiment, and ablation tickets use
leverage-advisor framing: capability, loss term, compounding move, baseline,
first proof step, and content upside. The final ticket must already contain the
idea; workers should not be asked to discover whether the idea is worth doing.

Every generated worker ticket needs a visible reviewable bet:

- `big_claim`: the external or operator-facing claim being tested or shown.
- `audience_tension`: why a real builder or Kenji would care.
- `surprise_factor`: what could make the result non-obvious.
- `baseline_or_contrast`: default, vanilla, normie, competitor-like, or current
  behavior when the result is audience-facing.
- `artifact_level`: the minimum artifact expected for the lane.
- `dedupe_status`: why this is not the same claim in the same format again.
- `review_surface`: what Kenji or a reviewer should inspect at completion.

Artifact levels are lane-specific. Experiments finish with a report containing
hypothesis, method, baseline/current behavior, result, conclusion, decision,
and limits. Ablations finish with a proof report comparing baseline and
variant. Trust distribution finishes with script, storyboard, visual/demo
brief, rendered clip, carousel, slides, or publish-ready thread; a note or
outline is only valid when explicitly scoped as a small planning card. Review
receipts, reminder pings, and approval waits are follow-up lanes, not product
throughput.

Product workflows live in product files and product skills, not in a separate
ticket-template matrix. `farplane/products/<product>/product.md` maps each
product to a primary skill such as
`farplane-experiment-report`, `farplane-ablation-proof`,
`farplane-productization`, `farplane-evidence-content`, or
`farplane-market-learning`. Generated tickets name the concrete instance:
product lane, primary skill, workflow id, claim/hypothesis, evidence refs,
artifact level, reward, guard, review surface, learning writeback target, and
final human gate. The owning product skill supplies the workflow todo list,
output contract, and collocated product-loop state.

Pulse-generated product work should never be a ticket whose main deliverable is
"call the product skill with this idea." The ticket is the concrete execution
sample. It names the artifact to produce, the product skill to use as the
process contract, the stop condition, the review surface, the reward check-in,
and the product progress writeback. If the next useful move is strategy,
prioritization, or idea selection, Pulse handles the bounded manager writeback
or requests Daily/Weekly planning instead of delegating a planning ticket.

## Product Loop File Equivalents

The product loop is the Farplane file equivalent of the Karpathy loop:

| Karpathy loop | Farplane file surface |
| --- | --- |
| Read code/state | product `product.md`, generated `farplane/products.json`, product-local `skill.md`, ignored `progress.md`, recent tickets/artifacts/metrics |
| Propose change | product-loop cycle entry with ranked candidate moves |
| Train/run small experiment | one concrete `tickets/TASK-*/ticket.md` worker attempt |
| Improved? | ticket proof, reviewer/Kenji verdict, metrics, review receipt |
| Commit | close/productize/update docs or skill behavior, then record learning |
| Roll back | reject/kill/revise ticket and record the failed move reason |
| Repeat | next product loop reads the progress tail and picks the next lever |

Tracked `product.md` files live beside product-local `skill.md` files under
`farplane/products/<product>/`. Runtime `progress.md` files at the same
location are ignored local learning state. Product identity, KPI refs, gates,
workflows, product-level goals, current strategy, loop contract, and progress
entry shape live in `product.md`. Product promotion and installation must not
treat live `progress.md` as reusable doctrine.

When a worker artifact is ready, the worker must use
`worker-artifact-review-request`. That wrapper borrows the
`optimize-with-human` enforcement pattern:

```text
artifact_ready(ticket, artifact, worker_thread_ref)
  -> feedback_channel=telegram
   + feedback_policy=ask_when_artifact_ready
   + phone-readable teaser
   + Telegram message id
   + review-cycle receipt
   + turn-exit gate satisfied
```

Fallback is not a normal deliverable. It is valid only when `telegram-message`
proves the route, credentials, or phone-readable review surface is unavailable
and records the exact blocker. A worker waiting on Kenji cannot stop silently:
it must record either a Telegram message id or a blocker. The review request
must be readable on a phone, include archive-safe artifact refs, ask one reply
action, and sell why the artifact matters now. Sending the review request does
not approve posting, publishing, spending, deploying, external contact, account
mutation, metric mutation, or follow-up ticket creation.

Review teasers are part of the worker artifact contract. A good Telegram
review request should include a provocative title, why Kenji should care, the
surprising claim or result, the artifact payoff, the exact reply action, and
desktop-only refs after the reviewable summary. Content and distribution
workers should include a thumbnail concept, visual hook, or rendered preview
when that is the natural review surface.

Human-review chasing is shared project policy from the freeform
`farplane/bindings.yaml#operator.review_chase_policy` prompt, not
per-automation config sprawl. Product Pulse, Taste Loop, and
`worker-artifact-review-request` read that prompt plus Kenji's active hours.
Skills own the timing defaults and receipt mechanics. A pending review remains
chaseable even after the worker ticket is archived if its review-cycle receipt
still expects Kenji's judgment. During active hours, due unanswered review
waits send worker-owned Telegram reminders first; if the stale Telegram
reminder remains unanswered, the loop routes one `phone-chaser` call for that
feedback item or records the blocker. There is no global daily phone cap; the
repeat guard is one phone escalation per feedback item unless a new
artifact/review cycle is created. Outside active hours, the loop records the
queued chase rather than silently returning `DONT_NOTIFY`.

Pulse is a manager heartbeat, not an implementation worker or all-product
planner. When it creates or admits a ticket, it should create a named
worker-thread handoff in the same beat under product-loop worker policy. The
parent beat may repair metadata, reconcile closed threads, invoke product
loops, and write state, but it should not implement the ticket body inline. If
a worker-thread tool is unavailable, Pulse records the handoff packet and
leaves the ticket ready/unclaimed instead of consuming the ticket itself.

Next-wave planning invokes product loops before ticket creation. Lane weights
derive product-loop worker budgets, not a global quota, and the Pulse report
should show invoked/skipped product loops with compact reasons. A one-ticket
wave is valid when one product loop has capacity and one specific,
evidence-backed, low-gate premise survives the specificity, review, learning
writeback, and autonomy gates.

Pulse still writes `request_planning` when the strategy inputs are stale,
missing, unsafe, require material product, KPI, goal, publishing, spend,
account, customer-contact, or authority decisions, or when a safe-local-prep
scan is exhausted. A final human gate alone is not an idle reason: while Kenji
is unavailable or review backlog is high, Pulse should prefer local proof,
research, packaging, ranking, draft, experiment, ablation, or review-request
work that can proceed without irreversible action.

Active complete/done tickets should not remain on the active board. Pulse may
archive them as mechanical board hygiene before selection when the ticket is
already complete/done and `ready: false`; otherwise it records the archive
needed receipt. The pre-commit closure gate blocks the current session's active
ticket and also rejects active complete/done tickets that should have been
archived.

Before:

```text
latest interval report -> one safe tactical ticket -> maybe parent execution
```

After:

```text
goals/products + product strategies + latest interval reports
  -> active product frontier + needed metric readings
  -> eligible product-loop invocations
  -> product-local move + bounded artifact ticket
  -> worker-thread handoffs under product-loop worker policy
  -> product-loop progress learning writeback
```

Daily and Weekly should read goal-axis SMART goals semantically. For each
active SMART goal, use its `kpis` to find metric recipes in
`farplane/bindings.yaml`; each recipe gives the interval agent a prompt-only
`refresh` instruction for today's reading. Do not parse interval reports as a
deterministic strategy database; use them as receipts that justify product
`## Current Strategy` updates and next ticket candidates.

## Daily Metric Update Lifecycle

Daily Interval owns the normal metric refresh cadence. It should refresh the
sources first, then compile the UI snapshot; the UI must not invent missing
metric state from stale bindings or goals.

```text
goals.yaml SMART goals
  -> KPI ids and targets
bindings.yaml metric recipes
  -> labels, products, units, display, pinned status, refresh prompts
platform skills and Core primitive reducers
  -> canonical MetricObservationBatch files
farplane project snapshot
  -> .farplane/project/ui/latest.json for Overview, Goals, Products, and tabs
interval report
  -> interpretation, source gaps, instrumentation tickets, next-window plan
```

The update order is:

1. Select KPI scope. Read active goal axes and SMART-goal KPI IDs from
   `farplane/goals.yaml`, then join each KPI ID to `farplane/bindings.yaml`.
   Missing KPI definitions are validation failures, not UI warnings.
2. Refresh external or skill-owned observations. Platform skills such as
   `instagram-account` and `x-account` fetch their own APIs or ledgers and
   write `.farplane/metrics/observations/<source_id>/<YYYY-MM-DD>.json`.
   Each file must validate as `MetricObservationBatch`.
3. Refresh Core primitive observations. Run:

   ```bash
   farplane metrics primitives --project-root <project> --date <YYYY-MM-DD>
   farplane metrics primitives --project-root <project> --date <YYYY-MM-DD> --ticket-status rejected
   ```

   Core reducers count ticket rewards, autonomy ratios, intervention metrics,
   AI spend estimates, and rollups such as total evidence-distribution views
   from Farplane-owned files and existing observation batches. The debug/index
   snapshot under `.farplane/metrics/daily/<date>.json` is optional support
   state; it is not the canonical provider contract.
4. Compile the project snapshot:

   ```bash
   farplane project snapshot --project-root <project> --date <YYYY-MM-DD>
   ```

   The compiler validates `goals.yaml`, `bindings.yaml`, and observation
   batches, joins targets and descriptions into metric definitions, builds
   series, propagates source-gap IDs, and writes
   `.farplane/project/ui/latest.json`.
5. Interpret and plan. The interval report reads the snapshot, names true
   source gaps, and creates instrumentation or access tickets when a missing
   provider blocks a real KPI. Human-created tickets without KPI rewards and
   old tickets with missing front matter are not metric source gaps; they are
   legacy or manual-work context.

Source-gap rules:

- Missing credentials, missing API fields, missing files, unsupported feedback
  mechanisms, or malformed observation batches are source gaps.
- A KPI listed in `goals.yaml` but absent from `bindings.yaml` is a validation
  failure.
- A metric with no current observation may show `missing` on its own KPI row,
  but it should become a global Needs Attention item only when the missing
  source blocks an accountable KPI or pinned rollup.
- Composite rollups should use the same observation shape as primitives. When a
  component has no same-day reading, Core may use the latest available reading
  on or before the snapshot date if the metric recipe says that is acceptable;
  otherwise it records a source gap.

Primitive metric contract:

```text
farplane metrics primitives(project_root, date, codex_home?, monthly_spend?)
  -> .farplane/metrics/daily/<date>.json
   + .farplane/metrics/observations/<primitive_id>/<date>.json
```

`.farplane/metrics/daily/<date>.json` is the raw primitive snapshot. It contains
the run window, diagnostic parse gaps, source gaps, support paths, and a
`primitives` map. This is useful for debugging and drilldowns, but the snapshot
compiler prefers canonical observation batches when they exist.

Each `.farplane/metrics/observations/<primitive_id>/<date>.json` file is a
`MetricObservationBatch`:

```json
{
  "schema_version": 1,
  "date": "2026-07-03",
  "source_id": "ticket_count_by_kpi",
  "status": "available",
  "observations": [
    {
      "metric_id": "accepted_harness_improvements",
      "date": "2026-07-03",
      "value": 2,
      "status": "available",
      "payload": {
        "tickets": []
      }
    }
  ],
  "gaps": [],
  "payload": {}
}
```

Primitive families:

| Primitive | Emits | Inputs | Notes |
| --- | --- | --- | --- |
| `ticket_count_by_kpi` | One observation per KPI ID found in `Reward.kpi_rewards[]`. Missing KPI rows compile as available zero for defined KPIs. | `tickets/**/ticket.md` | Human-created tickets without KPI rewards are diagnostics, not source gaps. Use `--ticket-status rejected` for a filtered companion reading; `ticket_count_by_kpi_status:rejected._total.value` is the rejected reward-bearing ticket count, and per-KPI rows support rejection-rate diagnosis. |
| `ticket_count_by_product` | `ticket_count_by_product:<product_id>` observations with touched, completed, and proofed ticket counts in payload. | product `product.md` KPI refs, `farplane/bindings.yaml#metrics`, ticket rewards | Product is transitive: product -> KPI IDs -> tickets. Tickets do not need `product_id`; metric recipe `product` fields remain a support-bucket mirror for groups without product files. |
| `kpi_attributed_ticket_ratio` | One ratio observation for rewarded tickets over touched tickets. | ticket rewards | Empty windows are available zero readings. |
| `codex_thread_usage` | Thread count, turn count, total token count, and span-minute observations through metric projection. | `~/.codex/sqlite/state_5.sqlite`, `~/.codex/sessions/**/*.jsonl` | Missing local Codex stores are source gaps. |
| `ai_burn_estimate` | Daily allocated AI spend plus derived burn-per-thread, burn-per-turn, and burn-per-token metrics. | monthly spend model plus thread usage | Missing spend model is a source gap for burn metrics. |
| `content_views_total` | `evidence_distribution_reach` rollup. | platform observation batches for `instagram_views`, `x_views`, `github_views` | Uses latest available component readings on or before the snapshot date. |
| `ticket_thread_association_backfill` | Association count plus support index rows. | `.farplane/mine/runs/**/input.json` | Backfill confidence is `completion_only`; it does not prove post-start intervention metrics. |
| `ticket_thread_link_coverage` | Ratio of completed tickets with association rows. | completed tickets plus association index | Support metric for debugging association coverage. |
| `autonomy_time_feedback` | `auto_time_ratio` and related human/autonomous time metrics when interval runtime ledgers exist. | `.farplane/events`, spawned-thread, and reward ledgers | Interval-owned provider shape; emits the same observation batch schema. |
| `ticket_intervention_feedback` | `auto_completion_rate`, `intervention_free_ticket_count`, `ticket_intervention_turn_count`. | tickets, association index, runtime events | Emits source gaps when completed tickets cannot be associated with execution threads. |

Primitive-to-snapshot compilation:

```text
MetricObservationBatch rows
  -> provider_observations()
  -> metric cards, chart series, pinned cards, goal KPI rows, product rollups

.farplane/metrics/daily/<date>.json primitives
  -> daily_observations() fallback only when no canonical batch exists
```

The compiler maps metric IDs to primitive IDs from `bindings.yaml` refresh
recipes and Core's primitive catalog. Canonical batches win over raw daily
fallbacks to prevent duplicate series. Source gaps propagate by ID into metric
cards and top-level `source_gaps[]`; the UI renders those gaps instead of
creating its own warnings.

## Reward Check-In Lifecycle

Expected reward is a planning claim with a time horizon. Generated and
interval-planned tickets should include `check_in_at` on each
`Reward.kpi_rewards[]` item. Daily and Weekly may enable the same
`reward_checkins` interval workflow:

```text
reward_checkins(ticket_dir, now, lookback_days, bad_threshold)
  -> due reward items missing actual_result or reward_score
   + already-scored low predictions
   + source gaps
   + retro ticket candidates only when follow-up is useful
```

At check-in, an analyzer fills:

```yaml
actual_result: "what really happened"
reward_score: 0.35
reward_score_reason: "actual partially matched expected reward"
```

`reward_score` is `-1..1`: `1` means actual strongly matched or exceeded
expected reward, `0` means unclear or weakly related, and `-1` means actual
contradicted expected reward or created negative value. The scalar is planning
calibration, not a KPI value. Low-scoring predictions should influence product
strategy or spawn a retro ticket only when they reveal a real investigation,
instrumentation, or strategy task.

Maintenance work should compete against the active frontier. It is selected
only when it unblocks the focus, protects proof, or has a clearer reward signal
than the current project work.

Daily and Weekly challenge product strategies; they do not turn every
interesting idea into a new row somewhere else. Use:

```text
working evidence -> keep or double down under guard
failed evidence -> revise, narrow, or drop
missing evidence -> source_gap or instrumentation ticket
```

## Budget And Runway

Fast AI-worker loops still need protected runway. Quarterly goals protect
compounding bets from daily noise; weekly intervals decide whether each active
project deserves another planning window.

Weekly Interval should write a Budget / Runway Review before the next-window
plan. It should cite active products/projects from product `## Current Strategy` sections, ticket
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
  strategy axes, current milestone, and material `farplane/goals.yaml` deltas.
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
- `pulse-update` delegates ready tickets to worker threads up to policy cap,
  records immediate outcomes, creates bounded tactical next-wave ticket waves
  from fresh strategy when the board is empty, or writes a planning request when
  no safe tactical work exists.

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
for Pulse delegation. When the board is empty, Pulse may also create small
tactical ticket waves directly from the latest Weekly/Daily strategy and
product lane weights, then hand them to worker threads. The next daily and
weekly intervals read the resulting reports
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
