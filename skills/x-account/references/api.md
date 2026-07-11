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
  require user-context authentication. Prefer OAuth 2.0 user access tokens for
  current v2 read paths; OAuth 1.0a credentials are legacy/fallback for flows
  that still require them.
- X API access is pay-per-use/rate-limited. Treat live calls as budgeted
  external operations.
- The read-only metrics script uses OAuth 2.0 user access when available,
  falling back to app-only bearer reads. Private or organic analytics require
  user-context auth and account access level support.

## Minimal Config Contract

Use runtime env first, normally through `farplane run -- <command>` / Doppler.
Private `~/.farplane/config.toml` remains a fallback/cache with the same field
shape:

```toml
[social.x]
bearer_token = ""
oauth2_client_id = ""
oauth2_client_secret = ""
oauth2_access_token = ""
oauth2_refresh_token = ""
access_token = ""
access_token_secret = ""
api_key = ""
api_key_secret = ""
user_id = ""
username = ""
```

Use explicit `FARPLANE_X_*` environment variables as the normal runtime
contract. Do not commit credentials or generated env files.

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
- `scripts/publish_post.py` is the live write path. It uses OAuth 2.0 user
  access for X API v2 media upload and `POST /2/tweets`. When the stored OAuth
  2.0 access token returns unauthorized and refresh credentials exist, it
  refreshes OAuth 2.0, saves the refreshed token back to private
  `~/.farplane/config.toml` unless `--no-save-refreshed-token` is set, and
  retries before using OAuth 1.0a user-context fallback for text-only
  `POST /2/tweets`. Dry-run is the default, and account mutation requires
  `--execute` plus `--approval-ref`.
  Dry-run writes a local `draft` content-ledger row using a stable
  `x:draft:<hash>` content ID; execute reuses that ID and updates the row to
  `posted` after the API returns the tweet ID.
- Deep mode (`--deep`) asks for owned-content metric buckets and emits
  retention/click observations when returned: `x_retention_score`,
  `x_video_starts`, quartile views, completions, engagements, profile clicks,
  and URL clicks. If the account tier or auth mode does not return them, record
  `source_gap` style gaps rather than inventing values.
