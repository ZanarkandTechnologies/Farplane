# Feed Scout Configure Intake

Minimum useful input:

```json
{
  "profiles": [
    {
      "url": "https://x.com/example",
      "content_kinds": ["post", "thread"],
      "tags": ["agents", "harness"]
    },
    {
      "url": "https://www.youtube.com/@anthropic-ai",
      "content_kinds": ["video"]
    },
    {
      "url": "https://cursor.com/blog",
      "content_kinds": ["article"]
    }
  ],
  "defaults": {
    "cadence": "daily",
    "min_signal": "high",
    "proposal_destination": "local_ledger"
  },
  "local_surfaces": {
    "profiles": ".farplane/feed-scout/profiles.jsonl",
    "entities": ".farplane/feed-scout/entities.jsonl",
    "resources": ".farplane/feed-scout/resources.jsonl",
    "ingestion_ledger": ".farplane/feed-scout/ingestion-ledger.jsonl",
    "proposal_ledger": ".farplane/feed-scout/proposals.jsonl"
  }
}
```

Only `url` is always required per profile. `content_kinds` and `tags` are
routing hints, not identity. Dedupe is URL-key based.

Keep the destination local unless live Notion routing is explicitly configured
and readback can verify required `Project` and `Areas` relations.
