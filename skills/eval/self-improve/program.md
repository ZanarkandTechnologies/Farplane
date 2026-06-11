---
title: Self-Improve Program: eval
owner: skills/eval
status: active
updated: 2026-06-11
metric: human_feedback_plus_eval_pass
---

# Self-Improve Program: eval

## Objective

Make the `eval` skill reliably produce realistic, modular, clean-room evals that
test one visible behavior at a time and improve through Goal-backed HITL loops.
Current pivot: use the eval-improvement loop to clarify the broader skill-system
model where Tier 0 is the universal phase protocol, skills are callable mini
harnesses with signatures, and review is a protocol/rubric surface rather than
the owner of all review workflow.

## Loop Contract

```text
goal_hitl_eval_loop(idea, candidate_eval_batch, proof, kenji_feedback)
  -> accepted_pattern | revised_batch | rejected_idea | next_hypothesis
```

Native Goal mode owns continuation. This program owns durable memory for the
loop: ideas, tests, feedback requests, Kenji's responses, accepted lessons, and
next hypotheses. `hitl-autoresearch` provides the human-feedback shape, but the
loop can stay lightweight until it needs a full session directory.

## Current Skill Contract

- Trigger: create, run, repair, or review evals for agent, prompt, skill, or
  workflow behavior.
- Default fixture: AGI Toy Shop for generic harness behavior that should not
  touch real files.
- Owner-local modularity: skill-specific evals live at
  `skills/<skill-name>/eval_task.json`.
- Active project sidecar: working harness evals live under `.farplane/evals`.
- Outcome: task JSON, run artifacts, summary, failure diagnosis, and next fix.
- Review: realistic query, visible reference points, fixture reuse, no live side
  effects, first-load sufficiency, reference-load precision, missing/noisy
  context risk, and maintenance locality.

## Feedback Metric

- Primary: Kenji accepts the eval-writing pattern or gives concrete revision
  instructions.
- Secondary: eval task files load through `run_evals.py` and can produce task
  detail artifacts.
- Do not treat "feedback requested" as completion. Feedback request is only the
  checkpoint that produces the next human signal.

Expected feedback shape:

```json
{
  "run": 1,
  "verdict": "accept | revise | reject",
  "feedback": "What feels good or wrong about the eval-writing pattern.",
  "next_instruction": "The next change Kenji wants."
}
```

## Goal Loop Protocol

1. Log the idea before or while testing it.
2. Create the smallest honest candidate artifact.
3. Run cheap validation first: JSON parse, setup status, deterministic smoke
   run, or targeted script.
4. Review the candidate against eval best practices and skill-structure
   metrics.
5. Write a feedback request with artifact paths and one clear question.
6. Send Telegram when configured; otherwise leave the local feedback request
   path.
7. Stop while waiting for Kenji feedback.
8. On resume, log Kenji's response before changing the artifacts.
9. Keep, revise, or reject the idea, then choose the next hypothesis.

## Durable Evals

- `skills/eval/eval_task.json`
- `.farplane/evals/tasks/harness_tasks.json`

## Idea Log

| Date | Run | Idea | Test | Result | Keep? | Lesson |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-06-11 | batch-01 | Seed `eval` with a skill-local four-task eval batch covering modular authoring, bad-task rejection, best-practice load precision, and skill-structure placement. | Added `skills/eval/eval_task.json` rows and audit note; deterministic custom-harness smoke wrote `.farplane/evals/runs/20260611-052148-eval-skill-smoke/summary.json` with 4 loaded tasks. | Pending HITL review. | pending | A useful eval-for-eval batch should test how evals are written, not only whether a sample answer sounds good. |
| 2026-06-11 | program-loop | Add `self-improve/program.md` so Goal loops have persistent memory for ideas, tests, feedback requests, and Kenji responses. | Created this program file. | Pending validation and feedback. | pending | Goal state is not enough; the skill needs local memory that future agents can read on first improvement pass. |
| 2026-06-11 | rubric-first | Define a good-eval-writing rubric before adding more eval-for-eval cases. | Added `references/eval-writing-rubric.md` and linked it from `SKILL.md`. | Pending HITL review. | pending | The eval skill needs a quality function for eval design before it can reliably choose high-ROI breadth/depth cases. |

