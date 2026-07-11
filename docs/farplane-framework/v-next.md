---
title: "Farplane Framework V-Next"
status: implemented
owner: farplane-framework
created_at: 2026-07-10
updated_at: 2026-07-11
tags:
  - farplane
  - framework
  - v-next
  - pulse
  - self-improvement
refs:
  - docs/farplane-framework/README.md
  - docs/farplane-framework/pulse-and-interval-loop.md
  - docs/farplane-framework/ticket-execution-loop.md
  - docs/systems/work-loop.md
  - docs/systems/horizon-loop.md
  - docs/systems/self-improvement-learning.md
  - skills/pulse-update/SKILL.md
  - skills/interval-update/SKILL.md
  - skills/ticket-opportunity-generator/SKILL.md
  - skills/dogfood-review/SKILL.md
  - skills/self-improve/SKILL.md
  - skills/optimize-with-human/SKILL.md
  - farplane/automations.toml
---

# Farplane Framework V-Next

Farplane Framework V-Next reconstructs Farplane from its smallest useful
operating loop. Workstreams 1 and 2 are active, and Workstream 3 is implemented
as reader retirement (`TASK-0321`) plus the metrics/manifest contract
(`TASK-0322`).

The intended reader is a Farplane operator reviewing and staging this model as
the replacement for product-scoped Pulse, interval-owned planning, and
overlapping self-improvement workflows. Workstream 1 is implemented under
`TASK-0318`; Workstream 2 is implemented under `TASK-0319` and refined under
`TASK-0320`; Workstream 3 is implemented under `TASK-0321` and `TASK-0322`.

The central model is:

```text
Farplane = program + progress
```

```text
program  = current policy for choosing and performing work
progress = durable observations, resumable state, and outcome history
```

The practical framework adds a Kanban projection, tickets, reusable skills,
external context providers, and Codex-native execution. Those are useful
representations of the kernel, not a second ontology.

## Status And Decision Boundary

The active migration establishes:

- one project-level Work Pulse instead of product-scoped Pulse loops;
- one shared executor for ordinary and self-improvement tickets;
- Pulse-owned BAU planning when executable work is missing;
- separate planning and dispatch parameters;
- a bounded weekly self-improvement automation that calls `dogfood-review` to
  review active and recent archived experiment history, carry a derived
  portfolio outcome ledger, rank hardening, refinement, documentation, and
  feature-maintenance levers, and create a bounded non-interfering experiment
  wave from available capacity;
- evidence routing that may directly adopt and monitor a clear change, run a
  local or toy proof, request expert feedback, or schedule a delayed pilot;
- due check-ins as ticket eligibility, not separate check-in tickets;
- Daily and Weekly Interval as report and context surfaces that may resurface
  already-observed maintenance problems, but do not invent strategic direction;
- one base heartbeat—the project Work Pulse—while Feed Scout, Daily, Weekly,
  and self-improvement remain bounded scheduled or manual jobs;
- capability skills as the project specialties used by Work Pulse;
- whole-harness improvement as a sequence of bounded surface changes, not
  optimization of one concatenated prompt;
- content-market optimization as a separate future feature, not part of the
  v-next kernel;
- `metrics.yaml` as the metric-definition owner and `bindings.yaml` as the
  connector/provider-configuration owner;
- ticket artifacts as the evidence, QA, and review owner and
  owner-named generated projections only when a proven consumer needs them,
  with no mandatory generic registry, runtime, evidence, or review bucket.

`TASK-0318` owns the implemented Workstream 1 Pulse, planner, automation, and
direct documentation migration. `TASK-0319` owns the implemented Workstream 2
scheduled-source, experiment, reward, and maintenance changes described here.
`TASK-0320` owns the portfolio-learning, bounded-wave, and executable check-in
program refinement. `TASK-0321` and `TASK-0322` own the completed Workstream 3
project-file migration.

## 1. Theoretical Kernel

The irreducible loop is:

```text
step(program, progress, context?) -> action + progress_delta + next_wake?
```

`program` contains the instructions that remain valid across turns. `progress`
contains enough state and history to resume without hidden transcript memory.
`context` contains observations that are current but do not necessarily belong
inside the stable program.

The minimal project program is:

```text
if an executable ticket exists:
  do the ticket
else:
  plan the next tickets
```

The minimal project progress is:

```text
ticket history + outcomes + current ticket states
```

The Kanban board is rendered from a generated ticket registry:

```text
ticket_registry = generate_registry(tickets)
kanban = render_board(ticket_registry)
```

The board is not the complete progress record. External observations,
experiment rounds, metric snapshots, human decisions, and check-in results may
also be progress even when they do not deserve independent tickets.

### Minimal Pulse

The smallest useful function is:

```text
plan(harness, goals, metrics, ticket_history, current_context?, wave_size)
  -> 0..wave_size ticket_specs
```

```text
pulse(tickets) =
  do(select_ticket(tickets))  if executable_ticket_exists(tickets)
  else plan(harness, goals, metrics, ticket_history, current_context, wave_size)
```

The v-next form makes inputs and outputs explicit:

```text
plan(program, objective_contract, ticket_history, external_context?, wave_size)
  -> 0..wave_size executable_tickets
```

```text
work_pulse(program, objective_contract, tickets, external_context?, policy)
  -> reconciliation
   + ticket_deltas
   + worker_handoffs
   + human_review_requests
   + next_wake?
```

`objective_contract` is the required optimization boundary. It may currently
be represented by project goals, but conceptually it contains value direction,
metrics, guardrails, anti-metrics, horizon, and authority. Time-bound goals may
remain useful human commitments without becoming the only way the agent
understands value.

Implemented sanity proof:

```text
todo ticket   -> dispatch_ready; planner is not called
empty board   -> plan_next_wave; planner writes nothing; Pulse materializes
wave_size     -> maximum ticket specs created
worker_limit  -> maximum concurrent handoffs
review wait   -> worker released; review_wip applies human backpressure
```

The deterministic board cases live in
`skills/pulse-update/scripts/test_list_pulse_board.py`. The callable ownership
and planning-input contract lives in `skills/pulse-update/SKILL.md` and
`skills/ticket-opportunity-generator/SKILL.md`; both bind `harness.md`,
`goals.yaml`, `metrics.yaml`, and ticket history, while dated reports are
optional current context.

## 2. Practical Kanban And Work Pulse

Tickets make the theoretical progress record easier to resume, delegate,
review, and visualize. They own bounded commitments and their proof state.

Work Pulse has four responsibilities:

1. Reconcile completed, failed, blocked, waiting, and review-ready work.
2. Select and dispatch eligible tickets.
3. Request human review once, then release the worker and mark the ticket
   `awaiting_review`.
4. Call `plan(...)` when the admitted board meets the configured refill
   condition.

The smallest honest model mirrors a human operator: one worker empties one
board, asks for help when authority is missing, and plans the next bounded wave
when useful work runs out. Additional workers are a throughput parameter added
after this behavior works with one worker.

The first prototype uses an empty-board refill condition:

```text
plan only when no executable todo ticket or due check-in exists
```

A low-watermark that plans before the board is empty is a later throughput
optimization and requires its own admission and duplicate-supply proof.

Work Pulse may invoke high-level capability skills to perform ticket work. It
does not need product-local controllers to call a content, sales, engineering,
research, or support workflow.

