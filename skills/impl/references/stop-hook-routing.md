# Stop Hook Routing

The Stop hook is the central router for active `$impl` ticket work and bounded
same-session `$loop` work.

It uses two internal role passes, and only when needed:

1. `reviewer`
   - decides whether same-ticket work clearly remains
   - may route directly to orchestrator or block for user
   - may judge evidence sufficiency as part of the same review decision
   - on completion paths, treats the main model's completion claim as a
     candidate only and must explicitly judge whether one obvious next step
     still remains
   - should explicitly run `$review` to ground completion judgment and then
     `$advise` to return one best immediate next same-ticket step
     when continuing
2. `orchestrator`
   - chooses at most one next ticket or stops
   - may return the same ticket for a new explicit phase such as documenting

Rules:

- do not call both roles on every Stop event
- do not add a fourth foresight role until the stronger reviewer gate proves insufficient
- disable hooks on inner `codex exec` role calls
- active `$loop` should branch before ticket resolution, evaluate only its local deterministic predicates, and either continue the same session or stop safely without entering reviewer/orchestrator routing
- same-ticket `$impl` continuation requires both:
  1. a loopable build ticket state
  2. an active session-scoped `impl_loop_active` gate plus matching runtime `claim`
- tmux `auto_continue` only controls whether the helper may spawn or reuse a visible lane; it is not sufficient on its own to authorize same-ticket continuation
- explicit same-session stop intent is the v1 `$loop` stop control; Escape/cancel is not a reliable harness-level stop signal
- ticket selection precedence is:
  1. explicit selector
  2. current-run state
  3. one unambiguous active ticket
  4. otherwise block safely
- the ticket remains the durable source of truth
