---
name: work
description: Classify one request, ticket, ticket batch, board-selected unit, epic, or metric loop into an execution profile, then route to the right Codexter skill, native Goal, compute target, and proof policy before implementation starts.
tier: 3
group: coding
source: local
version: 0.1.0
allowed-tools: Read, Glob, Grep
---

# Work

<!-- BEGIN CODEXTER_IMPORTANT_CHECKLIST -->
## Important Checklist

Source: `SKILL.md`

- [ ] Read the operator request, ticket, batch, or board context.
- [ ] Classify the work unit: direct request, single ticket, ticket batch,
  board drain, epic slice, or metric loop.
- [ ] Check scope readiness: executable now, needs `impl-plan`, needs
  reslicing, or needs a metric/research loop.
- [ ] Choose the execution profile: ambition, Goal policy, compute target,
  planning route, proof route, testability route, and blocker policy.
- [ ] Use [plan](../plan/SKILL.md) or `impl-plan` only when material planning
  is warranted.
- [ ] Use [execute](../execute/SKILL.md), `$impl`, direct local work, or
  `close-ticket` only after the work unit is executable.
- [ ] For ticket batches, require one proof row per ticket plus one batch-level
  regression row before completion.
- [ ] For board drains, hand board selection and grouping to `$ralph`; do not
  create hidden scheduler state here.
- [ ] Use `goal-crafter` or native `/goal` when the work is ambitious,
  long-running, batch-oriented, board-draining, metric-driven, or likely to
  need durable unblock behavior.
- [ ] When a ticket already has metrics, acceptance criteria, proof commands,
  or blockers and Goal is recommended, route through goal-crafter's
  ticket-backed `GoalPrepState` branch instead of restarting discovery.
- [ ] Record blockers with evidence instead of asking the operator when the
  ticket policy already gives a safe fallback.
<!-- END CODEXTER_IMPORTANT_CHECKLIST -->

`$work` is Codexter's Work Admission surface.

Use it when the operator wants one prompt, ticket, ticket batch, board-selected
unit, epic, or metric loop handled intelligently, but the system first needs to
decide how much ceremony, compute, planning, Goal persistence, proof, and
batching the work deserves.

`$work` is not a build engine. It chooses the execution profile and routes to
the owning surface:

- native `/goal` for durable ambition and stopping criteria
- `goal-crafter` when the Goal needs a crisp proof and blocked-stop contract
- `$ralph` for board context and board-drain selection
- `batch-work` for an explicit operator-supplied ticket range or list
- `spec-to-ticket` or PRD work when the unit is an epic, not executable work
- `impl-plan` when a material ticket needs implementation planning
- `$impl` when an accepted work package should be built and proved
- `autoresearch-plan` / `autoresearch-exec` only for real metric loops
- direct local work for tiny obvious changes

## Mental Model

Tickets and cards are durable work contracts. They are not automatically the
right compute unit.

```text
Board = source of truth for work items
Ticket/card = durable work contract
Goal = durable intent + stopping checker
Work = admission + execution profile for one work unit
Batch-work = explicit operator range/list runner
Ralph = board-aware scheduler/context provider
Compute = selected per work unit
```

## Execution Profile

Every `$work` pass should classify the work into an execution profile:

```ts
type WorkUnit =
  | { kind: "direct_request"; prompt: string }
  | { kind: "single_ticket"; ticketPath: string }
  | { kind: "ticket_batch"; ticketPaths: string[]; batchReason: string }
  | { kind: "board_drain"; boardPath: string }
  | { kind: "epic_slice"; sourcePath: string }
  | { kind: "metric_loop"; ticketPath: string; metricRef: string };

type ExecutionProfile = {
  unit: WorkUnit["kind"];
  ambition: "tiny" | "normal" | "large" | "epic";
  goal: "none" | "recommend" | "required";
  goalPrep: "none" | "paste_ready" | "ticket_backed_state";
  compute: "local_shared" | "local_worktree" | "codex_cloud" | "symphony";
  planning: "none" | "light" | "impl_plan" | "reslice";
  proof: Array<"smoke" | "tests" | "qa" | "visual_qa" | "review" | "demo">;
  testability: "single_proof" | "batch_ledger" | "batch_ledger_plus_regression";
  blockerPolicy: "continue_with_fallbacks" | "record_blocker" | "ask_user";
};
```

The profile is a decision aid, not a persisted runtime daemon.

## Goal Admission

Use native `/goal` when the work benefits from durable continuation:

- one ambitious ticket
- a ticket batch
- a board-drain run
- a metric optimization loop
- a long unblock or research loop
- any work where stopping criteria must survive context drift

Use goal-crafter's ticket-backed `GoalPrepState` branch when Goal is useful and
the work unit already carries a ticket, plan, or Proof Contract with metrics,
acceptance criteria, verification commands, blockers, or scope boundaries. In
that case `$work` should preserve the existing work contract and ask only
missing execution-safety questions, not broad product-discovery questions.

