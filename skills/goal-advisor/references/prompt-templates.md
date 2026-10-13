---
title: Goal Advisor Prompt Templates
owner: goal-advisor
status: active
created_at: 2026-06-13
updated_at: 2026-10-13
---

# Goal Advisor Prompt Templates

Load this reference only after `goal-advisor` has chosen a Goal or heartbeat
branch and needs to emit prompt text. Every packet lives on one GitHub issue in
the project's own repository; `<issue>` below means `owner/repo#n`.

## Goal Architecture

```text
Goal Architecture:
Verdict: ready | revise | blocked
Issue: <owner/repo#n>
Goal program: <## Goal program, compiled_from_ticket_sha>
Current Goal state: <## Current Goal state>
Launcher comment: <**Goal launcher** comment URL or withheld>
Files:
Trigger:
Budget:
Metric / Feedback Provider:
Drift Policy:
Approval:
Heartbeat Prompt:
Native Goal Prompt:
Next Action:
```

For `revise` or `blocked`, also emit the compilation result. Do not rely on
prose such as “compilation rejected” to carry these state transitions.

```text
Verdict: ready | revise | blocked
Failed bindings: <diagram/order | stale reference | orphan reference | proof closure>
Completion Closure: supported | unsupported
Launcher: emitted | withheld
stop_complete: allowed | withheld
```

## Compilation map

```text
issue_to_goal_packet(issue body)
  intent_and_boundaries <- Summary + Scope + Delta
  execution_units <- Change Plan
  completion_scoreboard <- Done
  proof_policy <- QA Strategy
  current_state <- ## Current Goal state + Goal turn comment tail (80 lines)
  context_and_evidence <- Links + only branch-required files
  execution_path <- Contract Diagram + Change Plan + assertions
  completion_closure <- Done + QA Strategy + evidence owners
```

## Issue commands

Every `gh` call names the repository (`R=owner/repo`), so it works outside the
checkout.

```bash
# Freshness: compiled_from_ticket_sha
gh issue view <n> -R "$R" --json body -q .body | tr -d '\r' \
  | sed -e '/^## Goal program/,$d' -e 's/[[:space:]]*$//' | shasum -a 256 | cut -c1-12

# First load: the body plus the newest whole Goal turn comments within 80 lines.
# Pipe to `wc -l` for the context gate: target 300, hard 400.
gh issue view <n> -R "$R" --json body,comments -q '.body, ([.comments[]
  | select(.body | startswith("**Goal turn"))] | reverse
  | reduce .[] as $c ({n: 0, stop: false, out: []};
      ($c.body | split("\n") | length) as $l
      | if .stop or ((.n + $l > 80) and (.out | length > 0)) then .stop = true
        else .n += $l | .out = [$c.body] + .out end)
  | .out[])'

# Resume: the newest launcher comment is the run's prompt.
gh issue view <n> -R "$R" --json comments \
  -q '[.comments[] | select(.body | startswith("**Goal launcher**"))] | last | .body'

# Writeback: post the turn, then replace only the last section.
gh issue comment <n> -R "$R" --body-file turn.md
gh issue view <n> -R "$R" --json body -q .body | tr -d '\r' \
  | sed '/^## Current Goal state/,$d' > body.md
cat state.md >> body.md   # starts with "## Current Goal state"
gh issue edit <n> -R "$R" --body-file body.md
```

## Goal Packet Setup

```text
Read the whole issue once: gh issue view <n> -R "$R" --json title,body,labels,comments
Update the issue body in this order:
- ticket sections (Summary, Scope, Delta, Change Plan, Done, QA Strategy, Links)
- ## Goal program from tickets/templates/goal-loop/program.md; fold in every
  Decision: comment whose rule still binds
- ## Current Goal state from tickets/templates/goal-loop/progress.md (last)
Create .farplane/goal-advisor/issue-<n>/hypothesis-tree.json from
tickets/templates/goal-loop/hypothesis-tree.json only when the packet is
experiment-backed, and link its path from ## Goal program. On a fresh clone,
rebuild it from the Goal turn comments' selected-node receipts or return blocked.
Post one launcher comment: "**Goal launcher** · compiled_from_ticket_sha <sha>",
then the verdict and the native /goal prompt. A regenerated packet posts a new
launcher comment; the newest one wins. Approval lives only in the Goal Mode
`approval:` field of ## Goal program; the operator approves by setting it to
`approved` (directly or by telling goal-advisor), which leaves the hash intact.

Record compiled_from_ticket_sha (Issue commands) plus the approval state. Set approval: pending for material packets unless the
operator explicitly pre-approved auto-run. Do not run the native Goal until the
packet is approved. Engineering facts only: the repository is public, so
private evidence stays under .farplane/ and is described, not pasted.

For delayed Reward packets, replace the Check-In Program placeholders with the
experiment's executable evidence, scoring, decision, writeback, idempotency,
and source-gap procedure. Otherwise keep only mode: not_applicable plus a reason.
```

