---
title: Instagram API Reference
kind: skill-reference
owner: instagram-account
status: draft
source_refs:
  - https://developers.facebook.com/docs/instagram-platform/overview/
  - https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/
  - https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights/
---

# Instagram API Reference

Load this before live Instagram API work.

## Grounding

- Instagram Login / Business Login is the metrics path for this skill.
- Insights are account/media metrics and should be normalized before reaching
  the KPI cockpit.
- The read-only metrics script uses `graph.instagram.com` profile/media fields
  plus best-effort media insights for view-like metrics. Metric availability
  depends on account type, permissions, media type, token type, and API version.
- Facebook Page, `/me/accounts`, and Page-linked `instagram_business_account`
  flows are intentionally out of scope for this skill.

## Minimal Config Contract

Use local private `~/.farplane/config.toml`:

```toml
[social.instagram]
username = ""
api_mode = "instagram_login"
login_access_token = ""
login_user_id = ""
business_account_id = ""

[social.meta]
app_id = ""
app_secret = ""
graph_version = "v21.0"
```

Explicit `FARPLANE_INSTAGRAM_*` and `FARPLANE_META_*` environment variables
remain supported as one-off runtime overrides, not the persisted source of
truth.

## Live API Gates

- Confirm professional-account/API eligibility before promising insights or
  publishing.
- `publish_post` and `publish_reel` require explicit approval for the exact
  artifact and account alias.
- Store normalized outputs, not raw credential-bearing responses.
- `scripts/fetch_metrics.py` is the live read-only smoke path. With no
  `--media-id`, it writes `instagram_followers` from profile fields and
  best-effort `instagram_likes` / `instagram_views` from recent media fields or
  insights. With one or more `--media-id` values, it reads the specified media
  and aggregates returned fields or insights for those IDs.
- Deep mode (`--deep`) asks for Reels/media judgment metrics including views,
  reach, saved, shares, comments, total interactions, average watch time, and
  total watch time. Pass `--duration-seconds` to normalize average watch time
  into `instagram_retention_score`; otherwise preserve watch-time observations
  and record that normalized retention requires duration.
