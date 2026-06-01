# Todos

- [ ] Read existing feed-scout config, profile rows, tracked entities,
  tracked harness resources, ledger/proposal artifacts, and the requested mode
  before doing any external discovery.
- [ ] Use [plan](../plan/SKILL.md) when cadence, destination, profile value, or
  live-spend boundaries are unclear.
- [ ] Configure or validate tracked profiles, entities, and harness-resource
  references before discovery.
- [ ] Use [apify](../apify/SKILL.md) only when the platform, credentials,
  actor, spend, and live-run boundary are explicit.
- [ ] Normalize content items, compute canonical URL keys, and dedupe before
  extraction or scouting.
- [ ] Use [summarize](../summarize/SKILL.md) for transcripts, articles, and
  linked source extraction.
- [ ] Use [harness-scout](../harness-scout/SKILL.md) for eligible content items
  and [best-of-worlds](../best-of-worlds/SKILL.md) only when multiple items
  converge on one harness pattern.
- [ ] Write proposals or tickets only for strong adopt/adapt/defer signals; do
  not turn this skill into a daemon or crawler platform.
- [ ] Before writing a live Notion Tasks ticket, resolve required `Project` and
  `Areas` relations from explicit context or private Notion handles, then
  verify readback; if unresolved, mark `routing_missing` or use local-only
  output instead of claiming task writeback success.
