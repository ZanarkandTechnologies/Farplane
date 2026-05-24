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

