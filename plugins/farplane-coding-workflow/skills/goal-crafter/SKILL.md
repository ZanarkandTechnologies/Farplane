---
name: goal-crafter
description: Turn fuzzy operator intent into a strong Codex /goal command with an auditable outcome, verification surface, constraints, boundaries, iteration policy, and blocked stop condition. Use before activating Goal mode when the task should continue across turns but the completion contract is not yet crisp.
tier: 2
source: local
version: 0.1.0
allowed-tools: Read, Glob, Grep
---

# Goal Crafter

## Context

`goal-crafter` turns a rough desire into one compact native Codex `/goal`
prompt.

Use it when the operator wants Codex to keep working toward an outcome across
turns, but the completion contract still needs sharper proof, boundaries,
iteration policy, or blocked-stop behavior.

Do not use it for a one-line edit, a simple answer, a normal code review, or
work that already has a precise `/goal`.

Use `$work` when Farplane still needs to decide how to execute one request,
ticket, ticket batch, board-selected unit, epic, or metric loop. Use `$ralph`
when the task is already decomposed into prepared filesystem tickets and the
operator wants board context and drain selection.

`goal-crafter` is not a deep interview surface. When a ticket, plan, or Proof
Contract already exists, compile the known state first and ask only for missing
execution-safety fields. Route broad product discovery, unclear system
boundaries, or unknown user value to PRD, `deep-interview`, or
`deep-system-design` before drafting a Goal.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Important Checklist

- [ ] Read the operator ask and identify whether it needs a native `/goal`,
  normal prompt, ticket workflow, or `$ralph` board drain.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) when the goal
  depends on current docs, repo behavior, source evidence, or tool capability.
- [ ] Identify the desired end state, specific evidence, constraints, allowed
  inputs/tools/boundaries, iteration policy, blocked report, and optional
  budget.
- [ ] For skill-improvement goals, require the Goal to read the target skill's
  `self-improve/program.md`, evals, latest results, failure analysis, prompt
  candidates, and prior run notes when present; use those files as Goal
  context rather than creating a separate loop runner.
- [ ] When an existing ticket, plan, or Proof Contract exists, compile those
  fields into `GoalPrepState` before asking questions.
- [ ] Ask only missing execution-safety questions that materially affect the
  goal contract; cap the ask at 3 questions and otherwise proceed from the
  ticket evidence.
- [ ] Reject proxy-only completion evidence unless it satisfies the actual
  objective; label proxy, partial, and blocked evidence separately.
- [ ] Use [advise](../advise/SKILL.md) only when multiple goal framings are
  genuinely viable; otherwise emit the best goal directly.
- [ ] Prefer native `/goal` for evidence-based continuation; use `$ralph` only
  for prepared filesystem tickets that should drain through board context.
- [ ] Use `$work` in the Goal when Farplane must decide
  direct work, planning, implementation, batching, reslicing, compute, or proof.
- [ ] For ticket-batch Goals, require one proof row per ticket plus one
  batch-level regression row.
- [ ] Do not write a Goal that only says "improve", "fix", or "make better"
  without a verification surface.
- [ ] Do not let Goal mode bypass human-owned boundaries such as destructive
  operations, publishing, deployment, billing, credential provisioning, or
  materially branching product decisions.
- [ ] Output according to the template below.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Goal Contract

A strong goal should include:

- `Desired end state`: what should be true when done
- `Specific evidence`: how Codex proves completion
- `Constraints`: what must not regress or be crossed
- `Allowed inputs, tools, or boundaries`: where Codex may operate
- `Iteration policy`: how Codex chooses the next useful action after each
  result
- `Blocked report`: what Codex reports when no valid path remains, including
  attempted paths, evidence, safe options, recommended next action, and the one
  missing input that would unlock progress
- `Budget`: optional turn/time/spend limit when relevant

For skill-improvement work, native Goal mode is the durable loop runner. Draft
the Goal so it reads the target skill package plus any `self-improve/`
context, optimizes toward `program.md`, uses `$self-improve` only for
eval/memory/prompt scaffolding, and uses `$skill-maintenance` for accepted
writeback into `SKILL.md`, references, or plugin/source copies.

