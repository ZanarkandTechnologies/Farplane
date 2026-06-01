---
name: goal-crafter
description: Turn fuzzy operator intent into a strong Codex /goal command with an auditable outcome, verification surface, constraints, boundaries, iteration policy, and blocked stop condition. Use before activating Goal mode when the task should continue across turns but the completion contract is not yet crisp.
tier: 2
source: local
version: 0.1.0
allowed-tools: Read, Glob, Grep
---

# Goal Crafter

<!-- BEGIN CODEXTER_IMPORTANT_CHECKLIST -->
## Important Checklist

Source: `SKILL.md`

- [ ] Read the operator ask and identify whether it needs a native `/goal`,
  normal prompt, ticket workflow, or `$ralph` board drain.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) when the goal
  depends on current docs, repo behavior, source evidence, or tool capability.
- [ ] Use [advise](../advise/SKILL.md) when multiple goal framings are viable.
- [ ] Draft the goal with outcome, verification surface, constraints,
  boundaries, iteration policy, blocked stop condition, and optional budget.
- [ ] Ensure the blocked stop condition requires attempted paths, evidence,
  safe options, recommended next action, and the one missing user input.
- [ ] Prefer native `/goal` for evidence-based continuation; use `$ralph` only
  for prepared filesystem tickets that should drain through board context.
- [ ] Use `$work` in the Goal when Codexter must decide
  direct work, planning, implementation, batching, reslicing, compute, or proof.
- [ ] For ticket-batch Goals, require one proof row per ticket plus one
  batch-level regression row.
- [ ] Return a paste-ready `/goal` command and short use notes.
<!-- END CODEXTER_IMPORTANT_CHECKLIST -->

`goal-crafter` turns a rough desire into a strong native Codex `/goal`.

Use it when the operator wants Codex to keep working toward an outcome across
turns, but the prompt still needs a clearer finish line, proof surface,
autonomy boundary, or blocked-stop contract.

Do not use it for a one-line edit, a simple answer, a normal code review, or
work that already has a precise `/goal`.

## Mental Model

`/goal` is the preferred continuation surface for evidence-based, multi-turn
work.

Use `$work` when the operator needs Codexter to decide how to execute one
request, ticket, ticket batch, board-selected unit, epic, or metric loop. Use
`$ralph` when the task is already decomposed into prepared filesystem tickets
and the operator wants board context and drain selection. Use `goal-crafter`
when the problem is a fuzzy finish line, insufficient proof, batch
testability, board-drain durability, or "figure it out" autonomy within one
native Codex Goal.

## Workflow

1. Restate the operator's desired outcome in one sentence.
2. Identify the proof surface: test, benchmark, build, report, artifact,
   screenshot, local command, source evidence, or claim inventory.
3. Name constraints that must stay intact: behavior, API, budget, scope,
   safety, style, data, or no-regression rules.
4. Name boundaries: allowed files, tools, repos, online research, credentials,
   external services, write permissions, and publish/deploy/spend limits.
5. Define the iteration policy: how Codex should choose the next attempt after
   each result, including when to use `advise` for tradeoffs.
6. Define the blocked stop condition: what evidence must be gathered before
   stopping, what options were considered, and what single input would unlock
   progress.
7. Draft one `/goal` command. Keep it compact enough to paste, but complete
   enough to audit.
8. If the task is too vague to verify, propose exactly 3 viable goal framings,
   recommend one, and ask only for the missing detail that cannot be inferred.

## Goal Contract

A strong goal should include:

- `Outcome`: what should be true when done
- `Verification surface`: how Codex proves it
- `Constraints`: what must not regress
- `Boundaries`: where Codex may operate
- `Iteration policy`: how Codex chooses the next useful action
- `Blocked stop condition`: when stopping is honest and what must be reported
- `Budget`: optional turn/time/spend limit when relevant

## Codexter Goal Templates

### One Ticket

```text
/goal Complete <ticket> using `$work`. Classify the execution profile, run
`impl-plan` only if material planning is needed, then execute through the
owning Codexter skill. Stop only when the ticket is complete with required
proof/review evidence, or when a blocker is recorded with attempted paths,
evidence gathered, safe options considered, the recommended next action, and
the single missing input.
```

### Ticket Batch

```text
/goal Complete this related ticket batch using `$work` or `batch-work`.
Maintain a batch ledger with one row per ticket: change, local proof, result,
evidence path, and blocker. Run one batch-level regression check before
claiming completion. Stop only when every ticket row is passed or blocked with
evidence and the batch regression row is passed or explicitly blocked.
```

### Board Drain

