# Content / Proposal Ledger DB Template

Use this as the high-volume URL-keyed ledger of discovered content and proposal
state.

Recommended fields:

- `Canonical Key`: unique text key generated from the canonical URL
- `Canonical URL`: normalized content URL
- `Title`: content title or compact thread label
- `Platform`: `x`, `youtube`, or `blog`
- `Kind`: `post`, `thread`, `video`, `short`, or `article`
- `Profiles`: relation to tracked profiles
- `First Seen At`: date/time
- `Last Seen At`: date/time
- `Last Ingested At`: date/time
- `Content Hash`: optional hash for changed content detection
- `Status`: `seen`, `ignored`, `scout-queued`, `scouted`, `proposed`,
  `rejected`, or `ticketed`
- `Scout Run`: local path to `experiments/harness-scout/runs/...`
- `SRC Ref`: optional `SRC-*` when promoted to durable source provenance
- `Decision`: `adopt`, `adapt`, `defer`, `reject`, or `needs-benchmark`
- `Proposal Summary`: short operator-facing proposal
- `Ticket Link`: optional local ticket path or external task URL

Uniqueness rule: one canonical URL/key should map to one ledger row. If the
same content is discovered from several profiles, append profile relations
instead of creating duplicate rows.

