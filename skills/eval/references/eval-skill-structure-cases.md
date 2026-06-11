---
title: Eval Skill Structure Cases
owner: skills/eval
status: draft
updated: 2026-06-11
---

# Eval Skill Structure Cases

Use this reference only when converting skill-structure standards into eval
cases for the `eval` skill. The general structure standard lives in
[`docs/skills/best-practices.md`](../../../docs/skills/best-practices.md#structure-optimization).

## Review Skill Upgrade Candidate

Do not update `review` yet just because this idea is plausible. First write eval
cases that expose bad skill structure. If those cases show repeated misses, add
these checks to `docs/review/rubrics/skill-contract.md`:

- `first-load-sufficient`: required default behavior is present in `SKILL.md`.
- `reference-load-precise`: branch-specific detail is in references and linked
  from the right todo branch.
- `prompt-size-constrained`: first-load content is compact enough to use.
- `optimization-metrics-named`: material skill-structure changes name the
  reward/loss terms they improve.

## Eval Skill Eval Backlog

Write these as `skills/eval/eval_task.json` rows first:

1. `eval_skill_first_load_sufficiency_01`
   - Query: asks the agent to write one eval for `advise`.
   - Expected: chooses `skills/advise/eval_task.json`, uses AGI Toy Shop shared
     context, writes realistic query and observable reference points, avoids
     live side effects.

2. `eval_skill_best_practices_branching_01`
   - Query: asks whether to load eval best practices for a run-only task.
   - Expected: does not load full best practices for run-only work; loads them
     only when writing/revising tasks or judge prompts.

3. `eval_skill_bad_task_rejection_01`
   - Query: proposes a vague eval such as `"Make the company better"` with
     reference point `"Gives a good answer"`.
   - Expected: rejects or rewrites it into one behavior, realistic query,
     visible reference points, tags, and notes.

4. `eval_skill_structure_metric_01`
   - Query: asks whether to move all best practices into `SKILL.md`.
   - Expected: uses harness-algebra tradeoffs: maximize first-load sufficiency
     and task success while minimizing prompt size, duplication, and noisy
     context.

Hold out one workflow-level case for later:

- `workflow_skill_review_structure_01`
  - Tests whether review catches a bloated or under-specified skill contract
    before approving it.

## Acceptance Criteria

The prep is ready to turn into eval rows when:

- the candidate task IDs map to one behavior each;
- each expected behavior can be judged from visible output;
- at least one task catches overloading `SKILL.md`;
- at least one task catches underloading `SKILL.md`;
- the review-upgrade candidate has a failing example before being promoted.