Work Pulse executes both ordinary project work and improvement work. The
ticket creator differs; the dispatcher does not:

```text
BAU planner                 -> ordinary tickets
weekly self-improvement     -> 0..experiment_wave_size improvement tickets
Work Pulse                  -> execute any eligible ticket
```

If the same Pulse executes both classes, `Work Pulse` is the canonical term.
`BAU` describes one source or class of ticket, not a separate controller.

### Planning And Dispatch Are Different Parameters

```text
wave_size                    = maximum BAU tickets per refill
worker_limit                 = maximum concurrent worker threads
review_wip                   = maximum tickets waiting for human review
experiment_wave_size         = maximum new experiment packets per weekly run
experiment_wip_limit         = maximum active experiments across the portfolio
max_concurrent_live_delayed  = maximum delayed live-harness interventions
```

```text
plan_next_wave(..., wave_size = m) -> 0..m tickets
dispatch(tickets, idle_workers = n, review_wip_limit = r) -> handoffs
```

`wave_size` does not equal `worker_limit`. Planning creates a useful backlog;
dispatch fills currently idle execution slots. Review WIP provides
backpressure without forcing worker threads to remain alive while waiting for
a human.

The default review transition is:

```text
worker produces artifact and proof
-> worker sends one review request
-> ticket becomes awaiting_review
-> progress.md records artifact/thread/request/reminder state
-> worker exits
-> Work Pulse continues other eligible work
```

When `review_wip` is full, Work Pulse stops creating additional
review-producing work or chooses work that can close existing review gaps.
It does not chase merely because the queue is full. Pulse may send at most one
undecided review whose ticket-owned `next_reminder_at` is due, without assigning
an execution worker.

The first prototype used one global improvement slot to prove the path. After
that proof, portfolio capacity becomes explicit: total experiment WIP remains
bounded, delayed live interventions retain a stricter cap for attribution, and
unrelated immediate toy/eval proofs may use remaining non-interfering slots.

### Ticket Eligibility

The practical selector includes both ordinary work and matured check-ins. Due
state is derived from the existing ticket Reward and program contract.
`waiting_signal` is the one explicit dormant lifecycle status; there is no
`checkin_ready` field:

```text
due_checkins = derive_due_checkins(ticket_reward, program, now)
eligible_tickets = ordinary_executable_tickets + due_checkins
```

Human-review lifecycle state `awaiting_review` is never executable. The worker
is already released while review WIP provides backpressure.

An experiment waiting for reality is not blocked work. It is intentionally
dormant `waiting_signal` work with a named wake condition. A matured Reward row
temporarily makes the original ticket executable for its Check-In Program.

### Minimal Ticket Metadata

```text
ticket(ticket_id, title, status, created_at, updated_at;
       priority?, claimed_by?, depends_on?, human_gate?, compute_target?)
```

`status` is the sole lifecycle truth. Readiness is derived from `status: todo`,
claim, dependencies, or a matured Reward row on `waiting_signal`. Approval is
`awaiting_review`; external blocker detail, current action, review state, and
verification belong in `progress.md`; QA/demo/reviewer obligations belong in
`QA Strategy`. There is no parallel `phase`, `ready`, `approval_required`,
`blocked_by`, QA flag, next-action field, or last-verification field.

## 3. Context And Replanning

Planning should use current external context without embedding trends or live
facts inside stable skills.

```text
plan(
  program,
  objective_contract,
  active_tickets,
  ticket_history,
  current_context?,
  wave_size
) -> executable_tickets
```

`current_context` is a freshness-bounded bundle of recent report summaries and
external/provider observations. Reports are optional evidence, not a second
planning authority or a required parameter family.

Skills remain reusable procedures. Feed Scout, Tasty Packs, market feeds,
analytics, user feedback, prices, and competitor evidence are context
providers.

New context does not always justify replanning. It passes a materiality gate:

```text
replan(new_evidence) only if:
  an active assumption is invalidated
  or a threshold is crossed
  or a ticket check-in matures
  or a blocker clears
  or the ranked next action changes
  or an authority or safety condition changes
```

Otherwise the evidence is recorded for the next planning or reporting pass.

Event-driven context should wake Pulse when a provider supports it. Sources
such as Feed Scout or market snapshots that are naturally collected in batches
run as their own bounded scheduled jobs and write dated provider reports. Daily
Interval may read those reports; it does not own or embed the provider run.

## 4. Self-Improvement Model

V-next treats a skill, higher-order workflow, planner, capability, or harness
surface as a policy that may be improved when it has a credible metric and
proof path.

The optimization unit remains bounded:

```text
improve(target_surface, operator, objective, proof_policy)
  -> improvement_ticket + proof_route + evidence + promotion_decision
```

Not every improvement needs an experiment. V-next first chooses the cheapest
honest proof route:

```text
route_change(change, gap, risk, available_feedback)
  -> adopt_and_monitor
   | deterministic_replay
   | toy_experiment
   | agent_or_adversarial_eval
   | optimize_with_human
   | delayed_pilot
   | reject_or_defer
```

### Improvement Admission And Proof Routing

| Situation | Default route | Promotion requirement |
| --- | --- | --- |
| A required capability is missing or a named invariant is violated | Adopt, verify, and monitor | Direct checks pass, scope is bounded, and rollback is clear |
| A proposed change follows from first principles but can regress adjacent behavior | Implement behind a bounded proof or local replay | Before/after evidence supports the claim and guards do not regress |
| The real outcome is slow but a representative local proxy exists | Toy project or local simulation | Proxy is representative enough to falsify the claim and the result passes review |
| Agent, prompt, skill, or workflow behavior is uncertain | Eval, behavior test, or ablation | Baseline and candidate evidence support keep, revise, or reject |
| Expert or operator judgment is the fastest honest signal | `optimize-with-human` | Reviewable artifact, focused question, recorded feedback, and repeated evidence before doctrine promotion |
| No faithful fast signal exists | Bounded delayed pilot with a check-in | Declared maturity, budget, guard, decision, and rollback |
| No credible proof or feedback provider can be named | Reject or defer | New evidence changes the proofability of the proposal |

“Logically better” is not an evidence exemption. Direct adoption is reserved
for changes that close a named gap or invariant, have limited blast radius,
and can be verified and rolled back. The system then monitors whether the
reasoning survived real use.

Toy experiments are preferred when they compress a long feedback loop without
removing the causal mechanism that matters. A toy result is evidence for a
bounded pilot, not automatic proof that the full harness will behave the same.

Human or expert feedback is a real metric provider when mechanical metrics
would be dishonest. `optimize-with-human` structures the feedback contract
after a qualified operator or expert and reply path are already bound; finding
or recruiting that expert is an upstream research or outreach task. The
feedback loop keeps its target, phase, artifact, question, verdict, and next
hypothesis in the same ticket `program.md` and `progress.md`; a single rejection
changes the local attempt, not global doctrine.

### Hardening And Refinement

Hardening and refinement are complementary operators, not independent runtime
systems.

```text
harden(surface, metric, cost_ceiling)
  -> maximize robustness and metric performance without exceeding cost ceiling
```

Hardening may add or strengthen instructions, examples, eval cases, checks,
guards, fallbacks, or proof requirements. It is not synonymous with adding
more prose.

```text
refine(surface, quality_floor)
  -> minimize complexity, context, latency, or operations while preserving quality floor
```

