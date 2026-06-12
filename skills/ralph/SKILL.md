---
name: ralph
description: "Turn a prepared Farplane ticket board into eligible work selection, safe grouping, and Work Admission handoffs under Goal control."
tier: 3
group: coding
source: local
allowed-tools: Read, Glob, Grep, Bash
---

# Ralph

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Read `tickets/README.md`, active tickets, `docs/MEMORY.md`, and `docs/LESSONS.md`.
- [ ] Run the read-only selector and inspect skipped-ticket reasons.
- [ ] Stop on human gates, unresolved blockers, unresolved dependencies, claims, missing tools, or missing permissions.
- [ ] Decide whether the next safe work unit is one ticket or a low-risk related tiny-ticket batch.
- [ ] For any batch, require same module/workflow, same setup, compatible proof surface, no conflicting write scope, and no separate human gate.
- [ ] Hand the selected work unit to [$work](../work/SKILL.md); let `$work` choose `impl-plan`, `$impl`, `close-ticket`, direct local work, reslice, or autoresearch.
- [ ] For a batch, require one proof row per ticket plus one batch-level regression row before completion.
- [ ] After each work unit, reread the board before selecting again.
- [ ] Apply the three-ring QA policy before deciding whether to continue the board drain.
- [ ] End with `RALPH_RESULT: status=... selected=... reason=...`.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

`$ralph` is the board-drain context surface.

It reads a prepared ticket board, selects the next eligible work unit or a safe
batch of related small work, and hands that unit to `$work`. Native Codex
`/goal` owns the durable "keep draining until done or blocked" stopping
condition. `$ralph` does not implement tickets itself, and it does not launch
parallel agents in v0.

## Use When

- specs and tickets already exist under `tickets/TASK-*/ticket.md`
- the operator wants a prepared board drained without manually picking every
  next ticket
- the operator wants related tiny tickets grouped into a testable batch before
  handing them to `$work`
- tickets already carry enough `Done / Proof`, run hints, state, and blocker
  detail for unattended work to be safe

Do not use this for vague requirements, new architecture discovery, Notion or
Linear adapters, cloud runners, deploy/push/spend actions, or parallel
multi-agent dispatch.

## Relationship To Goal And Work

Use native `/goal` for durability:

```text
/goal Drain this board until no eligible unblocked tickets remain. After each
work unit or batch, reread the board. Stop only when every remaining ticket is
complete, archived, or explicitly blocked with evidence.
```

Use `$ralph` for board context:

- list eligible tickets
- skip blocked, claimed, dependent, or approval-gated tickets
- group safe related tiny tickets when that reduces local overhead
- hand each selected work unit to `$work`
- reread the board after each `$work` result

Use `$work` for execution admission:

- decide direct work vs `impl-plan` vs `$impl` vs reslice vs autoresearch
- decide whether a Goal is needed for the work unit
- decide proof, batch ledger, compute, and blocker policy

## Workflow

1. Read `tickets/README.md`, the active tickets, `docs/MEMORY.md`, and
   `docs/LESSONS.md` for queue and autonomy constraints.
2. Run a read-only selector pass. Prefer
   `python3 skills/ralph/scripts/select_next_ticket.py --root . --json` when
   working in this repo. The helper reads tickets through `FileTicketAdapter`
   and applies `ComputeSelector`; it reports compute blockers and setup hints
   but never mutates tickets, launches Codex, or creates worktrees.
3. Stop immediately when the selector reports no eligible ticket, a human gate,
   unresolved blockers, unresolved dependencies, or the configured loop limit.
4. Decide whether the next safe work unit is one ticket or a low-risk batch of
   related tiny tickets. Batch only when tickets share module/workflow, runtime
   setup, proof surface, and no conflicting write scope.
5. Hand the selected work unit to `$work`.
6. If `$work` returns completion, blocker, or revise evidence, write or preserve
   that evidence in the ticket surface.
7. After each work unit, reread the board and repeat from selector, never from
   stale transcript memory.
8. End with a compact result line:
   `RALPH_RESULT: status=<stopped|blocked|loop_limit|failed|complete> selected=<ticket|none> reason=<why>`.

## Batch Testability

Ralph may group tiny related tickets for solo local efficiency, but it must not
turn proof into one blob.

A Ralph-selected batch must leave a batch ledger:

