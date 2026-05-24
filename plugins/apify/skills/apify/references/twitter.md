# Twitter Platform Reference

Actor for scraping tweets and Twitter content.

## Available Actors

| Actor ID                | Purpose                    |
| ----------------------- | -------------------------- |
| `apidojo/tweet-scraper` | Tweets, threads, profiles  |

## Workflow: Fetch Tweets

### Step 1: Get Actor Documentation
```
Use apify MCP `docs` tool with actor: "apidojo/tweet-scraper"
```

### Step 2: Prepare Input
Common input parameters:
- `startUrls`: Array of tweet URLs or profile URLs.
- `searchTerms`: Array of search queries.
- `maxTweets`: Maximum number of tweets to fetch.
- `includeReplies`: Whether to include replies.

Example input (search-based):
```json
{
  "searchTerms": ["AI agents"],
  "maxTweets": 100
}
```

Example input (profile-based):
```json
{
  "startUrls": ["https://twitter.com/username"],
  "maxTweets": 50
}
```

### Step 3: Execute Run
```
Use apify MCP `runs` tool with:
  - actorId: "apidojo/tweet-scraper"
  - input: (the JSON from Step 2)
```

### Step 4: Extract Data
Parse the output array for tweet objects.

## Output Fields Reference

Common fields returned:
- `text`: Tweet content
- `author`: Author's handle and display name
- `createdAt`: Timestamp
- `retweetCount`: Number of retweets
- `likeCount`: Number of likes
- `replyCount`: Number of replies
- `quoteCount`: Number of quote tweets
- `media`: Attached images or videos

## Tips

1. **Search vs. Profile**: Use `searchTerms` for topic discovery, `startUrls` for specific accounts.
2. **Thread Handling**: Replies to the same user often indicate a thread.
3. **API Limits**: Twitter is aggressive with rate limiting. Keep requests reasonable.

