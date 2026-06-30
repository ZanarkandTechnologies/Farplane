---
title: Instagram API Reference
kind: skill-reference
owner: instagram-account
status: draft
source_refs:
  - https://developers.facebook.com/docs/instagram-platform/overview/
  - https://developers.facebook.com/docs/instagram-platform/api-reference/instagram-user/insights/
  - https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media/
  - https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-media/insights/
  - https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media_publish/
---

# Instagram API Reference

Load this before live Instagram API work.

## Grounding

- Instagram Platform APIs support professional-account workflows including
  content publishing and account/media insights when permissions are configured.
- Content publishing uses container creation and publish steps for eligible
  Instagram accounts.
- Insights are account/media metrics and should be normalized before reaching
  the KPI cockpit.
- The read-only metrics script uses Instagram Graph API profile/media fields
  plus best-effort media insights for view-like metrics. Metric availability
  depends on account type, permissions, media type, and API version.

## Minimal Env Contract

Use private env only:

```bash
FARPLANE_INSTAGRAM_ACCESS_TOKEN=
FARPLANE_INSTAGRAM_BUSINESS_ACCOUNT_ID=
FARPLANE_INSTAGRAM_USERNAME=
FARPLANE_META_APP_ID=
FARPLANE_META_APP_SECRET=
```

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
