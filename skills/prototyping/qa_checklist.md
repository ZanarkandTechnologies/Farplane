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

## Checklist

- [ ] The scale risk and falsifiable hypothesis are named.
- [ ] The first slice is representative of the real risk and uses real examples,
  files, users, records, edge cases, or failure modes where possible.
- [ ] Manual or non-scalable work is considered when it would reveal the pattern
  faster than automation.
- [ ] The Prototype Note names evidence, promote criteria, revise/stop criteria,
  next scale step, and any prototype-only shortcuts.
- [ ] The next step follows `1 -> 10 -> 100`, or explains a safer scale, and no
  broad batch command, automation, or rollout is recommended without sample
  evidence.

## Reviewer Prompt

```text
Review the Prototype Note against skills/prototyping/qa_checklist.md.
Return pass, violation, or deferral for each failed check.
Focus on representativeness, falsifiability, and whether scale is justified.
Do not expand the prototype into the domain workflow.
```
