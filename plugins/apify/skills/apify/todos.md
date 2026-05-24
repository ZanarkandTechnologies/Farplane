# Todos

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
