---
name: apify
version: 1.0.0
description: "Hub skill for external data acquisition via Apify MCP. Use when scraping YouTube, Twitter, Instagram, TikTok, LinkedIn, or Google Places. Centralizes actor configurations, execution patterns, and data normalization workflows."
tier: 2
source: local
allowed-tools: apify, web_search, documentation-searcher
---

# Apify Integration Skill

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Important Checklist

- [ ] Identify the platform, actor, live-run boundary, credential/spend status,
  and output needed before invoking Apify.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) to confirm the
  actor, source URL, and requested data are the right evidence source.
- [ ] Fetch the actor docs or reference file before constructing input.
- [ ] Prefer dry-run or schema inspection when credentials, spend, proxies, or
  legality are unclear.
- [ ] Execute the smallest actor run that can produce the needed records.
- [ ] Normalize output into the caller's expected shape and preserve actor/run
  provenance.
- [ ] Use [advise](../advise/SKILL.md) when live scraping vs fixture/dry-run is
  a material tradeoff.
- [ ] Use [review](../review/SKILL.md) before changing durable actor configs or
  public scraping recipes.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

The centralized "Data Acquisition Layer" for all external scraping operations.

## Purpose

Encapsulate the technical complexity of the Apify MCP so that other skills can delegate data fetching without understanding the underlying actor configurations, proxy management, or rate limiting.

## Documentation Index (Source of Truth)

### Apify Platform
- **[Apify Console](https://console.apify.com)**: Manage actors and runs.
- **[Apify MCP Documentation](https://mcp.apify.com)**: MCP-specific integration details.
- **[Actor Store](https://apify.com/store)**: Browse all available actors.

### MCP Tools
The Apify MCP provides three core tools:
- `actors`: List and get details about available actors.
- `docs`: Fetch documentation for a specific actor.
- `runs`: Execute an actor and retrieve results.

## Configured Actors Index

| Platform      | Actor ID                              | Reference                                  |
| ------------- | ------------------------------------- | ------------------------------------------ |
| YouTube       | `streamers/youtube-scraper`           | [references/youtube.md](references/youtube.md) |
| YouTube       | `streamers/youtube-comments-scraper`  | [references/youtube.md](references/youtube.md) |
| YouTube       | `streamers/youtube-shorts-scraper`    | [references/youtube.md](references/youtube.md) |
| Twitter       | `apidojo/tweet-scraper`               | [references/twitter.md](references/twitter.md) |
| Instagram     | `apify/instagram-scraper`             | [references/instagram.md](references/instagram.md) |
| Instagram     | `apify/instagram-reel-scraper`        | [references/instagram.md](references/instagram.md) |
| TikTok        | `clockworks/tiktok-scraper`           | [references/tiktok.md](references/tiktok.md) |
| TikTok        | `clockworks/tiktok-comments-scraper`  | [references/tiktok.md](references/tiktok.md) |
| LinkedIn      | `dev_fusion/Linkedin-Profile-Scraper` | [references/linkedin.md](references/linkedin.md) |
| Google Places | `compass/crawler-google-places`       | [references/google-places.md](references/google-places.md) |

## Integration Workflow

```
1. Identify Platform → 2. Fetch Actor Docs → 3. Execute Run → 4. Normalize Output
```

1. **Identify Platform**: Find the relevant actor in the table above.
2. **Fetch Actor Docs**: Use the MCP `docs` tool to get the latest input schema.
3. **Execute Run**: Use the MCP `runs` tool with the correct input parameters.
4. **Normalize Output**: Follow the platform-specific reference for data extraction.

## Architectural Decisions

- **Hub Pattern**: All scraping goes through this skill to centralize maintenance.
- **MCP-First**: Use the Apify MCP tools instead of direct API calls.
- See [references/architecture.md](references/architecture.md) for details.

## Common Gotchas

- **Rate Limits**: Some platforms aggressively rate-limit. Use delays.
- **Proxy Requirements**: Instagram and LinkedIn often require residential proxies.
- See [references/gotchas.md](references/gotchas.md) for the full list.

## Platform References

- [youtube.md](references/youtube.md) - Video, Shorts, Comments, Transcripts
- [twitter.md](references/twitter.md) - Tweet Scraping
- [instagram.md](references/instagram.md) - Posts, Reels
- [tiktok.md](references/tiktok.md) - Videos, Comments
- [linkedin.md](references/linkedin.md) - Profile Scraping
- [google-places.md](references/google-places.md) - Business Listings

## Technical References

- [architecture.md](references/architecture.md) - MCP configuration and proxy strategy.
- [gotchas.md](references/gotchas.md) - Common scraping pitfalls and mitigations.
