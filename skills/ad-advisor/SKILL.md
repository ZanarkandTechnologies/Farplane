---
name: ad-advisor
description: "Turn an advertising goal, offer, audience, and platform binding into a reviewed campaign config, CLI plan, and spend-gated handoff."
tier: 3
group: marketing
source: local
template_uses:
  skill-template: "0.3.7"
  skill-surface-budget: "0.1.0"
allowed-tools: Read, Glob, Grep, web_search
eval: eval_task.json
qa_checklist: qa_checklist.md
---

# Ad Advisor

## Context

Use this skill when the operator wants help designing, checking, or using a paid
ad campaign configuration. It owns ad strategy, campaign settings, review gates,
and tool handoff. It does not own creative drafting, organic posting, account
credential storage, or live spend execution without explicit approval.

For Meta, prefer the official Ads CLI or Marketing API route when it is
available and the caller has supplied an account binding. Treat CLI commands as
external side effects: default to dry-run, draft, or paused campaign creation
until the operator or ticket explicitly approves spend and launch.

## Skill Signature

```text
ad_advisor(ad_goal, offer?, audience?, platform?, account_binding?,
           budget_cap?, campaign_artifacts?, launch_intent?)
  -> campaign_config_review + cli_or_api_plan + spend_gated_handoff
state:
  reads(public platform docs when current rules matter, supplied offer/creative,
        project bindings, private credential readiness checks when available,
        qa_checklist.md)
  writes(review packet or draft config only when caller owns an output path)
gates:
  account_binding_resolved_or_blocked; spend_cap_named; launch_approval_explicit;
  primary_hypothesis_named; measurement_method_named; policy_risks_labeled;
  creative_and_landing_page_ready; no_secret_echo; dry_run_before_mutation
routes:
  social-content | landing-page | metric-advisor | x-account |
  instagram-account | review
fails:
  launching spend without approval; hiding account IDs or budget assumptions;
  treating ad copy as approved creative; copying secrets into artifacts;
  using stale platform rules as fact
```

## Phase Boundary

Keep campaign configuration advice and dry-run planning inline. Use
`social-content` for ad copy or creative concepts, `landing-page` for offer or
landing-page work, account skills for owned social account publishing/metrics,
and `review` before first live spend or durable campaign config changes.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the ad goal and platform boundary.
  - [ ] Resolve platform, offer, conversion event, audience, geography, budget
        cap, schedule, creative assets, landing page, account binding, and
        launch intent.
  - [ ] Read `qa_checklist.md` as preflight guardrails.
  - [ ] Write the campaign thesis before settings: audience pain or demand
        signal, offer promise, channel reason, conversion event, creative angle
        families, market awareness, market sophistication, category entry
        point, distinctive brand asset, primary hypothesis, and what would make
        the campaign obviously wrong.
  - [ ] If the platform rules, CLI behavior, or ad specs affect the answer, use
        current official docs or `web_search` before giving exact guidance.
- [ ] 2. Check spend and account gates.
  - [ ] Require explicit approval before live launch, budget activation, or
        account mutation.
  - [ ] Keep secrets in private runtime env or Doppler; store only non-secret
        aliases, account IDs, and policy coordinates in bindings when needed.
  - [ ] If credentials, account access, payment, pixels, events, or business
        permissions are missing, return a blocked setup report.
- [ ] 3. Shape the campaign config.
  - [ ] Define objective, conversion event, audience hypothesis, exclusions,
        placements, budget, schedule, creative variants, landing-page fit,
        success metric, guard metrics, and stop conditions.
  - [ ] Build a small test matrix: audience slice, angle, creative asset, offer
        promise, isolated variable, matched setup, landing page, metric, guard
        metric, learning-phase or platform-stability risk, read window/spend,
        kill rule, scale rule, and next iteration for each variant.
  - [ ] Keep the first test narrow enough to learn one thing: avoid mixing new
        audience, creative, offer, and landing-page changes in a way that makes
        the result uninterpretable.
  - [ ] Label uncertain assumptions and policy risks, especially sensitive
        targeting, employment/housing/credit-like categories, health, finance,
        or personal-attribute claims.
- [ ] 4. Produce the tool handoff.
  - [ ] For Meta, produce an Ads CLI or Marketing API dry-run plan when the
        account binding exists; keep command examples redacted and non-secret.
  - [ ] For other platforms, produce a manual setup checklist or route to the
        relevant account/platform skill when one exists.
  - [ ] Prefer paused/draft campaign creation before active delivery.
- [ ] 5. Define measurement and review.
  - [ ] Name the primary success metric, guard metrics, attribution method,
        and source of truth; route metric uncertainty through the appropriate
        measurement advisor after the campaign packet exists.
  - [ ] Select the measurement method: monitoring attribution for status,
        A/B or split test for variant comparison, holdout/lift for causal
        incrementality, or blocked until a real measurement source exists.
  - [ ] Name reporting cadence, source of truth, evidence to capture, and the
        rule for killing or iterating the campaign.
  - [ ] Use `review` before first live spend, new account setup, or durable
        config changes.
- [ ] 6. Finish-check the ad packet.
  - [ ] Apply `qa_checklist.md` to the finished packet.
  - [ ] Campaign config, assumptions, policy risks, budget cap, launch gate,
        dry-run evidence, and next owner are visible.
  - [ ] No command or artifact contains credentials or unapproved live-spend
        actions.
  - [ ] The packet can be used to review, configure, or block the campaign
        without hidden chat context.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Campaign config review:

```text
Ad goal:
Platform:
Account binding:
Offer:
Audience:
Objective / event:
Primary hypothesis:
Creative variants:
Landing page:
Budget cap:
Schedule:
Policy risks:
Measurement:
Measurement method:
Dry-run / CLI plan:
Launch gate:
Stop / iterate rule:
Learning or stability risk:
Next owner:
```

- [examples/meta-lead-campaign/example.md](examples/meta-lead-campaign/example.md)
  - compact example of a Meta Ads CLI dry-run handoff.

## Gotchas

- Do not launch, schedule, or activate paid campaigns without explicit approval.
- Do not treat Meta Ads CLI availability as credential readiness; account,
  business, payment, app, token, and permission setup may still block.
- Do not use old platform rules for live setup when current docs can change the
  config.
- Do not let ad targeting imply sensitive personal attributes.

## Reference Map

- [qa_checklist.md](qa_checklist.md) - read before campaign planning and apply
  before completion.
- [social-content](../social-content/SKILL.md) - use for ad copy,
  creative concepts, variants, captions, hooks, or asset handoffs.
- [landing-page](../landing-page/SKILL.md) - use when offer or
  landing-page fit is the blocker.
- [metric-advisor](../metric-advisor/SKILL.md) - use for success
  metrics, guard metrics, anti-metrics, and measurement routes.
- [x-account](../x-account/SKILL.md) and
  [instagram-account](../instagram-account/SKILL.md) - use for
  owned organic publishing or account metrics, not paid campaign launch.

## Output

- `campaign_config_review`: recommended settings, assumptions, risks, budget,
  measurement, and stop rules.
- `cli_or_api_plan`: dry-run or paused/draft setup handoff with redacted command
  examples and required bindings.
- `blocked_report`: missing account binding, credentials, permissions, payment,
  creative, landing page, metrics, or approval.
