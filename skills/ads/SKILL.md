---
name: ads
description: "Use for \"run ads\", \"set up a Meta campaign\", \"how are my ads doing\" or \"test this ad\": a one-variable campaign plan created paused, or a read-only ad report with facts apart from advice."
source: local
department: marketing
capability:
  kind: integration
methods:
  - id: ads:plan
    class: artifact
    output: campaign-plan
  - id: ads:launch
    class: integration
    output: paused-setup-receipt
  - id: ads:report
    class: integration
    output: ads-report
template_uses:
  skill-template: "0.6.5"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash
---

# Ads

## Context

Use this when the operator wants paid ads planned, set up, or read: a campaign
thesis and test matrix, a paused setup after approval, or a factual account
report. One pass runs one mode and returns one packet. It does not write ad
copy (`copywriting`), make images (`ai-image`) or clips (`ai-video`), plan
organic posts (`social-content`), post organically (`zernio`), or fix the
landing page (`landing-page`). Meta is the bound platform; other platforms get
a manual setup checklist. Nothing here activates spend without a named approval.

## Skill Signature

```text
ads(goal | report_request, mode?: plan | launch | report, offer?, audience?,
    account_binding?, budget_cap?, creative?, landing_page?, date_window?)
  -> campaign_plan | paused_setup_receipt | ads_report | blocked_report
reads: offer, creative, landing page, binding aliases, current Meta docs, the issue
does: plans a one-variable test, creates paused objects after approval, or reads
writes: the plan on the private-repo GitHub issue, else .farplane/ads/<date>-<slug>/
returns: the packet, its approval gates, source gaps, and the next owner
```

## Modes

- `plan`: thesis, config, one-variable matrix, measurement, approval inventory.
- `launch`: dry run, then paused or draft creation after paused-setup approval.
- `report`: read-only Meta Ads CLI report of accounts, inventory, or insights.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Pick the mode and bind the campaign.**
  `request -> mode + bound facts + named blockers | blocked_report`

  Rule: "How are my ads doing", "pull the numbers", "list my accounts" is
  `report`; "create it", "set it up" with an accepted plan is `launch`;
  everything else, including any pause, budget, or scale request, is `plan`.
  Bind platform, offer, conversion event, audience, geography, budget cap,
  schedule, creative, landing page, account binding, and launch intent. Each
  unknown becomes a named blocker with its next owner, never a guess. Check
  current official Meta Ads CLI and Marketing API docs before giving exact
  command, field, or permission guidance.

  Example: "pause the loser and add 50 a day to the winner" -> `plan` (a delivery
  change needs a fresh review and its own approval), not a CLI call.

  Assert:
  - No budget, event, or account binding is invented.
  - A write or spend request never runs in `report` mode.
- [ ] **N2 — plan: write the thesis and a one-variable test matrix.**
  `bound facts -> thesis + hypothesis + falsifier + test matrix + policy risks`

  Rule: Write the thesis before settings (demand signal, offer promise, channel
  reason, conversion event, angle families). Each test changes one variable
  only: audience, creative, offer, or landing page; the rest is matched. Every
  row names the hypothesis, the isolated variable, the read window, and the
  kill and scale rule written before launch. Label policy risks and reframe
  sensitive targeting to observable business context. Load
  [campaign plan](references/campaign-plan.md) for the columns and
  [market signals](references/market-signals.md) for demand and competitor ads.

  Example: three copy angles, same audience, offer, page, and budget -> learns
  which angle wins; a new audience plus new creative learns nothing.

  Assert:
  - The first test isolates one variable and names its kill and scale rule.
  - No targeting implies hardship, health, finances, or another personal trait.
- [ ] **N3 — plan: name the measurement method and route the creative.**
  `thesis + matrix -> measurement method + metrics + creative routes`

  Rule: Name the method up front: platform attribution (monitoring only),
  A/B or split test (variant comparison), or holdout or lift (did ads cause
  sales); with no real source the plan is blocked on measurement. Take success,
  guard, and anti-metrics from the
  [metric card](../goal-advisor/references/metrics.md). Add a creative row only
  when its condition holds: copy to `copywriting`, images to `ai-image`, clips
  to `ai-video`, organic variants to `social-content`, page fit to
  `landing-page`. Approved creative is reused.

  Assert:
  - Platform attribution is never presented as proof of causation.
  - The plan does not draft copy or assets itself.
