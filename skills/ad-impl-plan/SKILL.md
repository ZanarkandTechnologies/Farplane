---
name: ad-impl-plan
description: "Turn a paid-ad directive into an approval-ready canonical campaign ticket with conditional creative routes, Goal Packet handoff, and spend-safe operating gates."
tier: 3
group: marketing
source: local
template_uses:
  skill-template: "0.4.1"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Ad Impl Plan

## Context

Use this skill when a paid-ad directive needs to become one durable campaign
ticket before creative production, Meta setup, or spend begins. It owns the
canonical ticket's paid-ad action graph and approval boundaries. A recognizable
directive produces a `draft` ticket even when setup facts are missing: name
them as blocked action rows rather than returning strategy prose. It does not
write campaign strategy, ad copy, asset plans, a Goal Packet, or any Meta
mutation.

Use [Ad Advisor](../ad-advisor/SKILL.md) for campaign thesis, test matrix,
measurement, and spend review. Use [Goal Advisor](../goal-advisor/SKILL.md)
only after the ticket is approved to compile `program.md` and `progress.md`.
The installed [Meta Ads](../meta-ads/SKILL.md) route remains read-only.
When a reviewable creative or campaign packet actually exists, use
[Worker Artifact Review Request](../worker-artifact-review-request/SKILL.md)
to deliver one phone-readable internal approval request through Telegram. A
draft ticket alone never sends a message.

## Skill Signature

```text
ad_impl_plan(directive, offer?, audience?, platform?, account_binding?,
             brand_kit?, tasty_pack?, constraints?, artifact_owner?)
  -> paid_ad_campaign_ticket + campaign_lock + approval_inventory | blocked_report

state:
  reads(operator directive, approved Brand Kit, optional Tasty Pack, supplied
        creative/landing-page evidence, canonical ticket template, the first-load Todo List guardrails)
  writes(one canonical ticket.md)
owns: paid_ad_campaign_ticket
gates: directive_identifiable; campaign_lock_accepted_or_action_blocked;
       action_rows_complete; conditional_routes_owned; approval_boundaries_visible;
       no_unapproved_spend_or_mutation
routes: ad-advisor | social-content | content-impl-plan | asset-advisor |
        landing-page | goal-advisor | meta-ads | worker-artifact-review-request |
        review
fails: strategy_reimplementation; production_by_default; tasty_pack_required;
       plan_approval_implies_spend; ticket_creates_program; auto_scale_or_pause
```

## Phase Boundary

Create the ticket and stop at `draft | awaiting_approval`. A missing conversion
event, binding, budget, schedule, measurement source, or Ad Advisor receipt
blocks its specific action row and launch readiness—not creation of the ticket.
Return only `blocked_report` when the directive cannot identify an offer or
campaign aim to plan. Do not invoke child skills, generate assets, create
campaigns, activate spend, or schedule a heartbeat merely because they appear
in the action graph. Ticket approval permits only the explicitly admitted local
planning work; each external, generation-cost, or spend-affecting action
retains its own approval gate.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the paid-ad directive and read the first-load Todo List guardrails.
  - [ ] Resolve offer, audience, platform, conversion event, account binding,
        budget cap, schedule, landing-page state, measurement source, and the
        operator's approval policy. Create the draft ticket when the directive
        is identifiable; represent each unknown as a named action-row blocker
        rather than guessing a budget, event, or launch authority.
- [ ] 2. Obtain or block on a campaign lock from [Ad Advisor](../ad-advisor/SKILL.md).
  - [ ] Require one primary hypothesis, falsifier, small interpretable test
        matrix, guard metrics, policy risks, and a draft/paused setup route.
        When the receipt is absent, admit one blocked Ad Advisor row that
        produces it before any creative or setup row unlocks.
  - [ ] Keep `ad-advisor` as the sole owner of campaign settings and
        kill/scale recommendations; record its accepted receipt/reference in
        the ticket instead of synthesizing strategy in this parent plan.
- [ ] 3. Add the paid-ad action graph to one canonical ticket.
  - [ ] Start from [the canonical ticket template](../../tickets/templates/ticket.md).
  - [ ] Render literal `## Summary`, `## Scope`, `## Delta`, `## Change Plan`,
        `## Done`, `## QA Strategy`, `## State`, and `## Links` headings in that
        order. `## Change Plan` is mandatory even when `Delta` is empty; never
        substitute the `Paid Ad Campaign` subheading for it or return only an
        action list or prose blocked report for an identifiable directive.
  - [ ] For every admitted action, name `owner`, `accepted_inputs`,
        `primary_output`, `acceptance_or_blocker`, `approval_gate`, and
        `evidence_writeback`. Use one owner per row; do not write child outputs
        into the parent.
- [ ] 4. Route creative work only when its condition is true.
  - [ ] Treat an approved Brand Kit as identity/policy truth when supplied;
        treat a Tasty Pack as optional, explicitly chosen inspiration.
  - [ ] Route copy and static concepts to [Social Content](../social-content/SKILL.md).
        For reference-led or video production, include three conditional
        action rows in the ticket, in this order: [Content Impl
        Plan](../content-impl-plan/SKILL.md), [Storyboard](../storyboard/SKILL.md),
        then [Asset Advisor](../asset-advisor/SKILL.md). They are planning
        dependencies only until their own gates pass; do not call them, call
        Asset Advisor for copy-only tests, or make a Tasty Pack mandatory.
