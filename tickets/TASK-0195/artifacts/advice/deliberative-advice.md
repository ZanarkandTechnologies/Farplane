---
title: "Deliberative Advice: Direct Lesson/Trouble Logging"
status: draft
owner: TASK-0195
created_at: 2026-06-12
updated_at: 2026-06-12
tags:
  - self-improvement
  - hooks
  - lessons
  - troubles
refs:
  - tickets/TASK-0195/ticket.md
  - docs/specs/self-improvement-contracts.md
  - docs/specs/filesystem-lifecycle.md
  - docs/features/registry.jsonl#FEAT-0012
  - docs/features/registry.jsonl#FEAT-0039
---

# Deliberative Advice: Direct Lesson/Trouble Logging

## Decision

Should the revived repent-style feature spawn a bounded reviewer agent every N
turns, inspect the past 10 turns, detect troubles and lessons, pair resolved
cases, and write directly to `docs/TROUBLES.md` and `docs/LESSONS.md`?

## Recommendation

Yes. The feature should be direct file logging in the hot path, plus a weekly
drain that calls `optimize-harness` for logged issues that need actual harness
changes.

The clean product contract is:

```text
every_n_turns(window, docs)
  -> trouble_append | lesson_append | pair_resolved_case | no_change
```

The hook owns cadence and launch. The reviewer agent owns judgment and writes.
`optimize-harness` is not part of the every-N-turn logging path; it belongs in a
weekly drain over `docs/TROUBLES.md` and `docs/LESSONS.md`.

## Grounding

Current state:

- `bin/user_turn.py` already stores bounded rolling windows; the implemented
  revamp should use the flatter `.farplane/state/message-windows/` path while
  reading legacy `.farplane/state/self-improve/windows/` state.
- `bin/stop_hook.py` already has a `skill-opportunity-review` hooklet and a
  default 10-turn cadence.
- `agents/skill-opportunity-applier.toml` is still Notion-task oriented and
  assumes a sidecar proposal path.
- `docs/specs/filesystem-lifecycle.md` defines `docs/TROUBLES.md` as the raw
  pain log and `docs/LESSONS.md` as the distilled learning log.
- `deep-init-project` already scaffolds `docs/TROUBLES.md` and
  `docs/LESSONS.md`, so it is the right bootstrap owner for a weekly drain
  habit.
- `docs/features/registry.jsonl` has the old gated skill-opportunity applier
  (`FEAT-0012`) and the newer behavior-correction loop (`FEAT-0039`), so this
  should be a revamp of the existing hooklet rather than a new public `repent`
  skill.

Runtime limitation for this deliberation: no native subagents were spawned
because the operator did not explicitly request subagents. Perspectives below
are isolated local council passes, not independent agent runs.

## Perspectives

### Operator Value

The direct logging model is the right feature. The operator expectation is not
"capture something for a later optimizer." It is "every 10 turns, check what
just happened and write the learning files."

The learning files are the product surface:

- `docs/TROUBLES.md` for raw repeated misses, blockers, and correction pain.
- `docs/LESSONS.md` for distilled prevention lessons.

If the agent only writes an inbox, the feature can feel dead again. If it writes
the files directly, the learning loop is visible and immediately useful.

### Engineering Risk

The dangerous version is deterministic hook code trying to classify lessons.
The acceptable version is a bounded reviewer agent with a strict write contract.

The hook should only decide:

```text
is_due(window, cadence, hints) -> launch_reviewer | skip
```

The reviewer should decide:

```text
review_recent_turns(window, recent_troubles, recent_lessons)
  -> append_trouble | append_lesson | pair | no_change
```

This avoids putting model judgment into hook code while still letting the model
write canonical docs.

### Evidence Skeptic

Direct docs writes are acceptable only if the reviewer is constrained:

- no raw transcripts
- compact sanitized evidence only
- dedupe against recent entries
- pair a lesson with a trouble when the trouble was resolved
- return `no_change` for weak or ambiguous signals
- write only `docs/TROUBLES.md` and `docs/LESSONS.md`

The proof should be fixture based: feed synthetic 10-turn windows and assert the
expected doc delta or no-op.

### Systems Fit

This belongs in existing hook/runtime and agent surfaces:

