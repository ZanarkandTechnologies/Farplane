# Feed Scout Data Model

## TrackedEntity

Tracked entities identify the people and organizations behind multiple source
surfaces. They keep provenance stable when one person appears through an X
account, GitHub org, repo, package, video channel, or blog.

## FeedScoutConfig

Project-local Feed Scout setup normally lives in `farplane/bindings.yaml` under
`feed_scout`. It is declarative configuration for sources, paths, UI rendering,
and write policy; it is not the item ledger.

```text
FeedScoutConfig {
  enabled: boolean
  cadence: "daily" | "weekly" | string
  timezone: string
  report_root: string
  latest_report: string
  daily_feed_root: string
  ledger: string
  proposal_ledger: string
  scout_brief: string
  destination: "local_ledger" | "local_inbox" | "notion_tasks"
  write_policy: "local_first" | "report_only"
  ui?: {
    default_view: "daily_feed" | string
    date_param: string
    latest_feed: string
  }
  entities: map<string, FeedEntity>
}

FeedEntity {
  name: string
  kind: "person" | "organization" | "project" | string
  tags: string[]
  enabled: boolean
  instructions?: string
  owned_sources: map<string, TrackedProfile | TrackedHarnessResource | SourceRef>
  search_entity_on_platform?: ("x" | "web" | "reddit" | "trustpilot" | "github" | string)[]
  search_queries?: string[]
}
```

Rules:

- Config paths are project-relative unless absolute.
- `scout_brief` points to one Scout Brief Markdown file updated in place. It is current
  synthesis, not a daily/monthly ledger or snapshot timeline.
- Key sources by the person, organization, or project the operator wants to
  track, for example `entities.theo-ping.sources.instagram`, so UI can render
  one creator with all websites, social accounts, repos, channels, and docs
  together.
- `entities.<entity_id>.owned_sources.<source_id>` is the high-signal source
  list for posts created by the entity. Keep it to official accounts, docs,
  repos, feeds, sites, or creator-owned surfaces.
- `instructions` is one plain operator task prompt. Entity instructions apply
  to every source under the entity; source instructions refine the inherited
  task. It may describe what to extract or prioritize, which first-party
  sources to discover, and which source, entity/thesis, or feature changes to
  propose. It does not grant update authority: fixed Feed Scout policy routes
  each proposal through its existing review boundary.
- `entities.<entity_id>.search_entity_on_platform` is the high-signal mention
  search list for posts about the entity. Keep queries exact enough to avoid
  broad web drift.
- Acquisition route choice is skill behavior, not project config. Do not add
  fields for `acquisition_route`, provider priority, backend names, or scraper
  selection unless a future ticket proves the operator needs to override the
  default route order.
- Live spend and live Notion writes require explicit automation params in
  addition to config.

```text
SourceRef {
  url?: string
  handle?: string
  repo?: string
  org?: string
  user?: string
  fetch_method?: string
  instructions?: string
}
```

The `owned_sources` key is the source identity and type hint, for example
`website`, `x_founder`, `github_repo`, or `youtube`. Do not repeat that
information in a `kind` field. URL/handle/repo coordinates and Feed Scout's
platform routing determine acquisition.

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
  kind: "post" | "thread" | "video" | "short" | "article" | "repo_change" | "skill_change" | "release" | "mention" | "site_change"
  canonical_url: string
  canonical_key: string
  native_id?: string
  title: string
  author: string
  published_at?: string
  discovered_at: string
  date_basis: "source_published_at" | "source_updated_at" | "source_metric_delta" | "snapshot_diff" | "observed_at" | "unknown"
  daily_eligible?: boolean
  summary: string
  why_care_today: string
  today_delta: TodayDelta
  novelty: "new_today" | "changed_today" | "rediscovered" | "context_only" | "stale"
  actionability: {
    label: "watch" | "inspect" | "adapt" | "ignore"
    reason?: string
  }
  rank: number
  instructions_ref?: {
    entity_hash?: string
    source_hash?: string
    effective_hash: string
  }
  signal?: "high" | "medium" | "low"
  source_snapshot?: object
  embed?: SourceBookmarkCard
  evidence_refs: string[]
  content_hash?: string
  status: "new" | "seen" | "changed" | "ignored" | "scout-queued" | "scouted" | "proposed" | "rejected"
}
```

```text
TodayDelta {
  kind: "release" | "commit" | "stars_delta" | "new_video" | "new_article" |
        "new_post" | "mention" | "site_change" | "no_material_change"
  observed_at: string
  previous_observed_at?: string
  before?: object
  after?: object
  delta?: object
  confidence: "high" | "medium" | "low"
}

