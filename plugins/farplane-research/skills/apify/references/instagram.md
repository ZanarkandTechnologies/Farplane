# Instagram Platform Reference

Actors for scraping Instagram posts, reels, and profile data.

## Available Actors

| Actor ID                      | Purpose                      |
| ----------------------------- | ---------------------------- |
| `apify/instagram-scraper`     | Posts, profiles, hashtags    |
| `apify/instagram-reel-scraper`| Reels and short-form videos  |

## Workflow: Fetch Instagram Posts

### Step 1: Get Actor Documentation
```
Use apify MCP `docs` tool with actor: "apify/instagram-scraper"
```

### Step 2: Prepare Input
Common input parameters:
- `directUrls`: Array of post or profile URLs.
- `resultsLimit`: Maximum number of results.
- `searchType`: Type of search (`"user"`, `"hashtag"`, `"place"`).
- `search`: Search query (used with `searchType`).

Example input (profile scrape):
```json
{
  "directUrls": ["https://www.instagram.com/username/"],
  "resultsLimit": 20
}
```

Example input (hashtag search):
```json
{
  "searchType": "hashtag",
  "search": "aiart",
  "resultsLimit": 50
}
```

### Step 3: Execute Run
```
Use apify MCP `runs` tool with:
  - actorId: "apify/instagram-scraper"
  - input: (the JSON from Step 2)
```

## Workflow: Fetch Instagram Reels

### Step 1: Get Actor Documentation
```
Use apify MCP `docs` tool with actor: "apify/instagram-reel-scraper"
```

### Step 2: Prepare Input
- `directUrls`: Array of reel URLs or profile URLs.
- `resultsLimit`: Maximum number of reels.

### Step 3: Execute and Extract
Run the actor and parse the reels from the output.

## Output Fields Reference

Common fields returned:
- `shortCode`: Unique post identifier
- `caption`: Post caption text
- `commentsCount`: Number of comments
- `likesCount`: Number of likes
- `timestamp`: When posted
- `ownerUsername`: Author's handle
- `displayUrl`: Image/video preview URL
- `videoUrl`: Direct video URL (for reels/videos)

## Tips

1. **Proxy Requirements**: Instagram heavily blocks datacenter IPs. Use residential proxies for reliable scraping.
2. **Login State**: Some content requires authenticated sessions.
3. **Rate Limits**: Keep requests low and add delays between batches.
4. **Private Accounts**: Cannot scrape private profiles without authentication.