For ticket-backed work, use `GoalPrepState` as a field-gathering aid before
emitting the single `/goal` template:

```text
GoalPrepState {
  objective: string
  metric: string | "none mechanical"
  validation: string[]
  done: string[]
  non_goals: string[]
  constraints: string[]
  current_state: string[]
  next_action: string
  proxy_rejects: string[]
  blocked_stop: string
  questions: string[]
}
```

Fill the template from `GoalPrepState`:

- `desired end state`: `objective` plus `done`
- `specific evidence`: `validation` plus `metric`
- `constraints`: `constraints`, `non_goals`, and `proxy_rejects`
- `allowed inputs, tools, or boundaries`: ticket/operator boundaries
- `iteration policy`: `next_action` plus how Codex should choose after each
  result
- `blocked report`: `blocked_stop` plus unresolved `questions`

Question policy:

- Ask when the answer changes safety, scope, verification, spend, destructive
  boundaries, or irreversible external side effects.
- Do not ask for fields already present in the ticket body, Proof Contract,
  linked plan, or operator message.
- Do not ask broad interview questions just because the goal could be richer.
- If more than 3 fields are missing, ask the 3 that affect execution safety
  most and mark the rest as assumptions.

## Template

```text
/goal <desired end state> verified by <specific evidence> while preserving
<constraints>. Use <allowed inputs, tools, or boundaries>. Between iterations,
<how Codex should choose the next best action>. If blocked or no valid paths
remain, <what Codex should report and what would unlock progress>.
```

If several framings are genuinely viable, use `advise` first, then emit the
recommended goal using this template.

## Skill Improvement Template

```text
/goal Improve <target skill> as a native Goal-backed skill-improvement loop,
verified by <eval command/artifact, metric, or human-reviewed artifact> while
preserving <skill contract constraints>. Read the target skill package,
including `SKILL.md`, references, scripts, and `self-improve/` context when
present: `program.md`, evals, latest results, failure analysis, prompt
candidates, and prior run notes. Optimize toward the metric, rubric, or human
feedback schema defined in `program.md`; if no metric exists, first define the
cheapest honest feedback surface before mutating the skill. Use Goal mode as
the durable loop runner, `$self-improve` only for eval/memory scaffolding, and
`$skill-maintenance` for accepted writeback. Between iterations, change one
bounded part of the skill, verify it, record the lesson, and promote only
durable accepted rules. If blocked or no valid paths remain, report attempted
paths, evidence gathered, safe options considered, the recommended next action,
and the one missing input.
```

## Examples

Bad:

```text
/goal Improve performance.
```

Good:

```text
/goal Reduce checkout p95 latency below 120 ms, verified by the existing
`npm run bench:checkout` report and unchanged `npm test` results, while
preserving public API behavior. Use local source, tests, package scripts, and
benchmark output only. Between iterations, fix the largest measured bottleneck
that does not violate the tests. If blocked or no valid paths remain, report
the attempted optimizations, benchmark evidence, safe options, recommended next
action, and the one missing input that would unlock progress.
```

Bad:

```text
/goal Finish this ticket.
```

Good:

```text
/goal Complete TASK-123 using its Proof Contract, verified by the listed test
commands, required evidence artifacts, and final review result, while
preserving the ticket's Scope Out and repo guardrails. Use the ticket body,
linked plan, local repo files, and approved tools. Between iterations, choose
the next action from the latest failing proof or missing acceptance criterion.
If blocked or no valid paths remain, record attempted paths, gathered evidence,
safe options, recommended next action, and the one missing input.
```

Bad:

```text
/goal Research the topic.
```

Good:

```text
/goal Produce an evidence-backed answer to <question>, verified by a claim
inventory mapping each important claim to source evidence or local proof, while
labeling unsupported claims separately. Use official docs, local code, and
current web sources as needed. Between iterations, pursue the highest-risk or
least-supported claim first. If blocked or no valid paths remain, report the
missing evidence, checked sources, remaining uncertainty, recommended next
query, and the one missing input.
```
