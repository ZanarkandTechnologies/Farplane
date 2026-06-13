---
title: Harness Engineering Doctrine
status: active
owner: harness-advisor
created_at: 2026-04-24
updated_at: 2026-06-13
refs:
  - docs/fundamentals/harness-algebra.md
  - docs/specs/goal-loop-contract.md
  - docs/specs/filesystem-lifecycle.md
  - docs/skills/README.md
---

# Harness Engineering Doctrine

## Purpose

This is the concise field guide for choosing which harness lever to pull.

Use `docs/fundamentals/harness-algebra.md` for the formal model. Use this file
when the practical question is:

```text
What lever should change, what does it do to the system, what can it break,
and what proof would show the change worked?
```

The doctrine is Farplane-first. It routes proposed harness changes to the
smallest surface that can reduce the named loss.

```text
harness_algebra(change, state)
  -> coordinate + loss_term + proof_signal + accept_rule

harness_engineering_doctrine(change, coordinate)
  -> lever + owner_surface + rejected_surfaces + proof_route
```

## Priority Order

Do not treat every objective as a flat maximize/minimize problem. Optimize in
this order:

```text
1. Preserve correctness, safety, proof, and operator control.
2. Load always-needed constraints where they are cheapest to retrieve.
3. Minimize tool calls for predictable context.
4. Minimize irrelevant always-loaded prompt.
5. Minimize turns and coordination cost.
6. Add control loops only when the failure mode justifies them.
```

Default tuning order:

```text
proof/review requirement
-> ticket or work-package contract
-> skill contract or skill selection
-> context/file/memory policy
-> subagent boundary
-> hook or validator
-> tool/MCP capability
-> automation or heartbeat
-> root/global prompt
```

Root prompt is last because every token is paid by every task. Promote to root
only when the rule is durable, global, frequently needed, and expensive to
recover later.

## Lever Guide

| Lever | What It Changes | Use When | Can Break | Proof |
| --- | --- | --- | --- | --- |
| System prompt | Always-loaded constraints and defaults. | A rule must apply every turn across many workflows. | Prompt bloat, contradictions, global overreach. | Prompt/token diff plus behavior regression check. |
| Project `AGENTS.md` | Repo-local routing, priorities, and boundaries. | Farplane-specific agents need the same map or invariant. | Local prompt bloat, stale routing. | Representative agent behavior or doc invariant check. |
| Global template | Cross-repo default operating contract. | Every installed project needs the behavior. | Broad blast radius. | Template diff plus install/docs validation. |
| Skill | Just-in-time reusable workflow context. | A procedure repeats but is not globally needed. | Stale triggers, wrong skill routing. | Skill eval, checklist conformance, or transcript replay. |
| Skill contract | Skill inputs, outputs, state reads/writes, proof, and side effects. | Agents invoke a skill inconsistently or cannot compose it. | Ceremony in tiny skills. | Skill eval and `check_skills.py`/registry validation. |
| Reference file | Skill-local background or examples. | Detail is useful only after the skill is selected. | Hidden stale context. | Skill task uses the reference correctly. |
| Script/template | Repeatable mechanical step or artifact skeleton. | Manual steps are error-prone or verbose. | Brittle automation, generated clutter. | Script test or generated artifact review. |
| Ticket contract | Task boundary, Done / Proof, current state, and handoff. | Work size or proof target is unclear. | Ticket bureaucracy or fragmented work. | Ticket metadata/checks plus reviewer or QA proof. |
| `program.md` | Loop config, metric, drift policy, heartbeat, and stop conditions. | A ticket is Goal-backed, heartbeat-based, rollout-like, or long-running. | Second-ticket confusion. | Goal Packet drift review. |
| `progress.md` | Append-only observed execution memory. | Future turns must reconstruct state without transcript memory. | Transcript dumping, noisy logs. | Resume from files alone. |
| Portfolio | Long-horizon goal graph and current frontier. | Work spans multiple tickets, goals, and projects. | Overplanning future branches. | Parent heartbeat selects one executable leaf. |
| File/memory policy | What state is durable, searchable, drained, or archived. | Lessons are lost or context is stale/noisy. | Artifact graveyard, stale retrieval. | Drain/retrieval test. |
| Subagent | Independent context and owned output. | Self-approval, role separation, or parallel evidence matters. | Coordination cost, duplicated work. | Subagent artifact plus integration review. |
| Tool/MCP | External capability or source of truth. | The agent cannot inspect, operate, or verify ground truth. | Latency, side effects, unused tools. | Tool-backed evidence artifact. |
| Hook | Deterministic boundary decision. | A mechanical pass/block/continue decision repeats. | False blocks or hidden routing. | Fixture test. |
| Validator | Mechanical invariant over files or generated state. | A repeated high-signal structural failure can be checked. | Noise, over-policing narrative nuance. | Validator test. |
| Eval | Repeatable behavior or placement claim. | A harness change should be scored across cases. | Overfit, brittle judges, eval burden. | Baseline + heldout result. |
| Review | Judgment-heavy sufficiency or quality claim. | Taste, proof quality, or readiness requires independent judgment. | Latency, subjective churn. | TAS verdict and cited evidence. |
| QA/browser proof | User-visible behavior. | UI or workflow needs operated evidence. | Slow proof loops. | Screenshot, console/log trace, QA report. |
| Automation/cron | Scheduled or event-triggered inspection. | Time, feedback, or external state determines next action. | Hidden autonomy, noisy wakeups. | Logged no-op/action and stop condition. |
| Heartbeat | Delayed check over existing Goal Packet or portfolio state. | Work should resume only after time/feedback/external state. | Untracked background planning. | `progress.md` heartbeat entry. |
| Native Goal | Immediate continuation for one executable leaf. | Multi-turn work should keep moving now. | Prompt-only loops, drift. | Goal Packet with drift policy. |