Do not use Goal for:

- one obvious typo
- one small button fix
- one mechanical config tweak
- work whose proof and next step are already deterministic

## Batch Testability

Batching is good for solo local work when setup, module area, proof surface,
and regression checks are shared. It is bad when failures become hard to
attribute.

Batchable work should satisfy all of these:

- same module, workflow, or product surface
- same runtime setup
- same proof surface or compatible proof surfaces
- low or medium risk
- no conflicting write ownership
- no separate human approval gate
- each ticket can still get an independent proof row

Every ticket batch must maintain:

| Ticket | Change | Local proof | Result | Blocker |
| --- | --- | --- | --- | --- |
| TASK-0001 | short change | focused check | pass/block/fail | none or evidence |
| Batch | combined regression | batch check | pass/block/fail | none or evidence |

The batch may claim completion only when every ticket row is passed or blocked
with evidence and the batch-level regression row is passed or explicitly
blocked.

## Compute Defaults

Choose compute from invocation source and risk:

| Invocation | Default compute |
| --- | --- |
| local chat, tiny or normal work | `local_shared` |
| local risky or isolation-sensitive work | `local_worktree` |
| explicit local `batch-work` | `local_shared` or `local_worktree` based on risk |
| remote kanban runner | `codex_cloud` or external runner default |
| Symphony worker envelope | `symphony` |

Ticket `compute_target` is context, not authority. It may request a target, but
execution still starts only from explicit invocation.

## Workflow

1. Read the request, ticket, batch, or board context.
2. Decide whether this is executable work, a ticket batch, a board drain, an
   epic that needs slicing, or a metric loop.
3. Pick an execution profile:
   - `tiny/direct`: direct local work, no Goal, no `impl-plan`
   - `normal/single_ticket`: `impl-plan` if needed, then `$impl`
   - `ticket_batch`: Goal when useful, batch ledger, per-ticket proof rows, and
     one batch regression row
   - `board_drain`: use `$ralph` for board selection and repeat policy, then
     `$work` for each selected unit
   - `epic_slice`: route to PRD, `spec-to-ticket`, or `deep-system-design`
   - `metric_loop`: route to autoresearch before implementation
4. If Goal is recommended but not already active, use `goal-crafter` to produce
   one paste-ready Goal for the current scope. Use `goalPrep=ticket_backed_state`
   when the ticket already has metrics, acceptance criteria, proof commands,
   blockers, or scope boundaries.
5. Route to the owning skill and keep evidence in the ticket or batch surface.
6. If blocked, record evidence, attempted paths, safe options, recommended
   next action, and the single missing input that would unlock progress.

## Examples

### Tiny Direct Work

```text
$work "change the settings button label to Apply"
```

Profile:

```text
unit=direct_request
ambition=tiny
goal=none
planning=none
proof=smoke,review
```

### Single Ticket

```text
$work tickets/TASK-0123/ticket.md
```

Profile:

```text
unit=single_ticket
ambition=normal
goal=recommend only when long-running or ambiguous
goalPrep=ticket_backed_state when the ticket has a Proof Contract or blockers
planning=impl_plan when material
proof=tests,qa,review
```

### Ticket Batch

```text
$work TASK-0201 TASK-0202 TASK-0203
```

Profile:

```text
unit=ticket_batch
goal=required when the batch is more than a quick direct pass
testability=batch_ledger_plus_regression
```

### Board Drain

```text
$ralph tickets/
```

Ralph reads the board, chooses eligible work units, and calls `$work` for each
unit. Goal owns the durable "keep draining until no eligible unblocked tickets
remain" stopping condition.

### Metric Loop

```text
$work TASK-0300 improve retrieval quality by 15%
```

Use autoresearch only when the metric, verify command, guard, and iteration
budget are real.

## Guardrails

- Do not implement vague intent. Route it to PRD, `spec-to-ticket`, or
  `deep-system-design`.
- Do not make every task a Goal. Goal is for ambition, persistence, or loops.
- Do not make every task an `impl-plan`. Tiny work should stay tiny.
- Do not hide batch proof inside a summary. Use per-ticket rows.
- Do not let `$work` become a scheduler, daemon, or cloud runner.
- Do not override human gates, destructive boundaries, deploy, spend, or
  credential provisioning.
- Do not remove standalone `batch-work`; use it for explicit operator
  ranges/lists and align it with this policy.

## Outcome Contract

Return or write:

- selected `ExecutionProfile`
- chosen Goal policy and paste-ready Goal when needed
- chosen goal prep mode: none, compact paste-ready Goal, or ticket-backed
  `GoalPrepState`
- chosen compute target and why
- chosen route: direct, batch-work, Ralph, spec-to-ticket, impl-plan, `$impl`,
  autoresearch, or close-ticket
- proof policy, including batch ledger rows when batching
- blocker evidence if the work cannot proceed
