---
title: "Farplane Lifecycle"
status: active
owner: farplane-framework
created_at: 2026-06-23
updated_at: 2026-07-12
framework_template_version: "0.3.0"
tags:
  - farplane
  - lifecycle
  - automations
  - goals
  - graph
refs:
  - docs/farplane-framework/README.md
  - docs/prd.md
  - docs/farplane-framework/init-advisor-critical-path.md
  - docs/farplane-framework/project-files.md
  - docs/farplane-framework/ticket-execution-loop.md
  - docs/farplane-framework/pulse-and-interval-loop.md
  - docs/farplane-framework/graph-contract.md
  - docs/farplane-framework/hooks-and-runtime.md
  - docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md
  - docs/features/FEAT-0060-registry-backed-documentation-os.md
  - docs/features/FEAT-0071-project-work-pulse.md
  - docs/MEMORY.md
---

# Farplane Lifecycle

Farplane V1 is a file-backed operating system for agent-run projects. Its
center is deliberately small:

```text
project(program, progress)
  -> typed charter + selected metrics + reusable capability skills
  -> one ticket board
  -> one Work Pulse executes tickets or plans a bounded cross-area wave
  -> scheduled sources add reports and candidate context
  -> ticket programs, progress, QA, and review preserve proof
  -> durable outcomes flow back to docs, metric objectives, and skills
```

Files carry durable state, skills carry reusable workflows, tickets carry work
contracts, and native Codex Goals carry material continuation. A capability
skill may produce an important recurring artifact, but it does not receive its
own planner, worker pool, strategy file, or heartbeat.

## Quick Start

1. Run `init-advisor` to create or migrate the project substrate.
2. Read `farplane/harness.yaml` for identity, complete planning area records
   and each canonical `areas.<area_id>.planner_instruction`, policy, capabilities,
   and selected objectives/guards.
3. Read `farplane/metrics.yaml` for metric meaning, direction, freshness, and
   guard rules; read generated observations for current values.
4. Read the ticket board for executable commitments and proof.
5. Use `metric-advisor` when the objective, guard, or proof provider needs a material change.
6. Use `goal-advisor` when a selected material ticket needs a Goal Packet.
7. Activate exactly one Work Pulse heartbeat after the board and proof surfaces
   are ready. Feed Scout, BAU reports, Dogfood, and maintenance are
   separate cron or manual automations.

The deeper bootstrap path is [Init Advisor Critical Path](init-advisor-critical-path.md).
The file-by-file reference is [Project Files](project-files.md).

## Lifecycle Map

```mermaid
flowchart TD
  classDef program fill:#e0f2fe,stroke:#0369a1,color:#0c4a6e
  classDef work fill:#dcfce7,stroke:#15803d,color:#14532d
  classDef source fill:#fef3c7,stroke:#b45309,color:#78350f
  classDef proof fill:#f3e8ff,stroke:#7e22ce,color:#581c87

  A["Operator intent"]:::program --> B["init-advisor"]:::program
  B --> C["harness.yaml + metrics.yaml + capability skills"]:::program
  C --> D["one ticket board"]:::work
  D --> E["one Work Pulse"]:::work
  E --> F{"executable ticket?"}:::work
  F -->|yes| G["worker runs ticket / program / progress"]:::work
  F -->|no| H["plan_next_wave"]:::work
  H --> D
  G --> I["QA + review evidence inside ticket"]:::proof
  I --> J["closeout + durable writeback"]:::proof

  K["Feed Scout"]:::source --> O
  L["Daily / Weekly BAU"]:::source --> O
  M["Dogfood self-improvement"]:::source --> O
  N["Maintenance"]:::source --> O
  K --> O["dated reports"]:::source
  L --> O
  M --> O
  N --> O
  O --> H
```

## The Minimal Work Loop

```text
pulse(tickets, worker_limit, review_wip, wave_size)
  -> do(admitted_ticket)
   | plan_next_wave(harness.areas complete records and planner instructions,
                    metric_definitions, metric_state,
                    ticket_history, current_context, wave_size)
```

Work Pulse is the only execution heartbeat. On each beat it:

1. reconciles worker and review outcomes;
2. derives due check-in eligibility from ticket Reward rows;
3. admits executable tickets under worker and review capacity;
4. hands workers the original ticket Goal Packet and proof contract;
5. asks one adaptive planner for a bounded globally ranked wave only when no
   unclaimed executable or due-check-in work exists; human-active tickets do
   not consume Pulse worker capacity;
6. writes a dated receipt.

It does not run separate capability controllers or perform long-horizon
strategy review. The planner may call capability skills when a proposed ticket
needs them.

## Scheduled Sources

Scheduled automations are report and candidate-context producers, not
additional heartbeats or proactive ticket authorities:

