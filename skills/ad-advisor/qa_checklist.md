---
title: Ad Advisor QA Checklist
owner: ad-advisor
status: active
kind: qa-checklist
applies_to:
  - ad-advisor
---

# Ad Advisor QA Checklist

Use this checklist before planning a paid campaign and again before claiming a
campaign packet is ready for review, dry-run setup, or launch approval.

```text
ad_advisor_check(campaign_packet, launch_intent)
  -> pass | revise | blocked
```

## Preflight

- [ ] Platform, offer, audience, conversion event, account binding, budget cap,
  creative/landing-page readiness, measurement source, and launch intent are
  bound or blocked.

## Campaign Checks

- [ ] The campaign thesis is visible: audience demand signal, offer promise,
  channel reason, conversion event, creative angle families, market awareness,
  primary hypothesis, distinctive brand asset when growth-oriented, and falsifier.
- [ ] The packet includes a test matrix with audience slice, angle, creative,
  offer promise, isolated variable, matched setup, measurement method, metric,
  guard metric, kill/scale rule, and next iteration; each variant can teach one
  interpretable lesson.
- [ ] Spend and mutation gates are explicit: dry-run or paused/draft setup
  first, no active launch without approval, no secrets in artifacts, and
  account/payment/permission blockers named.
- [ ] Policy and measurement risks are labeled, especially sensitive targeting,
  personal-attribute claims, regulated categories, attribution gaps, weak
  landing-page fit, platform learning/stability risk, over-narrow growth
  targeting, or creative that is not approved final copy.

## Reviewer Prompt

```text
Review the campaign packet against skills/ad-advisor/qa_checklist.md.
Return pass, revise, or blocked. Focus on campaign thesis, test matrix,
spend gate, platform/account readiness, policy risk, and measurement fit.
```