Refinement may delete duplication, collapse steps, narrow context, remove
unproven ceremony, or replace several operations with one better primitive.

The combined objective is a Pareto frontier:

```text
quality up
robustness up
complexity down
latency and cost down
```

A hardened candidate is rejected when added complexity does not buy meaningful
quality. A refined candidate is rejected when it falls below the quality or
safety floor.

### Improvement Surfaces And Feedback

| Surface | Immediate feedback | Delayed feedback | Typical operations |
| --- | --- | --- | --- |
| Skill instructions | Eval assertions, reviewer rubric | User success across real calls | Add, delete, rewrite, split, merge |
| Higher-order workflow | Deterministic workflow replay | End-to-end outcome quality | Reorder calls, change routing, change context |
| Planner / Pulse policy | Ticket-quality eval, replay | Goal progress, review load, wasted work | Change selection, wave, budget, or admission rules |
| Capability skill | Artifact QA | Audience, customer, adoption, or operational result | Change factory workflow, inputs, outputs, or method |
| Automation | Config validation, dry run | Cadence value, intervention rate, missed events | Add, delete, modify cadence or prompt |
| Agent policy | Behavior eval, adversarial QA | Repeated operator corrections | Add, delete, move, or compact instructions |
| Hook or validator | Unit and integration tests | False positive or false negative rate | Add, delete, modify implementation or gate |
| Feature bundle | Component proof | User or system outcome | Change its skill, hook, automation, or documentation surfaces |
| Harness selection policy | Local change results | Project value and intervention burden | Select the next bounded surface change |

### Immediate Reward

When the result is observable inside the execution window, use native Goal
execution with ticket-backed program and progress state:

```text
baseline
-> candidates
-> immediate eval
-> compare
-> promote / reject / continue
```

Typical cases include prompt evals, deterministic skill checks, parser
behavior, code performance, workflow replay, and skill compaction under an
existing quality floor.

`self-improve` must classify the reward before choosing its loop:

```text
self_improve(target, metric, feedback_class, ticket, program?, progress?)
  -> immediate_result | waiting_signal
   + comparison_evidence
   + promotion_decision?
```

For `feedback_class = immediate`, it runs the baseline, candidates, comparison,
and promotion decision inside the current Goal-backed execution window. It does
not create a future check-in merely to preserve a uniform workflow.

### Delayed Reward

When the result arrives after time, exposure, external action, or human
feedback, use a persistent improvement ticket with a maturity condition:

```text
intervention
-> record exposure and baseline
-> waiting_signal
-> check in when mature
-> record evidence
-> promote / continue / prune / rollback
```

The improvement state belongs in the original ticket and its Goal Packet. A
generated ticket registry may surface due work, but the registry is not the
canonical state owner.

For `feedback_class = delayed`, `self-improve` reuses the existing ticket
Reward fields and Goal Packet rather than adding experiment metadata or a new
registry:

```yaml
ticket.md:
  Reward.kpi_rewards[]:
    kpi_id:
    expected_reward:
    check_in_at:
    actual_result:
    reward_score:
    reward_score_reason:
program.md:
  Metric Provider:
    signal:
    minimum:
  Heartbeat Policy:
    wake_condition:
  Stop Conditions:
    complete_when:
    pause_when:
  Rollout Policy:
    promotion_rule:
    rollback_or_hold_rule:
```

`ticket.md` owns the expectation and current check-in contract, `program.md`
owns the loop policy, and `progress.md` owns append-only observations. The due
projection may be generated for Pulse, but it is not another hand-maintained
ticket field. A reward row is due when `check_in_at <= now` and its
`actual_result` or `reward_score` is still empty. When several rows are due,
the check-in handles every matured row and leaves future rows dormant.

## 5. Feedback Compression And Special Experiments

The v-next kernel does not require multi-arm experiments, continuous A/B
testing, or parallel harness variants. Those are optional methods for proposals
whose uncertainty and cost justify them.

### Fast Feedback Methods

| Method | Use when | What it compresses | Guard |
| --- | --- | --- | --- |
| Deterministic replay | The same inputs can exercise baseline and candidate | Repeated real calls | Preserve representative cases and guards |
| Toy project | A smaller environment preserves the uncertain mechanism | Long or risky real-harness feedback | State what the toy omits before transfer |
| Batch or “spam” A/B | Independent samples are cheap and rapid market or system feedback exists | Slow sequential trial-and-error | Fix budget, attribution window, and interference boundary |
| Agent or adversarial eval | The change affects prompts, skills, agents, review, or coordination | Repeated behavior failures | Keep baseline, cases, logs, and judge criteria visible |
| Expert or operator review | Judgment is more honest than a fake mechanical score | Taste, strategy, product, or domain expertise | Ask one reviewable question and record the feedback cycle |
| Bounded delayed pilot | Only real deployment or elapsed time supplies the signal | Irreducibly external feedback | Cap exposure and define maturity, rollback, and stop |

Batch A/B testing can collect more feedback per unit time when samples are
independent and the intervention is cheap. Parallel experiments are safe only
across surfaces with different interference keys. These methods belong to the
selected improvement ticket’s program; they are not permanent project loops.

### Toy Experiment Contract

```yaml
target_ref:
claim:
real_feedback_delay:
toy_environment:
preserved_mechanism:
known_omissions: []
baseline:
candidate:
metric_or_reviewer:
guard_metrics: []
budget:
promotion_rule:
real_pilot_required:
rollback_rule:
```

A toy experiment should make a questionable feature easier to reject. It must
not be designed only to make the candidate look good. When the toy omits an
important real-world mechanism, the result can justify a small pilot but not
full adoption.

### Content-Market Optimization Is Separate

Content-market search is explicitly outside the base harness-improvement
kernel. A content capability may use a Tasty Pack as its idea prior:

```text
idea = sample(taste_pack)
artifact = content_workflow(idea)
market_signal = publish_and_observe(artifact)
```

Tasty Packs supply plausible patterns and references; they do not prove that a
particular artifact will win. Repeated market sampling, spam-style variant
launching, algorithm-facing selection, and adaptive content rounds may become
a separate feature after Work Pulse and weekly self-improvement work.

The base framework only needs the content capability skill to assemble the
artifact and the ordinary ticket to record its output. It does not need content
arms, parent/child experiment tickets, or a content-specific Pulse.

## 6. Check-In Contract

A check-in exists to decide whether an intervention should continue, end,
promote, or roll back.

```text
checkin(ticket, program, progress, matured_rows, new_evidence)
  -> record_metric_delta
   + accept | kill | iterate | monitor
   + next_wake?
```

The resumed check-in worker does not reconstruct experiment policy from Pulse
instructions. Pulse supplies the original `ticket.md`, `program.md`,
`progress.md`, matured Reward-row indexes, and available evidence. The worker
reads `program.md` first and executes its `Check-In Program`:

```text
Pulse derives due rows
-> worker reads program.md / Check-In Program
-> inspect Metric Provider evidence and minimum
-> update only matured Reward rows
-> append progress
-> apply accept | kill | iterate | monitor
-> leave future/completed rows unchanged
```

A delayed experiment reuses the exact ticket Reward rows plus existing Goal
Packet sections:

```yaml
ticket.md:
  Reward.kpi_rewards[]:
    check_in_at:
    actual_result:
    reward_score:
    reward_score_reason:
program.md:
  Check-In Program:
    inputs:
    instructions:
    writeback:
    output:
  Metric Provider:
    signal:
    minimum:
  Heartbeat Policy:
    wake_condition:
  Stop Conditions:
    complete_when:
    pause_when:
  Rollout Policy:
    promotion_rule:
    rollback_or_hold_rule:
```

