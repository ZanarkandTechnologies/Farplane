---
name: optimize-with-human
description: "Route an optimization goal through Goal Advisor with human feedback as the metric and Telegram-first review requests."
tier: 2
source: local
version: 0.1.0
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.1.0"
eval: eval_task.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Write, Glob, Grep, Bash

---

# Optimize With Human

## Context

`optimize-with-human` is the human-feedback optimization preset for Farplane
Goal loops. Use it when Kenji's judgment is the fastest honest quality signal
for improving content, skills, creative artifacts, strategy, demos, video, UI,
taste, or artifact selection before a benchmark or market test exists.

This skill is not a separate continuation runtime. Native Goal mode owns
uninterrupted continuation; persistent Codex worker threads own Telegram reply
routing when feedback should resume the same job; `goal-advisor` owns Goal
architecture and native `/goal` prompt compilation; the ticket Goal Packet owns
durable state. This skill owns the human feedback policy, Telegram-first
communication protocol, phase experiment log, feedback request, and
feedback-file contract for optimization loops.

Plain one-off approval, non-optimization review, or deterministic QA should use
chat, `review`, `qa`, or `telegram-message` directly instead of this preset.

## Skill Signature

```text
optimize_with_human(target, objective, artifacts?, budget?, channel=telegram,
                    worker_thread_ref?, phase=planning|execution,
                    approved_plan_ref?)
  -> goal_advisor_params + feedback_protocol + goal_packet_ref +
     experiment_log_ref + feedback_request_ref
state: reads(operator intent, target skill/artifacts, ticket/program/progress?,
             worker_thread_ref?); writes(feedback-request.md? feedback.json?
             progress entry?)
gates: target_named; objective_named; feedback_policy_named;
       artifact_refs_visible_or_generation_step_named; goal_advisor_owns_loop;
       telegram_reply_path_bound_when_needed; goal_packet_exists;
       phase_bound; experiment_proposal_logged; turn_exit_gate_satisfied
routes: goal-advisor | telegram-message | review
fails: runs its own loop; treats human feedback as completion; asks vague broad
  questions; publishes or spends from feedback alone; sends a Telegram request
  from the wrong thread when replies are expected to resume the worker; edits a
  target skill from one rejection; asks for planning feedback on a thin
  hook-only artifact when the planned artifact needs a proposal; runs execution
  phase without an approved plan unless the artifact is explicitly a tiny
  planning test
```

## Phase Contract

```text
human_optimization_phase(target, objective, phase, artifacts, budget)
  -> goal_advisor_params
   + experiment_proposal
   + feedback_request
   + feedback_schema
   + pause_or_resume_policy
```

## Phase Boundary

`optimize-with-human` pre-binds a Goal Advisor call or worker-thread program
with:

```text
loop_shape = optimization | skill_improvement
metric_provider = human_feedback
feedback_channel = telegram
feedback_policy = ask_when_artifact_ready
```

It may create feedback artifacts after a Goal Packet exists, but it does not own
the parent Goal, heartbeat, rollout, skill improvement, market test, or thread
creation. When Telegram replies should drive the next iteration, the caller
must create or name the dedicated worker thread first, then invoke this preset
inside that thread or pass its `worker_thread_ref`.

Bind the current phase before asking for feedback:

- `planning`: the artifact should usually be a proposal card, offer brief,
  storyboard premise, draft hook batch, or other compact plan. For non-trivial
  artifacts, require enough detail to judge: audience/buyer, insight, artifact
  shape, core angle, execution beats, why it could win, cringe risks, references
  or taste pack, feedback question, and next step if approved. Hook-only cards
  are valid only when the thing being judged is the hook itself.
- `execution`: the artifact must implement an approved planning brief. Require
  `approved_plan_ref` unless the artifact is explicitly a tiny planning test.

Before a feedback request is sent, append an experiment proposal to
`progress.md`. After feedback arrives, append the result and promotion decision.
Promote a skill, prompt, workflow, or template change only after repeated
same-phase failure or a reusable operator-approved pattern. First rejections
perturb the local plan or execution attempt; they do not harden source skills.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the optimization target and objective.
   - [ ] Name the target skill, workflow, artifact set, or strategy surface.
   - [ ] Name what should improve and what should not change.
- [ ] 2. Decide whether a Goal Packet already exists.
   - [ ] If not, route to `goal-advisor` with human-feedback parameters.
   - [ ] If yes, read or name `ticket.md`, `program.md`, and `progress.md`.
