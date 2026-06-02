# LinkedIn Platform Reference

Actor for scraping LinkedIn profile data.

## Available Actors

| Actor ID                           | Purpose              |
| ---------------------------------- | -------------------- |
| `dev_fusion/Linkedin-Profile-Scraper` | Profile information |

## Workflow: Fetch LinkedIn Profiles

### Step 1: Get Actor Documentation
```
Use apify MCP `docs` tool with actor: "dev_fusion/Linkedin-Profile-Scraper"
```

### Step 2: Prepare Input
Common input parameters:
- `profileUrls`: Array of LinkedIn profile URLs.
- `cookie`: LinkedIn session cookie (often required).

Example input:
```json
{
  "profileUrls": [
    "https://www.linkedin.com/in/username/"
  ]
}
```

### Step 3: Execute Run
```
Use apify MCP `runs` tool with:
  - actorId: "dev_fusion/Linkedin-Profile-Scraper"
  - input: (the JSON from Step 2)
```

## Output Fields Reference

Common fields returned:
- `fullName`: Person's full name
- `headline`: Professional headline
- `summary`: About section
- `location`: Geographic location
- `connections`: Connection count
- `experience`: Array of work experiences
- `education`: Array of educational background
- `skills`: Array of listed skills
- `certifications`: Professional certifications

## Tips

1. **Authentication Required**: LinkedIn aggressively blocks unauthenticated scraping. A valid session cookie is typically required.
2. **Residential Proxies**: Datacenter IPs are usually blocked. Use residential or mobile proxies.
3. **Rate Limits**: LinkedIn is very protective. Scrape slowly and in small batches.
4. **Legal Considerations**: Be aware of LinkedIn's Terms of Service regarding data scraping.
5. **Cookie Expiration**: Session cookies expire. Refresh them regularly.

