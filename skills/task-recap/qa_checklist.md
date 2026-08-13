---
title: Task Recap QA Checklist
owner: task-recap
status: active
kind: qa-checklist
applies_to:
  - resumption-briefs
  - delayed-task-replies
---

# Task Recap QA Checklist

Use this before returning a material recap and again before relying on it for a
decision or user reply.

```text
task_recap_check(task_boundary, sources, recap, next_action)
  -> pass | violation | source_gap
```

## Checklist

- [ ] Immediately after any governing response ledger, the recap opens with a
  grouped quick card (`Now`, `Delta`, and `Risks & action`), identifies one
  task boundary, and lists the authoritative sources used; each supplied
  readable path was opened before an unavailable ticket, artifact, or thread
  is called a source gap.
- [ ] Durable records outrank transcript memory, and observed fact, decision,
  inference, and stale snapshot are distinguishable in the recap.
- [ ] Every material change has a source-backed `Before` / `After` / indented
  `Example` visibly grouped in `Delta`; a full recap adds a dated,
  source-labeled chronology plus every problem's attempts, observed outcome,
  disposition, and remaining impact in a distinct `Problems and attempts`
  section; it names the operator's immediate goal and latest user question or
  decision, uses a full date on every dated event, and ends its detail ledger
  with one literal task-relative or supplied path per bullet plus one final safe
  next action.
- [ ] Completion, customer readiness, and next-action claims reconcile ticket,
  progress, evidence, and scoped worktree state; conflicts remain visible, and
  every worktree snapshot names its timestamp and explicit `historical, not
  live state` limit plus task-owned and excluded path(s), without expanding
  task scope or proving completion. A material proof conflict includes the full
  detail layer even when the operator asks for only a status check.
- [ ] The recap excludes unrelated state, performs no execution, and ends with
  one safe next action, reply posture, or concrete source request.

## Reviewer Prompt

```text
Review the proposed task recap against skills/task-recap/qa_checklist.md.
Return pass, violation, or source_gap for every failed check, citing the exact
source or missing source. Verify that it distinguishes evidence from inference,
preserves failed attempts, and does not overstate completion. Do not execute or
rewrite the underlying task.
```
