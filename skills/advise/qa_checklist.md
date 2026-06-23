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

## Preflight

- [ ] The request is a real decision among viable paths, not an obvious direct
  action disguised as advice.
- [ ] The decision is stated in one sentence before options are compared.
- [ ] Evaluation criteria are explicit and relevant to the user's goal,
  constraints, and risk.
- [ ] Evidence needs are known: local-only, supplied evidence, official/current
  source, peer norm, or higher-tier research.
- [ ] The expected output needs a recommendation, not a neutral menu.

## Final Review

- [ ] The answer compares exactly three viable options when three realistic
  options exist.
- [ ] The recommendation is explicit and appears before or with the tradeoff,
  not buried as a weak preference.
- [ ] The accepted tradeoff is named plainly.
- [ ] Evidence gaps are surfaced instead of hidden behind confident prose.
- [ ] The answer routes the direct next owner or next step without ending in a
  vague offer to help.
- [ ] The advice does not invent options, delay an obvious reversible action, or
  perform research synthesis that belongs to a higher-tier workflow.

## Reviewer Prompt

```text
Review the advice against skills/advise/qa_checklist.md.
Return pass, violation, or deferral for each failed check.
Focus on whether the recommendation is explicit, evidence-bounded, and useful.
Do not rewrite the advice unless a violation needs a concrete fix.
```
