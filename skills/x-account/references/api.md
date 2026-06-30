---
title: X API Reference
kind: skill-reference
owner: x-account
status: draft
source_refs:
  - https://docs.x.com/x-api/introduction
  - https://docs.x.com/x-api/fundamentals/data-dictionary
  - https://docs.x.com/x-api/posts/timelines/introduction
---

# X API Reference

Load this before live X API work.

## Grounding

- X API v2 provides REST endpoints for posts, users, DMs, lists, Spaces, and
  trends, including reading posts, publishing content, and user/profile access.
- X post/user objects can expose public metrics; non-public or organic metrics
  require user-context authentication.
- X API access is pay-per-use/rate-limited. Treat live calls as budgeted
  external operations.
- The read-only metrics script uses bearer auth for public user metrics and
  recent post public metrics. Private or organic analytics should be added as
  a separate user-context branch after the account access level is confirmed.

## Minimal Env Contract

Use private env only:

```bash
FARPLANE_X_BEARER_TOKEN=
FARPLANE_X_ACCESS_TOKEN=
FARPLANE_X_ACCESS_TOKEN_SECRET=
FARPLANE_X_API_KEY=
FARPLANE_X_API_KEY_SECRET=
FARPLANE_X_USER_ID=
FARPLANE_X_USERNAME=
```

## Live API Gates

- Read-only profile/post metrics may run only after `FARPLANE_X_*` credentials
  are present and the ticket/request names the account alias.
- `publish_post` and `publish_thread` require explicit approval for the exact
  draft artifact and account alias.
- Store normalized outputs, not raw credential-bearing responses.
- `scripts/fetch_metrics.py` is the live read-only smoke path. With no
  `--tweet-id`, it writes `x_followers` from user public metrics and
  best-effort `x_likes` / `x_views` from recent post public metrics. With one
  or more `--tweet-id` values, it reads the specified posts and aggregates
  returned public metrics for those IDs.
- Deep mode (`--deep`) asks for owned-content metric buckets and emits
  retention/click observations when returned: `x_retention_score`,
  `x_video_starts`, quartile views, completions, engagements, profile clicks,
  and URL clicks. If the account tier or auth mode does not return them, record
  `source_gap` style gaps rather than inventing values.
