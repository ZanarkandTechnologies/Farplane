# Stop Hook Routing

The Stop hook is the central router for active `ralph` / `impl` ticket work.

It uses two internal role passes, and only when needed:

1. `reviewer`
   - decides whether same-ticket work clearly remains
   - may route directly to orchestrator or block for user
   - may judge evidence sufficiency as part of the same review decision
2. `orchestrator`
   - chooses at most one next ticket or stops
   - may return the same ticket for a new explicit phase such as documenting

Rules:

- do not call both roles on every Stop event
- disable hooks on inner `codex exec` role calls
- ticket selection precedence is:
  1. explicit selector
  2. current-run state
  3. one unambiguous active ticket
  4. otherwise block safely
- the ticket remains the durable source of truth
