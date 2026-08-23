---
title: Meta Ads CLI Read-Only Guide
owner: meta-ads
status: active
source_cli: meta-ads-open-cli
---

# Meta Ads CLI Read-Only Guide

Load this reference only after the `meta-ads` read branch is selected. The
installed `meta-ads-open-cli` package is a read-only wrapper around the Meta
Marketing API. Run every command through Farplane so `META_ADS_ACCESS_TOKEN`
comes from Doppler rather than shell history or a tracked file.

```sh
farplane run -- meta-ads-open-cli me
farplane run -- meta-ads-open-cli ad-accounts
```

Use a discovered or explicitly supplied account/entity ID only in the live
command or caller-owned private/evidence path. Do not copy it into a skill,
README, or general tracked report.

## Read Commands

```sh
# Inventory
farplane run -- meta-ads-open-cli businesses
farplane run -- meta-ads-open-cli ad-account <account-id>
farplane run -- meta-ads-open-cli account-users <account-id> --business <business-id>
farplane run -- meta-ads-open-cli campaigns <account-id> --status ACTIVE
farplane run -- meta-ads-open-cli campaign <campaign-id>
farplane run -- meta-ads-open-cli adsets <account-id> --campaign <campaign-id>
farplane run -- meta-ads-open-cli adset <adset-id>
farplane run -- meta-ads-open-cli ads <account-id> --adset <adset-id>
farplane run -- meta-ads-open-cli ad <ad-id>
farplane run -- meta-ads-open-cli creatives <account-id>
farplane run -- meta-ads-open-cli creative <creative-id>

# Delivery and performance
farplane run -- meta-ads-open-cli insights <account-id> --date-preset last_7d --level campaign
farplane run -- meta-ads-open-cli insights-date <account-id> --start 2026-08-01 --end 2026-08-07

# Measurement and connected assets
farplane run -- meta-ads-open-cli pixels <account-id>
farplane run -- meta-ads-open-cli pixel-events <pixel-id>
farplane run -- meta-ads-open-cli custom-conversions <account-id>
farplane run -- meta-ads-open-cli custom-audiences <account-id>
farplane run -- meta-ads-open-cli custom-audience <audience-id>
farplane run -- meta-ads-open-cli saved-audiences <account-id>
farplane run -- meta-ads-open-cli reach-estimate <account-id> --targeting '<targeting-json>'
farplane run -- meta-ads-open-cli pages
farplane run -- meta-ads-open-cli page <page-id>
farplane run -- meta-ads-open-cli instagram-accounts <page-id>
farplane run -- meta-ads-open-cli lead-forms <page-id>
farplane run -- meta-ads-open-cli leads <form-id>
```

For an account/campaign/ad-set/ad-specific report, use the same `insights`
command with that exact entity ID. Request only the date range, level,
breakdowns, fields, and time increment needed for the question. Read results
are JSON by default; `--format compact` is available when a one-line JSON
record is needed for a caller-owned ignored evidence file.

`insights` defaults to `impressions`, `reach`, `clicks`, `cpc`, `cpm`, `ctr`,
`spend`, `actions`, `cost_per_action_type`, `conversions`,
`conversion_values`, and `frequency`. State `date_start` and `date_stop` from
the returned data in a successful report. If an unbound clean-room request
blocks the call, retain the exact date preset and include the intended command
and these fields as source gaps; do not invent calendar dates.

## Setup and Blocking

Install the CLI once with:

```sh
npm install -g meta-ads-open-cli
```

Store the access token only in Doppler under `META_ADS_ACCESS_TOKEN`, then
verify the runtime without displaying it:

```sh
farplane run -- python3 skills/meta-ads/scripts/check_config.py
farplane run -- meta-ads-open-cli me
farplane run -- meta-ads-open-cli ad-accounts
```

The token needs `ads_read` and access to the selected Meta ad account. A
successful `me` response alone is insufficient; `ad-accounts` must return the
account before an account report is claimed.

The checker reports `publish_ready: false` by design: this package has no
write branch, so a read-capable token never authorizes mutations. `ready: true`
means all supported read capabilities are available.

## Boundary

Do not use `curl`, a Marketing API SDK, or a different CLI to create or modify
campaigns through this skill. Route any write intent to `ad-advisor`, where
budget, policy, approval, and paused/draft gates are reviewed.
