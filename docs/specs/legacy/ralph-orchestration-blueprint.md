# Ralph Ticket-Orchestrated Runtime

Date: 2026-04-05

> Historical prototype blueprint. The current public build-phase orchestration
> surface is `$impl`; references here to removed binary-first prototype flows
> are background only, not the preferred future control plane.

## Goal

Define the practical system shape for a ticket-first `ralph` runtime that:

- ingests different input types
- turns them into executable SLC tickets
- uses fresh Codex sessions for bounded ticket phases
- uses a lightweight judge to advance/block work
- keeps the board and ticket memory trustworthy

This document is the canonical system blueprint.

## Thesis

`ralph` should be a **ticket-orchestrated runtime** on top of Codex, not a monolithic forever-loop and not a second chat UI.

The clean shape is:

1. **Operator / intake** creates or imports work
2. **Orchestrator** selects the next ready ticket and phase
3. **Worker session** runs one bounded phase via `codex exec`
4. **Judge** reads evidence and ticket state, then returns a transition verdict
5. **Orchestrator** either re-runs the same phase, advances the ticket, or schedules the next ready ticket

## Canonical Components

### 1. Kanban board

Human-facing planning and visibility surface.

Purpose:
- see backlog, review, building, blocked, done
- understand dependencies
- inspect priorities
- open the ticket file

Canonical truth:
- **not** the source of hot execution state
- should mirror ticket lane, status, owner, and next action

Good surfaces:
- Notion board
- local filesystem board
- both, if sync is summary-only

### 2. Ticket markdown file

The canonical execution contract for one SLC slice.

Purpose:
- store scope, dependencies, phase, plan, evidence, blockers, and handoff
- survive session resets
- give each agent a bounded unit of work

Canonical truth:
- yes, for ticket-local memory and machine-readable task state

### 3. Run artifact

Lightweight runtime state for the current execution attempt.

Purpose:
- record active phase run
- map ticket -> worker session -> judge verdict
- make resume cheap

Canonical truth:
- yes, for runtime-only data that should not bloat the ticket body

Examples:
- current session id
- phase attempt count
- last judge verdict
- last worker output path
- compute class / lane choice
- concurrency budget snapshot

### 4. Prompt files

Static `skill` instructions used by handoff sessions.

Examples:
- `prompts/ralphplan.md`
- `prompts/ralph.md`
- `prompts/ralph-docs.md`

Purpose:
- keep phase behavior stable
- reduce prompt drift
- make `codex exec` handoffs deterministic

Recommended mental model:

- each prompt file is a **function body**
- the orchestrator passes only the small runtime context needed to execute that function
- do not restate the whole phase contract in every shell command

### 5. Orchestrator session

The persistent coordinator, not the coder.

Purpose:
- choose next unblocked ticket
- spawn phase workers
- read judge verdicts
- transition ticket lane/phase
- decide whether to continue same ticket or move on

### 6. Judge session

An ephemeral verifier/classifier, often hook-triggered.

Purpose:
- read ticket acceptance/evidence state
- inspect worker output and test artifacts
- decide:
  - repeat same phase
  - advance phase
  - mark blocked
  - mark complete

The judge should decide, not implement.

## Core Runtime Model

```mermaid
flowchart TD
    A[Operator input] --> B[Intake normalization]
    B --> C[Create/update ticket(s)]
    C --> D[Select next ready ticket]
    D --> E[Spawn codex exec worker for one phase]
    E --> F[Worker updates ticket and writes evidence]
    F --> G[Judge reads ticket + evidence]
    G --> H{Verdict}
    H -->|repeat phase| E
    H -->|advance ticket phase| I[Update ticket and run state]
    I --> J{Ticket complete?}
    J -->|no| D
    J -->|yes| K[Move ticket lane / write docs / commit / PR]
```

## Recommended Ticket State Model

Lane comes from folder path. Phase comes from frontmatter.

Suggested phase progression:

- `intake`
- `planning`
- `building`
- `documenting`
- `complete`
- `failed`

Suggested lane progression:

- `tickets/`
- `tickets/`
- `tickets/`
- `tickets/`

Rules:
- lane answers "where is this in the board?"
- phase answers "what exact step is the agent doing now?"
- `blocked_by` answers "why can this not move?"
- `next_action` answers "what should happen next?"

## Data In Each Component

### Kanban card / board row

Should show only summary data:

- `ticket_id`
- title
- lane
- phase
- priority
- `depends_on`
- `blocked_by`
- `next_action`
- `last_verification`

It should not carry the full build log or test transcript.

### Ticket file

Should hold:

- frontmatter:
  - `ticket_id`
  - `phase`
  - `status`
  - `depends_on`
  - `blocked_by`
  - `ready`
  - `approval_required`
  - `next_action`
  - `last_verification`
- body:
  - summary/scope
  - implementation plan
  - acceptance criteria
  - evidence
  - blockers
  - handoff/resume notes

### Run artifact

Should hold runtime-only fields like:

```json
{
  "run_id": "run-20260405-001",
  "ticket_id": "TASK-0042",
  "phase": "building",
  "status": "running",
  "session_id": "sess_abc123",
  "attempt": 2,
  "prompt_file": "prompts/ralph.md",
  "compute_class": "local",
  "parallel_slots_reserved": 1,
  "last_worker_result": "continue_ralph",
  "last_judge_verdict": "repeat_ralph",
  "updated_at": "2026-04-05T11:20:00Z"
}
```

## Fresh Session Contract

Each `skill` worker should run in a fresh session through `codex exec`.

The worker should receive:

