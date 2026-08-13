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

- [ ] The recap identifies one task boundary and lists the authoritative sources
  used; an unavailable ticket, artifact, or thread is an explicit source gap.
- [ ] Durable records outrank transcript memory, and observed fact, decision,
  inference, and stale snapshot are distinguishable in the recap.
- [ ] Every material change has a source-backed `Before` / `After` / `Example`,
  and every problem retains its attempts, observed outcome, and disposition.
- [ ] Completion, customer readiness, and next-action claims reconcile ticket,
  progress, evidence, and scoped worktree state; conflicts remain visible.
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
