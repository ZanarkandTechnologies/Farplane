---
title: Eval QA Checklist
owner: skills/eval
status: active
kind: qa-checklist
updated_at: 2026-06-23
---

# Eval QA Checklist

This is the first-class skill-local QA checklist for eval task quality. Use it
after creating or materially revising eval rows, especially skill-local rows in
`skills/<skill-name>/evals/evals.json`.

Run each check against the actual changed eval files. Do not treat this as a
passive reminder; record violations, then fix or explicitly defer them in the
ticket, audit, or final proof notes.

```text
eval_qa_checklist(eval_files, changed_rows, claim, budget?)
  -> checklist_verdicts + fixes_or_deferrals + evidence_note
```

## Query Spoiler Check

Use this check when reviewing skill-local eval rows for answer leakage. The
target is the eval row, not the agent answer.

```text
review_eval_query(task_row, skill_name, owner_scope)
  -> pass | revise | fail + reason + rewrite_hint
```

### Pass

A query passes when it sounds like a realistic operator request and leaves the
skill contract to runner-provided skill context.

- The query does not name the target skill, contract, checklist, `SKILL.md`
  file, harness, runner, eval machinery, or invocation path unless the real
  operator request would naturally be about that artifact.
- The query does not instruct the agent to use a specific skill, read a specific
  skill file, follow a named checklist, or satisfy the eval reference points.
- The query includes only scenario facts the operator would plausibly provide.
- Expected behavior is carried by `reference_points`, fixture context, and the
  owning skill, not by the user wording.
- Domain nouns that overlap with a skill name are acceptable when they are
  natural to the scenario, such as "QA this UI change" for a QA task.

### Revise

Revise when the query is plausible but too polished, meta, or lightly leading.

- It describes the desired process instead of the user's problem.
- It mirrors one or more reference points as instructions.
- It adds unusual guardrail language that smells like an eval author wrote it.
- It gives a checklist-shaped request when the real operator would give a
  messy symptom, artifact, or goal.

### Fail

Fail when the query teaches the answer.

- It says to use the target skill, target contract, target checklist, or
  `skills/<skill-name>/SKILL.md`.
- It exposes the routing decision the agent is supposed to infer.
- It lists the exact proof, QA, artifact, review, or final-report obligations
  that the skill is supposed to supply.
- It includes private harness policy or eval internals as if they came from the
  user.
- It turns the eval into a memory test of the prompt instead of a behavior test
  of the skill.

## Finish Gate

For material eval row changes, record this in the ticket, audit, or final proof
notes:

```text
eval_query_review:
  changed_files:
  reviewed_rows:
  reviewer: self | reviewer | qa_lane | llm_judgment
  query_spoiler_verdict: pass | fail | unknown
  fixes_applied:
  deferrals:
  remaining_risk:
```

## Subagent Review Prompt

Use a reviewer or QA subagent when independent eval-row checking is worth the
coordination cost:

```text
Review the changed eval rows against skills/eval/qa_checklist.md.

For each changed row, return:
- verdict: pass | revise | fail
- evidence: file path, task id, and the specific query wording at issue
- reason: whether the query is natural or leaks invocation, policy, expected
  answer, or reference-point logic
- fix: smallest rewrite hint, or "none"

Do not judge the target agent answer. Do not add expected behavior to the user
query. Only report eval-row QA violations and the highest-risk unresolved issue.
```