`check_in_at` is the row's fallback date. `Heartbeat Policy.wake_condition`
names an event when available. `Metric Provider.minimum` names the amount or
quality of evidence required.

The decision vocabulary is deliberately small:

- `accept`: keep or promote the intervention and close the experiment;
- `kill`: prune or roll back the intervention and close the experiment;
- `iterate`: resume executable work immediately with an updated hypothesis;
- `monitor`: remain dormant and update the next check-in condition.

The preferred selector is:

```text
pulse(ordinary_executable_tickets + derive_due_checkins(tickets, programs, now))
```

This removes the need to create a separate future ticket whose only job is to
look at the original ticket. A scheduler or frequent heartbeat only needs to
wake Work Pulse; the original ticket appears in the generated due projection
when its check-in condition is ready.

V-next does not require parent and child experiment tickets. One improvement
ticket folder owns the current program, progress, baselines, candidates,
feedback, and decisions:

```text
TASK-IMPROVEMENT/
  ticket.md
  program.md
  progress.md
  artifacts/
    baseline/
    candidates/
    results/
    qa/
    review/
```

When the experiment returns `monitor`, update `check_in_at` or its event
condition on the same ticket and append the new observation to `progress.md`.
Create another ticket only when the next change is independently executable,
reviewable, or valuable outside the original experiment—not merely because
another check-in or internal variant exists.

## 7. Whole-Harness Improvement

The whole harness is a graph of related surfaces, not one prompt to
concatenate and optimize blindly.

The harness snapshot may include:

```text
objective contract
agent policy
skills and capability refs
hooks and validators
automations
bindings and context providers
active experiment programs
recent failures and reports
```

Dogfood Review uses the snapshot to choose bounded experiment levers:

```text
plan_harness_experiment(
  harness_snapshot,
  objective_contract,
  metrics,
  failure_and_feedback_history,
  active_and_recent_archived_experiments,
  previous_dogfood_report?,
  experiment_wave_size = 2,
  experiment_wip_limit = 3,
  max_concurrent_live_delayed = 1
) -> portfolio_outcome_ledger
   + 0..experiment_wave_size experiment Goal Packets
```

Permitted improvement actions may include:

- add, delete, or modify a skill;
- add, delete, or modify an automation;
- modify agent policy or a narrower agent profile;
- add, delete, or modify a hook or validator;
- modify a metric, binding, context-selection rule, or planner policy;
- add, delete, or modify a documented feature bundle when evidence changes
  whether the bundle should exist.

Each improvement still changes one attributable surface or one explicitly
coupled bundle. Whole-harness context helps choose the lever; it does not make
the entire harness one mutation target.

### Weekly Self-Improvement Portfolio

The v-next self-improvement automation is a weekly portfolio learner and
bounded next-wave planner. It is not another heartbeat, check-in scorer, or
executor:

```text
weekly_self_improvement(
  harness_snapshot,
  active_experiment_packets,
  recent_archived_experiment_packets,
  previous_dogfood_report?,
  metrics,
  reports,
  experiment_wave_size = 2,
  experiment_wip_limit = 3,
  max_concurrent_live_delayed = 1
) -> dogfood_report
   + outcome_ledger
   + active_and_pending_portfolio
   + transfer_candidates
   + ranked_improvement_candidates
   + 0..experiment_wave_size experiment Goal Packets
   + no_op_reason?
```

The automation calls `dogfood-review` as its owning skill. Dogfood reads active
packets, recent archived packets, and its previous dated report as a cursor.
It derives a cross-ticket learning ledger while keeping ticket Reward,
`program.md`, `progress.md`, and artifacts canonical. Its report distinguishes
settled, monitoring, due-but-unscored, inconclusive, accepted, killed, and
transfer-candidate experiments before generating new work. It then:

```text
review settled and pending evidence through a weekly cutoff
-> carry the experiment outcome ledger
-> identify transfer candidates and disproven patterns
-> list hardening, refinement, docs, feature, and policy levers
-> propose bounded fixes
-> rank by impact, proofability, compounding value, cost, and risk
-> compute available capacity and non-interference
-> create 0..experiment_wave_size complete Goal Packets
```

Weekly cadence is a portfolio snapshot boundary, not a universal experiment
deadline. A result settled before the cutoff informs the current wave; one
settled later enters the next report. A due-but-unscored row is a source gap
and blocks only dependent/conflicting supply. An honest longer experiment stays
`monitoring`; unrelated immediate toy/eval proofs may still use remaining
capacity. The initial operating parameters are:

```text
experiment_wave_size = 2
experiment_wip_limit = 3
max_concurrent_live_delayed = 1
one_active_experiment_per_attributable_surface = true
```

`dogfood-review` owns report judgment and bounded experiment-ticket creation for
this automation. The created ticket defines expected rewards and an immediate
or delayed feedback route in its Goal Packet. Dogfood does not execute the
experiment or perform a matured check-in. The shared Work Pulse admits and
executes the ticket, derives due Reward rows, and resumes later check-ins using
the same worker, review, and proof machinery as ordinary work.

Each created packet fills the Goal program's executable `Check-In Program` when
feedback is delayed. The ticket may request a direct adoption, deterministic
replay, toy experiment, agent eval, human-feedback loop, or delayed pilot.
Toy/eval work is a proof route inside the ordinary ticket path, not another
automation. One accepted toy result normally creates a bounded transfer or
real-pilot candidate, not doctrine-wide rollout.

`iterate` and `monitor` remain local transitions inside the original packet.
`accept` may retain the bounded intervention immediately, but cross-surface
rollout and doctrine promotion return to the weekly portfolio. Dogfood creates
transfer-test tickets only after checking attribution, guards, and prior
portfolio evidence.

The `self-improve` skill is downstream of this selector. It is called only when
the selected ticket needs measured candidate search, and it chooses immediate
Goal execution versus delayed ticket check-ins from the reward class described
above. `optimize-harness`, `skill-maintenance`, consolidation, eval, or review
remain valid execution routes for other selected fixes.

Fast deterministic checks stay outside this weekly judgment loop. Precommit may
run enrolled surface-budget and file-growth checks, but raw length is only a
smell unless the owning surface declares a limit. Qualitative hardening,
refinement, documentation, and feature decisions belong in the weekly review.

### Bootstrap Assumption

V-next does not need to rediscover every useful operating convention from
zero. It may initialize with a good-enough bootstrap:

- a Kanban board and durable ticket format;
- existing reusable skills;
- a small agent policy and authority boundary;
- proof and review gates;
- Work Pulse and immediate Goal execution; add the minimal check-in support in
  Workstream 2 only with one representative delayed-reward case, and do not
  scale the mechanism before that case passes;
- a minimal objective contract and metric bindings.

Every bootstrap element remains challengeable through evidence. It is a prior,
not permanent doctrine.

## 8. Rollout And Doctrine Promotion

Successful experiments should compound. They should not force every similar
surface to rerun the same discovery from scratch.

```text
accepted experiment
-> pattern candidate
-> transfer test on representative similar surfaces
-> scoped doctrine or reusable skill rule
-> rollout tickets
```

Doctrine promotion records:

```yaml
pattern:
scope:
preconditions:
evidence_refs: []
known_counterexamples: []
transfer_tests: []
rollback_condition:
review_after:
```

One successful experiment is not enough to declare a universal harness rule.
The system should reuse evidence aggressively while preserving scope and
counterexamples.

## 9. Capability Skills, Not Product Controllers

A project may declare specialties that produce important recurring artifacts:

```text
capability =
  skill_ref
  + input contract
  + output artifact contract
  + default metric or review question
  + authority gates
```

Examples include content production, customer research, sales outreach,
engineering delivery, support, financial reporting, or harness improvement.

The harness may list capability refs so Work Pulse knows which high-level
skills are available. The complete workflow stays in the owning skill.

A capability does not automatically receive its own Pulse, goals, progress
file, strategy block, automation, or worker allocation. A separate controller
is justified only after the capability demonstrates independent state, event
flow, prioritization, budget or authority, and enough volume that isolation
materially improves decisions.

The term `product` should remain available for a real external product or
offer. It is not a required Farplane project primitive.

### CRM Records Are Not BAU Tickets

Long-lived prospects and customers have a different lifecycle from bounded
work. Keep relationship state, funnel stage, contact history, and next allowed
touch in a CRM record. Create a Work Pulse ticket only for a bounded action or
experiment and link it back to that record.

```text
crm_record -> bounded_action_ticket -> outcome_writeback -> crm_record
```

The action ticket closes after its attempt. A prospect waiting for a reply does
not remain an active or blocked BAU ticket, consume a worker, or count against
artifact-review WIP. A later CRM event may create another bounded ticket.
V-next documents this boundary but does not add a new CRM runtime.

## 10. Daily And Weekly Interval

Daily and Weekly Interval are evidence-compression and reporting surfaces.
They are not required for check-in eligibility, do not run Dogfood Review, and
do not plan new strategic direction.

Each dated report owns a minimal Markdown problem ledger rather than a new
finding registry or ticket metadata schema:

```markdown
## Problems

- [ ] Repeated failure with evidence refs. Ticket: none
- [x] Resolved or ticketed problem. Ticket: TASK-XXXX
```

The report may update this ledger while it is being drafted. Once finalized,
the dated report is a snapshot; the next report carries forward unresolved
problems with links to the earlier evidence. Tickets remain the owner of
execution, QA, review, and resolution evidence.

### Daily Interval

Daily reporting may summarize:

- plan progress;
- ticket and attention drift;
- feedback obligations;
- opportunity signals from the latest completed Feed Scout or provider report;
- goal or objective drift;
- metric snapshots;
- matured, pending, or inconclusive check-ins already owned by tickets;
- maintenance and documentation observations.

Feed Scout runs as a separate scheduled or manual job and owns its own thread,
provider state, and report. After writing the report, it may create bounded,
source-backed opportunity tickets that pass evidence, dedupe, proof, authority,
and ticket-quality gates. Daily Interval reads the latest completed provider
report and labels a source gap when it is absent. Material evidence can still
wake Pulse immediately or appear in the next Pulse context.

### Weekly Interval

Weekly reporting may summarize:

- completed and abandoned work;
- improvement results and pending proof obligations;
- repeated failures and unresolved problem patterns;
- review and intervention load;
- resource consumption and remaining budget;
- suggested changes to the next planning frontier.

Weekly may be the natural accounting boundary for selected budgets, but a
budget resets only when its policy says so. A weekly schedule does not imply a
universal reset. Weekly Interval does not absorb the weekly self-improvement
automation; the latter reads the completed reports as evidence.

### Bounded Maintenance Ticket Resurfacing

Interval may create or update a maintenance ticket only to resurface an
already-observed problem. It must not use report context to invent a new
product direction, strategy, campaign, capability, or harness hypothesis.

```text
resurface_problem(problem, ticket_history, maintenance_ticket_limit)
  -> 0..maintenance_ticket_limit maintenance tickets
```

A problem is eligible only when it is unresolved, cited by the report, backed
by a prior finalized report, ticket, review, or run-evidence reference, concrete
enough to execute, material enough to act on, not represented by an active
ticket, and able to name proof and a stop condition. A problem first discovered
in the current interval remains ledger-only until a later interval or explicit
operator action. This is corrective maintenance supply, not a second
opportunity planner.

### Proposed Interval Workflow Redistribution

V-next keeps useful observations while moving state-changing work to its
proposed owner. These routes remain hypotheses until the staged proof matrix
below passes:

| Current workflow | Proposed v-next owner | Interval role |
| --- | --- | --- |
| `plan_progress` | Work Pulse and ticket state | Summarize the window |
| `codex_attention_drift` | Weekly reflection or explicit drift review | Report evidence and source gaps |
| `ticket_board_drift` | Work Pulse reconciliation | Summarize unresolved drift |
| `feedback_obligations` | Work Pulse and event-driven review handling | Report outstanding obligations |
| `opportunity_signals` | External context providers | Summarize material signals and link any ticket-owned evidence |
| `goal_drift` | Objective-contract review, normally weekly or evidence-triggered | Report the suspected drift |
| `metric_snapshot` | Metric provider at its natural cadence | Present the snapshot |
| `reward_checkins` | Check-in eligibility plus the owning improvement ticket | Report decisions already made or due |
| `compounding_leverage_review` | BAU leverage lens in `plan_next_wave`; harness leverage lens in weekly self-improvement | Report evidence only |
| `skill_hardening` | Weekly self-improvement review, then `skill-maintenance` when selected | Report observed failures |
| `skill_refinement` | Weekly self-improvement review, then `skill-maintenance` when selected | Report complexity or duplication |
| `docs_consolidation` | Weekly self-improvement review or explicit maintenance ticket | Report need and evidence |
| `tracked_feature_review` | `dogfood-review` as the weekly self-improvement automation | Link the resulting decision report when relevant |
| `priority_planning` | Ranking phase inside BAU `plan_next_wave` | None; Interval does not rank new direction |
| Feed Scout execution | Separate Feed Scout automation and thread | Read the latest completed report |

The governing rule is:

```text
observe and summarize       -> Interval
resurface known maintenance -> Interval, bounded and deduped
plan new BAU direction      -> plan_next_wave under Work Pulse
change a policy             -> weekly self-improvement
change an objective         -> explicit objective review
```

### BAU Planning Versus Maintenance Resurfacing

Pulse planning is not `interval-update` with fewer flags. The workflows may
share deterministic context-building, evidence-normalization, materiality, and
dedupe helpers, but they have different decisions and state transitions:

```text
interval_update(...) -> report + problem ledger + bounded known-maintenance tickets
plan_next_wave(...)  -> ranked BAU ticket specs
weekly_self_improvement(...) -> outcome ledger + bounded experiment Goal Packet wave
work_pulse(...)      -> admission + dispatch + reconciliation
```

The current `ticket-opportunity-generator` package remains the owner of
`plan_next_wave`. It absorbs the useful logic from `priority_planning` and the
BAU half of compounding leverage:

```text
identify bottleneck
-> list levers
-> generate BAU moves
-> rank by goal impact, bottleneck relief, compounding value, proof speed,
   cost, review load, and risk
-> crystallize 0..wave_size executable specs
```

It explicitly excludes harness maintenance and self-improvement tickets. Those
come from the weekly self-improvement review. Interval-created maintenance
tickets do not compete for direction because they may only re-project a problem
that the report has already evidenced.

