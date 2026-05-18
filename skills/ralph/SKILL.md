---
name: ralph
description: Serial board-draining dispatcher for prepared Codexter ticket boards. Use after specs, tickets, and plans exist when the operator wants one safe filesystem ticket at a time selected and handed to impl-plan, impl, or close-ticket until no ready work, a human gate, blocker, failed handoff, or loop limit stops the run.
tier: 3
group: coding
allowed-tools: Read, Glob, Grep, Bash
---

# Ralph

`$ralph` is the conservative autonomous board-draining surface.

It selects one eligible filesystem ticket, hands that ticket to the existing
phase skill, waits for that phase to finish, rereads the board, and repeats.
It is a dispatcher over `impl-plan`, `$impl`, and `close-ticket`; it is not a
replacement executor and it does not launch parallel agents in v0.

## Use When

- specs and tickets already exist under `tickets/TASK-*/ticket.md`
- the operator wants a prepared board drained without manually picking each
  next ticket
- tickets already carry enough `Autonomy Readiness`, proof, and blocker detail
  for unattended work to be safe

Do not use this for vague requirements, new architecture discovery, Notion or
Linear adapters, cloud runners, deploy/push/spend actions, or parallel
multi-agent dispatch.

## Workflow

1. Read `tickets/README.md`, the active tickets, `docs/MEMORY.md`, and
   `docs/TROUBLES.md` for queue and autonomy constraints.
2. Run a read-only selector pass. Prefer
   `python3 skills/ralph/scripts/select_next_ticket.py --root . --json` when
   working in this repo. The helper reads tickets through `FileTicketAdapter`
   and applies `ComputeSelector`; it reports compute blockers and setup hints
   but never mutates tickets, launches Codex, or creates worktrees.
3. Stop immediately when the selector reports no eligible ticket, a human gate,
   unresolved blockers, unresolved dependencies, or the configured loop limit.
4. If the selected ticket is `phase: planning`, run `impl-plan` for that ticket.
5. If the selected ticket is `phase: building`, run `$impl` for that ticket.
6. If the selected ticket is `phase: documenting`, run `close-ticket` for that
   ticket.
7. After each phase, reread the board and repeat from selector, never from stale
   transcript memory.
8. End with a compact result line:
   `RALPH_RESULT: status=<stopped|blocked|loop_limit|failed|complete> selected=<ticket|none> reason=<why>`.

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
  - `planning` -> `impl-plan`
  - `building` -> `$impl`
  - `documenting` -> `close-ticket`
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
- the selected phase skill fails or returns a revise/block result
- the loop reaches the operator-specified maximum iteration count
- QA risk is too high for the available proof surfaces

## Autonomy Readiness

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

1. Cheap per-ticket checks every time: typecheck, unit tests, narrow smoke
   checks, selector output, and ticket evidence.
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
2. Do not run multiple tickets in parallel from `$ralph` v0. Parallel dispatch
   needs worktrees, leases, merge policy, stale-worker handling, and batch QA.
   The design-only reference is `skills/ralph/references/parallel-ralph.md`;
   it is not an implementation permission by itself.
3. Do not let selector output mutate tickets or launch agents directly. Policy
   belongs in this skill and ticket evidence; the helper stays read-only.
4. Do not silently fall back from `local_worktree`, `symphony`, or
   `codex_cloud` to `local_shared`. Compute blockers are operator-visible
   stops until the right runtime or external adapter exists.

## Outcome Contract

When done, the run must leave:

- each attempted ticket updated by its owning phase skill
- selector and phase evidence linked from ticket `Evidence` when meaningful
- a final `RALPH_RESULT` line with status, selected ticket or `none`, and stop
  reason
- follow-up tickets for discovered parallel dispatch, external board adapters,
  missing testability, or batch-QA infrastructure