## Native Goal Prompt

```text
/goal Run the following issue and files as one Goal Packet.
Files:
- <owner/repo#n> (R=<owner/repo>): ticket sections + ## Goal program +
  ## Current Goal state; Goal turn comments are the progress log
- <.farplane/goal-advisor/issue-<n>/hypothesis-tree.json when the Experiment Backbone is enabled>
- <optional spec/design/board/artifact files>

Read the issue with the first-load command (goal-advisor Issue commands): the
body plus the newest whole Goal turn comments within 80 lines. Load other
comments only to resolve a named evidence gap. Context gate: the first-load
output is at most 300 lines, hard 400; above that return `revise`. First read `## Goal program`; it is the executable loop policy. Then read
the ticket sections; they are the scope, acceptance, and proof contract. Recompute
`compiled_from_ticket_sha` and compare it with `## Goal program`; on mismatch
return to `goal-advisor`. Before acting, verify that the Compiled Execution Path covers
the Contract Diagram and Change Plan, every Reference Manifest entry has a named
consumer, and every Done condition has a Completion Closure row. Return to
`goal-advisor` with `revise` when bindings are missing, contradictory, stale,
or circular; do not infer a replacement program during execution. When listed,
use `hypothesis-tree.json` as the sole research-state owner: derive eligible
leaves from parent and status, and never write a duplicate frontier, child
list, depth, or rank.

Task: Complete only the issue's `Scope: In` and `Done` conditions. Obey
`## Goal program` for trigger mode, budget, metric or feedback provider, proof
route, drift policy, after-turn routine, heartbeat or batch rules, and stop
conditions. Specs, designs, boards, and artifacts are constraints, evidence,
and context; they do not expand scope unless the ticket sections say so.
Preserve Scope, Delta, Change Plan, Done, QA Strategy, Docs Strategy, Agent
Contract, Run Hints, budget, blocker policy, and stop conditions. `Scope: Out`
wins unless the issue is updated and this packet is regenerated. Load extra
references only through the Reference Manifest for their named consumer.

Logging: Before ending each turn, post one `**Goal turn N**` comment with
observation, evidence, learning, decision, remaining_budget, and next_action,
then replace only `## Current Goal state` (Issue commands, Writeback). Never
edit `## Goal program` during the run: a needed rule change gets a `Decision:`
comment, then return `request_feedback` or go back to `goal-advisor`, which
updates `### Binding Decisions` and asks for approval again. For multi-issue Goals, comment on every issue whose state changed and
add a coordination note to the primary issue.

Metric: Satisfy the Done conditions, QA Strategy, Docs Strategy, and provider
declared in the issue. For multi-issue Goals each issue needs its own QA result;
batch proof is additional. If the ticket and program proof policies conflict,
QA Strategy wins and the packet is revised. When QA Strategy includes `qa`,
`visual_qa`, `agent_qa`, `review`, or `qa` closeout, use the delegated lane and
do not count self-certification as proof.

Final checkpoint: Before `stop_complete` on material work, run the QA evidence
review, draft the user-facing response, and run the completion review required
by QA Strategy or `## Goal program`. For a material implementation Goal, run
the `qa` closeout skill for the narrated lead-engineer recap MP4 after QA
passes and before completion review (not for heartbeats, feedback checks,
planning-only Goals, or direct work). If QA review, completion review,
`approved_response`, docs validation, or packet freshness is missing, stale, or
below the gate, stop blocked or revise. When every gate passes, post one proof
comment (what changed, commit hashes, checks run, demo video or screenshots for
UI work) and run `gh issue close <n> -R "$R" --reason completed`. Do not stop complete
while any Completion Closure row is pending, unsupported, stale, or
contradicted. Every operator screenshot complaint is a closure row keyed to the
image, complaint, design state, and viewport; it closes only with repair, newer
comparable evidence, and an independent verdict, or a recorded operator
withdrawal.

