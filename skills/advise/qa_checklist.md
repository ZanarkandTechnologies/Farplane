---
title: Advise QA / Review Checklist
owner: advise
status: active
kind: qa-checklist
applies_to:
  - advice
  - recommendations
---

# Advise QA / Review Checklist

Use this checklist before giving material advice and again before claiming the
recommendation is ready. For high-stakes, durable, or expensive decisions, ask
an independent reviewer/subagent to apply it to the final recommendation.

```text
advise_check(decision, options, recommendation, evidence?)
  -> pass | violation | deferral
```

## Checklist

- [ ] The request is a real decision among viable paths, not an obvious direct
  action, and the expected output needs a recommendation rather than a neutral
  menu.
- [ ] The decision and evaluation criteria are stated before comparing options.
- [ ] Evidence needs are known and any gaps are surfaced instead of hidden
  behind confident prose.
- [ ] The answer compares exactly three viable options when three realistic
  options exist, then recommends one clearly and names the accepted tradeoff.
- [ ] The answer routes the direct next owner or next step without inventing
  options, delaying an obvious reversible action, or performing higher-tier
  research synthesis.

## Reviewer Prompt

```text
Review the advice against skills/advise/qa_checklist.md.
Return pass, violation, or deferral for each failed check.
Focus on whether the recommendation is explicit, evidence-bounded, and useful.
Do not rewrite the advice unless a violation needs a concrete fix.
```
