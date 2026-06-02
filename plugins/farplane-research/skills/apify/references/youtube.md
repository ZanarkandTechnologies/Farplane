# YouTube Platform Reference

Actors for scraping YouTube content: videos, shorts, comments, and transcripts.

## Available Actors

| Actor ID                             | Purpose                          |
| ------------------------------------ | -------------------------------- |
| `streamers/youtube-scraper`          | Full video data and transcripts  |
| `streamers/youtube-comments-scraper` | Comments from videos             |
| `streamers/youtube-shorts-scraper`   | YouTube Shorts content           |

## Workflow: Fetch YouTube Transcripts

This is the most common use case for research and content analysis.

### Step 1: Get Actor Documentation
```
Use apify MCP `docs` tool with actor: "streamers/youtube-scraper"
```

### Step 2: Prepare Input
Common input parameters:
- `startUrls`: Array of YouTube video URLs to scrape.
- `maxResults`: Limit the number of results (default varies).
- `downloadSubtitles`: Set to `true` to fetch transcripts.
- `subtitlesLanguage`: Language code (e.g., `"en"` for English).

Example input:
```json
{
  "startUrls": ["https://www.youtube.com/watch?v=VIDEO_ID"],
  "downloadSubtitles": true,
  "subtitlesLanguage": "en"
}
```

### Step 3: Execute Run
```
Use apify MCP `runs` tool with:
  - actorId: "streamers/youtube-scraper"
  - input: (the JSON from Step 2)
```

### Step 4: Extract Transcript
The output will include a `subtitles` or `transcript` field containing the full text.

## Workflow: Fetch Video Comments

### Step 1: Get Actor Documentation
```
Use apify MCP `docs` tool with actor: "streamers/youtube-comments-scraper"
```

### Step 2: Prepare Input
- `startUrls`: Array of YouTube video URLs.
- `maxComments`: Maximum number of comments to fetch.

### Step 3: Execute and Extract
Run the actor and extract the `comments` array from the output.

## Workflow: Scrape YouTube Shorts

### Step 1: Get Actor Documentation
```
Use apify MCP `docs` tool with actor: "streamers/youtube-shorts-scraper"
```

### Step 2: Prepare Input
- `startUrls`: Array of Shorts URLs or channel URLs.
- `maxResults`: Limit the number of shorts.

## Output Fields Reference

Common fields returned by the YouTube scraper:
- `title`: Video title
- `description`: Video description
- `viewCount`: Number of views
- `likeCount`: Number of likes
- `duration`: Video length
- `channelName`: Uploader's channel name
- `uploadDate`: When the video was published
- `subtitles`: Full transcript text (if requested)

## Tips

1. **Batch Processing**: Pass multiple URLs in `startUrls` for efficiency.
2. **Transcript Fallback**: If `downloadSubtitles` fails, auto-generated captions may not be available.
3. **Rate Consideration**: YouTube is generally lenient, but avoid excessive parallel runs.

