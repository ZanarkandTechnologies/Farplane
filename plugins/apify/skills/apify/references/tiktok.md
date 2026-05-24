# TikTok Platform Reference

Actors for scraping TikTok videos and comments.

## Available Actors

| Actor ID                          | Purpose                    |
| --------------------------------- | -------------------------- |
| `clockworks/tiktok-scraper`       | Videos, profiles, hashtags |
| `clockworks/tiktok-comments-scraper` | Comments on videos      |

## Workflow: Fetch TikTok Videos

### Step 1: Get Actor Documentation
```
Use apify MCP `docs` tool with actor: "clockworks/tiktok-scraper"
```

### Step 2: Prepare Input
Common input parameters:
- `profiles`: Array of TikTok profile URLs or usernames.
- `hashtags`: Array of hashtags to search.
- `resultsPerPage`: Number of results per page.
- `maxItems`: Maximum total items to fetch.

Example input (profile scrape):
```json
{
  "profiles": ["https://www.tiktok.com/@username"],
  "maxItems": 30
}
```

Example input (hashtag search):
```json
{
  "hashtags": ["aitools"],
  "maxItems": 50
}
```

### Step 3: Execute Run
```
Use apify MCP `runs` tool with:
  - actorId: "clockworks/tiktok-scraper"
  - input: (the JSON from Step 2)
```

## Workflow: Fetch TikTok Comments

### Step 1: Get Actor Documentation
```
Use apify MCP `docs` tool with actor: "clockworks/tiktok-comments-scraper"
```

### Step 2: Prepare Input
- `postURLs`: Array of TikTok video URLs.
- `maxComments`: Maximum comments per video.

Example input:
```json
{
  "postURLs": ["https://www.tiktok.com/@user/video/1234567890"],
  "maxComments": 100
}
```

### Step 3: Execute and Extract
Run the actor and parse the comments array from output.

## Output Fields Reference

Common fields returned by the video scraper:
- `id`: Video ID
- `desc`: Video description/caption
- `createTime`: Upload timestamp
- `diggCount`: Number of likes
- `shareCount`: Number of shares
- `commentCount`: Number of comments
- `playCount`: Number of views
- `author`: Author information
- `music`: Associated audio track

## Tips

1. **Hashtag Discovery**: Great for trend research and content ideation.
2. **Video Downloads**: The output includes `downloadUrl` for the video file.
3. **Rate Limits**: TikTok can be aggressive. Use reasonable limits and delays.

