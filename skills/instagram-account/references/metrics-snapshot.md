---
title: Instagram Metrics Snapshot
kind: skill-reference
owner: instagram-account
status: active
---

# Instagram Metrics Snapshot

Normalize API responses, CSV exports, or manual reports into a compact daily
reading snapshot:

```json
{
  "source": "instagram_account_metrics",
  "date": "YYYY-MM-DD",
  "status": "available",
  "metrics": {
    "instagram_followers": {"value": 0},
    "instagram_views": {
      "value": 0,
      "items": [
        {
          "id": "instagram:media-id",
          "value": 0,
          "kind": "reels",
          "url": "https://www.instagram.com/..."
        }
      ]
    },
    "instagram_likes": {"value": 0},
    "instagram_retention_score": {
      "value": null,
      "items": [
        {
          "id": "instagram:media-id",
          "value": null,
          "gap": "retention_requires_reel"
        }
      ]
    }
  },
  "gaps": []
}
```

Do not include values whose source did not supply them. Use `source_gap` in the
source snapshot when the account/export/API cannot provide the metric.

For content review windows, keep the stable KPI as the key and put media IDs
under that KPI's `items`. Do not create dynamic KPI names from media IDs.
`metrics.<kpi>.value` is the provider reading for that date; the UI derives
the requested-window value, preceding equal-window comparison, trend, and
cumulative view when the metric is a flow.

Only Reel media can produce watch-time/retention observations. Non-Reel media
should record a retention source gap, not zero.

Run the skill-local validator after writing a snapshot:

```bash
python3 skills/instagram-account/scripts/validate_metrics.py --snapshot .farplane/metrics/manual/instagram_account.json
```