1. prompt file
2. repo root
3. ticket path
4. relevant spec/PRD paths
5. optional run artifact path

Preferred handoff shape:

- keep the **entire skill contract** in the prompt file
- keep the shell wrapper thin
- pass the **ticket path**, not only the ticket id, so the worker never has to guess which file is canonical

Thin wrapper example:

```bash
RALPH_TICKET="tickets/TASK-0042-example.md" \
RALPH_RUN_STATE=".harness/runs/run-20260405-001.json" \
codex exec --skip-git-repo-check -C "$ROOT" - < prompts/ralph.md
```

The prompt file itself should say things like:

- read `AGENTS.md`
- read the ticket at `$RALPH_TICKET`
- read linked docs from the ticket
- run the bounded `skill` only
- update ticket evidence / notes
- emit one `RALPH_RESULT` line

The canonical model should live in the `skill` prompt file. Specs should not present large inline heredoc prompts as normal usage because they blur the boundary between wrapper context and `skill` behavior.

## Why Bounded Skills Matter

Bounded `skill` workers prevent:

- one session coding forever
- prompt drift
- state confusion
- bloated transcripts
- accidental hidden orchestration inside the coding session

The `skill` should do one job and exit.

## Judge Contract

The judge should inspect:

- ticket acceptance gaps
- evidence gaps
- blocker state
- worker result line
- required proof artifacts

And return a small structured verdict such as:

```json
{
  "decision": "advance_ticket",
  "next_phase": "building",
  "reason": "plan is coherent and ticket is ready for ralph",
  "orchestrator_message": "launch ralph for TASK-0042"
}
```

Possible decisions:

- `repeat_ralphplan`
- `repeat_ralph`
- `advance_ticket`
- `block_ticket`
- `complete_ticket`
- `escalate_to_operator`

## Stop Hook Role

The stop hook is a good place to trigger the judge.

Recommended use:
- read latest assistant message
- resolve active ticket
- run a small ephemeral classification pass
- emit a bounded transition verdict

Do **not** make the stop hook:
- the planner
- the scheduler
- the code executor
- an invisible infinite continuation loop

The stop hook should judge. The orchestrator should act.

## Worktree Policy

Worktrees should be selective, not mandatory.

Use a worktree when:
- multiple tickets run in parallel
- a ticket needs branch isolation
- the same repo paths would otherwise conflict

Do not use a worktree when:
- only one ticket is active
- the change is small and local
- coordination overhead outweighs isolation

## Compute Policy

Compute choice is a scheduler/orchestrator concern.

The orchestrator should be able to choose among:

- `local`
- `local_worktree`
- `remote_vm`
- `remote_container`

This is primarily a **capacity and isolation** decision, not a phase-design decision.

Suggested policy:

- small / single-ticket / low-risk work -> `local`
- parallel tickets on one machine -> `local_worktree`
- many heavy tickets or long test suites -> `remote_vm` or `remote_container`
- risky untrusted execution -> isolated remote/container lane

The ticket can optionally carry hints like:

```yaml
compute_preference: auto
compute_class: standard
isolation_required: false
parallelizable: true
estimated_parallel_slots: 1
```

The run artifact can record the actual scheduler choice:

```json
{
  "compute_class": "remote_vm",
  "executor_target": "vm-eu-west-1-build-03",
  "parallel_slots_reserved": 2
}
```

## Capacity Model

The orchestrator should know the current budget before spawning work.

It does **not** need deep infrastructure state in the ticket, but it should know:

- max concurrent local workers
- max concurrent heavy test lanes
- available remote slots
- whether the next ticket would exceed the current budget

Simple example:

```json
{
  "local_parallel_limit": 3,
  "local_heavy_limit": 1,
  "remote_parallel_limit": 8,
  "local_parallel_in_use": 2,
  "remote_parallel_in_use": 0
}
```

If a ticket exceeds local budget, the orchestrator can:

1. queue it
2. downgrade parallelism
3. pick a cheaper local lane
4. escalate to remote compute

## Orchestrator Responsibilities

The orchestrator should do only five things:

1. discover ready tickets
2. choose the next ticket by dependency + priority rules
3. spawn the correct phase worker
4. read judge verdict
5. transition ticket/run state

It should not be the main code-writing session.

## Agent Stories

### Orchestrator story

As the orchestrator, I want to inspect ticket dependencies and phase state so I can always choose the next unblocked executable ticket without re-reading the whole project transcript.

### Ticket worker story

As a ticket worker, I want one ticket, one phase prompt, and one proof target so I can perform bounded work and write back deterministically.

### Judge story

As the judge, I want to inspect only the ticket contract and required evidence so I can decide whether work advances, repeats, blocks, or completes without accidentally doing implementation work.

### Operator story

As the operator, I want to see which ticket is active, why it advanced or blocked, and what the next action is so I can trust the automation without reading every transcript.

## What This Blueprint Bets On

This system bets on:

- tickets as durable memory
- bounded `codex exec` sessions
- lightweight judge logic
- orchestration through files and bash
- subagents inside worker sessions when useful

It does **not** bet on:

- one immortal per-ticket transcript
- hidden auto-continue forever loops
- a heavy tmux runtime as the first dependency
- board-first runtime state

## Open Questions

- exact ticket phase vocabulary
- exact run artifact schema
- how much of lane movement should the worker do vs orchestrator
- whether review/prove are distinct tickets or ticket phases
- when to force fresh-session resets inside a single ticket phase

## Suggested Next Step

Translate this blueprint into:

1. a ticket schema revision proposal
2. phase prompt templates
3. a stop-hook verdict schema
4. a minimal orchestrator loop shell script
