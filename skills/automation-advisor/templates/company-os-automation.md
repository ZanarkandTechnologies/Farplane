# Company OS Automation Template

Start from the complete operated templates below. They are the Farplane
adaptation of Zanarkand AI's Company OS automations:

- `<office-root>/automations/daily-operating-update.md`
- `<office-root>/automations/weekly-operating-review.md`

`office-root` is the explicit AI Office checkout, never the installed skill
directory and never a managed project's thin `farplane/` adapter. If it is not
bound, stop with the missing input instead of searching for another copy.

Replace project identity, source bindings, destinations, and schedules. Retain
the full stage contract: collection boundaries, exact matching, pagination,
cache shape, isolated skill writes, JSON validation, rendering, freshness
checks, provider allowlists, readback, and receipts. This outline is a review
map, not a replacement prompt:

```text
Use $pm-daily | $pm-weekly.

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