SourceBookmarkCard {
  provider: string
  card_type: "repo" | "release" | "video" | "article" | "post" | "profile" | "website" | "mention"
  url: string
  image_url?: string
  title?: string
  byline?: string
}
```

Daily feed ranking rules:

- `why_care_today` is required for every card. It should be one crisp sentence
  explaining the today-specific reason to inspect, watch, adapt, or ignore.
- Daily feed eligibility is based on source launch/change time, not discovery
  time. `observed_at` means Feed Scout saw the source today; it is not evidence
  that the source launched today.
- Items with `date_basis: "observed_at"` or `"unknown"` should be excluded
  from the main daily feed unless a later extraction proves a source-published
  date or snapshot diff inside the review window.
- The effective operator instructions should steer source work and ranking.
  Emit `instructions_ref` when configured so debugging can prove which
  entity/source task shaped the card without dumping long prompts into the UI.
- Main daily feed output should include only rows that passed the daily
  significance gate. Use `rank` to order the few surviving cards; do not add a
  separate `interesting` boolean or `interesting_item_count`.
- Eligible daily items require a clear `today_delta` such as a new release,
  meaningful commit summary, new video/post/article, external mention, site
  change, or metric delta. Generic repo metadata, homepage presence, or
  rediscovered old content should stay out of `items[]` and appear only in
  report/exclusion evidence when useful.
- GitHub `pushed_at` alone is not high-signal. Promote only when Feed Scout can
  summarize what changed, detect a release, detect a meaningful star/fork
  delta, or map recent commits/features.
- Static websites are `context_only` or `stale` unless content changed today or
  a new page/news item was found. Homepage rows should normally be excluded
  from the daily feed unless Feed Scout has stored and compared snapshots and
  can point to changed fields.
- Use `embed` only as a source-native bookmark hint. Do not store iframe HTML.

Recommended `source_snapshot` fields:

- GitHub: `repo`, `stars`, `forks`, `pushed_at`, `latest_release`,
  `release_published_at`, `recent_commits`, and `stars_delta` when known.
- YouTube: `channel_id`, `video_id`, `latest_video_title`, `published_at`,
  `thumbnail`, `view_count`, and `duration` when available.
- Web/RSS: `title`, `published_at`, `changed_fields`, or explicit
  `no_material_change`.

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

## DailyFeedFile

The daily feed is the UI-facing slice of newly found or changed items for one
date. It should be compact enough to render directly and should point to larger
reports or scout runs instead of embedding raw transcripts.

Feed Scout compiles and writes this object agentically after acquisition,
extraction, ranking, and synthesis. The skill-local
`scripts/validate_daily_feed.py` helper only validates the final artifact; it
does not fetch sources, rank items, or write files. Keep helper scripts inside
the skill package so installed projects receive the same deterministic checks
with the skill.

```text
DailyFeedFile {
  date: string
  generated_at: string
  config_ref: string
  window: string
  groups: FeedEntityGroupSummary[]
  items: ContentItem[]
  source_gaps: string[]
  report_ref?: string
  latest_report_ref?: string
}
```

## FeedScoutBrief

The Scout Brief file is the compact retrieval surface between daily Feed Scout runs
and downstream planning. It uses Markdown because the content is
judgment-shaped, but deterministic headings and frontmatter keep the contract
inspectable.

```text
FeedScoutBrief {
  frontmatter: {
    kind: "feed-scout-brief"
    status: "active"
    updated_at: datetime
    canonical_icp_ref: "farplane/harness.yaml#areas"
    source_ledger: string
    last_report_ref?: string
  }
  sections: {
    ICPs: CompactAreaBullet[]
    Trends: CompactTrendBullet[]
    "Other Notable Things": CompactNotableBullet[]
    "Source Gaps": string[]
  }
  max_non_empty_lines: 100
}

CompactAreaBullet {
  syntax: "- `<area_id>` — `<ICP label>` | ref=`farplane/harness.yaml#areas.<area_id>.icp` | concerns=<short> | language=<short> | refs=<refs>"
}

CompactTrendBullet {
  syntax: "- observed|analogous|hypothesis|source_gap | icp=<area_ids> | claim=<one claim> | use=<causal use> | seen=<YYYY-MM-DD> | conf=<low|medium|high> | refs=<refs>"
}

CompactNotableBullet {
  syntax: "- observed|analogous|hypothesis|source_gap | type=<type> | icp=<area_ids> | note=<one observation> | use=<safe use> | seen=<YYYY-MM-DD> | refs=<refs>"
}
```

Rules:

- `harness.areas.<area_id>.icp` is canonical. Scout Brief renders only area
  IDs, labels, current concerns/language, trends, notable things, source gaps,
  and provenance; full canonical profile text stays in `harness.yaml`.
- Update existing concepts in place, merge duplicates, and remove or replace
  superseded synthesis. Do not append dated run sections or preserve snapshots.
- Stale facts may remain when useful, but `last_observed`, confidence, and
  source gaps must make their status honest.
- Keep the live file at or under 100 non-empty lines. Demote detail to the
  dated Feed Scout report when memory pressure appears.
- Scout Brief is optional evidence. It never overrides metrics, ticket history,
  authority, or the planner's admission gates.
- Validate the final file with `scripts/validate_scout_brief.py`; the helper checks
  line cap, simple syntax, structure, and provenance affordances but does not
  author or rank content.

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
