# Architectural Decisions for Apify Integration

This file documents the "Why" behind the Apify skill's design and configuration.

## Core Architecture: The Hub Pattern

The Apify skill is designed as a **centralized hub** for all external data acquisition.

```
┌─────────────────────────────────────────────────────────────┐
│                      Other Skills                           │
│   (youtube-analysis, content-research, competitor-intel)   │
└─────────────────────────────┬───────────────────────────────┘
                              │ "Fetch data from X"
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Apify Hub Skill                          │
│   - Knows MCP configuration                                 │
│   - Handles proxy/auth requirements                         │
│   - Normalizes output schemas                               │
└─────────────────────────────┬───────────────────────────────┘
                              │ MCP Tool Calls
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Apify MCP                             │
│   tools: actors, docs, runs                                 │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              External Platforms                             │
│   YouTube, Twitter, Instagram, TikTok, LinkedIn, Google     │
└─────────────────────────────────────────────────────────────┘
```

### Why Hub Pattern?

1. **Single Point of Maintenance**: MCP configuration changes are isolated to one skill.
2. **DRY Principle**: Avoids duplicating scraping logic across multiple domain skills.
3. **Expertise Encapsulation**: Platform-specific quirks (proxies, rate limits) are documented once.

## MCP Configuration

The Apify MCP is configured in `.claude.json` with specific actors enabled:

```
URL: https://mcp.apify.com/
Tools: actors, docs, runs
Actors: (10 configured - see SKILL.md for full list)
```

### MCP Tools Explained

| Tool     | Purpose                                    | When to Use                        |
| -------- | ------------------------------------------ | ---------------------------------- |
| `actors` | List available actors and their metadata   | Discovery, validation              |
| `docs`   | Fetch input schema for a specific actor    | Before constructing run input      |
| `runs`   | Execute an actor with input, get results   | Actual data fetching               |

### Authentication

The MCP uses a Bearer token for authentication:
- Token is stored in `.claude.json` headers
- All actor runs use the same authentication context

## Design Decisions

### Decision 1: Platform-Specific Reference Files
**Rationale**: Each platform has unique input schemas, output formats, and quirks. Separate files allow targeted documentation without bloat.

### Decision 2: MCP-First (No Direct API)
**Rationale**: The Apify MCP abstracts away direct API complexity (pagination, authentication, run polling). Always prefer MCP tools over raw HTTP calls.

### Decision 3: Lazy Documentation Fetching
**Rationale**: Actor input schemas can change. Always fetch docs via `docs` tool before constructing input rather than hardcoding schemas.

## Integration with Tech Stack

### Convex Integration
When storing scraped data in Convex:
1. Normalize the Apify output to match your Convex schema
2. Use Convex mutations to insert/update records
3. Consider using Convex actions for the scraping + storage pipeline

### Next.js Integration
For frontend-triggered scrapes:
1. Create an API route that delegates to Convex action
2. The action calls Apify via this skill's patterns
3. Results are stored and reactively synced to the UI

## Trade-offs

| Choice                     | Gained                          | Sacrificed                      |
| -------------------------- | ------------------------------- | ------------------------------- |
| Single hub skill           | Centralized maintenance         | Slightly longer delegation path |
| Platform-specific refs     | Targeted documentation          | More files to navigate          |
| MCP-first approach         | Simplified integration          | Less control over low-level API |
