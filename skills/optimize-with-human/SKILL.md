---
name: optimize-with-human
description: "Route an optimization goal through Goal Advisor with human feedback as the metric and Telegram-first review requests."
tier: 2
source: local
version: 0.1.0
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.2.0"
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
durable state. Multi-turn experiment-backed packets also use
`hypothesis-tree.json` as their current hypothesis state; simple one-off
feedback does not require it. This skill owns the human feedback policy, Telegram-first
communication protocol, phase experiment log, feedback request, and
feedback-file contract for optimization loops.

Plain one-off approval, non-optimization review, or deterministic QA should use
chat, `review`, `qa`, or `telegram-message` directly instead of this preset.

## Skill Signature

```text
optimize_with_human(target, objective, artifacts?, budget?, channel=telegram,
                    worker_thread_ref?, phase=planning|execution,
                    approved_plan_ref?, founder_lens=false?)
  -> goal_advisor_params + feedback_protocol + goal_packet_ref +
     progress_log_ref + feedback_request_ref
state: reads(operator intent, target skill/artifacts, ticket/program/hypothesis-tree?/progress?,
             worker_thread_ref?); writes(feedback-request.md? feedback.json?
             hypothesis-tree mutation? progress entry?)
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

When `founder_lens=true`, the worker should behave like a founder validating a
commercial bet, not like an internal reviewer collecting preferences. The
feedback request must name the customer, problem, wedge, offer/artifact,
distribution angle, validation question, and what feedback would change the
next bet. The objective is not merely "impress Kenji"; it is to earn Kenji's
conviction that this bet is worth making, selling, or testing.

Before a feedback request is sent, select and mark the current tree node when
the packet is experiment-backed, then append the hypothesis cycle to
`progress.md`. After feedback arrives, update that node and append the human
signal, learning, tree mutation, and next hypothesis.
Promote a skill, prompt, workflow, or template change only after repeated
same-phase failure or a reusable operator-approved pattern. First rejections
perturb the local plan or execution attempt; they do not harden source skills.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the optimization target and objective.
   - [ ] Name the target skill, workflow, artifact set, or strategy surface.
   - [ ] Name what should improve and what should not change.
   - [ ] When the artifact is product, content, distribution, or offer work,
     bind `founder_lens=true` unless the caller explicitly wants a narrower
     artifact review.
- [ ] 2. Decide whether a Goal Packet already exists.
   - [ ] If not, route to `goal-advisor` with human-feedback parameters.
   - [ ] If yes, read or name `ticket.md`, `program.md`, `progress.md`, and
     `hypothesis-tree.json` when Experiment Backbone is enabled.
   - [ ] For a new multi-turn optimization campaign, run the program's bounded
     source stage over prior feedback, supplied references, Feed Scout signals,
     or direct research; extract techniques, mechanisms, and variables, then
     seed intervention hypotheses with expected rewards. Skip this tree for a
     one-off feedback request.
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
- [ ] 4. Log the hypothesis cycle in `progress.md`.
   - [ ] For an experiment-backed packet, use Leverage Advisor to select one
     eligible pending tree leaf by ordinal compounding leverage. Do not use a
     variant tournament as the hypothesis-selection algorithm; human ranking
     remains valid only as the feedback signal for the selected experiment.
   - [ ] Include `phase`, `current_hypothesis`, `planned_attempt`,
     `artifact_refs`, `human_question`, `expected_signal`, and
     `skill_delta_candidate`.
   - [ ] If `founder_lens=true`, include the customer, problem, wedge,
     offer/artifact, distribution angle, validation question, and what feedback
     would change the next bet.
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
   - [ ] If the fresh feedback is `revise` or `reject`, acknowledge the
     feedback, restate the corrected artifact/workflow/product/stage, and ask
     for the next instruction or present the next revised review request. Do
     not stop after only saying the feedback was recorded.
   - [ ] If the loop is terminal, record keep/approve/convergence/budget/blocker
     in `progress.md`.
- [ ] 11. Record the experiment result.
   - [ ] When a tree exists, update the selected node before appending the
     progress receipt. Add bounded diagnostic children only when feedback is
     surprising or causally ambiguous, then repair, reject, defer, or backtrack.
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
state_surfaces: ticket.md + program.md + hypothesis-tree.json + progress.md
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

## Progress Log Contract

For experiment-backed packets, store the live hypothesis in
`hypothesis-tree.json` and append this receipt shape to `progress.md` before
feedback is requested, then update the tree and append the feedback result and
next hypothesis after the reply. The cycle
does not need a fresh named experiment id; timestamped `progress.md` headings
are enough unless the caller needs a stable artifact handle.

```text
hypothesis_cycle:
  phase: planning | execution
  target:
  scenario:
  approved_plan_ref:
  current_hypothesis:
  planned_attempt:
  artifact_refs:
    - path:
      role:
  human_question:
  expected_signal:
  skill_delta_candidate:
  human_signal:
    verdict:
    feedback:
    labels:
  learning:
  next_hypothesis:
  promotion_decision: keep_local | rerun | harden_skill | discard