| Source | Reads | Writes | Ticket authority |
| --- | --- | --- | --- |
| Feed Scout | configured feeds and prior source reports | source report + candidates | none; next-wave planner compares candidates |
| Daily / Weekly BAU | bounded project window and prior finalized evidence | Problems ledger + candidates | none; next-wave planner compares candidates |
| Dogfood | active and recent archived experiments plus prior report | portfolio learning report + experiment candidates | none; self-improvement competes globally |
| Maintenance | registries, docs, skills, validators | maintenance report + repair candidates | none unless directly invoked by the operator |

Daily and Weekly do not invent new direction. Feed Scout and Dogfood do not
materialize their candidates. Work Pulse is the single normal path that turns
a winning proactive candidate into a ticket on the shared board.

Ticket completion is the narrow event-driven exception, not another heartbeat:

```text
ticket.completed
-> bounded learning report
-> strongest grounded finding
-> one deduped direct-fix or prove-or-reject ticket
```

The semantic reviewer remains read-only. Deterministic Core owns the local
ticket write after schema, evidence, privacy, confidence, KPI, and dedupe gates.
Declared KPI work enters `todo`; missing KPI remains `awaiting_review`.
Only source-ticket and self-improvement KPI bindings qualify. A stable semantic
key dedupes paraphrases, and a projected ticket's own completion is report-only
to prevent recursive ticket supply.

## Goal Packets And Check-Ins

Material or resumable work uses:

```text
tickets/TASK-XXXX/
  ticket.md    # scope, Reward, Done / Proof, QA/review contract
  program.md   # loop, budgets, stop rules, executable Check-In Program
  progress.md  # append-only observations and decisions
  artifacts/   # implementation, QA, review, and supporting evidence
```

For delayed Reward rows, Work Pulse derives readiness and resumes the original
ticket. The worker reads `program.md` first and executes its `Check-In Program`.
It updates only matured rows and decides `accept | kill | monitor` as
the program permits. Future rows remain dormant. Pulse dispatches this work; it
does not reconstruct or independently score the experiment policy.

## State Ownership

| State | Durable owner |
| --- | --- |
| Identity, planning areas/instructions, constraints, authority, capabilities, selected metric refs | `farplane/harness.yaml` |
| Metric meaning, direction, freshness, and guard rules | `farplane/metrics.yaml` |
| Recurring workflow | reusable `skills/*` or project-local `.agents/skills/*` |
| Executable commitment and all QA/review evidence | owning ticket and `artifacts/` |
| Goal/check-in loop policy | ticket `program.md` |
| Append-only task or experiment observations | ticket `progress.md` |
| Desired automation topology and prompts | `farplane/automations.toml` |
| Provider coordinates | `farplane/bindings.yaml` |
| Runtime receipts and derived context | `.farplane/reports/**` and other generated `.farplane/**` projections |

Reports help the next reader plan, but are not a second source of executable
state. Generated indexes are projections over these owners, not hand-maintained
strategy ledgers.

## Capability Skills

Important recurring outputs should have callable skills:

```text
capability_skill(ticket, metric_objectives, current_context)
  -> artifact + evidence + ticket_state_delta
```

Use a root `skills/<name>/` package when the workflow is reusable across
projects. Use `.agents/skills/<name>/` when it is company- or project-specific.
Promote only after repeated evidence. A skill owns how to produce the artifact;
`harness.yaml` selects the measurable contribution; the ticket owns the current commitment and
proof.

## Minimum Autonomous Instruction Set

A project needs:

- `farplane/harness.yaml` with identity, planning areas/instructions, stable policy, authority,
  capability refs, and selected metric refs;
- `farplane/metrics.yaml` with definitions, direction, freshness, and guard
  rules for every referenced metric;
- `farplane/automations.toml` with exactly one Work Pulse heartbeat and bounded
  scheduled sources;
- `farplane/bindings.yaml` for non-secret provider coordinates;
- reusable or project-local capability skills for recurring workflows;
- tickets with Reward, Done / Proof, and ticket-owned QA/review evidence;
- dated reports as derived context.

If required context is missing, write a source gap, planning request, or
bounded instrumentation ticket instead of guessing or rebuilding a controller
layer.

## Durable Learning

Closeout and scheduled maintenance compress useful outcomes back to the
smallest owner:

- measurement evidence can propose a `metrics.yaml` definition or
  `harness.yaml` selection delta;
- stable policy evidence can propose a human-reviewed `harness.yaml` delta;
- repeated workflow evidence can harden or refine the owning skill;
- unresolved executable work remains a ticket;
- raw run detail stays in ticket artifacts or dated reports.

This preserves `program + progress` without turning every observation into a
new schema or global ledger.
