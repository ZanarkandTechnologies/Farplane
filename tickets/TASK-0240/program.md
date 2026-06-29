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
progress_unit = hypothesis_cycle
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
  append a timestamped hypothesis_cycle in progress.md before asking for feedback
  create 1-3 TasteProposal items for AGI Toy Shop / Pocket Intern
  ask one compact founder decision from the worker thread
  record human_signal, learning, and next_hypothesis in progress.md

execution_phase:
  require an approved concept or brief
  append an execution hypothesis_cycle in progress.md
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
- Do not create fresh TL experiment labels as the unit of progress. Keep this
  ticket as the workflow container and append hypothesis cycles to
  `progress.md` until approval, convergence, blocker, budget exhaustion, or
  operator closeout.

## Feedback Shape

```json
{
  "artifact_id": "current planning artifact",
  "score": null,
  "verdict": "keep | revise | reject | approve",
  "feedback": "Short reason.",
  "labels": ["idea", "social_thread"],
  "next_instruction": "What the worker should do next."
}
```