```

For a self-improvement human-feedback ticket, planning experiments usually
present one to three concrete proposals and execution cycles present the
approved proposal's generated artifact. Use the fixed AGI Toy Shop scenario
when no live scenario is supplied.

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
For `revise` or `reject` feedback, a valid acknowledgement must include the
updated understanding and the next operator-facing action. It should ask a
concrete follow-up such as "Do you want me to revise this into X, switch to Y,
or stop this experiment?" when the next action is ambiguous.

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

## Founder Lens Contract

Use the founder lens for product, content, distribution, offer, and market
learning artifacts where Kenji's taste is standing in for early founder
judgment:

```text
founder_lens(target, market_context, phase, human_feedback?)
  -> customer
   + problem
   + wedge
   + offer_or_artifact
   + distribution_angle
   + validation_question
   + next_bet_if_approved
   + pivot_trigger_if_rejected
```

The founder lens changes framing, not ownership. `optimize-with-human` still
owns the feedback protocol, Telegram request, pause/resume contract, and
progress logging. The artifact skill still owns generation. The worker should
ask Kenji questions like "Would this make you want to build, sell, or test
this?" instead of "Is this artifact good?" when the bet is still being shaped.

## Output

Return or write:

- `goal_advisor_params`
- `goal_packet_ref`
- `phase`
- `approved_plan_ref`
- `progress_log_ref`
- `feedback_request_path`
- `artifact_refs`
- `review_question`
- `feedback_schema`
- `pause_or_resume_policy`
- `notification_status`
- `turn_exit_gate_status`

For an experiment-backed setup, also return `source_stage`,
`hypothesis_tree_ref`, and a concrete `selected_tree_node` containing
`hypothesis`, `mechanism`, `expected_observation`, `falsifier`,
`expected_reward`, `reward_basis`, and `source_refs`. Name
`selection_owner=leverage-advisor` and give one ordinal compounding-leverage
rationale; do not substitute human variant ranking. After feedback, return `tree_mutation` before
`progress_log_ref`, plus preserved siblings and bounded diagnostic children
when the signal is surprising or causally ambiguous. Omit these fields for a
one-off feedback request.

When asked to show the feedback-turn writeback, render this order literally;
if feedback is still pending, show it as the required future writeback without
inventing the result:

```text
tree_mutation: selected node result + insight + status
preserved_siblings: []
diagnostic_children: [] | bounded child ids
progress_receipt: feedback + mutation summary + next action
```

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
- Do not reduce founder-mode feedback to "do you like this?" Name the customer,
  problem, wedge, validation question, and next bet so Kenji can judge founder
  conviction.
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
- the first-load Todo List guardrails - Telegram/request exit gate and phone
  feedback proof checklist.
- [../goal-advisor/SKILL.md](../goal-advisor/SKILL.md) - owns Goal
  architecture, packet setup, and native `/goal` prompt compilation.
- [../telegram-message/SKILL.md](../telegram-message/SKILL.md) - optional
  Telegram notification provider.