- [ ] 3. Bind the phase, reply path, and feedback policy.
   - [ ] Choose `phase=planning` or `phase=execution`.
   - [ ] For planning, accept proposal cards or compact artifact plans as
     reviewable artifacts; reject hook-only summaries for non-trivial artifacts.
   - [ ] For execution, require `approved_plan_ref` unless this is a tiny
     planning test.
   - [ ] If Telegram replies should continue the job, confirm the current
     context is the dedicated worker thread or a `worker_thread_ref` is named.
   - [ ] If no worker thread exists and replies need routing, return a handoff
     requirement instead of sending from the parent thread.
   - [ ] Default `channel=telegram`.
   - [ ] Default `metric_provider=human_feedback`.
   - [ ] Default pause policy: ask when reviewable artifacts exist, then wait.
   - [ ] Fall back to a local `feedback-request.md` path when Telegram is not
     configured.
- [ ] 4. Log the experiment proposal in `progress.md`.
   - [ ] Include `experiment_id`, `phase`, `hypothesis`,
     `skill_delta_candidate`, `scenario`, `rollout_batch`, and
     `expected_feedback`.
   - [ ] Keep `skill_delta_candidate` as a candidate until repeated feedback
     proves it should be hardened.
- [ ] 5. Choose the feedback type.
   - [ ] `score`: 0-10 or another small bounded scale.
   - [ ] `decision`: keep/revise/reject/approve.
   - [ ] `observation`: qualitative feedback or labels.
   - [ ] `ranking`: pick best/worst among variants.
- [ ] 6. Write one short review question.
   - [ ] Ask for the decision Kenji can provide fastest.
   - [ ] Ensure the artifact has enough proposal detail for that decision; do
     not make the Telegram question short by hiding the proposal itself.
   - [ ] Avoid broad strategy prompts when a label, score, rank, or keep/revise
     decision is enough.
- [ ] 7. Define `feedback.json`.
   - [ ] Include artifact/run id, verdict or score, feedback, labels, and next
     instruction.
   - [ ] Name how the parent Goal should use the feedback.
- [ ] 8. Write or update `feedback-request.md` under the ticket artifacts or
   owning Goal Packet path.
- [ ] 9. Notify via `telegram-message` when configured; otherwise report the
   local feedback request path.
- [ ] 10. Apply the turn exit gate.
   - [ ] If waiting for human feedback, prove the Telegram send succeeded or
     report the fallback path/blocker.
   - [ ] If fresh human feedback was processed and the loop is not terminal,
     send the next artifact feedback request or a blocker before stopping.
   - [ ] If the loop is terminal, record keep/approve/convergence/budget/blocker
     in `progress.md`.
- [ ] 11. Record the experiment result.
   - [ ] Append the feedback verdict and phase-specific next action to
     `progress.md`.
   - [ ] Use `promotion_decision=keep_local`, `rerun`, `harden_skill`, or
     `discard`.
   - [ ] Reserve `harden_skill` for repeated same-phase failure or a reusable
     approved pattern.
- [ ] 12. Stop or pause cleanly while waiting for feedback; do not pretend the
   feedback signal exists yet.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Goal Advisor Params

When a Goal Packet is missing or stale, call `goal-advisor` conceptually with:

```text
intent: optimize <target> toward <objective>
loop_shape: skill_improvement | optimization
metric_provider: human_feedback
feedback_channel: telegram
feedback_policy: ask_when_artifact_ready
state_surfaces: ticket.md + program.md + progress.md
phase: planning | execution
approved_plan_ref: <required for execution unless tiny planning test>
after_each_turn: log progress, request feedback when artifacts exist, pause or continue from feedback
```

When a worker Goal Packet and thread already exist, do not create another
packet. Bind this preset inside the worker's `program.md` and feedback request:

```text
worker_thread_ref: <thread id or URL>
metric_provider: human_feedback
feedback_channel: telegram
feedback_policy: ask_when_artifact_ready
phase: planning | execution
approved_plan_ref: <brief/concept ref when phase=execution>
resume_policy: Telegram replies land in worker_thread_ref; worker appends
  feedback to progress.md and generates the next artifact revision.
```

## Experiment Log Contract

Append this shape to the owning `progress.md` before feedback is requested, then
fill the feedback and result fields after the reply:

```text
experiment:
  id: OWH-EXP-###
  phase: planning | execution
  target:
  scenario:
  approved_plan_ref:
  hypothesis:
  skill_delta_candidate:
  rollout_batch:
    - artifact_id:
      artifact_ref:
      expected_feedback:
  feedback:
  result: pass | revise | reject | no_reply | blocker
  promotion_decision: keep_local | rerun | harden_skill | discard
```

