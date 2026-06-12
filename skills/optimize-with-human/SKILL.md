---
name: optimize-with-human
description: "Route an optimization goal through Goal Advisor with human feedback as the metric and Telegram-first review requests."
tier: 2
source: local
version: 0.1.0
skill_template_version: "0.2.0"
feature_refs:
  - FEAT-0046
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Optimize With Human

## Context

`optimize-with-human` is the human-feedback optimization preset for Farplane
Goal loops. Use it when Kenji's judgment is the fastest honest quality signal
for improving content, skills, creative artifacts, strategy, demos, video, UI,
taste, or artifact selection before a benchmark or market test exists.

This skill is not a separate continuation runtime. Native Goal mode owns
continuation; `goal-advisor` owns Goal architecture and native `/goal` prompt
compilation; the ticket Goal Packet owns durable state. This skill owns the
human feedback policy, Telegram-first communication protocol, feedback request,
and feedback-file contract for optimization loops.

Plain one-off approval, non-optimization review, or deterministic QA should use
chat, `review`, `qa`, or `telegram-message` directly instead of this preset.

## Skill Signature

```text
optimize_with_human(target, objective, artifacts?, budget?, channel=telegram)
  -> goal_advisor_params + feedback_protocol + goal_packet_ref
state: reads(operator intent, target skill/artifacts, ticket/program/progress?); writes(feedback-request.md? feedback.json? progress entry?)
gates: target_named; objective_named; feedback_policy_named; artifact_refs_visible_or_generation_step_named; goal_advisor_owns_loop
routes: goal-advisor | telegram-message | review
fails: runs its own loop; treats human feedback as completion; asks vague broad questions; publishes or spends from feedback alone
```

## Phase Contract

```text
human_optimization_phase(target, objective, artifacts, budget)
  -> goal_advisor_params
   + feedback_request
   + feedback_schema
   + pause_or_resume_policy
```

## Phase Boundary

`optimize-with-human` pre-binds a Goal Advisor call with:

```text
loop_shape = optimization | skill_improvement
metric_provider = human_feedback
feedback_channel = telegram
feedback_policy = ask_when_artifact_ready
```

It may create feedback artifacts after a Goal Packet exists, but it does not own
the parent Goal, heartbeat, rollout, skill improvement, or market test.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the optimization target and objective.
   - [ ] Name the target skill, workflow, artifact set, or strategy surface.
   - [ ] Name what should improve and what should not change.
- [ ] 2. Decide whether a Goal Packet already exists.
   - [ ] If not, route to `goal-advisor` with human-feedback parameters.
   - [ ] If yes, read or name `ticket.md`, `program.md`, and `progress.md`.
- [ ] 3. Bind the feedback policy.
   - [ ] Default `channel=telegram`.
   - [ ] Default `metric_provider=human_feedback`.
   - [ ] Default pause policy: ask when reviewable artifacts exist, then wait.
   - [ ] Fall back to a local `feedback-request.md` path when Telegram is not
     configured.
- [ ] 4. Choose the feedback type.
   - [ ] `score`: 0-10 or another small bounded scale.
   - [ ] `decision`: keep/revise/reject/approve.
   - [ ] `observation`: qualitative feedback or labels.
   - [ ] `ranking`: pick best/worst among variants.
- [ ] 5. Write one short review question.
   - [ ] Ask for the decision Kenji can provide fastest.
   - [ ] Avoid broad strategy prompts when a label, score, rank, or keep/revise
     decision is enough.
- [ ] 6. Define `feedback.json`.
   - [ ] Include artifact/run id, verdict or score, feedback, labels, and next
     instruction.
   - [ ] Name how the parent Goal should use the feedback.
- [ ] 7. Write or update `feedback-request.md` under the ticket artifacts or
   owning Goal Packet path.
- [ ] 8. Notify via `telegram-message` when configured; otherwise report the
   local feedback request path.
- [ ] 9. Stop or pause cleanly while waiting for feedback; do not pretend the
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
after_each_turn: log progress, request feedback when artifacts exist, pause or continue from feedback
```

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
- `feedback_request_path`
- `artifact_refs`
- `review_question`
- `feedback_schema`
- `pause_or_resume_policy`
- `notification_status`

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

Artifact refs:
- <path or URL>

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
- Do not treat human feedback as permission to publish, spend, contact users,
  or make external promises.
- Do not confuse human taste feedback with mechanical QA. Use QA/review when
  correctness evidence is needed.
- Do not call this for tasks where a deterministic command is the honest metric.
- Do not bypass `goal-advisor` when the loop architecture or Goal Packet does
  not exist yet.

## Reference Map

- [docs/specs/goal-loop-contract.md](../../docs/specs/goal-loop-contract.md) -
  Goal Packet and feedback-provider model.
- [../goal-advisor/SKILL.md](../goal-advisor/SKILL.md) - owns Goal
  architecture, packet setup, and native `/goal` prompt compilation.
- [../telegram-message/SKILL.md](../telegram-message/SKILL.md) - optional
  Telegram notification provider.
