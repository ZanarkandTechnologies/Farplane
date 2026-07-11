---
title: "PRD: Farplane V1"
status: active
owner: farplane
created_at: 2026-05-26
updated_at: 2026-07-11
version: "1.0"
refs:
  - docs/farplane-framework/lifecycle.md
  - docs/farplane-framework/project-files.md
  - docs/farplane-framework/pulse-and-interval-loop.md
  - docs/farplane-framework/ticket-execution-loop.md
  - farplane/harness.md
  - farplane/goals.yaml
  - farplane/metrics.yaml
  - farplane/automations.toml
  - tickets/README.md
---

# PRD: Farplane V1

## Product Thesis

Farplane is a file-backed operating system for agent-run projects. It helps a
human operate long-running Codex work through visible programs, tickets,
capability skills, bounded automations, and reviewable proof.

```text
Farplane = program + progress
```

The V1 product promise is simple:

> Give an agent a project program and one ticket board; it should execute the
> best admitted work, ask for help without occupying a worker, plan a bounded
> next wave when the board is empty, and preserve enough proof to resume and
> improve safely.

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

The result is hidden state, duplicate work, weak attribution, inflated
metadata, and operator distrust.

## Audience

- Primary: founders and operators running agent-heavy projects.
- Secondary: engineers and agent designers maintaining reusable harnesses.
- Tertiary: collaborators reviewing artifacts, decisions, and evidence without
  reading raw transcripts or runtime logs.

## Jobs To Be Done

1. When I give an agent a project objective, I want it to choose and execute
   bounded work without losing my constraints.
2. When work spans turns or days, I want durable state that another agent can
   resume without hidden conversation context.
3. When an agent needs review or waits for reality, I want execution capacity
   released while the obligation remains visible.
4. When the board runs out of useful work, I want a bounded, ranked next wave
   grounded in goals, metrics, ticket history, and current context.
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
   -> plan bounded BAU wave when executable board is empty
-> bounded scheduled ticket/report sources
-> ticket-local QA, review, reward, and closeout
-> durable learning back into goals, policy, skills, docs, or features
```

### Canonical State

| Surface | Responsibility |
| --- | --- |
| `farplane/harness.md` | stable thesis, authority, guardrails, capability refs |
| `farplane/goals.yaml` | current value direction, KPIs, milestone, bets, holds |
| `farplane/metrics.yaml` | provider-independent metric meaning |
| `farplane/bindings.yaml` | safe provider coordinates and refresh recipes |
| `farplane/automations.toml` | one Work Pulse plus bounded scheduled jobs |
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
| BAU planner | new ranked project-progress tickets when the executable board is empty |
| Feed Scout | source report and bounded evidence-backed opportunity tickets |
| Daily/Weekly BAU | problem report and deduped already-evidenced maintenance |
| Dogfood Review | experiment portfolio report and bounded self-improvement tickets |
| Operator | explicit direction, feedback, correction, or approval |

Only Work Pulse executes tickets and matured check-ins.

## Functional Requirements

### FR-1: Project Program

- A project can express stable policy, current goals, metrics, provider
  bindings, capability routes, and automation topology in tracked files.
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
- Pulse plans a bounded BAU wave only when no admitted executable work exists.
- Wave size, worker capacity, review WIP, and experiment capacity remain
  separate controls.

### FR-4: Human Review

- A worker sends one review request, records its Review block, sets
  `awaiting_review`, clears its claim, and exits.
- Queue size provides backpressure but does not itself trigger chasing.
- Pulse may send at most one ticket-owned due reminder per beat.

### FR-5: Scheduled Sources

- Feed Scout, BAU Interval, and Dogfood run as bounded cron/manual jobs rather
  than extra heartbeats.
- Each source may create only its declared ticket class.
- Interval does not choose new strategy; Dogfood does not execute experiments;
  Feed Scout does not execute opportunities.

### FR-6: Self-Improvement

- Every proposed change names a target surface, objective, feedback class,
  proof route, budget, guard, and rollback.
- Immediate feedback runs inside the current Goal-backed ticket.
- Delayed feedback stays on the original ticket and resumes through its
  Check-In Program.
- Accepted patterns require transfer evidence before doctrine promotion.

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

## Success Metrics

| Metric | Direction | Meaning |
| --- | --- | --- |
| `auto_completion_rate` | maximize | completed associated tickets required no post-start human intervention |
| `intervention_free_ticket_count` | maximize | autonomous completion produces useful throughput |
| `ticket_intervention_turn_count` | minimize within quality floor | supervision falls without false completion or drift |
| `rejected_ai_ticket_count` | minimize | Pulse planning produces fewer low-value tickets |
| `todo_unclaimed_ticket_count` | bounded operating signal | executable supply is visible without uncontrolled backlog growth |
| `accepted_harness_improvements` | increase selectively | self-improvement produces reviewed durable value |
| `latest_eval_pass_rate` | preserve or improve | refinement does not silently lower tested behavior quality |

Metric semantics live in `farplane/metrics.yaml`; provider refresh mechanics
live in `farplane/bindings.yaml`. Dispatch correctness, review-worker release,
resumeability, maintenance precision, and experiment-packet completeness remain
binary feature/test gates until repeated operation justifies registered metric
cards.

## V1 Acceptance

- [x] Product-scoped Pulse controllers and product state are retired.
- [x] One project Work Pulse handles ordinary tickets and matured check-ins.
- [x] Ticket metadata is reduced to lifecycle and sparse routing.
- [x] Human review and signal waits release workers.
- [x] Feed Scout, Daily/Weekly BAU, and Dogfood are bounded independent jobs.
- [x] Immediate and delayed self-improvement use ticket Goal Packets.
- [x] `metrics.yaml` owns metric definitions; bindings own provider mechanics.
- [x] QA and review evidence are ticket-scoped.
- [x] Current Farplane project files and init templates validate.
- [ ] Representative scheduled operation proves the loop over longer real
  windows without unacceptable duplicate supply or operator burden.

The unchecked item is continuing operational evidence, not a missing V1
architecture surface.

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
