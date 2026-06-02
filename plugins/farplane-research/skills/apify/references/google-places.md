# Google Places Platform Reference

Actor for scraping Google Maps and Places data.

## Available Actors

| Actor ID                       | Purpose                        |
| ------------------------------ | ------------------------------ |
| `compass/crawler-google-places`| Business listings, reviews     |

## Workflow: Fetch Business Listings

### Step 1: Get Actor Documentation
```
Use apify MCP `docs` tool with actor: "compass/crawler-google-places"
```

### Step 2: Prepare Input
Common input parameters:
- `searchStringsArray`: Array of search queries (e.g., `["coffee shops in NYC"]`).
- `startUrls`: Direct Google Maps URLs.
- `maxCrawledPlaces`: Maximum number of places to fetch.
- `language`: Language code for results.
- `includeReviews`: Whether to fetch reviews.
- `maxReviews`: Maximum reviews per place.

Example input (search-based):
```json
{
  "searchStringsArray": ["restaurants in San Francisco"],
  "maxCrawledPlaces": 50,
  "includeReviews": true,
  "maxReviews": 10
}
```

Example input (direct URL):
```json
{
  "startUrls": [
    "https://www.google.com/maps/place/..."
  ],
  "includeReviews": true,
  "maxReviews": 20
}
```

### Step 3: Execute Run
```
Use apify MCP `runs` tool with:
  - actorId: "compass/crawler-google-places"
  - input: (the JSON from Step 2)
```

## Output Fields Reference

Common fields returned:
- `title`: Business name
- `address`: Full address
- `phone`: Phone number
- `website`: Business website
- `categoryName`: Business category
- `totalScore`: Average rating (1-5)
- `reviewsCount`: Total number of reviews
- `openingHours`: Operating hours
- `location`: Latitude and longitude
- `reviews`: Array of review objects (if requested)

Review object fields:
- `name`: Reviewer name
- `text`: Review content
- `stars`: Rating given
- `publishedAtDate`: When posted

## Tips

1. **Search Queries**: Be specific with location for better results.
2. **Geolocation**: Use specific city/area names rather than broad regions.
3. **Review Depth**: Fetching many reviews per place increases run time significantly.
4. **Rate Limits**: Google Maps is generally tolerant but avoid excessive parallelism.
5. **Data Freshness**: Business data changes frequently. Consider re-scraping periodically.

