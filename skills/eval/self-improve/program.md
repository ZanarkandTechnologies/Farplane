---
title: Legacy Self-Improve Program: eval
owner: skills/eval
status: legacy
updated: 2026-07-21
metric: human_feedback_plus_eval_pass
---

# Legacy Self-Improve Program: eval

This file preserves pre-Goal experiment notes. It is inert historical material:
the active `self-improve` workflow does not read, write, parse, migrate, or use
it as lifecycle state. New eval-skill optimization uses an owning ticket's
ordinary Goal Packet.

## Objective

Make the `eval` skill reliably produce realistic, modular, clean-room evals that
test one visible behavior at a time and improve through Goal-backed
human-feedback loops.
Current pivot: use the eval-improvement loop to clarify the broader skill-system
model where Tier 0 is the universal phase protocol, skills are callable mini
harnesses with signatures, and review is a protocol/rubric surface rather than
the owner of all review workflow.

## Historical Loop Contract

```text
goal_human_feedback_eval_loop(idea, candidate_eval_batch, proof, kenji_feedback)
  -> accepted_pattern | revised_batch | rejected_idea | next_hypothesis
```

## Current Skill Contract At Capture Time

- Trigger: create, run, repair, or review evals for agent, prompt, skill, or
  workflow behavior.
- Default fixture: AGI Toy Shop for generic harness behavior that should not
  touch real files.
- Owner-local modularity: skill-specific evals live at
  `skills/<skill-name>/evals/evals.json`.
- Active project sidecar: working harness evals live under `.farplane/evals`.
- Outcome: task JSON, run artifacts, summary, failure diagnosis, and next fix.

## Feedback Metric

- Primary: Kenji accepts the eval-writing pattern or gives concrete revision
  instructions.
- Secondary: eval task files load through `run_evals.py` and can produce task
  detail artifacts.
- A feedback request is a checkpoint, not completion.

## Durable Evals

- `skills/eval/evals/evals.json`
- `.farplane/evals/tasks/harness_tasks.json`

## Idea Log

| Date | Run | Idea | Test | Result | Keep? | Lesson |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-06-11 | batch-01 | Seed `eval` with a skill-local four-task eval batch covering modular authoring, bad-task rejection, best-practice load precision, and skill-structure placement. | Added `skills/eval/evals/evals.json` rows and audit note; deterministic custom-harness smoke wrote `.farplane/evals/runs/20260611-052148-eval-skill-smoke/summary.json` with 4 loaded tasks. | pending | A useful eval-for-eval batch should test how evals are written, not only whether a sample answer sounds good. |
| 2026-06-11 | program-loop | Add persistent memory for ideas, tests, feedback requests, and Kenji responses. | Created this historical program file. | superseded | Goal state now belongs to the owning ticket packet. |
| 2026-06-11 | rubric-first | Define a good-eval-writing rubric before adding more eval-for-eval cases. | Added `references/eval-writing-rubric.md` and linked it from `SKILL.md`. | pending | The eval skill needs a quality function before it can choose high-ROI cases. |
| 2026-06-12 | core-self-improvement-batch | Add first eval coverage for core self-improvement skills. | Added skill-local evals and one project-level workflow canary. | pending | Split skill behavior quality from project-level workflow enforcement. |
| 2026-06-12 | skill-maintenance-fixtures | Make skill-maintenance evals realistic without mutating the real skill tree. | Added sandbox fixtures and revised queries. | pending | Mutation-capable evals need concrete bad skills in isolated fixtures. |

## Feedback Log

| Date | Run | Request | Kenji Response | Action |
| --- | --- | --- | --- | --- |
| 2026-06-11 | design-question | Ask how to test whether the eval skill is good. | Separate skill evals from workflow evals; cover ROI, realism, breadth/depth, edge cases, and degradation guardrails. | Shape the next batch before rollout. |
| 2026-06-11 | rubric-first | Suggest starting from a good rubric for writing evals. | A good rubric should probably come before more task cases. | Added a draft eval-writing rubric. |
| 2026-06-11 | skill-model | Ask whether review is a skill and whether skills are mini harnesses. | Treat review as rubric/protocol and distinguish universal task phases from skill tiers. | Preserve this model in active skill-system docs. |

## Accepted Learnings

- Eval skill quality belongs in `skills/eval/evals/evals.json`; workflow
  enforcement belongs in project-level eval suites.
- Test whether eval authoring chooses high-ROI cases across breadth, depth,
  edge cases, and degradation guardrails.
- Define the eval-writing quality function before expanding cases.
- Treat skills as mini harnesses with task, state, proof, and escalation
  contracts; Tier 0 is a phase protocol, not a skill tier.
- Backpropagate missing skill-signature inputs before execution.

## Rejected Ideas

- Do not rely on chat history as the only memory for eval-writing improvements.
- Do not call a feedback request complete.
- Do not treat this legacy file as active Goal state.

## Historical Next Hypotheses

- Review `references/eval-writing-rubric.md` against operator feedback.
- Add a skill-level case for selecting a high-ROI eval set.
- Add a project-level case for selecting the right proof surface.
- Prefer seeded fixture repos plus temporary sandboxes for mutation-capable
  skills.
