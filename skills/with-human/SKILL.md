---
name: with-human
description: "Turn a Goal loop's subjective quality need into a human feedback request, feedback file contract, and continuation signal."
tier: 2
source: local
version: 0.1.0
skill_template_version: "0.2.0"
feature_refs:
  - FEAT-0046
allowed-tools: Read, Write, Glob, Grep, Bash
---

# With Human

## Context

`with-human` is the human feedback provider for Farplane Goal loops. Use it
when Kenji's judgment is the fastest honest quality signal for content,
creative, strategy, demo, video, UI, taste, or artifact-selection work.

This is not a separate continuation runtime. Native Goal mode owns
continuation; the ticket Goal Packet owns state; `with-human` owns the feedback
request and feedback-file contract.

Older session-shaped human feedback loops should be modeled as Goal Packets
with `with-human` as the provider name.

## Skill Signature

```text
with_human(goal_packet, artifact_refs, review_question, feedback_schema?) -> feedback_request + feedback_contract
state: reads(ticket.md, program.md, progress.md, artifact refs); writes(feedback-request.md? feedback.json?)
gates: question_short; artifact_refs_visible; feedback_shape_explicit; no_external_action_claim
routes: telegram-message | goal-advisor | review
fails: treats feedback request as completion; asks vague questions; publishes or spends based on feedback alone
```

## Phase Contract

```text
human_feedback_phase(goal_packet, artifacts)
  -> review_question
   + feedback_request
   + feedback_schema
   + continuation_signal
```

## Phase Boundary

`with-human` provides feedback input to a Goal loop. It does not own the parent
Goal, heartbeat, rollout, skill improvement, or market test.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the Goal Packet and artifacts.
   - [ ] Read or name `ticket.md`, `program.md`, and `progress.md`.
   - [ ] Confirm the artifact refs are visible and reviewable.
- [ ] 2. Choose the feedback type.
   - [ ] `score`: 0-10 or another small bounded scale.
   - [ ] `decision`: keep/revise/reject/approve.
   - [ ] `observation`: qualitative feedback or labels.
   - [ ] `ranking`: pick best/worst among variants.
- [ ] 3. Write one short review question.
   - [ ] Ask for the decision Kenji can provide fastest.
   - [ ] Avoid broad strategy prompts when a label, score, or keep/revise
     decision is enough.
- [ ] 4. Define `feedback.json`.
   - [ ] Include artifact/run id, verdict or score, feedback, and next
     instruction.
   - [ ] Name how the parent Goal should use the feedback.
- [ ] 5. Write or update `feedback-request.md` under the ticket artifacts or
   owning session path.
- [ ] 6. Notify via `telegram-message` when configured; otherwise report the
   local feedback request path.
- [ ] 7. Stop or pause cleanly while waiting for feedback; do not pretend the
   feedback signal exists yet.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

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

- `feedback_request_path`
- `artifact_refs`
- `review_question`
- `feedback_schema`
- `continuation_policy`
- `notification_status`

## Templates

### Feedback Request

```text
# Feedback Request

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

## Reference Map

- [docs/specs/goal-loop-contract.md](../../docs/specs/goal-loop-contract.md) -
  Goal Packet and feedback-provider model.
- [../telegram-message/SKILL.md](../telegram-message/SKILL.md) - optional
  Telegram notification provider.
- [../goal-advisor/SKILL.md](../goal-advisor/SKILL.md) - decide whether a Goal
  loop should use human feedback.
