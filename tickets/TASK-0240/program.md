---
ticket_id: TASK-0240
kind: goal-program
status: active
created_at: 2026-06-27T22:50:30+08:00
---

# TASK-0240 Program

## Objective

Create a high-signal planning concept batch for AGI Toy Shop's `social_thread`
workflow, then use Kenji's feedback to decide whether to execute a draft thread.

## Loop Shape

```text
loop_shape = optimization
metric_provider = human_feedback
feedback_channel = telegram
feedback_policy = ask_when_artifact_ready
phases = planning, execution
primary_metric = idea_pass_rate
secondary_metric = execution_pass_rate
default_scenario = tickets/TASK-0237/artifacts/agi-toy-shop-scenario.md
```

## Inputs

- `tickets/TASK-0240/ticket.md`
- `tickets/TASK-0240/program.md`
- `tickets/TASK-0240/progress.md`
- `tickets/TASK-0237/artifacts/agi-toy-shop-scenario.md`
- `farplane/products.md`
- `skills/social-content/SKILL.md`
- `/Users/kenjipcx/.codex/skills/optimize-with-human/SKILL.md`

## Algorithm

```text
planning_phase:
  log TL-EXP-001 in progress.md before asking for feedback
  create 1-3 ConceptCard items for AGI Toy Shop / Pocket Intern
  ask one compact keep/revise/reject or pick-best question from the worker thread
  record feedback result in progress.md

execution_phase:
  require an approved concept or brief
  log execution experiment proposal in progress.md
  draft the social thread through social-content:twitter-thread
  ask for execution feedback from the worker thread
```

## Guardrails

- Do not send feedback from the parent controller thread.
- Do not execute a full thread before concept approval.
- Do not publish or post externally.
- Do not harden `social-content`, `taste-loop`, or other source skills from one
  rejection.
- Use `promotion_decision=keep_local`, `rerun`, `harden_skill`, or `discard`
  when feedback is recorded.

## Feedback Shape

```json
{
  "artifact_id": "TL-EXP-001",
  "score": null,
  "verdict": "keep | revise | reject | approve",
  "feedback": "Short reason.",
  "labels": ["idea", "social_thread"],
  "next_instruction": "What the worker should do next."
}
```
