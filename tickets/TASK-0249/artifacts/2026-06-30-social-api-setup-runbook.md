---
title: Social API Setup Runbook
owner: TASK-0249
status: active
kind: runbook
updated_at: 2026-06-30
source_refs:
  - https://docs.x.com/x-api/fundamentals/authentication/oauth-2-0
  - https://docs.x.com/x-api/fundamentals/authentication/oauth-1-0a
  - https://docs.x.com/x-api/fundamentals/metrics
  - https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login
  - https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights
---

# Social API Setup Runbook

This runbook connects Farplane-owned social metrics without storing secrets in
tracked files.

## Private Env Target

Write credentials only to:

```text
~/.codex/private/social.env
```

Never copy token values into chat, tickets, tracked docs, skill files, tests, or
fixtures.

## X Setup

Create or use an X Developer app for the Farplane account.

Required for shallow account/post metrics:

```bash
export FARPLANE_X_BEARER_TOKEN=
export FARPLANE_X_USER_ID=
export FARPLANE_X_USERNAME=
```

Required for deep owned-content metrics such as clicks, engagement buckets, and
video playback quartiles:

```bash
export FARPLANE_X_ACCESS_TOKEN=
export FARPLANE_X_ACCESS_TOKEN_SECRET=
export FARPLANE_X_API_KEY=
export FARPLANE_X_API_KEY_SECRET=
```

Notes:

- Bearer token covers app-auth reads where the access tier allows them.
- Deep metrics may require user-context OAuth and an access tier that returns
  non-public / organic metrics.
- `FARPLANE_X_USER_ID` is preferred; `FARPLANE_X_USERNAME` can resolve the id.

Smoke commands:

```bash
python3 skills/x-account/scripts/check_config.py
python3 skills/x-account/scripts/fetch_metrics.py --date 2026-06-30 --out tmp/x-account-live.json
python3 skills/x-account/scripts/fetch_metrics.py --date 2026-06-30 --tweet-id <post-id> --deep --out tmp/x-retention-live.json
```

## Instagram Setup

Create or use a Meta app with Instagram Graph access for the professional
Farplane Instagram account.

Required:

```bash
export FARPLANE_INSTAGRAM_ACCESS_TOKEN=
export FARPLANE_INSTAGRAM_BUSINESS_ACCOUNT_ID=
export FARPLANE_INSTAGRAM_USERNAME=
```

Optional but useful for app/account tracking:

```bash
export FARPLANE_META_APP_ID=
export FARPLANE_META_APP_SECRET=
export FARPLANE_META_GRAPH_VERSION=
```

Notes:

- The Instagram account must be professional and connected through the Meta app
  / Facebook page flow supported by Instagram Graph API.
- Media insights availability depends on permissions, media type, API version,
  and account eligibility.
- Reels retention score requires a known media duration to normalize average
  watch time.

Smoke commands:

```bash
python3 skills/instagram-account/scripts/check_config.py
python3 skills/instagram-account/scripts/fetch_metrics.py --date 2026-06-30 --out tmp/ig-account-live.json
python3 skills/instagram-account/scripts/fetch_metrics.py --date 2026-06-30 --media-id <media-id> --deep --duration-seconds <seconds> --out tmp/ig-retention-live.json
```

## KPI Loop Smoke

After either platform fetch succeeds, write to the default output path or copy
the successful output into `.farplane/metrics/manual/<platform>_account.json`,
then run:

```bash
python3 bin/farplane.py metrics snapshot --project-root . --date 2026-06-30 --json
```

Expected result:

- `ok: true`
- source snapshot path for the manual account source
- `.farplane/metrics/ui/latest.json` includes the fetched metric ids

## Daily Strategy Loop

The intended loop is:

1. Ops memory names the live content/account IDs worth tracking.
2. Daily interval reads bindings and the tracked KPI registry.
3. Account skills fetch shallow account metrics and deep content retention
   metrics for listed IDs.
4. Metrics snapshot normalizes the day into the KPI cockpit.
5. Interval report compares deltas, source gaps, and target-hit markers.
6. Strategy updates the next content/project plan from observed retention,
   engagement, clicks, and follower movement.

Minimum ops-memory shape:

```text
tracked_social_content:
  - platform: x
    id: "<post-id>"
    label: "<campaign/content name>"
    duration_seconds: null
    review_until: "YYYY-MM-DD"
    reason: "why this content teaches us something"
  - platform: instagram
    id: "<media-id>"
    label: "<reel/campaign name>"
    duration_seconds: 42
    review_until: "YYYY-MM-DD"
    reason: "why this content teaches us something"
```

Do not add broad scraping or viewer identity to this loop. Use aggregate,
owned-account metrics only.
