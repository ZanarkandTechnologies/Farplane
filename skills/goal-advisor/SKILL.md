---
name: goal-advisor
description: "Turn an ambitious request into Goal architecture, ticket-backed loop state, and a native Codex /goal prompt when warranted."
tier: 3
group: harness
source: local
version: 0.2.0
skill_template_version: "0.2.0"
feature_refs:
  - FEAT-0029
  - FEAT-0046
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Goal Advisor

## Context

`goal-advisor` is the entrypoint for deciding and crafting how to use native
Codex Goals in Farplane. Use it when the operator wants to "run a shop", start
a durable loop, roll out a pattern, optimize a skill, use human feedback,
schedule heartbeat work, write a sharper `/goal`, choose the metric to optimize,
or decide whether a task should use Goal mode at all.

Native Goal mode is the only formal continuation loop. Farplane adds the visible
state around it through a Goal Packet:

```text
GoalPacket := ticket.md + program.md + progress.md + generated_goal_prompt + drift_check_contract
```

This skill owns both the architecture decision and the final native `/goal`
prompt when Goal mode is warranted. Do not split prompt compilation into a
separate skill; keep the template as part of this contract so the architecture,
metric, drift policy, and prompt stay coherent.

## Skill Signature

```text
advise_goal_use(intent, state?, constraints?, budget?) -> goal_architecture + goal_packet + native_goal_prompt? + next_action
state: reads(operator intent, tickets, program.md?, progress.md?, goal-loop contract, relevant skills/docs); writes(ticket/program/progress? generated goal prompt? or recommendation)
gates: material_goal_has_ticket; loop_owner_single; progress_surface_named; metric_provider_named; drift_policy_named; logging_policy_named
routes: with-human | work | ralph | review | direct-answer
fails: creates hidden loop runtime; uses Goal without durable state; treats human feedback/heartbeat/rollout as competing loop owners; emits prompt-only material Goal
```

## Phase Contract

```text
goal_advice_phase(intent, state)
  -> task_shape
   + trigger_mode
   + state_surfaces
   + metric_provider
   + drift_policy
   + native_goal_prompt?
   + next_owner
```

## Phase Boundary

This skill may route to `with-human`, `work`, `ralph`, or `review` only after it
chooses the Goal architecture. It does not run the Goal loop itself.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the intent and decide whether this is material enough for Goal.
   - [ ] If the task is tiny or one-turn, recommend direct work instead of Goal.
   - [ ] If native Goal is warranted, require a ticket or create-ticket step.
- [ ] 2. Classify the loop shape.
   - [ ] `active_goal`: immediate continuation across turns.
   - [ ] `heartbeat`: scheduled continuation after time or external state.
   - [ ] `feedback_loop`: needs human or reviewer feedback before continuing.
   - [ ] `skill_improvement`: improves a target skill using evals, review, or
     feedback.
   - [ ] `rollout`: applies a proven pattern across a target set.
   - [ ] `business_loop`: recurring strategy loop that creates or updates
     child tickets.
- [ ] 3. Choose the state surfaces.
   - [ ] `ticket.md` owns task contract, proof, acceptance, and current status.
   - [ ] `program.md` owns loop config, metric provider, drift policy, heartbeat,
     after-each-turn routine, and stop conditions.
   - [ ] `progress.md` owns append-only turn logs, evidence, feedback samples,
     drift verdicts, and next actions.
- [ ] 4. Choose the metric or feedback provider.
   - [ ] `mechanical`: command, script, eval, benchmark, or artifact check.
   - [ ] `review`: TAS verdict from review.
   - [ ] `agent_qa`: adversarial QA evidence.
   - [ ] `with-human`: human score, qualitative feedback, or approval decision.
   - [ ] `market`: external result such as clicks, replies, sales, or retention.
   - [ ] `hybrid`: combine signals without inventing fake numbers.
- [ ] 5. Define drift policy.
   - [ ] Use inline drift checks for small normal goals.
   - [ ] Use `goal-drift-reviewer` for material, long-running, strategic,
     rollout, or self-approval-prone loops.
   - [ ] Drift review is read-only and compares `ticket.md`, `program.md`, and
     recent `progress.md`; it does not plan or implement.
