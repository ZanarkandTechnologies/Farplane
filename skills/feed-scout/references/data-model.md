# Feed Scout Data Model

## TrackedEntity

Tracked entities identify the people and organizations behind multiple source
surfaces. They keep provenance stable when one person appears through an X
account, GitHub org, repo, package, video channel, or blog.

```text
TrackedEntity {
  id: string
  kind: "person" | "organization"
  display_name: string
  aliases: string[]
  home_urls: string[]
  organization_ids?: string[]
  member_entity_ids?: string[]
  confidence: "low" | "medium" | "high"
  evidence_refs: string[]
  notes?: string
}
```

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

## TrackedHarnessResource

Harness resources are monitored source surfaces owned by or linked to one or
more `TrackedEntity` rows. Use them for GitHub orgs, repos, skill folders,
agent-framework docs, personal harness repos, and social profiles when the
monitoring goal is to copy harness techniques rather than just watch content.

```text
TrackedHarnessResource {
  id: string
  resource_type: "x_profile" | "github_org" | "github_repo" | "github_skill" | "blog" | "docs" | "package"
  url: string
  entity_ids: string[]
  parent_resource_id?: string
  repo?: string
  repo_path?: string
  watch_paths?: string[]
  content_kinds: ("post" | "thread" | "repo_change" | "skill_change" | "article" | "release")[]
  fetch_method: string
  tags: string[]
  cadence: string
  enabled: boolean
  min_signal: "low" | "medium" | "high"
  identity_confidence: "operator_asserted" | "source_correlated" | "verified"
  observed_commit?: string
  notes?: string
}
```

## ContentItem

Content items are discovered from tracked profiles.

```text
ContentItem {
  profile_id: string
  resource_id?: string
  entity_ids?: string[]
  platform: string
  kind: "post" | "thread" | "video" | "short" | "article" | "repo_change" | "skill_change" | "release"
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
  resource_ids?: string[]
  entity_ids?: string[]
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

## ProposalDraft

Proposal drafts are the low-volume review surface for scouted content that
earned an adopt, adapt, defer, reject, or needs-benchmark decision.

```text
ProposalDraft {
  canonical_key: string
  canonical_url: string
  title: string
  decision: "adopt" | "adapt" | "defer" | "reject" | "needs-benchmark"
  summary: string
  source_refs: string[]
  scout_runs: string[]
  handoff_body?: string
  destination: "proposal_ledger" | "local_inbox" | "notion_tasks"
  task_projection?: NotionTaskProjection
}
```

Use the `harness-scout` handoff body for strong adopt/adapt items. The content
title alone is not enough task body.

## NotionTaskProjection

`NotionTaskProjection` is required only when feed-scout writes to a live Tasks
database. It prevents a half-created task from looking complete when workspace
routing fields were never resolved.

```text
RelationRef {
  handle: string
  page_url?: string
  source: "operator_context" | "parent_context" | "private_context" | "operator_asserted"
}

ProjectionVerification {
  page_url?: string
  project_present: boolean
  areas_present: boolean
  checked_at: string
  status: "passed" | "routing_missing" | "write_failed"
}

NotionTaskProjection {
  title: string
  body_source: "harness_scout_handoff" | "best_of_worlds_handoff" | "operator_summary"
  project_relation?: RelationRef
  areas_relations: RelationRef[]
  routing_status: "resolved" | "routing_missing" | "local_only"
  routing_evidence: string[]
  readback?: ProjectionVerification
}
```

Rules:

- `project_relation` and at least one `areas_relations` entry are required for
  `routing_status=resolved`.
- Reusable skill files, templates, fixtures, and docs must use relation handles
  or placeholder URLs, not private database IDs or page IDs.
- A live Tasks write may claim success only after readback confirms both
  `project_present=true` and `areas_present=true`.
- If routing cannot be resolved, write to the proposal ledger or local inbox
  with `routing_status=routing_missing` instead of creating a partial task.

## Promotion Rule

Do not create a `SRC-*` record for every discovered item. Promote only content
that was actually scouted, influenced a decision, or became durable evidence.
When two resources are linked by `entity_ids`, cite the entity relationship in
the source run, but keep the source record tied to the exact repo, skill, post,
video, or article that supplied the evidence.
