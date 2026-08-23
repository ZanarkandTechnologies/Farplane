---
title: Ad Impl Plan QA Checklist
owner: ad-impl-plan
status: active
kind: qa-checklist
applies_to:
  - paid-ad-campaign-tickets
  - approval-inventories
---

# Ad Impl Plan QA Checklist

Read before compiling a paid-ad campaign ticket and apply again before calling
it ready. Use an independent reviewer for a campaign that can spend money.

## Checks

1. **Canonical ticket** — exactly one ticket owns the campaign scope, action
   graph, `Done`, and `QA Strategy`; `program.md` and `progress.md` remain a
   later Goal Advisor handoff rather than a parallel plan. Every ticket,
   including an existing-creative test, retains a conditional Goal Advisor row
   after plan acceptance.
2. **Campaign lock** — platform, account binding, objective/event, offer,
   audience, budget cap, primary hypothesis, falsifier, measurement, guard
   metrics, policy risks, creative/landing-page readiness, and first test are
   bound or visibly blocked.
3. **Conditional ownership** — each admitted row has one owner, accepted
   inputs, primary output, acceptance/blocker, approval gate, and evidence
   writeback. Ad Advisor owns strategy; Social Content owns copy; Content Impl
   Plan owns production planning; Asset Advisor owns asset decisions; Meta Ads
   owns facts; no unnecessary route is admitted.
4. **Creative-source integrity** — Brand Kit is accepted identity/policy truth
   when provided; Tasty Pack is optional inspiration with an explicit
   choose/augment/reject/block decision. Neither authorizes use of unreviewed
   reference assets.
5. **Permission integrity** — plan approval, generation-cost approval, final
   creative approval, draft/paused setup, launch, pause, budget change, scale,
   replacement, and any Meta mutation are separate where applicable. No
   observation, ticket state, or campaign result implies an approved write.
6. **Check-in integrity** — the Goal handoff defines bounded read-only evidence,
   a no-op path, written recommendations, and operation-specific feedback
   requests. It never describes Meta Ads as a write-capable executor.
7. **Approval delivery** — a reviewable creative or campaign packet may use
   Worker Artifact Review Request for one internal, phone-readable Telegram
   decision. A visual decision has a PNG/JPEG review image and photo receipt;
   the notification is never production, spend, launch, or mutation authority.

## Reviewer Output

Return each failure as `violation | deferral`, cite the ticket section or
action row, name the smallest repair, and finish with `pass | revise | block`.
