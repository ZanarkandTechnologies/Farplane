# Stop Hook Routing

The Stop hook is the central router for active `$impl` ticket work.

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
- same-ticket `$impl` continuation requires both:
  1. a loopable build ticket state
  2. an active session-scoped `impl_loop_active` gate plus matching runtime `claim`
- tmux `auto_continue` only controls whether the helper may spawn or reuse a visible lane; it is not sufficient on its own to authorize same-ticket continuation
- ticket selection precedence is:
  1. explicit selector
  2. current-run state
  3. one unambiguous active ticket
  4. otherwise block safely
- the ticket remains the durable source of truth
