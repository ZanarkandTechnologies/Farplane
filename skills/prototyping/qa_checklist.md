---
title: Prototyping QA / Review Checklist
owner: prototyping
status: active
kind: qa-checklist
applies_to:
  - prototype-notes
  - scale-decisions
---

# Prototyping QA / Review Checklist

Use this checklist before choosing a prototype slice and again before expanding
scope. For broad rollout, batch edits, automation, or architecture changes, ask
an independent reviewer/subagent to apply it to the Prototype Note.

```text
prototype_check(hypothesis, slice, evidence, promote_rule)
  -> pass | violation | deferral
```

## Preflight

- [ ] The scale risk is named: data volume, workflow breadth, file count,
  users, architecture, automation, polish, research breadth, or operational
  complexity.
- [ ] The hypothesis can be falsified by the prototype.
- [ ] The first slice is representative of the real risk, not merely convenient
  or pleasant to demo.
- [ ] Real examples, files, users, records, edge cases, or failure modes are
  used where possible.
- [ ] Manual or non-scalable work is considered when it would reveal the pattern
  faster than automation.

## Final Review

- [ ] The Prototype Note names hypothesis, scale risk, representative slice,
  evidence, promote criteria, revise/stop criteria, and next scale step.
- [ ] Prototype-only shortcuts are labeled and cannot be mistaken for
  production readiness.
- [ ] The evidence supports the proposed next scale; otherwise the note chooses
  revise, shrink, split, or stop.
- [ ] The next step follows `1 -> 10 -> 100` or explains why a different scale
  is safer.
- [ ] No broad batch command, automation, or rollout is recommended without
  sample evidence.

## Reviewer Prompt

```text
Review the Prototype Note against skills/prototyping/qa_checklist.md.
Return pass, violation, or deferral for each failed check.
Focus on representativeness, falsifiability, and whether scale is justified.
Do not expand the prototype into the domain workflow.
```
