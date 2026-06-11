---
title: Eval Writing Rubric
owner: skills/eval
status: draft
updated: 2026-06-11
---

# Eval Writing Rubric

Use this rubric when judging whether an eval task, eval batch, or eval-writing
proposal is good. This is different from judging the target agent's answer.

```text
judge_eval_writing(candidate_eval, target_change, owner_scope)
  -> accept | revise | reject + missing_dimension + next_fix
```

Only `accept` is pass. `revise` is useful signal but not ready to roll out.

## Owner Boundary

Before judging quality, classify the eval's owner:

- `skill`: tests whether one skill behaves or writes artifacts correctly. Store
  in `skills/<skill-name>/eval_task.json`.
- `workflow`: tests cross-skill process behavior, such as whether a skill change
  triggers proof-surface selection. Store in `.farplane/evals/tasks/*`.
- `system-prompt`: tests always-on harness behavior. Store in project-level
  suites unless one skill owns the behavior.
- `validator`: not an LLM eval. Use when the expected behavior is structural,
  parseable, or mechanically checkable.

Reject or revise evals that put workflow enforcement inside a skill-local eval
unless the skill itself owns that workflow.

## Rubric Dimensions

| Dimension | Accept | Revise | Reject |
| --- | --- | --- | --- |
| `behavior_focus` | Tests one visible behavior or decision. | Tests a related bundle but cause of failure would be blurry. | Tests vague goodness, style, or "make better." |
| `roi_guardrail` | Protects a high-value behavior likely to regress silently or compound across future work. | Useful but low priority or already mostly covered. | Only checks wording, taste, or unlikely edge behavior. |
| `breadth_depth_balance` | Batch covers a small breadth of distinct failure modes and at least one deep edge/regression case. | Covers breadth or depth, but not both. | Many near-duplicate tasks or one giant mega-task. |
| `realistic_query` | Query sounds like a real operator request under pressure, with fixture context kept outside the query. | Query is plausible but too artificial, overexplained, or too clean. | Query is toy wording that would never occur or hides the behavior being tested. |
| `judgeability` | Reference points are visible, boolean-ish, and inspectable in answer/artifact. | Some points need interpretation or combine multiple checks. | Reference points say "good answer" or require hidden intent. |
| `fixture_safety` | Uses AGI Toy Shop or an inspect-only/sandboxed real fixture without live side effects. | Needs clearer fixture boundary or context override. | Touches real config, secrets, deploys, pushes, or private paths unnecessarily. |
| `owner_locality` | Lives at the correct owner surface and can run without chat context. | Correct owner is plausible but needs a note or split. | Skill eval and workflow eval are mixed together. |
| `proof_surface_fit` | Chooses eval, validator, deterministic test, or no-new-proof for the right reason. | Eval is acceptable but a stronger mechanical check may exist. | Uses LLM eval for purely structural checks or skips eval for behavioral drift. |
| `failure_diagnosticity` | A failure tells us what to fix next. | Failure would indicate a problem but not the exact owner. | Failure would be noisy, subjective, or impossible to attribute. |
| `maintenance_cost` | Minimal new tasks, clear tags/notes, no duplicated long rubric policy. | Slightly too broad or duplicated but manageable. | Bloats task files or repeats shared standards inside every task. |

## Batch Admission

A good first batch usually has `2-4` evals:

- one happy-path behavior the skill must preserve;
- one known or likely failure mode;
- one edge case or boundary case;
- one high-ROI workflow/placement distinction only if it belongs to the same
  owner.

Prefer fewer high-signal tasks over many plausible tasks. Add more only when a
run teaches something new.

## High-ROI Candidate Sources

Use these inputs to find evals worth writing:

- a user correction or repeated miss;
- a Tier 1, meta, or `eval` skill change;
- a behavior that silently degrades without syntax errors;
- a workflow boundary that agents often confuse;
- a deterministic validator that cannot cover the behavior;
- a task that council or reviewer consensus says is a compounding guardrail.

## Council Use

Use `deliberative-advice` or a council pass for high-impact eval design when:

- the target is Tier 1, meta, `eval`, or cross-skill;
- several plausible evals compete for limited budget;
- the failure modes need breadth across operator value, engineering risk,
  evidence quality, and systems fit.

Council output should be a ranked eval backlog, not immediate rollout. Apply
this rubric before adding the tasks.

## Common Rejects

Reject or rewrite evals that:

- ask the agent to be "good", "comprehensive", or "better" without a visible
  behavior;
- mix skill-local quality with project-level workflow enforcement;
- repeat the AGI Toy Shop context in every query instead of using fixture
  context;
- require real filesystem mutation when a clean-room scenario would test the
  behavior;
- add five tiny variants of the same failure mode;
- use LLM judging where JSON/schema/static validation would be stronger.
