---
title: "PRD: Farplane V1"
status: active
owner: farplane
created_at: 2026-05-26
updated_at: 2026-09-19
version: "1.0"
refs:
  - docs/farplane-framework/lifecycle.md
  - docs/farplane-framework/project-files.md
  - docs/farplane-framework/pulse-and-interval-loop.md
  - docs/farplane-framework/ticket-execution-loop.md
  - farplane/harness.yaml
  - farplane/metrics.yaml
  - automations/
  - tickets/README.md
---

# PRD: Farplane V1

## Product Thesis

Farplane is a file-backed operating system for moving an operator-chosen
commercial bet toward money. It helps a human operate long-running agent work
through visible project goals, current evidence, bounded actions, tickets,
capability skills, automations, and reviewable proof.

```text
Farplane = commercial intent + execution + evidence
```

The V1 product promise is simple:

> Give Farplane an explicit customer, painful problem, offer, price, and route
> to sale. It should keep the resulting projects moving, expose the constraint
> closest to money, ask for the smallest missing fact or decision, and preserve
> enough evidence for the operator to continue, revise, or kill the bet.

The operator owns strategy. Farplane may expose when evidence contradicts the
commercial hypothesis, but it does not claim to autonomously discover a novel
business strategy or outperform the operator's judgment. Its strength is
maintaining context, following through, reconciling evidence, and keeping the
next consequential action visible.

### Direction Status

This PRD is the accepted product direction. The money-execution boundary and
lean Daily/Weekly Company OS contract are implemented by the active automation
prompts and the `pm-daily` and `pm-weekly` skills. The AI Office hierarchy is
not yet fully implemented. The Interval weekly-draft and broad promotion
machinery is legacy reference and has no active Daily or Weekly binding.

## Problem

General-purpose agents can produce useful work, but sustained operation breaks
down when:

- priorities and constraints live only in chat;
- multiple planners or automation loops compete to choose direction;
- waiting for humans or external signals consumes execution capacity;
- experiments, QA, review, and check-ins use separate state systems;
- evidence is scattered across generic runtime directories;
- reusable workflows are confused with independent products or controllers;
- self-improvement adds machinery before the basic work loop is proven.
- work looks productive but has no evidenced relationship to earning,
  retaining, accelerating, or protecting money.

The result is hidden state, duplicate work, weak attribution, inflated
metadata, and operator distrust.

## Audience

- Primary: founders and operators running agent-heavy projects.
- Secondary: engineers and agent designers maintaining reusable harnesses.
- Tertiary: collaborators reviewing artifacts, decisions, and evidence without
  reading raw transcripts or runtime logs.

## Jobs To Be Done

1. When I define a commercial bet, I want agents to execute bounded work that
   moves it toward money without losing my constraints.
2. When work spans turns or days, I want durable state that another agent can
   resume without hidden conversation context.
3. When an agent needs review or waits for reality, I want execution capacity
   released while the obligation remains visible.
4. When the board runs out of useful work, I want the smallest next commitments
   grounded in the commercial hypothesis, money-linked evidence, ticket
   history, and current constraints.
5. When the harness changes itself, I want the cheapest honest proof route and
   a reversible promotion decision.
6. When I inspect the system, I want every important claim to lead back to an
   owning ticket, report, metric observation, or durable policy file.

## V1 Operating Model

```text
project program
-> one ticket board
-> one Work Pulse
   -> execute admitted ticket
   -> perform matured ticket check-in
   -> request worker-free human review
   -> plan a bounded cross-area wave when no unclaimed executable work exists
-> bounded scheduled report/candidate sources
-> ticket-local QA, review, reward, and closeout
-> durable learning back into metric objectives, policy, skills, docs, or features
```

Every project uses the same decision rule:

```text
commercial hypothesis
-> current evidence
-> constraint closest to money
-> smallest useful action, question, or decision
-> observed result
-> continue | revise | stop
```

Delivery, learning, distribution, capability, and maintenance are supporting
work. They enter the loop only when evidence or the project configuration ties
them to earning, retaining, accelerating, or protecting money. Missing money
evidence remains unknown rather than being replaced with activity proxies.

### Daily And Weekly Reviews

