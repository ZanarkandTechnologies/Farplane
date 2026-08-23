---
name: meta-ads
description: "Turn a bound Meta ad account and reporting request into a read-only account, delivery, or insight report through the Meta Ads CLI."
tier: 3
group: marketing
source: local
capability:
  kind: integration
methods:
  - id: meta-ads:report
    class: integration
    output: meta-ads-report
template_uses:
  skill-template: "0.4.1"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Grep, Glob, Bash
---

# Meta Ads

## Context

Use this skill for read-only Meta account discovery, inventory, delivery, and
performance analysis through `meta-ads-open-cli`. It owns a factual
`meta_ads_report`; [ad-advisor](../ad-advisor/SKILL.md) owns strategy,
campaign configuration, policy review, and every spend-affecting action.

Use only private runtime credentials injected with `farplane run -- <command>`.
Never write tokens, raw credential responses, or account IDs to tracked files.
The installed CLI is intentionally read-only; a request to create, activate,
pause, delete, upload, or change a budget is outside this skill and must route
to `ad-advisor` with explicit approval.

## Skill Signature

```text
meta_ads_read(action, account_binding?, date_window?, entity_id?, output_path?)
  -> meta_ads_report + redacted_command_evidence | blocked_report
state:
  reads(private runtime META_ADS_ACCESS_TOKEN, supplied account/entity IDs);
  writes(only caller-owned ignored or ticket-scoped output paths)
owns: factual read-only Meta Ads CLI report
gates: cli_ready; read_token_ready; read_only_command; account_or_entity_resolved;
       no_secret_or_account_id_in_tracked_artifact
routes: ad-advisor | metric-advisor | review
fails: mutation attempt; invented account data; unbounded data pull;
       secret/account-ID persistence
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Route the request.
  - [ ] Accept `verify_access`, `list_accounts`, account/campaign/ad-set/ad
        inventory, creative/pixel/audience/page/lead-form inspection, or an
        insight report with a bounded entity and date window.
  - [ ] Route campaign creation, delivery changes, budget changes, uploads,
        or launch requests to [ad-advisor](../ad-advisor/SKILL.md).
  - [ ] For a write/spend request, hand `ad-advisor` the observed entity data
        and requested change, then require its campaign thesis, account binding,
        budget cap, policy and measurement review, dry-run/paused setup, and
        explicit launch approval. Do not offer a partial mutation plan here.
- [ ] 2. Bind the safe read context.
  - [ ] Run `farplane run -- python3 skills/meta-ads/scripts/check_config.py`.
  - [ ] If a clean-room or otherwise unavailable private runtime prevents that
        command from running, return a blocked report that names this exact
        command, `META_ADS_ACCESS_TOKEN`, and the next read-only account
        discovery command; do not merely say access is missing.
  - [ ] Resolve an exact supplied entity ID or discover accessible accounts with
        `farplane run -- meta-ads-open-cli ad-accounts`; do not store the result
        in a tracked file.
  - [ ] Require `--date-preset` or `--start`/`--end` for insight requests;
        default to the smallest useful window rather than an unbounded pull.
- [ ] 3. Produce the `meta_ads_report`.
  - [ ] Run only the read-only commands listed in
        [CLI guide](references/cli.md), through `farplane run --`.
  - [ ] Keep results in the response or a caller-owned ignored/ticket evidence
        path; summarize facts, time window, entity scope, and source command.
  - [ ] For `last_7d`, retain the exact `--date-preset last_7d` request and
        state the returned `date_start`/`date_stop` range when data is available.
        Report the available delivery fields (`impressions`, `reach`, `clicks`,
        `cpc`, `cpm`, `ctr`, `spend`, `actions`, `cost_per_action_type`,
        `conversions`, `conversion_values`, `frequency`). A blocked report
        retains that date preset and names the intended query (`farplane run --
        meta-ads-open-cli insights <account-id> --date-preset last_7d --level
        campaign`) and fields as unavailable rather than inventing dates.
- [ ] 4. Apply the reporting gate.
  - [ ] Preserve reported metric names and currencies; label unavailable fields
        as source gaps rather than treating them as zero.
  - [ ] Separate observed results from recommendations. Route experiment,
        targeting, creative, attribution, or spend judgments to `ad-advisor` or
        `metric-advisor`.
- [ ] 5. Return evidence and the next owner.
  - [ ] Name the read-only command, timestamp, scope, and redacted credential
        source; apply the first-load Todo List guardrails before returning.
  - [ ] End every report, including a blocked report, with `Decision boundary:`
        factual data only; optimization, targeting, creative, budget, status,
        or spend decisions route to `ad-advisor`.
  - [ ] Return a blocked report for unavailable CLI/token/account access with
        its exact safe next command; never substitute guessed campaign data.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

```text
meta_ads_report
Request:
Scope / entity:
Date window:
Observed results:
Source gaps:
Read-only evidence:
Next owner:
```

## Gotchas

- A valid Meta identity does not prove `ads_read` access or an accessible ad
  account; verify both before promising a report.
- Treat account IDs as private operational context: report aliases or redacted
  IDs outside a caller-owned private/evidence path.
- The CLI supports reads only. Do not use raw Graph API calls to bypass this
  skill's mutation boundary.

## Reference Map

- [CLI guide](references/cli.md) - load after choosing a read-only command or
  diagnosing CLI/token setup.
- [config checker](scripts/check_config.py) - run before every live account
  read to confirm the injected token and installed CLI without revealing either.
- [ad-advisor](../ad-advisor/SKILL.md) - use for campaign decisions, config,
  policy review, or any action that might spend money.
- [metric-advisor](../metric-advisor/SKILL.md) - use when interpreting a report
  requires metric selection, guard metrics, or causal claims.

## Output

- `meta_ads_report`: bounded, factual account/inventory/insight result with
  read-only evidence and source gaps.
- `blocked_report`: missing CLI, token, scope, account access, entity ID, or
  date window, with a non-secret remediation step.