- [ ] **N4 — plan: record the plan and its approval inventory on the issue.**
  `plan -> issue block + ordered action rows + approval inventory`

  Rule: Put the issue block under the issue body's `## Change Plan` on the
  business's private repo; budgets, prices, and account IDs never go on a
  public repo. Start with a `plan acceptance` row. Plan approval is not spend
  approval: creative spend, final creative, paused setup, launch, and each
  later pause, budget change, or scale is its own approval. A multi-day run gets
  a conditional `goal-advisor` row after plan acceptance. A scheduled check-in
  reads and recommends; it never pauses or scales by itself.

  Assert:
  - Every external, spend, or delivery action has its own approval row.
  - No row lets a report or an earlier approval change delivery.
- [ ] **N5 — launch: dry run, then create paused after approval.**
  `accepted plan + paused-setup approval -> dry run + paused objects | blocked`

  Rule: Confirm a write-capable route from current official docs (official
  Ads CLI or Marketing API, token with `ads_management`); the installed
  `meta-ads-open-cli` is read-only and cannot create. Run the dry run or
  validation first, then create every campaign, ad set, and ad paused or draft.
  Activating delivery needs a separate explicit approval naming the account,
  budget, creative, landing page, and launch window; before first live spend run
  `qa` outbound on every ad preview and its funnel (page, form, follow-up emails),
  then `review`. With no verified route, return a manual paused setup checklist.

  Assert:
  - Nothing is created active; the dry-run output is kept, redacted.
  - "Just get it running" is not launch approval.
- [ ] **N6 — report: read the account read-only.**
  `report request -> readiness + bounded read + observed facts | blocked`

  Rule: Run `farplane run -- python3 skills/ads/scripts/check_config.py`, then
  `me` and `ad-accounts`. A valid login or `me` response does not prove
  `ads_read`; the account must appear in `ad-accounts` before a report is
  claimed. Bound every insight read with `--date-preset` or `--start`/`--end`
  and run only the commands in [Meta CLI](references/meta-cli.md). Keep metric
  names and currencies; unavailable fields are source gaps, not zero. A blocked
  report names the checker, `META_ADS_ACCESS_TOKEN`, and the intended query.

  Assert:
  - No account data is invented; every figure carries its scope and window.
  - No create, pause, upload, or budget command is issued.
- [ ] **N7 — Return the packet and the next owner.**
  `mode result -> packet + gates + gaps + next owner`

  Rule: Keep observed facts apart from recommendations; a report ends with
  `Decision boundary:` factual data only, decisions go to `plan` mode. Name
  the command, timestamp, scope, and redacted credential source. Tokens and
  account IDs never enter a tracked file.

  Assert:
  - Facts and advice sit in separate sections.
  - No secret or raw account ID appears in a tracked artifact.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- A CLI that is installed is not credential readiness: business access,
  payment, pixel, events, and token scopes can still block.
- Changing audience, creative, offer, and page in one test makes the result uninterpretable.
- Cheap leads are an anti-metric when lead quality is the goal.
- Small budgets may never leave the learning phase; read after the window.
- Never bypass the read-only boundary with `curl` or raw Graph API calls.

## Reference Map

- [campaign plan](references/campaign-plan.md) - load in N2-N4: thesis
  fields, test matrix columns, measurement table, policy risks, issue block,
  approval inventory, creative routes, operating loop.
- [Meta CLI](references/meta-cli.md) - load in N5 and N6: read commands,
  setup, token scopes, and the write-route boundary.
- [config checker](scripts/check_config.py) - run before every live read.
- [Meta lead campaign example](examples/meta-lead-campaign/example.md) -
  calibrates a config review and issue block.
- Routes: [copywriting](../copywriting/SKILL.md) and its
  [final pass](../copywriting/references/final-pass.md), [ai-image](../ai-image/SKILL.md),
  [ai-video](../ai-video/SKILL.md), [social-content](../social-content/SKILL.md),
  [landing-page](../landing-page/SKILL.md), [zernio](../zernio/SKILL.md),
  [goal-advisor](../goal-advisor/SKILL.md).

## Output

```yaml
mode: plan | launch | report
campaign_plan: <thesis, hypothesis, falsifier, matrix, measurement method, policy risks, issue link>
approval_inventory: <plan | creative spend | final creative | paused setup | launch | each later change>
paused_setup_receipt: <redacted dry run, paused object list, route used>
ads_report: <scope, window, observed facts, source gaps, read-only command, timestamp>
recommendations: <kept apart from facts; plan mode only>
blocked: <missing binding, token scope, route, event, measurement, or approval + next owner>
next_owner: copywriting | ai-image | ai-video | landing-page | goal-advisor | review | operator
```
