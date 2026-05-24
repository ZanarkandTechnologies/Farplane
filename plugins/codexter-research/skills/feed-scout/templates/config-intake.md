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
    "proposal_destination": "notion"
  }
}
```

Only `url` is always required per profile. `content_kinds` and `tags` are
routing hints, not identity. Dedupe is URL-key based.