```text
/goal Drain the prepared ticket board using `$ralph`. After each selected work
unit or batch, reread the board. Use `$work` for execution admission. Stop only
when no eligible unblocked tickets remain, or every remaining ticket is
complete, archived, approval-gated, or blocked with evidence.
```

### Metric Loop

```text
/goal Improve <metric> for <scope>, verified by <verify command/artifact> and
guarded by <guard command/artifact>. Use autoresearch only while the metric,
direction, guard, and iteration budget remain valid. Stop when the target is
met, the budget is exhausted with the best attempt recorded, or a blocker is
recorded with evidence and the recommended next action.
```

### Figure-It-Out Unblock

```text
/goal Resolve <task> without stopping for weak ambiguity. Before reporting a
blocker, inspect the local code/docs/errors, try at least one safe fallback,
and use advise when multiple viable paths remain. Stop with a blocker only
after recording attempted paths, evidence gathered, options considered, the
recommended next action, and the one user input that would unlock progress.
```

## Output Shape

Return:

```text
Recommended /goal:
<paste-ready goal>

Why this goal is strong:
- outcome:
- verification:
- constraints:
- boundaries:
- iteration:
- blocked stop:

Use notes:
- <short notes, only when needed>
```

When several framings are viable, use:

```text
Decision:
<one sentence>

Options:
1. <goal framing> - pros / cons
2. <goal framing> - pros / cons
3. <goal framing> - pros / cons

Recommendation:
<chosen framing and why>

Recommended /goal:
<paste-ready goal>
```

## Examples

Fuzzy side-project ask:

```text
I want Codex to make this demo work. I do not care about perfect architecture.
If blocked, it should figure out a safe path and keep going.
```

Draft:

```text
/goal Make the side-project demo run end-to-end locally, verified by launching the app and completing the primary demo flow without runtime errors. Preserve existing setup unless a small reversible change is needed. Use local files, package scripts, logs, docs, and web research when dependencies or APIs are unclear. Between iterations, choose the next safest fix from the latest error or missing proof, and use advise when multiple viable paths remain. If blocked, stop only with attempted paths, evidence gathered, safe options considered, the recommended next action, and the one user input that would unlock progress.
```

Research ask:

```text
/goal Produce the strongest evidence-backed answer to <question>, verified by a claim inventory that maps each claim to source evidence or local proof. Use official docs, local code, and current web sources as needed. Between iterations, pursue the highest-uncertainty claim first. If exact proof is unavailable, label support-only evidence and blocked claims separately instead of flattening them into success.
```

Deterministic local ask:

```text
/goal Make the current branch pass `npm test`, verified by a clean test run, while preserving public API behavior. Use local source, tests, and package scripts only. Between iterations, fix the next failing test or setup issue shown by the latest output. If the test runner cannot execute, stop with the command output, attempted fixes, and the missing local dependency.
```

## Core Decision Branches

- **Clear proof exists:** write one paste-ready `/goal`.
- **Proof is fuzzy:** convert it to a report, artifact, command, screenshot, or
  claim inventory before drafting.
- **Several paths are valid:** use `advise` to compare 3 goal framings and name
  the best one.
- **Task is tiny:** recommend a normal prompt instead of `/goal`.
- **Task needs ticketed build/QA/review:** draft a goal that hands off to the
  ticket workflow rather than replacing `impl-plan`, `$impl`, QA, or review.
- **Task needs work sizing first:** draft a goal that invokes `$work` so
  Codexter can choose direct work, `impl-plan`, `$impl`, `batch-work`,
  `$ralph`, reslicing, or autoresearch.
- **Ticket batch:** require per-ticket proof rows plus one batch regression row.
- **Only a deterministic command or marker matters:** recommend a normal prompt
  or explicit command instead of a Goal.

## Top 3 Gotchas

1. Do not write a Goal that only says "improve", "fix", or "make better"
   without a verification surface.
2. Do not hide uncertainty. If exact proof may be unavailable, define how proxy
   evidence, partial success, blocked claims, and remaining uncertainty should
   be labeled.
3. Do not let Goal mode bypass human-owned boundaries such as destructive
   operations, publishing, deployment, billing, credential provisioning, or
   materially branching product decisions.

## Judgement Questions

Use `advise` when these are not mechanically obvious:

- Which outcome is the real user value?
- Which verification surface is cheapest and honest?
- Which constraints are essential versus preference?
- Which boundaries should be strict for this repo or project?
- What should count as a real blocker rather than a weak failure message?

## Outcome Contract

At the end, the operator has either:

- one paste-ready `/goal` command, or
- 3 viable goal framings with a clear recommendation and the smallest missing
  detail needed before activation.