Daily and Weekly are execution reviews, not independent strategy engines.
Daily maintains each project's current memory, surfaces material blockers or
missing evidence, and selects the smallest useful follow-up. Weekly compares
expected movement with observed results, consolidates what changed, carries
forward the closest commitments to monetization, and escalates contradictions
in the customer, problem, offer, price, or route to sale to the operator.

Reasoning techniques such as plan-versus-actual comparison, root-cause
analysis, and intervention comparison are helpers for filling the existing
project and report forms. They do not require separate workflow stages,
artifacts, or governance machinery.

### Canonical State

| Surface | Responsibility |
| --- | --- |
| `farplane/harness.yaml` | identity, planning areas/instructions, authority, capability refs, selected metrics |
| `farplane/metrics.yaml` | metric meaning, direction, freshness, and guard rules |
| `farplane/bindings.yaml` | safe provider coordinates |
| `automations/` | one office-wide Company OS Daily and Weekly review |
| `farplane/automations/` | one project Work Pulse plus bounded project-local jobs |
| `tickets/TASK-*/` | work, program, progress, reward, evidence, QA, review |
| `skills/*`, `.agents/skills/*` | reusable and project-local capabilities |
| `.farplane/reports/`, `.farplane/metrics/` | derived context and observations |

### Minimal Ticket Lifecycle

```text
todo | active | awaiting_review | waiting_signal |
blocked | done | failed | rejected
```

Required ticket metadata is limited to identity, status, and timestamps.
Priority, claim, dependencies, human gate, and compute target are sparse
routing overrides. QA, reward, review, evidence, blockers, and next actions
remain in the ticket body, Goal Packet, progress log, or artifacts.

### Work Sources

| Source | Authority |
| --- | --- |
| Work Pulse next-wave planner | globally ranked tickets when no unclaimed executable or due-check-in work exists |
| Feed Scout | source report, candidates, and bounded direct recovery tickets |
| Daily/Weekly review | project memory, targeted follow-ups, weekly reports, and operator-visible work proposals; no independent strategy or ticket admission |
| Dogfood Review | complete self-improvement portfolio checkpoint and bounded planner context |
| Operator | explicit direction, feedback, correction, or approval |

Only Work Pulse executes tickets and matured check-ins.

## Functional Requirements

### FR-1: Project Program

- A project can express stable policy, planning areas, selected metrics,
  provider bindings, capability routes, and automation topology in tracked files.
- Generated observations never silently replace those source owners.

### FR-2: Ticket-As-Program

- A material task can be reconstructed from `ticket.md`, `program.md`,
  `progress.md`, and linked artifacts.
- Ticket state is sufficient for selection, resumption, proof, review, and
  closeout without transcript memory.

### FR-3: One Work Pulse

- Pulse reconciles board and worker state before dispatch.
- Ordinary `todo` work and matured `waiting_signal` check-ins use the same
  worker path.
- `awaiting_review`, dormant signals, and blocked tickets do not occupy workers.
- Human-active tickets remain ineligible for redispatch but do not consume
  Pulse worker capacity.
- Pulse plans a bounded cross-area wave only when no unclaimed executable or
  due-check-in work exists.
- Wave size, worker capacity, review WIP, and experiment capacity remain
  separate controls.

### FR-4: Human Review

- A worker sends one review request, records its Review block, sets
  `awaiting_review`, clears its claim, and exits.
- Queue size provides backpressure but does not itself trigger chasing.
- Pulse may send at most one ticket-owned due reminder per beat.

### FR-5: Scheduled Sources

- Feed Scout, Daily/Weekly review, and Dogfood run as bounded cron/manual jobs rather
  than extra heartbeats.
- Scheduled sources write bounded reports or context but do not admit proactive
  tickets. Daily/Weekly maintains project memory and may apply only explicitly
  authorized updates or follow-ups to existing work. Dogfood writes only a
  checkpoint/context receipt. The one next-wave planner compares opportunities
  globally.
- Daily/Weekly does not choose new strategy; Dogfood does not create or execute
  experiments; Feed Scout does not create or execute opportunities.

## AI Office Product Story

The AI Office is the visible version of this loop. It should feel like a
founder operating a small company, not watching agents perform activity.

**Before:** the office foregrounds teams, sessions, skills, memory, and runtime
state. These surfaces explain what exists, but the operator must infer whether
the company is getting closer to money.