- `bin/user_turn.py`: rolling windows
- `bin/stop_hook.py`: cadence and launch
- `agents/skill-opportunity-applier.toml`: repurpose from Notion proposal agent
  to local learning reviewer, or add a clearer replacement role
- `bin/self_improve_hook_probe.py`: simulate and dry-run doc deltas
- `docs/TROUBLES.md` / `docs/LESSONS.md`: canonical outputs

It does not need `optimize-harness` in the hot path. `optimize-harness` is for
the weekly drain after learning has been logged.

## Options

### Option A: Hook Code Writes Docs Directly

Pros:

- Very simple runtime.
- No sidecar launch dependency.

Cons:

- Puts judgment in deterministic hook code.
- Hard to sanitize, dedupe, and pair lessons well.
- More likely to produce bad memory.

Rank: 3.

### Option B: Every-N-Turn Reviewer Agent Writes Docs Directly

Pros:

- Matches the intended feature.
- Produces visible learning immediately.
- Lets the reviewer pair resolved troubles and lessons.
- Keeps the hook deterministic.
- Avoids an `optimize-harness` call in the every-N-turn hot path.
- Pairs naturally with a weekly `optimize-harness` drain for actual fixes.

Cons:

- Needs reliable sidecar launch.
- Needs idempotence and dedupe tests.
- Needs strict write boundaries.

Rank: 1.

### Option C: Inbox First, Later Drain

Pros:

- More robust if sidecar launch fails.
- Lower risk of noisy docs.

Cons:

- Adds a second step the operator does not want.
- Can become another dead backlog.
- Does not satisfy "just log into the files."

Rank: 2 as a fallback artifact only, not the primary feature.

### Weekly Drain Add-On

This is not a competing option; it is the natural second layer:

```text
weekly_learning_drain(docs/TROUBLES.md, docs/LESSONS.md)
  -> optimize-harness(issue) | no_change
```

`deep-init-project` should set this up for new projects because it already
creates the memory/troubles/lessons surfaces. The weekly drain reads recent
entries, selects items that imply a harness fix, eval, ticket, skill change, or
prompt change, and then calls `optimize-harness` with those issues.

## Final Recommendation

Implement Option B.

The reviewer agent should be treated as CRUD over two files:

```text
LearningReview(window, docs) -> DocsDelta

DocsDelta:
  trouble_appends: TroubleRow[]
  lesson_appends: LessonRow[]
  pairings: Pairing[]
  no_change_reason?: string
```

Write policy:

- trouble rows go to `docs/TROUBLES.md`
- lesson rows go to `docs/LESSONS.md`
- pairings should reference the related trouble row in the lesson source or
  note field
- weak signals produce `no_change`
- broader repairs become ordinary follow-up work after logging, not part of the
  reviewer loop
- weekly drain sends selected logged issues to `optimize-harness`

## Tradeoff Accepted

Accept bounded canonical docs writes by a spawned reviewer agent.

This trades some noise risk for a much more alive learning loop. The guardrail
is not "send every 10-turn review to optimize-harness"; the guardrail is a
narrow reviewer contract, dry-run fixture tests, dedupe, pairing, write limits,
and a weekly drain for actual improvements.

## Next Owner

Primary owner: `TASK-0195`.

Implementation owners:

- `bin/user_turn.py` for rolling-window access helpers
- `bin/stop_hook.py` for cadence and reviewer launch
- `agents/skill-opportunity-applier.toml` or a replacement learning-reviewer
  role for direct local docs logging
- `bin/self_improve_hook_probe.py` for simulate/status/dry-run doc deltas
- `bin/test_stop_hook.py` for disabled/not-due/due/idempotence coverage
- `docs/specs/self-improvement-contracts.md` for the reviewer contract if the
  broader self-improvement spec is revised
- `skills/deep-init-project/SKILL.md` for the weekly drain setup
- `docs/features/registry.jsonl` for feature status

## Proof

Required proof:

- simulate 10 turns and show proposed `docs/TROUBLES.md` /
  `docs/LESSONS.md` deltas
- prove not-due windows do not launch the reviewer
- prove disabled mode does not write docs
- prove hook code itself does not perform docs judgment
- prove reviewer output is idempotent
- prove weak windows return `no_change`
- prove resolved trouble/lesson pairs are linked
- prove weekly drain guidance exists for troubles/lessons to optimize-harness
- run ticket metadata and diff checks