## Promotion Rules

Choose the cheapest reliable place for context.

```text
promote_to_system_prompt(context)
  iff always_needed(D, context) is high
  AND omission_cost(context) is high
  AND contradiction_or_bloat_risk(context) is low
```

```text
promote_to_skill(context)
  iff needed_for_task_family(D_i, context)
  AND not globally_needed(context)
```

```text
keep_in_file_or_memory(context)
  iff durable(context)
  AND not always_needed(context)
```

```text
use_tool_or_search(context)
  iff freshness_required(context)
  OR context_too_large_to_preload(context)
```

Interpretation:

- system prompt is for universal, durable, high-omission-cost rules
- skills are for repeated task-family procedures
- files are for durable state and detailed references
- tools are for current truth, operation, and inspection
- automations are for delayed triggers, not hidden work

## Placement Analysis

For material harness changes, compare these surfaces:

1. repo-local `AGENTS.md`
2. `templates/global/AGENTS.md`
3. `docs/fundamentals/*` or `docs/specs/*`
4. `skills/*`
5. `agents/*.toml`
6. hooks, validators, or `bin/*`
7. tickets, templates, or Goal Packet files
8. tool/MCP surface

For each candidate, state:

- what problem it would solve well
- why it is or is not the primary surface now
- what proof would show the lever worked
- what secondary surfaces must stay in sync

Expected output:

```text
Primary lever:
Owner surface:
Rejected surfaces:
Proof:
Secondary sync:
Rollback:
```

## Common Routing

```text
global invariant missing
  -> project AGENTS or global template

repeatable procedure inconsistent
  -> skill or skill contract

state not resumable
  -> ticket/program/progress or filesystem policy

proof weak or self-approved
  -> Done / Proof, review, QA, or subagent boundary

deterministic invariant failing
  -> validator or hook

current external truth needed
  -> tool/MCP

delayed external state or feedback needed
  -> heartbeat or automation

long-horizon goal drifting
  -> portfolio + child Goal Packets + drift review
```

## Ticket And Goal Memory

Use this hierarchy for long-running work:

```text
goal -> project[] -> task[]

portfolio.md = long-horizon map + current frontier
ticket.md = executable leaf contract + Done / Proof
program.md = loop policy + metric + stop condition
progress.md = observed execution memory
artifacts/ = evidence
```

Parent portfolio control:

```text
portfolio_heartbeat(portfolio, parent_program, progress)
  -> no_op | start_child_goal | resume_child_goal | request_feedback | replan
```

Leaf execution:

```text
leaf_native_goal(ticket, program, progress)
  -> artifact + evidence + completion_entry
```

Completion:

```text
complete_child_goal(child_packet, portfolio, parent_program)
  -> progress_entry + portfolio_state_delta + next_trigger
```

Use native Goal for the selected executable leaf. Use heartbeat/manual resume
for the parent portfolio. Do not run a whole portfolio as one indefinite native
Goal.

## Small-Eval Loop

For any harness change:

1. Name the observed failure.
2. Name the expected behavior.
3. Choose one primary lever.
4. Define the smallest proof that can kill or support the change.
5. Apply the smallest patch.
6. Run proof and review when judgment matters.
7. Accept, hold, or roll back.
8. Write durable learning to the owning artifact.

Default writeback order:

- ticket or active work artifact first
- canonical spec or skill second
- `docs/HISTORY.md` for meaningful shipped milestones
- `docs/MEMORY.md` only for durable invariants
- `docs/TROUBLES.md` only for raw repeated misses or corrections
- `docs/LESSONS.md` only for distilled prevention rules

## Anti-Goals

- do not solve every failure with more global prompt text
- do not create a new skill before checking the skill registry
- do not create a new subagent when a skill contract would fix the issue
- do not use hooks for judgment-heavy work
- do not split tickets below the proof boundary
- do not add validators before the failure pattern is clear
- do not make cron, heartbeat, or Goal mode into hidden autonomy
- do not claim harness improvement without proof
