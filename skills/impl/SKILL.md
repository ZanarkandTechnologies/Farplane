---
name: impl
description: Build-phase orchestrator for one selected ticket. Runs ephemerally, coordinates builder/reviewer/QA/evidence-check lanes, and hands results back to the Stop hook.
tier: 3
group: coding
source: local
common_chains:
  after: ["qa"]
---

# Impl

`$impl` is the build-phase orchestration surface for Codexter.

`$impl` is a Tier 3 Codexter coding-pipeline skill. It implements the generic
[execute](../execute/SKILL.md) interface for code tickets; it is not the
universal Tier 2 execution interface for every application domain.

Use it when:

- planning for a ticket is already complete
- the selected ticket should be attempted end-to-end rather than downscoped
  into an internal "part 1"
- one ticket should move through implementation and, when required, internal `qa` and `demo` subphases
- the same ticket may need repeated build/review/fix passes until proof is good enough
- the operator wants visible worker lanes instead of a hidden forever-running orchestrator

Do not use it when:

- the request is still ambiguous; use `brainstorm`, `deep-interview`, or `prd`
- the selected ticket still needs architecture/test-shape planning; use `impl-plan`
- the task is already small enough for direct solo implementation

## Contract

- `$impl` owns one selected ticket/work package at a time.
- `$impl` treats the selected ticket as the execution unit for the run. Builder,
  review, and QA passes may iterate, but the target is whole-ticket completion
  unless a blocker or explicit follow-up ticket makes narrower scope real.
- An explicit ticket selector outranks ambient runtime state.
- `$impl` reads the ticket plus linked specs/docs, launches the needed worker lanes, integrates their outputs, writes progress back to the ticket/progress surface, and exits.
- `$impl` reads the ticket `Proof Contract` before execution. The contract
  defines the metric targets, review rubric gates, hard gates, and required
  evidence that the run must satisfy.
- `$impl` is the public execution surface; `qa` and `demo` may run as internal subphases or explicit recovery surfaces.
- Delegated lanes should expose a small shared contract: `worker_name`, `main_artifact_path`, and a short `grounding_summary`.
- `$impl` does not require or create a permanent orchestrator pane.
- Worker panes are the primary visible runtime surface.

## Default Worker Shape

For a selected build ticket, `$impl` should coordinate:

1. builder lane for implementation and local validation
2. reviewer lane for rubric-based review
3. QA lane for evidence gathering
4. optional `autoresearch-exec` lane when the ticket links an autoresearch
   session in its `Proof Contract`
5. evidence-check lane for validating the QA evidence

Default enforced runtime set today:

- `builder`
- `reviewer`
- `qa`

`evidence-check` stays optional until it has a real agent/runtime implementation.

The orchestrator remains singular: worker lanes do not mutate queue state or claim completion on their own.

## Execution Subphases

Inside `status: building`, the runtime may progress through:

1. `impl`
2. `qa`
3. `demo`

The Stop hook should continue the same ticket until the required subphase artifacts exist.

## Selection Rules

- Prefer an explicit ticket path or ticket id from the invocation.
- If no explicit selector is provided, fall back to the current active ticket only when the surrounding run state is unambiguous.
- Do not silently jump to another ready ticket while a selected ticket is still active.

## Stop-Hook Re-entry

- Stop-hook and judge outputs remain the continuation/completion gate.
- When the verdict says repeat the same build work, the follow-up instruction should re-enter the same `$impl` contract for that ticket.
- Re-entry should reuse the existing verdict fields and `orchestrator_message`; do not invent a second continuation artifact.
- Former persistence-loop behavior now lives here: repeated same-ticket execution is a normal `$impl` re-entry path, not a separate public skill.

## Operator UX

- The operator should be able to see which ticket `$impl` selected.
- The operator should be able to see which worker lanes were launched.
- The operator should be able to recover by re-running `$impl` for the same ticket using the ticket plus the latest written evidence/handoff.

## Tmux Helper

When tmux-backed visible lanes are needed, `$impl` may use:

- `skills/impl/scripts/tmux_helper.py`

That helper is tmux/session plumbing only. It must not own orchestration
policy, queue selection, or review logic.

Reference:

- `skills/impl/references/tmux-runtime.md`
- `skills/impl/references/stop-hook-routing.md`

## Guardrails

- Keep the ticket as the canonical progress surface.
- Keep the ticket `Proof Contract` as the run scoreboard. Do not invent new
  metrics, rubric gates, or evidence obligations in lane prompts when the
  ticket already declares them; update the ticket if the contract is wrong.
- Aim to land the whole selected ticket; do not voluntarily turn a coherent
  ticket into an arbitrary "first slice" just because partial progress is
  easier to claim.
- Keep the delegated main artifact explicit instead of relying on transcript memory.
- Keep QA and review separate.
- Keep the orchestrator ephemeral.
- Keep one canonical public execution surface: `$impl`.
- Reuse existing hook verdicts instead of adding a parallel control plane.
- Run `autoresearch-exec` only when the ticket points to an existing
  autoresearch session or the approved plan explicitly created one; ordinary
  tickets should satisfy their Proof Contract through normal build, QA, and
  review.
- Leave board-wide dispatch, worktree orchestration, and binary/runtime cleanup to separate tickets.