- [ ] 6. Craft the native `/goal` prompt when Goal mode is warranted.
   - [ ] Bind `Task:` from ticket objective, scope, proof, constraints, and
     current next action.
   - [ ] Bind `Logging:` to required `progress.md` writeback before turn end.
   - [ ] Bind `Metric:` to the honest provider from `program.md`.
   - [ ] Bind `After each turn:` to drift check, continuation choice,
     complete/blocked policy, and heartbeat/feedback waits.
   - [ ] Ask only missing execution-safety questions that materially affect the
     Goal contract; cap questions at 3.
   - [ ] Reject proxy-only completion evidence unless it satisfies the actual
     objective.
- [ ] 7. Decide the next owner.
   - [ ] Use `with-human` when the metric provider is human feedback.
   - [ ] Use `$work` or `$ralph` when execution routing or board selection is
     the next step.
   - [ ] Use direct ticket creation/update when the missing surface is state.
- [ ] 8. Return a Goal Architecture note, create Goal Packet scaffolding, or
   output the final native `/goal` prompt.
   - [ ] Include before/after behavior when this changes how a loop will run.
   - [ ] Name open risks, blocked decisions, and proof path.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Goal Shapes

### Active Goal

```text
active_goal(ticket, program, progress)
  -> chained_turns_until_complete_or_blocked
```

Use for implementation, skill improvement, research, or app-building work that
should continue immediately.

### Heartbeat

```text
heartbeat(ticket, program, progress, schedule)
  -> inspect_state + maybe_resume_goal + progress_entry
```

Use when useful work depends on time, external state, feedback arrival, or
periodic operations.

### Feedback Loop

```text
feedback_loop(ticket, program, progress, provider)
  -> feedback_request + observation_or_score_or_decision + next_turn
```

Use `with-human` when Kenji's judgment is the fastest quality signal.

### Rollout

```text
rollout_goal(pattern, sample_proof, target_set)
  -> staged_batches + child_tickets? + rollout_progress
```

Use after one or a few examples prove the pattern. Promote to a reusable skill
only after repeated use proves the trigger and workflow.

## Goal Contract

A strong native Goal prompt should include:

- `Task`: what must be true, from `ticket.md`
- `Logging`: how to update `progress.md`
- `Metric`: how progress is judged, from `program.md`
- `After each turn`: how to drift-check, continue, wait, complete, or block
- `Budget`: optional turn/time/spend limit, from `program.md`

## Goal Algebra

Use this compact model when several workflow skills are invoked together. The
job of `goal-advisor` is to choose the Goal Packet architecture and compile the
operator's intent into one native Goal contract, not to run each named skill as
a separate top-level workflow.

```text
GoalPacket := Task + Program + Progress + Prompt + Drift

Task :=
  desired_end_state
+ boundaries
+ constraints
+ non_goals

Program :=
  metric_provider
+ after_each_turn
+ drift_policy
+ heartbeat_policy
+ stop_conditions

MetricProvider :=
  mechanical_evidence
| human_feedback
| review_verdict
| agent_qa
| market_signal
| hybrid_metric

Progress :=
  turn_log
+ evidence
+ metric_samples
+ drift_verdicts
+ next_action
```

Composition rules:

- `agent-qa-test` fills the `agent_qa` metric provider and the fix-or-rerun
  policy.
- `with-human` fills `MetricProvider.human_feedback` through
  `feedback-request.md`, `feedback.json`, and `human_score` or `accepted`.
- `review` fills the `review_verdict` provider for serious completion,
  skill-contract, or proof-bundle judgments.
- `$work`, `impl`, or an active ticket fills `Task` execution routing when the
  Goal requires implementation rather than planning only.

For skill-improvement work, native Goal mode is the durable loop runner. Draft
the Goal so it reads the target skill package plus any `self-improve/` context,
optimizes toward `program.md`, uses `$self-improve` only for eval, memory, or
prompt scaffolding, and uses `$skill-maintenance` for accepted writeback into
`SKILL.md`, references, or plugin/source copies.

