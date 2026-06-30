---
title: Instagram Metrics Snapshot
kind: skill-reference
owner: instagram-account
status: active
---

# Instagram Metrics Snapshot

Normalize API responses, CSV exports, or manual reports into:

```json
{
  "source_id": "manual_instagram_account",
  "date": "YYYY-MM-DD",
  "status": "available",
  "observations": [
    {"metric_id": "instagram_followers", "date": "YYYY-MM-DD", "value": 0, "status": "available"},
    {"metric_id": "instagram_views", "date": "YYYY-MM-DD", "value": 0, "status": "available"},
    {"metric_id": "instagram_likes", "date": "YYYY-MM-DD", "value": 0, "status": "available"}
  ]
}
```

Do not include values whose source did not supply them. Use `source_gap` in the
source snapshot when the account/export/API cannot provide the metric.
