---
title: Ticket Reflection And Proof Surface Decision Note
status: draft
owner: codex
created_at: 2026-06-22
context_ref: experiments/decisions/2026-06-22-ticket-reflection-progress/context.md
skill: deliberative-advice
---

# Ticket Reflection And Proof Surface Decision Note

## Decision

Use `progress.md` as the default ticket-local reflection, decision, and
execution log.

Keep proof under `tickets/TASK-XXXX/artifacts/` by default.

Add `decisions.md` only as an optional escape hatch for material branching
decisions, council outputs, or durable rationale that would make `progress.md`
hard to scan.

Do not put decision bodies in ticket frontmatter or `program.md`.

## Stakes

The operator wants Farplane to stay lean. Ticket directories already act like
mini isolated workspaces. Native Goals need a place to record reflection and
after-turn observations, but too many sidecar files create paperwork and
duplicate state.

## Grounding

Current repo contracts already define:

- `ticket.md`: task contract, proof scoreboard, blockers, links, next action.
- `program.md`: optional Goal loop configuration.
- `progress.md`: optional append-only observed execution and after-turn log.
- `artifacts/`: ticket-local proof, QA, review, evals, prompts, screenshots,
  reports, and bulky evidence.

The active ticket scan shows existing use of `program.md`, `progress.md`, and
`artifacts/`, but no current `decisions.md` convention.

## Perspectives

### Operator Value

One obvious resume path is best: `ticket.md` says what matters now,
`progress.md` says what happened and why, and `artifacts/` holds proof.

### Engineering Risk

Default `decisions.md` adds file sprawl and migration burden. Optional
`decisions.md` is useful only when a ticket has enough branching rationale to
justify a curated record.

### Evidence Skeptic

Current evidence supports the existing ticket plus progress plus artifacts
shape. A default `decisions.md` would be speculative until real tickets show
lost rationale or bloated progress logs.

### Systems Fit

This preserves ownership boundaries:

- `ticket.md` is contract and scoreboard.
- `program.md` is loop config.
- `progress.md` is observed execution and reflection.
- `artifacts/` is proof/evidence.
- optional `decisions.md` is curated durable rationale.

### Native Goal Fit

Native Goal needs after-turn logging: intent, actions, evidence, drift verdict,
next action, blocker/stop reason, and completion entry. `progress.md` already
matches that requirement.

## Critique / Ranking

### Option 1: `progress.md` Default, Optional `decisions.md`

Recommended.

It keeps the common path lean while preserving an escape hatch for real
architecture/council decisions.

### Option 2: One `progress.md` Only

Leanest and easiest to teach, but risks burying material rationale in long
chronology when a ticket has multiple hard choices.

### Option 3: Default `decisions.md`

Clean for retrieval, but premature. It creates another file on every ticket
without current evidence that most tickets need it.

## Recommendation

Adopt this policy:

```text
ticket.md
  -> contract + scoreboard + links + next_action

program.md
  -> Goal/run configuration only

progress.md
  -> append-only execution log + reflection + compact decision entries

artifacts/
  -> proof + bulky evidence + review + QA + evals + screenshots + reports

decisions.md
  -> optional curated rationale for material branching choices
```

## Dissent

The strongest dissent favors a default `decisions.md` because it makes
important rationale easier to scan and UI-render as a separate collection.

That becomes persuasive if resumed Goals or reviewers repeatedly miss decisions
buried in `progress.md`, or if future portal work needs a stable decision index
that cannot be derived from structured progress entries.

## Tradeoff Accepted

Farplane accepts that routine decisions live in chronology. In exchange, most
tickets stay small and obvious.

The escape hatch is explicit: when decisions become material enough to deserve
curation, create `decisions.md` and link it from `ticket.md` or a progress
entry.

## Confidence

High for proof staying ticket-local under `artifacts/`.

Medium-high for `progress.md` as the default reflection/decision log.

Medium for whether UI needs will eventually justify more frequent
`decisions.md`.

## Policy Constraints

- Do not create empty sidecar files by default.
- Do not put bulky decision text in frontmatter.
- Frontmatter may carry `decision_refs` only if needed.
- `program.md` must not become a progress log or decision journal.
- `progress.md` entries should be compact, append-only, and reconstructable.
- No raw transcript in tracked logs.
- Proof defaults to `tickets/TASK-XXXX/artifacts/`.
- Completion proof must leave a ticket-local evidence pointer and a final
  `progress.md` completion entry when a Goal Packet exists.
- Archive ticket, progress, optional decisions, and artifacts together as one
  workspace.

## Suggested `progress.md` Entry Shape

```md
## 2026-06-22T08:00:00Z

- Trigger: native_goal_turn
- Intent: tighten ticket reflection/proof policy
- Actions: read ticket and Goal contracts; ran council lanes
- Decision: use progress.md as default reflection log; decisions.md optional
- Evidence: artifacts/council-summary.md
- Drift: aligned
- Next: update ticket/docs if accepted
```

## Suggested `decisions.md` Threshold

Create `decisions.md` only when one is true:

- there are 2-3+ material branching decisions in one ticket;
- a council decision needs a stable curated record;
- an architecture/API/data-model choice needs future audit;
- the decision affects multiple tickets or future skills;
- reviewers or resumed agents would likely miss the rationale in chronology.

## Next Owner

If accepted, create a cleanup ticket to update:

- `tickets/README.md`
- `docs/specs/goal-loop-contract.md`
- `tickets/templates/goal-loop/progress.md`
- any proof path defaults that still point to global `.farplane/results` as
  durable proof rather than runtime output.