- [ ] 5. Make approval and measurement boundaries executable.
  - [ ] Separate approval of the plan, creative-generation spend, final
        creative, draft/paused setup, launch, pause, budget change, scale,
        replacement, and every future mutation. Read-only reporting may run
        without approval; it must request approval rather than change delivery.
  - [ ] Add a distinct `plan acceptance` action row before any Goal Advisor,
        creative-production, setup, or launch row. It accepts the ticket and
        campaign-lock reference only; it does not approve any downstream
        action, spend, or Meta mutation.
  - [ ] Include a conditional Goal Advisor row after `plan acceptance` in every
        ticket, including static-only or existing-creative tests. Its sole
        output is a later `program.md` and `progress.md`; it cannot create
        either before its own explicit approval.
  - [ ] When an actual creative or campaign decision packet becomes ready for
        review, add an internal `Worker Artifact Review Request` row. It sends
        one phone-readable Telegram request to Kenji with a single reply
        action; visual creative requires a PNG/JPEG review image and photo
        delivery. The notification does not approve production, setup, launch,
        spend, or a delivery mutation.
  - [ ] Add source of truth, reporting window, evidence path, no-op rule, and
        stop/replan rules to the ticket's `Done` and `QA Strategy`. If any are
        unresolved, add their binding action and preserve the read-only no-op
        rule instead of omitting the operating loop.
- [ ] 6. Hand an approved long-running ticket to [Goal Advisor](../goal-advisor/SKILL.md).
  - [ ] Goal Advisor compiles the ticket into `program.md` and `progress.md`.
        The program's heartbeat reads with Meta Ads, appends evidence, and
        selects `report_now | request_feedback | stop`; a proposed delivery
        change returns to Ad Advisor for a fresh review and then waits for
        explicit approval. That approval does not create a write-capable Meta
        route or authorize a mutation by itself.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Ticket Addition

Render this literal canonical heading skeleton, with no heading omitted or
renamed (including an empty `## Delta` when appropriate). Add the paid-ad
block under `## Change Plan`; do not create a parallel campaign schema or a
pre-approved `program.md`.

```md
## Summary
## Scope
## Delta
## Change Plan
## Done
## QA Strategy
## State
## Links
```

```md
### Paid Ad Campaign

- Platform / account binding:
- Objective / conversion event:
- Offer / landing page:
- Ad Advisor receipt / campaign thesis reference:
- Budget cap / schedule:
- Measurement / guard metrics:
- Brand Kit decision: absent | accepted | blocked
- Tasty Pack decision: absent | choose | augment | reject | blocked

| Order | Owner | Accepted inputs | Primary output | Gate or blocker | Approval gate | Evidence writeback |
| ---: | --- | --- | --- | --- | --- | --- |
```

The ticket records the accepted Ad Advisor receipt rather than a second
strategy artifact. Its `Done` and `QA Strategy` must name the first-live-spend
review, read-only reporting cadence/window and evidence path, factual no-op
rule, and the operation-specific approval policy. It must also contain a
distinct `plan acceptance` row before any Goal Packet, production, setup, or
launch row: plan acceptance accepts only the ticket and campaign-lock
reference, never downstream spend or a mutation. Every ticket also has a
conditional Goal Advisor row immediately after `plan acceptance`, even for a
static-only test, to later compile `program.md` and `progress.md` after an
explicit approval. For reference-led or video work, include conditional rows
for Content Impl Plan, Storyboard, and Asset Advisor even before they are
executable. When a real campaign or creative packet is ready for an internal
decision, include a Worker Artifact Review Request row to send one
phone-readable Telegram approval request; that request is a notification, not
action authority. An unbound item appears as an explicit action-row blocker
with its next owner; it does not disappear from the ticket.

## Templates

- [Meta lead campaign example](examples/meta-lead-campaign/example.md) — load
  when a small first test needs a concrete ticket-shaped reference.

## Gotchas

- Do not treat a Brand Kit as a creative asset inventory or a Tasty Pack as a
  license to copy its source material; Asset Advisor owns those decisions.
- Do not let campaign approval authorize a launch, delivery change, budget
  change, creative replacement, or provider spend.
- Do not let a scheduled check-in invent strategy from metrics; Meta Ads
  reports facts and Ad Advisor owns the resulting recommendation.

## Reference Map

- [Ad Advisor](../ad-advisor/SKILL.md) — campaign strategy, test matrix,
  policy/measurement review, and spend-gated setup handoff.
- [Content Impl Plan](../content-impl-plan/SKILL.md) — use only for
  reference-led or video creative production.
- [Asset Advisor](../asset-advisor/SKILL.md) — use only after a production
  route needs asset inventory, source, rights, or generation decisions.
- [Goal Advisor](../goal-advisor/SKILL.md) — compile the accepted campaign
  ticket into a Goal Packet and delayed check-in program.
- [Meta Ads](../meta-ads/SKILL.md) — factual read-only delivery reports.
- [Worker Artifact Review Request](../worker-artifact-review-request/SKILL.md)
  — deliver one phone-readable, internal Telegram approval request after a
  reviewable creative or campaign packet exists.
- the first-load Todo List guardrails — apply before planning and before return.

## Output

- `paid_ad_campaign_ticket`: one canonical ticket with the campaign lock,
  ordered action graph, proof/measurement contract, and approval inventory.
- `blocked_report`: missing binding, budget, event, measurement, creative
  readiness, policy review, or approval authority with the next owner.