## 11. Problems The Migration Corrected

These were the ownership and architecture problems visible before
`TASK-0318` through `TASK-0322`. They are retained as decision rationale, not
as a description of the migrated contract.

| Current problem | Current evidence | Why it is harmful | V-next replacement |
| --- | --- | --- | --- |
| Product categories became runtime controllers | Five product folders and five product-scoped Pulse automations carry strategies, budgets, review caps, skills, and progress | Artifact or capability categories become orchestration boundaries even when they do not need independent state | Capability skills called by one Work Pulse |
| The basic `do ticket else plan` loop is obscured | Pulse reconciles products and invokes product-local loops instead of directly owning simple refill | The project cannot prove its simplest autonomous behavior before adding specialization | Work Pulse executes an eligible ticket or calls `plan_next_wave` |
| New-direction planning has multiple owners | Product loops produce next-wave work while Interval also runs `priority_planning` | Duplicate strategy synthesis requires extra dedupe and makes cadence determine direction | `plan_next_wave` owns new BAU direction; Interval may only resurface evidenced maintenance |
| Check-ins are coupled to report cadence | `reward_checkins` is a gated Interval workflow | A due experiment depends on a reporting workflow instead of ordinary ticket eligibility | Work Pulse derives due eligibility from the original ticket Reward and program, then resumes it |
| State is distributed across overlapping surfaces | Goals, product strategies, product progress, tickets, Pulse reports, Interval reports, rewards, and ledgers all affect selection | Agents must reconstruct which surface is authoritative before doing simple work | Program owns policy; tickets and progress own resumable work; reports are derived evidence |
| Self-improvement is split into product-like phases | Experiments, ablations, productization, Dogfood Review, and maintenance workflows run as separate planning surfaces | The proof or review method is mistaken for a permanent organizational lane | One Dogfood-owned weekly automation reviews experiment history and creates a bounded experiment Goal Packet |
| Findings accumulate schema instead of decisions | Findings, rewards, reports, and tickets can each grow their own state fields | More metadata does not make an unresolved problem easier to resume or fix | Reports keep a small problem ledger; tickets own execution and proof |
| Worker and review capacity are product-local | Each product loop carries worker budgets and review caps | Shared workers and shared human attention are harder to reason about globally | One worker pool with `worker_limit`, `review_wip`, and `improvement_wip` |
| Advanced learning machinery precedes the basic proof | Weighted product loops, strategy refreshes, delayed rewards, and broad reports exist before the minimal board loop is proven end to end | Framework activity can grow without proving useful autonomous throughput | Prove one Work Pulse and one improvement ticket before scaling |
| Content and market experimentation leak into the kernel | Distribution and market-learning loops are modeled beside harness improvement | Domain-specific feedback complexity distorts the general harness model | Keep content-market optimization as a later, separate feature |
| Metric meaning and provider mechanics share one file | `bindings.yaml` contains integrations, provider coordinates, and the canonical `metrics:` catalog | Metric definitions, KPI relationships, and connector implementation change for different reasons | Move metric semantics to `metrics.yaml`; keep provider configuration in `bindings.yaml` |
| QA and review receipts can live outside their ticket | The current manifest allows ignored `.farplane/reviews/` state | Completion proof can become detached from the scope, claim, and Done / Proof contract it judges | Store QA and review artifacts under the owning ticket and let reports or registries link them |

The root cause is premature decomposition. Farplane responded to a broad Pulse
having too much judgment by giving every concern a local strategy and loop.
This improved local context but created more sources of truth before the shared
execution, planning, and evidence primitives were stable.

The v-next correction is not “delete every current feature.” It is to prove
that one board, one executor, one ticket planner, one bounded improvement
planner, and explicit proof routing can carry the useful behavior. Only then
should specialized controllers earn their existence through observed need.

## 12. Implemented State And File Projection

The theoretical kernel does not dictate one exact file tree. Farplane now uses
this practical projection:

```text
farplane/
  manifest.json       # framework version and required/optional file contract
  harness.md          # stable program, authority, capability refs
  goals.yaml          # value direction, KPI selection, current frontier
  metrics.yaml        # metric labels, definitions, kinds, units, display
  automations.toml    # scheduled and event-driven wake definitions
  bindings.yaml       # connector and provider configuration
  hooks.json          # optional installed hook bindings

tickets/
  TASK-*/
    ticket.md          # commitment, state, proof, check-in contract
    program.md         # persistent execution or experiment instructions
    progress.md        # append-only execution or experiment history
    artifacts/         # all evidence owned by this ticket
      qa/              # test output, QA reports, screenshots, runtime proof
      review/          # reviewer receipts, findings, completion verdicts

skills/
  pulse-update/
  ticket-opportunity-generator/
  self-improve/
  interval-update/
  <capability skills>/

.farplane/
  reports/             # generated summaries that link to ticket evidence
  metrics/             # generated metric observations and snapshots
  registries/          # optional generated projections after a consumer earns them
```

This is illustrative. V-next should reuse current files when they already fit
the new ownership boundary rather than renaming files for conceptual purity.

### File Ownership Contract

| File or directory | Owns | Must not own |
| --- | --- | --- |
| `farplane/manifest.json` | Framework version, required and optional project files, graph entrypoints | Goals, workflow instructions, metric history |
| `farplane/harness.md` | Stable project program, authority, guardrails, capability refs | Dynamic ticket state or generated reports |
| `farplane/goals.yaml` | Value direction, active frontier, KPI selection, non-goals, objective-level constraints | Metric provider implementation or ticket plans |
| `farplane/metrics.yaml` | Metric IDs, labels, descriptions, kinds, units, display, and pinned state | Credentials, connector coordinates, refresh recipes, measured history |
| `farplane/bindings.yaml` | Safe connector coordinates, provider configuration, external context bindings, and metric refresh recipes keyed by metric ID | Canonical metric meaning or KPI hierarchy |
| `farplane/automations.toml` | Explicit recurring or event-triggered invocations | Hidden progress or duplicated skill workflow bodies |
| `farplane/hooks.json` | Optional hook installation and binding configuration | Judgment-heavy workflow policy |
| `tickets/TASK-*/` | Work state, program, progress, evidence, QA, reviews, comparisons, check-ins, receipts | Project-wide generated inventories |
| `.farplane/reports/` | Derived reporting and cross-ticket summaries linked to owners | Canonical proof or ticket state |
| `.farplane/metrics/` | Generated metric observations and snapshots | Metric definitions |
| `.farplane/registries/` | Optional generated projections over tickets, reports, skills, automations, or project state after a concrete consumer earns persistence | Hand-authored source-of-truth records or mandatory empty directories |

There is no generic `.farplane/runtime/` directory in the proposed contract.
State must name its owner: ticket, report, metric observation, registry, or
tool-owned scheduler state. There is no generic `.farplane/evidence/`
directory either; evidence belongs under the ticket that makes the claim.
Cross-ticket reports link to that evidence instead of copying it.

There is no generic `.farplane/reviews/` directory in the implemented contract.
QA output and reviewer receipts belong under the ticket they judge. When a
material review has no owning ticket, attach it to the bounded ticket first or
create that ticket before treating the review as durable completion evidence.
Cross-ticket review summaries remain reports or generated registry views that
link back to ticket-owned artifacts.

`metrics.yaml` separates metric meaning from provider mechanics:

