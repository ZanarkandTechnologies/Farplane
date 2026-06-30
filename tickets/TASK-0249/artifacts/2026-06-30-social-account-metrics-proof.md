---
title: Social Account Metrics Proof Plan
owner: TASK-0249
status: active
kind: proof-plan
updated_at: 2026-06-30
skills:
  - x-account
  - instagram-account
---

# Social Account Metrics Proof Plan

## Target Behavior

Farplane account skills can read social feedback data for KPI snapshots without
posting, scraping broadly, leaking secrets, or inventing unavailable metrics.

Good proof establishes that:

- Missing credentials produce a blocked report with redacted setup guidance.
- Live credentials let a read-only script fetch account/profile metrics and
  write Farplane KPI observations.
- Agents using the skills select the metrics branch and do not treat publish or
  broad-read workflows as part of KPI refresh.

Good proof falsifies:

- A skill claims metrics without a source.
- A skill writes fake zeros for unavailable API fields.
- A skill prints tokens or writes raw credential-bearing responses.
- A skill routes KPI refresh to posting, scraping, or content drafting.

## Case Matrix

| case_id | behavior | fixture_state | oracle | surface | owner_if_fails |
| --- | --- | --- | --- | --- | --- |
| x_missing_credentials | X metrics request with no bearer token | `~/.codex/private/social.env` lacks X read token | blocked status, missing key names only, no metric invention | script smoke + eval row | `skills/x-account` config gate |
| x_live_read | X account metrics request with bearer token and account identity | private env has X bearer token plus user id or username | KPI observations for `x_followers` and available `x_likes` / `x_views`; redacted endpoint evidence | live integration smoke + eval row | `skills/x-account` fetch script/API reference |
| x_post_id_read | X post metrics request with one or more post IDs | private env has X bearer token plus user id or username | KPI observations for returned `x_likes` / `x_views`; post IDs recorded without raw response persistence | live integration smoke | `skills/x-account` fetch script/API reference |
| x_deep_retention_read | X video post retention request with one or more post IDs | private env has X access level returning owned-content metrics | `x_retention_score` plus quartile/click observations or explicit source gaps | live integration smoke | `skills/x-account` fetch script/API reference |
| instagram_missing_credentials | Instagram metrics request with no Graph token or IG business account id | private env lacks Graph read config | blocked status, missing key names only, no metric invention | script smoke + eval row | `skills/instagram-account` config gate |
| instagram_live_read | Instagram account metrics request with Graph token and IG business account id | private env has professional-account Graph credentials | KPI observations for `instagram_followers` and available `instagram_likes` / `instagram_views`; redacted endpoint evidence | live integration smoke + eval row | `skills/instagram-account` fetch script/API reference |
| instagram_media_id_read | Instagram media metrics request with one or more media IDs | private env has professional-account Graph credentials | KPI observations for returned `instagram_likes` / `instagram_views`; media IDs recorded without raw response persistence | live integration smoke | `skills/instagram-account` fetch script/API reference |
| instagram_reels_retention_read | Instagram Reels retention request with media ID and duration | private env has professional-account Graph credentials and insights permission | watch-time observations and normalized `instagram_retention_score` or explicit source gaps | live integration smoke | `skills/instagram-account` fetch script/API reference |

## Selected Cases

- `x_missing_credentials`: first-run failure mode; mechanically checkable.
- `x_live_read`: core proof that the account can fetch feedback data.
- `x_post_id_read`: exact-post proof for campaign/content-level analytics.
- `x_deep_retention_read`: owned-video retention/click proof.
- `instagram_missing_credentials`: first-run failure mode; mechanically
  checkable.
- `instagram_live_read`: core proof that Graph API setup can fetch feedback
  data.
- `instagram_media_id_read`: exact-media proof for campaign/content-level
  analytics.
- `instagram_reels_retention_read`: Reels retention-score proof.

## Proof Surface Map

- Deterministic local checks:
  - `python3 skills/x-account/scripts/check_config.py`
  - `python3 skills/instagram-account/scripts/check_config.py`
  - `python3 skills/x-account/scripts/fetch_metrics.py --date 2026-06-30 --out tmp/x-live.json`
  - `python3 skills/x-account/scripts/fetch_metrics.py --date 2026-06-30 --tweet-id <post-id> --out tmp/x-post.json`
  - `python3 skills/x-account/scripts/fetch_metrics.py --date 2026-06-30 --tweet-id <post-id> --deep --out tmp/x-retention.json`
  - `python3 skills/instagram-account/scripts/fetch_metrics.py --date 2026-06-30 --out tmp/ig-live.json`
  - `python3 skills/instagram-account/scripts/fetch_metrics.py --date 2026-06-30 --media-id <media-id> --out tmp/ig-media.json`
  - `python3 skills/instagram-account/scripts/fetch_metrics.py --date 2026-06-30 --media-id <media-id> --deep --duration-seconds <seconds> --out tmp/ig-retention.json`
- Agent behavior evals:
  - `skills/x-account/eval_task.json`
  - `skills/instagram-account/eval_task.json`
- KPI ingestion proof after a successful live fetch:
  - write output to `.farplane/metrics/manual/<platform>_account.json`
  - run `python3 bin/farplane.py metrics snapshot --project-root . --date 2026-06-30 --json`

## Grounding Notes

- X read proof uses X API v2 user/profile and user timeline endpoints with
  public metrics; private organic metrics remain a separate user-context branch.
- Instagram read proof uses Instagram Graph profile/media fields and
  best-effort media insights; availability depends on professional-account
  setup, permissions, media type, and Graph API version.
- Live proof is blocked until private credentials are populated; local
  validation should still pass without them.

## QA Verdict

`pass_with_blocked_live_credentials`: proof cases are distinct, mechanically
judgeable, and safe to rerun. Live fetch proof remains blocked until X and
Instagram private read credentials are configured.
