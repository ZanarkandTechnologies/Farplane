# Feed Scout

`feed-scout` monitors tracked profiles and turns newly discovered content into
Farplane proposal candidates.

Start with [SKILL.md](SKILL.md). A separate bounded Feed Scout automation calls
the skill directly; Interval only reads completed Feed Scout reports as BAU
context. Setup, review, and status remain conversational workflows.

Validation helpers:

```bash
python3 skills/feed-scout/scripts/validate_profiles.py skills/feed-scout/fixtures/example-profiles.jsonl
python3 skills/feed-scout/scripts/normalize_items.py skills/feed-scout/fixtures/example-items.jsonl
python3 skills/feed-scout/scripts/dedupe_key.py "https://www.youtube.com/watch?v=example"
python3 skills/feed-scout/scripts/validate_daily_feed.py .farplane/feed-scout/daily/latest.json
```

Feed Scout writes the daily feed JSON and report agentically after reading
project config, acquiring source evidence, calling other skills/tools, and
judging significance. Scripts in this package are deterministic helpers for
validation, dedupe, and normalization; they are not fetchers, rankers, or daily
feed writers.

The dated report contains source-backed, deduped, executable candidates with
Reward, proof, stop, authority, and ticket-quality evidence. Feed Scout may
create a bounded direct recovery ticket for an evidenced existing project
failure with a known fix and no experiment debt. Work Pulse's adaptive planner
ranks opportunities, uncertain fixes, and experiments globally.

Daily feed items should answer `why_care_today` and include `today_delta`,
`novelty`, `actionability`, `source_snapshot`, optional bookmark-card `embed`,
and `interest_prompt_ref` when entity/source prompts are configured.

Default local surfaces for project automations:

- tracked profiles: `.farplane/feed-scout/profiles.jsonl`
- tracked entities: `.farplane/feed-scout/entities.jsonl`
- tracked harness resources: `.farplane/feed-scout/resources.jsonl`
- ingestion ledger: `.farplane/feed-scout/ingestion-ledger.jsonl`
- proposal ledger or inbox: `.farplane/feed-scout/proposals.jsonl`

These files stay ignored local state unless a project deliberately promotes
fixture examples into tracked docs. Use `farplane/automations.toml` to store the
reviewable prompt for an explicit run; do not add a hidden daemon or live
scraping loop.

Notion proposal pages may remain a review surface, but live Tasks admission is
outside Feed Scout and belongs to the project planner or an explicit operator action.