## Feedback Log

| Date | Run | Request | Kenji Response | Action |
| --- | --- | --- | --- | --- |
| 2026-06-11 | batch-01 | Ask whether the first four eval-for-eval tasks are realistic, judgeable, and the right batch size. | Pending. | Wait for response before rollout. |
| 2026-06-11 | design-question | Ask how to test whether the eval skill is good. | Separate skill evals from workflow evals. Skill evals should test whether `eval` writes high-ROI, realistic, breadth/depth-aware, edge-case-covering tasks. Workflow evals should live at project level and test whether skill changes trigger proof-surface/eval decisions automatically. Consider council to find high-ROI guardrail evals. | Use this to shape the next batch before rollout. |
| 2026-06-11 | rubric-first | Suggest starting from a good rubric for writing evals. | A good rubric should probably come before more task cases. | Added a draft rubric covering behavior focus, ROI, breadth/depth, realism, judgeability, safety, locality, proof-surface fit, diagnosticity, and maintenance cost. |
| 2026-06-11 | skill-model | Question whether review is really a skill, whether every skill is a mini harness, and whether plan/impl/review should be primitives used inside all skills. | Review may be better understood as a rubric/proof contract store plus judging protocol; each skill should expose a granular unit of work and phase checkpoints. Need distinguish universal task phases from skill tiers. | Use this mental model before expanding eval/review standards. |
| 2026-06-11 | tier0-phase-protocol | Adopt Option 3 direction: native Codex owns plan/execute phases, Tier 0 is phase protocol, and skills should bind signatures before execution. | Updated skill-system docs, global AGENTS template, skill template, and best-practices draft. | Pending validation and HITL review. | pending | Do not create `tier: 0` skills; use Tier 0 for universal phases and `group: meta`/`group: skills` for meta workflows. |

## Accepted Learnings

- Skill-improvement Goal loops should have a local `self-improve/program.md`
  when the loop depends on subjective or iterative human feedback.
- For eval authoring, the first durable memory can be simple: idea, test,
  feedback request, Kenji response, action.
- Eval quality has two layers: `eval` skill quality belongs in
  `skills/eval/eval_task.json`; workflow enforcement belongs in project-level
  eval suites such as `.farplane/evals/tasks/*`.
- The eval skill should be tested on whether it chooses high-ROI evals across
  breadth, depth, edge cases, and degradation guardrails, not only whether it
  emits syntactically valid task JSON.
- Define the eval-writing quality function before expanding eval cases. Without
  a rubric, the skill can generate plausible tasks without knowing what "good"
  means.
- Treat skills as mini harnesses with a task unit, phase contract, state reads
  and writes, proof surfaces, and escalation routes. Keep skill tiers as
  capability/ownership levels; do not confuse them with the universal
  plan/review/implement/prove phases that can appear inside any tier.
- Tier 0 is a phase protocol, not a skill tier or frontmatter value. Meta skills
  remain normal skills with `group: meta`, `group: skills`, or `group: harness`.
- Skill signatures should be treated like callable contracts. If required
  inputs are missing, backpropagate to gather or generate those parameters
  before executing the skill.

## Rejected Ideas

- Do not rely on chat history as the only memory for eval-writing improvements.
- Do not call a feedback request "done"; it is a checkpoint, not acceptance.

## Next Hypotheses

- Review `references/eval-writing-rubric.md` against Kenji feedback, then use it
  to revise `skills/eval/eval_task.json`.
- Add a skill-level eval where `eval` must inspect a proposed skill change and
  propose the highest-ROI eval set with breadth, depth, and edge-case coverage.
- Add a project-level workflow eval where a skill change should trigger a
  proof-surface decision: deterministic check, skill-local eval, project eval,
  or no new eval.
- Use a deliberative/council pass only to generate or review high-ROI eval
  candidates for important skills; do not make council mandatory for every
  small eval change.
- Add one eval for judge-prompt quality after Kenji accepts or revises the seed
  batch shape.
- Add one eval for deciding when a deterministic validator is better than an
  LLM eval.
- Add one eval for task-level context overrides after the AGI Toy Shop default
  fixture proves useful in practice.