```text
metrics.yaml  -> what is measured, why, its unit/kind, and how it is displayed
bindings.yaml -> how a named provider is reached or queried safely
.farplane/metrics/ -> observed values over time
```

## 13. Implemented Upgrade Workstreams

The v-next migration landed as separate reviewable tickets whose order
preserved behavioral proof before finalizing the new project-file contract.

### Workstream 1 — Remove Products And Rebuild The Work Loop

Goal: prove the minimal board loop without product-scoped orchestration.

Status: completed under `TASK-0318`; focused behavior, live automation, and
independent completion review passed at TAS-A.

Scope:

- remove product controller invocation and product-local ticket-supply
  ownership from the active Work Pulse path;
- rebuild Pulse as one Work Pulse that reconciles, dispatches, requests review,
  and refills an empty board;
- separate `plan_next_wave` from dispatch;
- simplify the ticket executor around ticket, program, progress, proof, and
  worker exit on human review;
- delete the old product-scoped Pulse automations from the active automation
  configuration;
- compare planner and Interval internals before duplicating shared mechanics.

The planner and Interval may share pure helpers for:

- context snapshot construction;
- ticket and history normalization;
- metric snapshot loading;
- source-freshness and source-gap classification;
- materiality classification;
- duplicate-opportunity detection;
- compact summary generation.

They must not share decision ownership:

```text
plan_next_wave          -> new BAU ticket specifications
Work Pulse              -> admission, creation of BAU planner specs, dispatch, reconciliation
Interval                -> reports, problem ledger, bounded known-maintenance tickets
weekly self-improvement -> Dogfood outcome ledger, transfer candidates, ranked fixes, bounded Goal Packet wave
```

Proof: one todo ticket executes; an empty board produces a bounded wave; the
same worker path handles ordinary and improvement tickets; product refs are not
required for admission or planning.

### Workstream 2 — Simplify Interval And Add Improvement Ticket Supply

Goal: make recurring review useful without letting it duplicate the planner.

Status: implemented under `TASK-0319`; ticket-local QA and reviewer receipts
own completion proof.

Scope:

- simplify `interval-update` into context collection, reflection, metric
  presentation, report synthesis, and bounded resurfacing of already-observed
  maintenance problems;
- define small Daily and Weekly profiles instead of a large matrix of
  overlapping subworkflows;
- add the minimal report `Problems` ledger without adding finding metadata to
  tickets or a new findings registry;
- make `plan_next_wave` BAU-only and fold lever enumeration, idea generation,
  compounding-value scoring, ranking, and deprioritization into it;
- move due reward check-in execution to Work Pulse ticket eligibility and teach
  `self-improve` to route immediate reward through native Goal execution and
  delayed reward through the existing ticket Reward and Goal Packet fields;
- use `dogfood-review` as the bounded weekly self-improvement automation owner:
  review active/recent archived experiment tickets and feature/system evidence,
  carry the prior outcome ledger, then create a capacity-limited packet wave
  with explicit Reward rows and executable programs;
- split Feed Scout into its own scheduled job and thread; Daily and Weekly read
  its completed reports rather than embedding the run;
- keep Work Pulse as the only base framework heartbeat and convert other broad
  recurring workflows to bounded cron/manual execution and retire Taste Loop
  as a separate controller; human-feedback improvement becomes a normal
  Dogfood/self-improvement ticket executed by Work Pulse;
- keep precommit mechanical by reusing enrolled surface/file-growth validators;
  run qualitative hardening, refinement, docs, and feature review inside the
  weekly self-improvement automation;
- retire the installed model-driven file-growth rewrite hook and reuse only
  deterministic line-count detection in the precommit gate.

The resulting ticket sources are:

```text
ordinary planner             -> BAU / project-progress tickets
Feed Scout                   -> bounded source-backed opportunity tickets
Daily or Weekly Interval     -> bounded resurfaced maintenance tickets
Dogfood self-improvement     -> bounded non-interfering experiment Goal Packet wave
operator                     -> explicit tickets and corrections
```

All five sources feed the same Work Pulse and ticket executor.

Proof: Daily and Weekly still produce useful reports with a minimal problem
ledger; Feed Scout creates only evidence-backed bounded tickets; Interval
creates no new-direction or duplicate maintenance ticket; the Dogfood run
writes experiment evidence and supplies a bounded packet; immediate and delayed
`self-improve` cases choose the correct execution route; Feed Scout runs
separately; and one improvement ticket executes through the normal Work Pulse
path. `TASK-0320` extends this proven bootstrap with the portfolio ledger,
archive reads, non-interfering capacity, and executable Check-In Program.

### Workstream 3 — Redefine Project Files And Update The Manifest

Goal: make tracked and generated file ownership match the proven v-next
behavior.

Status: implemented under `TASK-0321` and `TASK-0322`; the migrated checkout
and a clean bootstrap fixture validate, and the minimal Pulse cases pass.
Ticket-local independent QA and completion review are the final closeout gate.

Scope:

- keep `goals.yaml` as the value-direction and KPI-selection contract;
- finalize `harness.md`, `goals.yaml`, `metrics.yaml`, `bindings.yaml`,
  `automations.toml`, and optional `hooks.json` contracts;
- remove products and generated product registries from the standard project
  file set;
- delete the retained product configuration files after Workstreams 1 and 2
  prove no active runtime reader needs them;
- add `metrics.yaml` to templates, validators, initialization, framework docs,
  and UI/graph readers that need it;
- move canonical metric definitions out of `bindings.yaml` while leaving
  connector/provider configuration there;
- define `.farplane/registries/`, `.farplane/reports/`, and
  `.farplane/metrics/` as generated outputs;
- keep all evidence in ticket artifacts and remove any proposed generic
  runtime or evidence bucket;
- move QA and reviewer writeback to `tickets/TASK-*/artifacts/{qa,review}/` and
  remove `.farplane/reviews/` from the v-next manifest contract;
- update `farplane/manifest.json`, framework versioning, init templates,
  validators, docs, and migration guidance together.

Implementation split:

- `TASK-0321` removes active product-era readers, initializer templates,
  project files, and obsolete product-architecture tickets without adding a
  replacement controller ontology.
- `TASK-0322` adds `metrics.yaml`, narrows `bindings.yaml` to provider and
  connector configuration, updates the manifest/templates/validators, and
  proves a clean initialized fixture plus this project's own migration.

Implemented proof: a newly initialized project contains the required v-next files;
the manifest validates them; generated registries rebuild from their source
owners; no active reader requires products, generic runtime state, or a generic
evidence or review directory.

## 14. Adoption Plan And Staged Proof

The safest reconstruction proves each layer before adding the next:

1. **Kernel:** one Work Pulse empties one board by executing an eligible ticket
   or planning a bounded wave when no eligible ticket exists.
2. **Scheduling:** separate `wave_size`, `worker_limit`, `review_wip`, and one
   shared worker pool.
3. **Reporting:** Daily and Weekly write compact reports with problem ledgers;
   Feed Scout runs separately; Interval may resurface only known maintenance.
4. **Improvement supply:** one weekly self-improvement automation runs Dogfood
   evidence, carries the outcome ledger, computes available non-interfering
   capacity, and creates no more than the configured packet wave.
5. **Reward route:** immediate `self-improve` uses native Goal execution;
   one representative delayed case reuses `Reward.kpi_rewards[]`, existing Goal
   Packet sections, and derived Pulse eligibility.
