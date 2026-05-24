## Multiplayer 2-Player Game Testing (Cheat Sheet)

### What to test (minimum)
- **Sync**: do both clients converge on the same state?
- **Latency tolerance**: behavior at realistic ping + jitter.
- **Disconnect/reconnect**: state recovery and session resumption.
- **Cheating / trust boundary**: server authoritative rules where needed.

### Agentic harness (must-have)
Agents must drive **two clients**. Do not rely on “a human plays the other side”.

- Launch two browser contexts or two pages:
  - `pageA` (player 1)
  - `pageB` (player 2)
- Ensure both can deterministically join the same room:
  - “Create room” on `pageA` → copy room code → “Join room” on `pageB`
- Expose room code + player IDs in the DOM (text) so assertions are possible.
- If realtime state is hard to observe visually, expose a test-only state panel or `window.__TEST__.getState()`.

### Recommended backpressure
- **Deterministic simulation tests**: run two clients headless with scripted inputs and assert state invariants.\n
- **Property tests**: “score never decreases”, “players cannot occupy invalid positions”, etc.\n
- **Soak tests**: long-running sessions to catch memory leaks/state drift.\n
- **Network simulation**: inject packet loss/jitter/latency in the harness.

### Evidence to capture
- Serialized state snapshots per tick for failing runs.
- Latency histograms and reconciliation counters.

