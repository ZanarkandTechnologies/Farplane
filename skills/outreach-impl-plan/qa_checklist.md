---
title: Outreach Impl Plan QA Checklist
owner: outreach-impl-plan
status: active
kind: qa-checklist
applies_to:
  - outreach-campaign-tickets
  - advisor-action-lists
---

# Outreach Impl Plan QA Checklist

Read before campaign planning and apply again to the finished campaign ticket.
Use an independent reviewer for material or customer-facing campaigns.

## Checks

1. **Grounded campaign thesis** — objective, audience, relationship strategy,
   candidate evidence, value hypothesis, learning questions, falsifiers, and
   stop conditions are explicit; inferred pain and response likelihood remain
   labeled rather than becoming campaign facts.
2. **Executable advisor program** — each action has an owner, input, output,
   acceptance check, blocker, approval gate, and evidence writeback; the parent
   sequences child skills without reimplementing them. Evidence writeback must
   name a discoverable report, CRM proposal, campaign state update,
   event/observation, proof artifact, or review receipt—not “record result.”
   Missing table columns fail even when equivalent prose appears elsewhere.
   `same as Wave 1`, arrows, and multi-skill action owners fail: admitted child
   work needs one owner and one complete row; unadmitted later waves get only a
   parent re-planning row that produces future rows.
3. **Learning-sized waves** — Wave 1 is small, shares a testable hypothesis,
   produces evidence before expansion, and has entry, exit, promotion, review,
   and stop rules; later waves change when earlier evidence changes.
4. **State and measurement integrity** — CRM receives only sourced durable
   relationship truth and validated opportunities; mutable campaign stages
   remain in the campaign artifact; metrics cover replies, corrections,
   validated problems, calls, partnerships, or revenue rather than sends alone.
   Every planned send/reply event binds stable campaign, person, and interaction
   `offer_id` values; a first-value `offer_id` is attribution only and does not
   imply a commercial offer or opportunity.
5. **Permission integrity** — plan approval, CRM writes, private data,
   enrichment, spend, artifact production, exact sends, publishing, proposals,
   and promises are separately visible; no planned action is described as
   already executed without evidence. When contact is in scope, a distinct
   post-review send action names the exact approved person, artifact, message,
   and channel, and produces a send-or-stop receipt before metric recording.

## Reviewer Output

Return each failed check as `violation | deferral`, cite exact evidence, name
the smallest repair, and finish with `pass | revise | block`.
