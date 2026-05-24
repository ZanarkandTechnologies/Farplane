# Feed Scout

`feed-scout` monitors tracked profiles and turns newly discovered content into
Codexter proposal candidates.

Start with [SKILL.md](SKILL.md). The important operator modes are:

- `feed-scout:configure`
- `feed-scout:run`
- `feed-scout:review`
- `feed-scout:status`

Validation helpers:

```bash
python3 skills/feed-scout/scripts/validate_profiles.py skills/feed-scout/fixtures/example-profiles.jsonl
python3 skills/feed-scout/scripts/normalize_items.py skills/feed-scout/fixtures/example-items.jsonl
python3 skills/feed-scout/scripts/dedupe_key.py "https://www.youtube.com/watch?v=example"
```