After each turn: observe -> choose_next(objective, evidence, eligible_moves,
remaining_budget) -> execute | diagnose | report_now | request_feedback | stop
-> act -> verify -> write_back. Spend budget only when the move beats the
outside options; apply `references/choose-next.md` only when several moves need
judgment. Evaluate with the declared provider before writeback. When a tree is
listed, update the selected node and bounded children first. When a result
materially misses its expectation, is implausibly strong, or looks invalid,
check evaluator and evidence integrity and allow bounded reruns only while a
concrete concern remains. Request <goal-drift-reviewer at checkpoint> or the
delegated QA/review lane when `## Goal program` requires it. For UI work, stop
complete only with the strongest screenshot as a Markdown image plus artifact
links, or a recorded blocker. The final response includes `Ticket:`,
`Execution Path:`, `Reference Manifest:`, `Completion Closure:`,
`Verification:`, `Artifacts:`, `Grounding:`, and `Residual risk:`, and states
that `stop_complete` is withheld until every closure row is supported.

Approval: Run only while `## Goal program` Goal Mode shows `approval:
approved`. If the ticket sections changed after compilation, return to
`goal-advisor`, regenerate `## Goal program` and this prompt, and ask for
approval again.
```

## Goal Turn Receipt

```yaml
observation:
evidence: []
learning:
decision: execute | diagnose | report_now | request_feedback | stop | blocked
remaining_budget:
next_action:
```

## Parent Heartbeat Prompt

```text
Inspect the following as a heartbeat Goal.
Files:
- <parent issue or board query, e.g. gh issue list -R <owner/repo> --label <label>>
- <optional child issues>

Task: Choose exactly one next action: start_goal, resume_goal, request_feedback,
replan, blocked, or no_op. For board drain, fetch proceedable issues, skip
blocked, gated, or dependency-blocked work, and select the next time- and
budget-bounded issue set.

Logging: Post one `**Goal turn N** (heartbeat)` comment on the parent issue before ending,
including no-op reasons when nothing useful can happen yet.

Metric: Preserve the listed issues' Done, QA Strategy, budget, and stop policies.

After each turn: If an executable issue set is selected, output its native Goal
prompt with an inline `Files:` list. Use `blocked` when inputs, approval,
evidence, or tools are missing. Do not create hidden automation or a competing
scheduler.
```

## Delayed Check-In Resume Prompt

```text
Resume the original experiment Goal Packet for one due check-in.
Files:
- <owner/repo#n>
- <named evidence artifacts, when any>

Matured Reward IDs: <stable reward_id values derived by Work Pulse>
Evidence refs: <refs supplied by Work Pulse or named in ## Goal program>
Current time: <pulse timestamp>

First read `## Goal program`, then execute its `Check-In Program` exactly.
Update only the supplied matured rows, preserve future and complete rows, post
the observation and decision as a Goal turn comment, replace only `## Current Goal
state`, and return `accept`, `kill`, or `monitor`. Scope and QA Strategy win on
conflict. If the program is missing, stale, not in `delayed_reward` mode, or
lacks an evidence or decision rule, record the source gap and return blocked
for Goal Advisor repair; do not invent a check-in algorithm here.
```

## Skill Improvement Goal

```text
/goal Run <owner/repo#n> as a native Goal-backed skill-improvement loop for
<target skill>, verified by <eval command/artifact, metric, or human-reviewed
artifact> while preserving <skill contract constraints>.

Files:
- <owner/repo#n>
- <.farplane/goal-advisor/issue-<n>/hypothesis-tree.json>
- <target skill SKILL.md>
- <optional references/scripts/evals files>

Task: Improve the target skill toward the metric, rubric, or feedback schema in
`## Goal program`. If no metric exists, first define the cheapest honest
feedback surface before mutating the skill.

State: `hypothesis-tree.json` is the current source/hypothesis/result state.
Derive pending leaves; do not store a tournament rank or duplicate frontier.

Logging: Update the selected tree node first, then post a Goal turn comment with
the selection and mutation receipt, changed files, verification, metric sample,
drift verdict, next action, and blockers; rewrite `## Current Goal state`.

Metric: Use the listed eval, review, or human feedback provider. Do not promote
unverified changes as accepted rules.

After each turn: Apply the program's Decision Backbone. Use the choose-next
comparison only when several eligible nodes need judgment; otherwise execute
the implied node. Change one bounded part of the skill, run the declared
evaluator, update the tree, post the receipt, then request drift review when
required. Promote only durable accepted rules: Goal mode runs the loop,
`harness` optimize mode owns eval/memory/prompt scaffolding, and `harness`
maintain mode owns accepted writeback.
```