Question policy:

- Ask when the answer changes safety, scope, verification, spend, destructive
  boundaries, or irreversible external side effects.
- Do not ask for fields already present in the ticket body, Proof Contract,
  linked plan, or operator message.
- Do not ask broad interview questions just because the Goal could be richer.
- If more than 3 fields are missing, ask the 3 that affect execution safety
  most and mark the rest as assumptions.

## Output

Return either:

```text
Goal Architecture:
Ticket:
Program:
Progress:
Trigger:
Metric / Feedback Provider:
Drift Policy:
Native Goal Prompt:
Next Action:
```

Or create/update the Goal Packet files and then report their paths.

## Templates

### Goal Architecture

```text
Goal Architecture:
Ticket:
Program:
Progress:
Trigger:
Metric / Feedback Provider:
Drift Policy:
Native Goal Prompt:
Next Action:
```

### Goal Packet Setup

```text
Create or update:
- tickets/TASK-XXXX/ticket.md
- tickets/TASK-XXXX/program.md from tickets/templates/goal-loop/program.md
- tickets/TASK-XXXX/progress.md from tickets/templates/goal-loop/progress.md

Then generate the native `/goal` prompt from the same packet.
```

### Native Goal Prompt

```text
/goal Run <ticket path> as a Goal Packet.
Task: <ticket objective, scope, proof contract, constraints, and current next_action>.
Logging: Before ending each turn, append a compact structured entry to <progress.md>
with trigger, intent, actions, files/artifacts, metric or feedback sample, drift
verdict, next_action, and blockers.
Metric: Optimize or satisfy <program.md metric_provider>, using <specific evidence>.
After each turn: compare progress against <ticket.md> and <program.md>, request
<drift reviewer> when required, then continue from the largest unresolved
acceptance/evidence/blocker gap, pause for heartbeat or feedback, stop complete,
or report blocked with attempted paths and one missing input.
```

### Skill Improvement Goal

```text
/goal Run <ticket path> as a native Goal-backed skill-improvement loop for
<target skill>, verified by <eval command/artifact, metric, or human-reviewed
artifact> while preserving <skill contract constraints>. Read the target skill
package, including `SKILL.md`, references, scripts, and `self-improve/` context
when present: `program.md`, evals, latest results, failure analysis, prompt
candidates, and prior run notes. Use `program.md` as loop config and
`progress.md` as the turn log. Optimize toward the metric, rubric, or human
feedback schema defined in the ticket Goal program; if no metric exists, first
define the cheapest honest feedback surface before mutating the skill. Use Goal
mode as the durable loop runner, `$self-improve` only for eval/memory/prompt
scaffolding, and `$skill-maintenance` for accepted writeback. Between
iterations, append progress, change one bounded part of the skill, verify it,
request drift review when required, and promote only durable accepted rules. If
blocked or no valid paths remain, report attempted paths, evidence gathered,
safe options considered, the recommended next action, and the one missing input.
```

## Gotchas

- Do not treat `program.md` as a second ticket. The ticket says what must be
  true; the program says how the loop runs.
- Do not treat `progress.md` as transcript storage. It is compact observed
  state.
- Do not create nested Goals unless there is an explicit parent-child ticket
  relationship and stop condition.
- Do not make heartbeat automations into hidden autonomy. They are delayed
  triggers for the same Goal Packet contract.
- Do not force numeric metrics onto judgment-heavy work. Use human feedback,
  review verdicts, or artifact-presence signals when those are more honest.
- Do not emit a prompt-only material Goal without a named ticket/program/progress
  setup path.

## Reference Map

- [docs/specs/goal-loop-contract.md](../../docs/specs/goal-loop-contract.md) -
  canonical Goal Packet, heartbeat, feedback, drift, and rollout model.
- [with-human](../with-human/SKILL.md) - create human feedback requests and
  feedback-file contracts for Goal loops.
- [tickets/templates/goal-loop/program.md](../../tickets/templates/goal-loop/program.md) -
  program template.
- [tickets/templates/goal-loop/progress.md](../../tickets/templates/goal-loop/progress.md) -
  progress template.