For Taste Loop, planning experiments usually present one to three TasteProposal
artifacts and execution experiments present the approved proposal's generated
artifact. Use the fixed AGI Toy Shop scenario when no live scenario is supplied.

Minimum TasteProposal shape for non-trivial planning feedback:

```text
title:
one_line_bet:
audience_or_buyer:
taste_insight:
artifact_shape:
core_angle:
execution_beats:
why_it_could_win:
what_would_make_it_cringe:
references_or_taste_pack:
feedback_question:
next_if_approved:
```

## Turn Exit Gate

Before every stop, satisfy exactly one of these exits:

```text
waiting_for_feedback:
  telegram_message_sent == true
  or fallback_feedback_request_ref is visible
  or blocker_ref explains why Telegram could not be sent

feedback_processed_non_terminal:
  next_artifact_ref is visible
  and next_feedback_request_sent == true
  or blocker_ref explains why the next artifact/request cannot be produced

terminal:
  terminal_reason in [keep, approve, convergence, budget, blocker]
  and progress.md records the decision
```

This is the guard against worker threads going quiet after Kenji replies. If
the worker changes a skill, workflow, prompt, or artifact in response to
feedback, it must either send the next review request through Telegram or send
a blocker that tells Kenji what is needed next.

## Feedback Schema

Default shape:

```json
{
  "artifact_id": "run-1",
  "score": 8,
  "verdict": "keep | revise | reject | approve",
  "feedback": "Short reason.",
  "labels": ["optional", "tags"],
  "next_instruction": "What the next Goal turn should do."
}
```

Use `score: null` when the feedback type is qualitative only.

## Output

Return or write:

- `goal_advisor_params`
- `goal_packet_ref`
- `phase`
- `approved_plan_ref`
- `experiment_log_ref`
- `feedback_request_path`
- `artifact_refs`
- `review_question`
- `feedback_schema`
- `pause_or_resume_policy`
- `notification_status`
- `turn_exit_gate_status`

## Templates

### Goal Advisor Preset

```text
Use goal-advisor with:
- target: <skill/workflow/artifact>
- objective: <what should improve>
- loop_shape: skill_improvement | optimization
- metric_provider: human_feedback
- feedback_channel: telegram
- feedback_policy: ask_when_artifact_ready
- budget: <turn/time/artifact budget>
```

### Feedback Request

```text
# Feedback Request

Optimization target:
<target>

Objective:
<objective>

Worker thread:
<worker_thread_ref or current thread>

Artifact refs:
- <path or URL>

Proposal summary:
- audience/buyer:
- taste insight:
- artifact shape:
- core angle:
- execution beats:
- why it could win:
- risk:
- next if approved:

Question:
<one short decision, score, label, or ranking request>

Please write feedback to:
<feedback.json path>

Feedback shape:
<schema>
```

## Gotchas

- Do not make Kenji invent the next prompt from scratch. Present artifacts and
  ask for a small judgment.
- Do not make Kenji judge a non-trivial plan from only a title, hook, and angle.
  Planning feedback needs proposal detail; compress it for Telegram but do not
  erase the reasoning.
- Do not treat human feedback as permission to publish, spend, contact users,
  or make external promises.
- Do not send a Telegram feedback request from a parent heartbeat if Kenji's
  reply is meant to continue a dedicated worker thread.
- Do not confuse human taste feedback with mechanical QA. Use QA/review when
  correctness evidence is needed.
- Do not call this for tasks where a deterministic command is the honest metric.
- Do not bypass `goal-advisor` when the loop architecture or Goal Packet does
  not exist yet.
- Do not stop after processing non-terminal feedback without sending the next
  Telegram review request or an explicit blocker.
- Do not send execution-phase feedback without an approved planning reference
  unless the artifact is explicitly a tiny planning test.
- Do not harden a skill, prompt, or template because of one rejection. Log the
  phase failure, perturb the local experiment, and only promote repeated or
  reusable wins.

## Reference Map

- [docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md](../../docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md) -
  Goal Packet and feedback-provider model.
- [qa_checklist.md](qa_checklist.md) - Telegram/request exit gate and phone
  feedback proof checklist.
- [../goal-advisor/SKILL.md](../goal-advisor/SKILL.md) - owns Goal
  architecture, packet setup, and native `/goal` prompt compilation.
- [../telegram-message/SKILL.md](../telegram-message/SKILL.md) - optional
  Telegram notification provider.