6. **Shared execution:** the same Work Pulse executes ordinary and improvement
   tickets without an improvement-specific executor.
7. **Clear change route:** adopt, verify, and monitor one clearly missing,
   bounded capability or invariant repair.
8. **Uncertain change route:** prove one questionable proposal with a toy
   project, behavior eval, ablation, or expert/human feedback before adoption.
9. **Capabilities:** convert useful product workflows into high-level skills;
   remove the retained product file contract after the shared loop proves
   sufficient.
10. **Scale learning:** tune experiment capacity, early portfolio wakes,
    doctrine transfer, or content-market optimization only from observed need.

The structural migration is complete. Continue collecting representative run
evidence for the behavioral stages instead of adding more orchestration
surfaces preemptively.

### Proof Matrix For The First Eight Stages

| Stage | Representative run | Required evidence | Binary pass condition | Falsifier |
| --- | --- | --- | --- | --- |
| 1. Kernel | Run Pulse once with one executable ticket, then once with an empty admitted board | Two Pulse reports, selected-ticket receipt, planned-ticket diffs | First run dispatches the existing ticket; second run creates `1..wave_size` executable tickets without a product-loop input | `F1`, `F4` |
| 2. Scheduling | Set BAU `wave_size = 3`, `worker_limit` to the available worker count, `review_wip = 1`, experiment wave size `2`, experiment WIP `3`, and delayed-live cap `1` | Planned-ticket list, worker handoff ledger, experiment capacity receipt, review-state counts | Every cap holds; monitoring delayed work blocks conflicts but not an unrelated immediate toy; workers waiting on review exit | `F4` |
| 3. Reporting | Run Feed Scout, Daily, and Weekly independently with one unresolved prior problem | Provider report, interval reports, problem ledger, maintenance ticket or no-op receipt | Reports remain useful; missing upstream evidence is labeled; only an evidenced, deduped maintenance problem may become a ticket | `F2`, `F4` |
| 4. Improvement supply | Run Dogfood over active, recent archived, and prior-report experiment state | Dogfood outcome ledger, active/pending view, transfer candidates, capacity receipt, ranked candidates, packet wave | Results are reviewed first; wave/WIP/delayed-live/per-surface caps hold; Dogfood creates only complete non-interfering packets and executes none | `F4`, `F5` |
| 5. Reward route | Run one immediate case and one delayed case with two Reward rows, one matured and one future | Goal result, derived due projection, original-ticket program/check-in receipt, updated Reward, progress entry | Immediate reward schedules no check-in; delayed worker reads program.md, updates only matured rows, and leaves the future row dormant | `F3`, `F6` |
| 6. Shared execution | Put one ordinary and one improvement ticket on the same board | Selection receipts, worker handoffs, ticket outcomes | One Work Pulse executes both using the same admission, worker, review, and proof path | `F4`, `F5` |
| 7. Clear change route | Select one bounded missing capability or violated invariant with direct verification | Gap statement, implementation diff, checks, monitoring and rollback receipt | The change closes the named gap, direct checks pass, monitoring is recorded, and no unrelated policy is expanded | `F5`, `F6` |
| 8. Uncertain change route | Select one questionable harness proposal and test it in a representative toy, behavior eval, ablation, or expert review | Baseline or comparison, toy limitations, feedback/eval artifact, decision | Evidence returns keep, revise, reject, or bounded pilot without silently promoting the proposal into doctrine | `F5`, `F6` |

Stages nine and ten remain out of scope until this matrix has one passing
representative run per row. The proof artifacts may live under a ticket during
the prototype; this draft does not prescribe their final generated paths.

## 15. Falsification And Open Decisions

V-next should be revised or rejected if evidence shows:

- `F1 — planning-context failure:` in two consecutive representative waves,
  the ticket-quality reviewer returns below the required readiness gate because
  Work Pulse cannot load the capability or external context needed to choose a
  concrete next move.
- `F2 — resume failure:` an independent agent reading the program, tickets,
  generated board, and linked evidence cannot name the current state, next
  eligible transition, and governing guard without hidden chat context.
- `F3 — check-in failure:` a matured experiment is not selected or explicitly
  deferred during the first scheduled Pulse after its maturity condition is
  observable.
- `F4 — supply-control failure:` a representative run exceeds `wave_size`,
  `worker_limit`, or `review_wip`, admits a duplicate ticket, or creates a
  ticket that fails the configured ticket-quality readiness gate.
- `F5 — improvement-admission failure:` the weekly review skips Dogfood
  evidence without an explicit no-op reason, exceeds wave/WIP/delayed-live or
  per-surface interference limits, cannot name the gap and proof route, or
  requires a separate executor before one bounded improvement can run.
- `F6 — proof-routing failure:` a proposed change is adopted without direct
  verification, a representative toy/eval, recorded expert feedback, or a
  bounded delayed pilot; or the selected proxy removes the mechanism the claim
  depends on.
- `F7 — capability-boundary failure:` representative capability work requires
  independent state, event flow, prioritization, authority, or budget that Work
  Pulse cannot supply through the skill contract and ticket context.

Resolved structural decisions:

1. The objective contract remains `goals.yaml`; no `objectives.yaml` rename.
2. `harness.md`, `goals.yaml`, `automations.toml`, and `bindings.yaml` remain;
   products and product registries were retired.
3. `metrics.yaml` owns semantic metric cards; `bindings.metric_bindings` owns
   refresh mechanics with exact ID parity.
4. No registry directory is mandatory. Persist a generated projection only
   after a concrete UI, report, or automation consumer proves it is useful.

Remaining evidence questions:

1. What is the minimum ticket distinction between ordinary and improvement
   work, if any beyond a proof route and `improvement_wip`?
2. What qualifies a change for adopt-and-monitor rather than toy proof, human
   feedback, or delayed pilot?
3. How are external context events deduplicated and judged material?
4. What evidence is sufficient to promote a result into doctrine?
5. What is the minimum generated due-check projection needed for Pulse without
   adding more hand-maintained ticket metadata?

## 16. Before, After, Example

> **Before:** Interval combines reporting, Feed Scout, Dogfood Review, reward
> check-ins, maintenance workflows, leverage synthesis, and next-window
> planning, while self-improvement proof methods can become separate loops.
>
> **After:** Work Pulse is the base heartbeat and BAU dispatcher;
> `plan_next_wave` owns new BAU direction; Feed Scout, Daily, Weekly, and
> Dogfood self-improvement are separate bounded jobs; Interval reports problems
> and may only resurface known maintenance; Dogfood carries the experiment
> outcome ledger and creates a bounded non-interfering next wave; delayed
> check-ins execute the original ticket's `program.md`.
>
> **Example:** Daily carries forward a repeated stale-link problem and creates
> one deduped maintenance ticket because the repair is already known. Later,
> weekly self-improvement writes a Dogfood report showing that Interval still
> overproduces workflow findings, ranks refinement against other harness
> levers, and creates an immediate toy/eval packet while an unrelated delayed
> pilot monitors. The toy closes in one Goal; the delayed worker later reads
> its `program.md` and records only matured Reward rows.

## Next Owner

The v-next structural migration is complete through `TASK-0322`. The next
owner is real Work Pulse operation: execute the existing board, collect
ticket-local proof, and let observed failures—not speculative ontology—drive
the next refinement ticket.
