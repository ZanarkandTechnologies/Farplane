# Feed Scout Data Model

## TrackedProfile

Tracked profiles are the user-facing configuration surface.

```text
TrackedProfile {
  id: string
  platform: "x" | "youtube" | "blog"
  profile_url: string
  display_name?: string
  content_kinds: ("post" | "thread" | "video" | "short" | "article")[]
  fetch_method: string
  tags: string[]
  cadence: string
  enabled: boolean
  min_signal: "low" | "medium" | "high"
}
```

## ContentItem

Content items are discovered from tracked profiles.

```text
ContentItem {
  profile_id: string
  platform: string
  kind: "post" | "thread" | "video" | "short" | "article"
  canonical_url: string
  canonical_key: string
  native_id?: string
  title: string
  author: string
  published_at: string
  discovered_at: string
  content_hash?: string
  status: "new" | "seen" | "changed" | "ignored" | "scout-queued" | "scouted" | "proposed" | "rejected"
}
```

## IngestionLedgerRow

The ledger is high-volume and URL-keyed. It is the place to remember which
resources have already been seen or ingested.

```text
IngestionLedgerRow {
  canonical_key: string
  canonical_url: string
  profile_ids: string[]
  first_seen_at: string
  last_seen_at: string
  last_ingested_at?: string
  content_hash?: string
  scout_run?: string
  src_id?: string
  proposal_url?: string
  status: string
}
```

## Promotion Rule

Do not create a `SRC-*` record for every discovered item. Promote only content
that was actually scouted, influenced a decision, or became durable evidence.

