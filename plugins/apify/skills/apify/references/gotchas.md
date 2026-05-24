# Common Gotchas & Pitfalls for Apify Integration

Document known issues, edge cases, and patterns to avoid when scraping.

## Critical Gotchas

### 1. Rate Limiting
**Issue**: Most platforms aggressively rate-limit scraping requests.
**Mitigation**:
- Use reasonable `maxItems` / `maxResults` limits
- Add delays between batch requests
- Avoid parallel runs against the same platform

### 2. Proxy Requirements
**Issue**: Platforms like Instagram and LinkedIn block datacenter IPs.
**Mitigation**:
- Configure residential proxies in the actor input
- Some actors have built-in proxy options
- Check actor documentation for proxy configuration

### 3. Authentication Expiration
**Issue**: LinkedIn and some Instagram features require session cookies that expire.
**Mitigation**:
- Refresh cookies regularly
- Monitor for authentication errors in run logs
- Have a fallback for unauthenticated data

### 4. Schema Changes
**Issue**: Actor input/output schemas can change without notice.
**Mitigation**:
- Always fetch docs via `docs` tool before constructing input
- Don't hardcode field names in extraction logic
- Validate output structure before processing

## Platform-Specific Gotchas

### YouTube
- **Transcript Availability**: Not all videos have subtitles. Auto-generated captions may be missing.
- **Age-Restricted Content**: Some videos require authentication.

### Twitter/X
- **API Volatility**: Twitter's scraping landscape changes frequently.
- **Thread Detection**: Replies to the same author often indicate threads.

### Instagram
- **Private Profiles**: Cannot scrape without authenticated session.
- **Reel vs. Post**: Different actors for different content types.
- **High Block Rate**: Most aggressive anti-scraping platform.

### TikTok
- **Video Downloads**: URLs may expire quickly. Download immediately if needed.
- **Region Locks**: Some content is geo-restricted.

### LinkedIn
- **Legal Sensitivity**: LinkedIn actively litigates against scrapers.
- **Cookie Dependency**: Almost always requires valid session cookie.
- **Profile Variations**: Different profile types (personal, company, school) have different fields.

### Google Places
- **Review Limits**: Fetching many reviews significantly increases run time.
- **Location Precision**: Broad searches return inconsistent results.

## Edge Cases

### Empty Results
**Scenario**: Actor returns empty array.
**Causes**:
- Invalid URL format
- Content was deleted
- Rate limit hit silently
- Authentication required

**Handling**: Check run logs for warnings before assuming no data exists.

### Partial Data
**Scenario**: Some fields are missing from output.
**Causes**:
- Platform changed their page structure
- Content was partially loaded
- Actor timeout

**Handling**: Implement null checks for all optional fields.

### Run Timeouts
**Scenario**: Long-running actors time out.
**Causes**:
- Too many items requested
- Slow proxy
- Platform throttling

**Handling**: Use smaller batches and pagination.

## "DO NOT" Patterns

- **DO NOT** hardcode input schemas. Always fetch via `docs` tool.
- **DO NOT** run massive batches (1000+ items) in a single run.
- **DO NOT** ignore run logs. They contain critical error information.
- **DO NOT** store raw Apify output directly. Normalize to your schema first.
- **DO NOT** scrape LinkedIn without understanding legal implications.
- **DO NOT** assume all actors support the same proxy configuration.

## Debugging Checklist

When a scrape fails:
1. Check the run logs in Apify Console
2. Verify the input matches current actor schema (use `docs` tool)
3. Test with a single URL before batching
4. Check if the platform is having issues (DownDetector)
5. Verify proxy configuration if using one
6. Check authentication tokens haven't expired
