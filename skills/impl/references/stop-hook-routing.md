# Stop Hook Routing

The Stop hook is the mechanical router for active `$impl` ticket work.

Native Codex `/goal` owns semantic continuation and stopping criteria for
Goal-backed work such as board drains, ticket batches, metric loops, or
"figure it out" tasks. Stop hook should not reimplement that autonomy judgment.
It should validate objective protocol and artifact gates for active ticket
work.

It uses one internal review role plus one routing role, and only when needed:

1. `completion-reviewer`
   - validates whether active ticket completion claims satisfy the ticket's
     visible review and evidence requirements
   - currently handles missing-result review for impl-mode stops
   - may route directly to orchestrator or block for user when the assistant
     implied active-ticket completion but did not emit required structure
2. `orchestrator`
   - chooses at most one next ticket or stops
   - may return the same ticket for a new explicit phase such as documenting

Final completion review should be visible instead of hidden:

- when mechanical phase and artifact gates pass, Stop hook should request one
  visible completion-review receipt keyed by a nonce
- the live reviewer lane should run `review`, write the receipt under
  `tickets/TASK-XXXX/artifacts/review/`, and link it from ticket `Links` or `State`
- Stop hook should validate that receipt on the next Stop event before routing
  to orchestrator or completion

Rules:

- do not call both roles on every Stop event
- do not add a fourth foresight role until the stronger reviewer gate proves insufficient
- do not ask Stop hook to judge fuzzy Goal satisfaction, research sufficiency,
  or whether the assistant was thoughtful enough; put that in the native Goal
  contract or the owning skill
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
