# Stop Hook Routing

The Stop hook is the central router for active `$impl` ticket work and bounded
same-session `$loop` work.

It uses one internal review role plus one routing role, and only when needed:

1. `completion-reviewer`
   - decides whether same-ticket work clearly remains
   - currently handles missing-result review for impl-mode stops
   - may route directly to orchestrator or block for user when the assistant
     implied more same-ticket work but did not emit a structured `IMPL_RESULT`
2. `orchestrator`
   - chooses at most one next ticket or stops
   - may return the same ticket for a new explicit phase such as documenting

Final completion review should be visible instead of hidden:

- when mechanical phase and artifact gates pass, Stop hook should request one
  visible completion-review receipt keyed by a nonce
- the live reviewer lane should run `review`, write the receipt under
  `tickets/TASK-XXXX/artifacts/review/`, and link it from the ticket `Evidence`
- Stop hook should validate that receipt on the next Stop event before routing
  to orchestrator or completion

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