**After:** the office opens on the commercial bet, current money state, the
constraint closest to the next monetization event, and the few projects and
commitments affecting it. Agents, sessions, leverage, resources, and memory
remain drill-down evidence and execution surfaces.

**Example:** an operator defines a customer, painful inventory problem, paid
offer, price, and route to sale. The office shows that customer validation is
complete, the proposal is awaiting a decision, and one missing margin input
blocks pricing. The next visible mission is to obtain that input and close or
reject the offer; adding another research project is not presented as progress.

The primary app sequence becomes:

```text
Set the commercial bet
-> see money and the next monetization event
-> inspect the blocking project or decision
-> approve or perform the smallest useful action
-> observe the result
-> continue, revise, or stop
```

This story reuses the existing Office, Leverage and its Finance-owned Capital
view, Projects, Tasks, Memory, and review surfaces. It changes their hierarchy:
commercial movement is the frame; the existing modules explain or operate that
movement.

### FR-6: Self-Improvement

- Every proposed change names a target surface, objective, feedback class,
  proof route, budget, guard, and rollback.
- Immediate feedback runs inside the current Goal-backed ticket.
- Delayed feedback stays on the original ticket and resumes through its
  Check-In Program.
- Accepted patterns require transfer evidence before doctrine promotion.
- Self-improvement is one evidence-gated planning area in the global ranking,
  not a separate Pulse or guaranteed weekly quota.

### FR-7: Capability Boundary

- Important recurring artifact workflows are callable skills, not independent
  planning controllers by default.
- Independent state is introduced only for a genuinely distinct event stream,
  authority boundary, budget, or prioritization policy.
- Long-lived prospects remain CRM records; only bounded actions become tickets.

### FR-8: Proof And Observability

- QA evidence and reviewer receipts live under the ticket they judge.
- Reports and registries link to source evidence rather than copying canonical
  state.
- Missing or ambiguous evidence becomes a source gap, not an inferred pass.

### FR-9: Portable Event Mining

- `farplane ticket finalize TASK-XXXX` performs the successful terminal/archive
  transition and writes one typed `farplane.ticket.completed` event to the
  durable local outbox. Failed mining leaves that event retryable; no hook,
  file watcher, or cloud dispatcher infers completion from file writes.
- `bindings.yaml` maps the explicit completion event to an immutable mining
  program. `hooks.json` owns lifecycle telemetry plus bounded deterministic
  guards such as final-response length; it never owns completion.
- Default completion mining emits coverage, observations, material findings,
  source gaps, and escalation without a scalar quality score.
- Farplane UI edits routes and renders Core runs; it does not own event,
  program, run, replay, rerun, or report semantics.

### FR-10: Money-Execution Boundary

- Project goals state the commercial hypothesis or their explicit contribution
  to earning, retaining, accelerating, or protecting money.
- Daily and Weekly may read project-local harness configuration, metric
  definitions, and current observations when filling existing memory and report
  forms.
- Nonfinancial progress is material only when its relationship to money is
  explicit in configuration or supported by evidence.
- When evidence challenges the customer, painful problem, offer, price, or
  route to sale, the system escalates the strategy decision to the operator.
- Legal, trust, delivery-quality, authority, and runway constraints remain hard
  guards; short-term cash does not override them.

## Success Metrics

The primary outcome is verified money movement. Each deployment chooses the
authoritative money measure available to it, such as cash collected, gross
profit, recurring revenue, retained revenue, or validated paid commitments.
Pre-revenue measures are diagnostic only and must state their evidenced path to
the selected money outcome.

### Selected Money Outcome

Each deployment selects the applicable authoritative outcome; it does not
maximize every row simultaneously.

| Metric | Direction | Meaning |
| --- | --- | --- |
| `revenue_usd` | maximize | realized revenue from the authoritative connected business system; missing access remains unknown rather than zero |
| `active_subscriptions` | maximize | paid active relationships when subscriptions represent the selected money model |

### Money-Linked Diagnostic Measures

These measures guide work only when the project configuration states their
evidenced relationship to the selected money outcome.

