---
title: X Metrics Snapshot
kind: skill-reference
owner: x-account
status: active
---

# X Metrics Snapshot

Normalize API responses, CSV exports, or manual reports into a compact daily
reading snapshot:

```json
{
  "source": "x_account_metrics",
  "date": "YYYY-MM-DD",
  "status": "available",
  "metrics": {
    "x_followers": {"value": 0},
    "x_views": {
      "value": 0,
      "items": [
        {
          "id": "x:post-id",
          "value": 0,
          "kind": "post",
          "url": "https://x.com/account/status/post-id"
        }
      ]
    },
    "x_likes": {"value": 0}
  },
  "gaps": []
}
```

Do not include values whose source did not supply them. Use `source_gap` in the
source snapshot when the account/export/API cannot provide the metric.

For content review windows, keep the stable KPI as the key and put post IDs
under that KPI's `items`. Do not create dynamic KPI names from post IDs.
`metrics.<kpi>.value` is the provider reading for that date; the UI derives
the requested-window value, preceding equal-window comparison, trend, and
cumulative view when the metric is a flow.

Run the skill-local validator after writing a snapshot:

```bash
python3 skills/x-account/scripts/validate_metrics.py --snapshot .farplane/metrics/manual/x_account.json
```