| Ticket | Change | Local proof | Result | Blocker |
| --- | --- | --- | --- | --- |
| TASK-0001 | short change | focused check | pass/block/fail | none or evidence |
| Batch | combined regression | batch check | pass/block/fail | none or evidence |

If the batch cannot produce per-ticket rows plus a batch regression row, select
one ticket instead.

## Eligibility Policy

A ticket is eligible only when all are true:

- it lives in active `tickets/TASK-*/ticket.md`, not `tickets/archive/`
- `ready: true`
- `approval_required: false`
- `blocked_by: []`
- `claimed_by:` is empty
- every `depends_on` ticket is complete, archived, or explicitly waived in the
  ticket body
- the ticket's requested or default compute target is allowed by the repo
  `WORKFLOW.md` compute policy
- `phase` maps to a supported handoff:
  - `planning` -> `$work` chooses `impl-plan` or reslice
  - `building` -> `$work` chooses `$impl` or direct recovery
  - `documenting` -> `$work` chooses `close-ticket`
- `status` is not `blocked`, `done`, or `failed`

When multiple tickets are eligible, continue already-building tickets first,
then documenting closeout, then planning tickets. Within that phase order,
prefer higher priority and then lexical ticket id.

## Stop Conditions

Stop instead of improvising when:

- no eligible tickets remain
- the next ticket requires human plan review or human QA
- a dependency, blocker, claim, missing permission, missing credential, missing
  compute resource, missing tool, or destructive/deploy/spend action is needed
- the selector reports a compute blocker such as `missing_worktree_runtime`,
  `unsupported_target`, or `disallowed_by_workflow`
- `$work` or the selected downstream skill fails or returns a revise/block result
- the loop reaches the operator-specified maximum iteration count
- QA risk is too high for the available proof surfaces

## Board Readiness

Before a long run, check whether the board says what the agent will need:

- human inputs, assets, credentials, and external-service access
- GPU or other compute needs
- missing tools, browser paths, seeds, reset paths, probes, and debug views
- hard-to-QA surfaces such as motion, canvas, simulations, async jobs, or
  multi-service coordination
- human gates for plan approval, QA approval, deploy, spend, or destructive
  actions
- decision boundaries the agent may choose autonomously

If those answers are missing for a risky ticket, stop and make the missing
readiness explicit instead of discovering it mid-run.

## QA Policy

Use three rings:

1. Cheap per-ticket or per-row checks every time: typecheck, unit tests, narrow
   smoke checks, selector output, and ticket evidence.
2. Targeted heavy QA only for tickets with UI, data-risk, motion, async,
   multi-service, or hard-to-inspect behavior.
3. Batch or release QA after a declared milestone, not after every trivial
   ticket, when a Ralph run drained multiple related tickets.

## Judgement Questions

Use `advise` before continuing when these choices are not mechanically clear:

- should this board run serially now, or should the operator review the next
  risky ticket first?
- is a dependency truly waived, or should it block the dispatcher?
- is final batch QA enough, or does this ticket need targeted heavy QA before
  the next ticket starts?

## Top Gotchas

1. Do not revive `.ralph/`, `docs/progress.md`, `ralph_orchestrate.py`, or
   hidden queue state as live surfaces.
2. Do not bypass `$work` and call `impl-plan`, `$impl`, or `close-ticket`
   directly from Ralph except as a documented emergency fallback.
3. Do not run multiple tickets in parallel from `$ralph` v0. Parallel dispatch
   needs worktrees, leases, merge policy, stale-worker handling, and batch QA.
   The design-only reference is `skills/ralph/references/parallel-ralph.md`;
   it is not an implementation permission by itself.
4. Do not let selector output mutate tickets or launch agents directly. Policy
   belongs in this skill and ticket evidence; the helper stays read-only.
5. Do not silently fall back from `local_worktree`, `symphony`, or
   `codex_cloud` to `local_shared`. Compute blockers are operator-visible
   stops until the right runtime or external adapter exists.

## Outcome Contract

When done, the run must leave:

- each attempted ticket updated by `$work` or the downstream owning phase skill
- selector and phase evidence linked from ticket `Links` or `State` when meaningful
- per-ticket proof rows and a batch regression row when Ralph selected a batch
- a final `RALPH_RESULT` line with status, selected ticket or `none`, and stop
  reason
- follow-up tickets for discovered parallel dispatch, external board adapters,
  missing testability, or batch-QA infrastructure