| Metric | Direction | Meaning |
| --- | --- | --- |
| `evidence_distribution_reach` | maximize | accepted evidence reaches qualified builders through proof-backed media and demos |
| `distribution_reach_per_artifact` | maximize | attention efficiency rises without rewarding output spam |
| `accepted_evidence_cycles` | maximize | ablations, experiments, or proof cycles finish with accepted reusable evidence |
| `activated_external_projects` | maximize | nearby non-standard projects run the current contract and record a Work Pulse decision after migration |

### System-Health Guards

These protect execution quality; they are not alternate business objectives.

| Metric | Direction | Meaning |
| --- | --- | --- |
| `auto_completion_rate` | maximize | completed associated tickets required no post-start human intervention |
| `intervention_free_ticket_count` | maximize | autonomous completion produces useful throughput |
| `ticket_intervention_turn_count` | minimize within quality floor | supervision falls without false completion or drift |
| `rejected_ai_ticket_count` | minimize; guard ≤ 1/day | rejected AI-planned work backpressures planner quality |
| `todo_unclaimed_ticket_count` | bounded operating signal | executable supply is visible without uncontrolled backlog growth |
| `accepted_harness_improvements` | increase selectively | self-improvement produces reviewed durable value |
| `latest_eval_pass_rate` | diagnostic | latest local eval result is visible without treating unrelated suites as one global guard |

Metric semantics and grouped refresh prompts live in `farplane/metrics.yaml`; provider coordinates
live in `farplane/bindings.yaml`. Dispatch correctness, review-worker release,
resumeability, maintenance precision, and experiment-packet completeness remain
binary feature/test gates until repeated operation justifies registered metric
cards.

## V1 Acceptance

- [x] Product-scoped Pulse controllers and product state are retired.
- [x] `harness.yaml` owns typed identity, planning areas, capabilities, and metric selection.
- [x] One project Work Pulse handles ordinary tickets and matured check-ins.
- [x] Ticket metadata is reduced to lifecycle and sparse routing.
- [x] Human review and signal waits release workers.
- [x] Daily/Weekly uses the project-memory, money-linked review contract and
      does not independently admit tickets or choose strategy.
- [x] Immediate and delayed self-improvement use ticket Goal Packets.
- [x] `metrics.yaml` owns metric definitions; bindings own provider mechanics.
- [x] Core owns explicit completion events and mining; UI is an adapter over
      Core artifacts.
- [x] QA and review evidence are ticket-scoped.
- [x] Current Farplane project files and init templates validate.
- [ ] Representative scheduled operation proves the loop over longer real
  windows without unacceptable duplicate supply or operator burden.

The remaining acceptance work is representative scheduled operation over
longer real windows and the AI Office hierarchy described above.

## Non-Goals

- A hidden scheduler, daemon, hosted control plane, or autonomous cloud wrapper.
- A separate planner or worker pool for every capability or artifact category.
- A generic runtime, evidence, review, or hand-maintained registry ontology.
- Treating reports, CRM records, prospects, or observations as tickets by
  default.
- High-volume content-market experimentation without a separate budget and
  interference contract.
- Automatic doctrine promotion from one successful experiment.
- Silent changes to human thesis, spend, publishing, customer contact, deploy,
  or destructive authority.

## Risks And Backpressure

| Risk | Backpressure |
| --- | --- |
| Planner creates busywork | empty-board gate, bounded wave, ticket-quality review, duplicate detection |
| Review queue overwhelms operator | review WIP, worker release, one due reminder per beat |
| Delayed experiments interfere | explicit experiment WIP and delayed-live caps |
| Reports become alternate planners | source-specific authority and report Problems ledger |
| Self-improvement bloats the harness | hardening/refinement proof, toy/eval routes, rollback, transfer tests |
| Generated state becomes canonical | owner-named source files and registry/report links back to owners |
| Minimal schema hides necessary state | Goal Packet and ticket artifacts retain detail outside frontmatter |

## Release And Change Policy

V1 is the current standard. Future changes must begin from observed operating
failures or accepted operator direction, update the smallest owner surface, and
prove that the change improves the relevant metric without violating quality,
authority, or proof constraints.

Structural replacements of the V1 kernel require an explicit reviewed PRD or
feature decision. Ordinary refinements should update the owning lifecycle doc,
skill, template, validator, or ticket contract without inventing a new
framework generation name.
