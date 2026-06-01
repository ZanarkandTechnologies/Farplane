# Tracked Profiles DB Template

Use this for the curated profiles the operator wants to monitor.

Recommended fields:

- `Profile ID`: stable short id, such as `x-example`
- `Name`: display name
- `Platform`: `x`, `youtube`, or `blog`
- `Profile URL`: account, channel, blog, or feed URL
- `Content Kinds`: `post`, `thread`, `video`, `short`, `article`
- `Tags`: routing hints such as `agents`, `harness`, `evals`
- `Cadence`: `daily`, `weekly`, or a plain-language interval
- `Fetch Method`: `x-api`, `apify:apidojo/tweet-scraper`, `youtube-rss`,
  `rss`, `sitemap`, or `manual`
- `Min Signal`: `low`, `medium`, or `high`
- `Enabled`: checkbox
- `Last Checked At`: date/time
- `Notes`: short operator note

The profile DB is not the ingestion ledger. A profile can produce many content
items over time.

## Entity and Harness Resource Rows

Use entity rows when several resources should be understood as coming from the
same person or organization. Use harness-resource rows when the watched thing is
a repo, GitHub skill folder, docs site, package, or social profile whose value
is harness technique extraction.

Recommended entity fields:

- `Entity ID`: stable short id, such as `person-steipete` or `org-openclaw`
- `Kind`: `person` or `organization`
- `Name`: display name
- `Aliases`: handles or alternate names
- `Home URLs`: profile, org, homepage, or canonical identity URLs
- `Confidence`: `low`, `medium`, or `high`
- `Evidence Refs`: why this identity link is trusted
- `Notes`: short provenance caveat

Recommended harness-resource fields:

- `Resource ID`: stable short id, such as `github-openclaw-agent-skills`
- `Resource Type`: `x_profile`, `github_org`, `github_repo`, `github_skill`,
  `blog`, `docs`, or `package`
- `URL`: canonical resource URL
- `Entity IDs`: linked people or organizations
- `Parent Resource ID`: for a skill folder inside a repo
- `Repo` / `Repo Path`: GitHub owner/name and watched subpath when relevant
- `Watch Paths`: paths that should trigger scouting when changed
- `Content Kinds`: `post`, `thread`, `repo_change`, `skill_change`,
  `article`, or `release`
- `Fetch Method`: `manual`, `git-clone`, `github-api`, `rss`, `x-api`, or an
  explicitly approved Apify actor
- `Identity Confidence`: `operator_asserted`, `source_correlated`, or
  `verified`
