# Company OS Automation Template

Start from the complete operated templates below. They are the Farplane
adaptation of Zanarkand AI's Company OS automations:

- `<office-root>/farplane/automations/daily-operating-update.md`
- `<office-root>/farplane/automations/weekly-operating-review.md`

`office-root` is the explicit AI Office workspace. Start new configured records
from the Farplane source checkout's root `automations/` recipes.
`bootstrap.sh --office` materializes both paused records in the office's
`farplane/automations/`. Ordinary project bootstrap excludes them. Bind the
office before activation.

Replace project identity, source bindings, destinations, and schedules. Retain
the full stage contract: collection boundaries, exact matching, pagination,
cache shape, isolated skill writes, JSON validation, rendering, freshness
checks, provider allowlists, readback, and receipts. This outline is a review
map, not a replacement prompt:

```text
Use $progress-update | $report-gen.

1. Fetch the bounded provider and project context; freeze sources and coverage.
2. Cache exact local inputs with IDs, revisions, timestamps, URLs, and hashes.
3. Run the owning skill against local files only; require one exact JSON output.
4. Validate, render reports or memory, apply authorized existing-issue actions,
   reread before mutation, and read back every effect.

Do not create or execute tickets, invent strategy, promote broad knowledge, or
perform external side effects.
```

Reject a proposed Company OS prompt that compresses the operated template into
this outline or omits the detailed rules needed to run any stage safely.
