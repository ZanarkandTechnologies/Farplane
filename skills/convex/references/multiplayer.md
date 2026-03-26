# Realtime multiplayer on Convex

Consolidated reference for architecture, room/presence modeling, player state sync, planning, testing, and art-direction workflow.

## 1) Architecture: choose one sync model

### A) Client-driven positions (recommended default)
- Client sends position/velocity at a fixed rate (start at 10 Hz, consider 20 Hz for smoother motion).
- Server stores latest state; other clients subscribe and interpolate.
- Add server-side validation (bounds and speed caps) to reduce obvious cheating.

Use when:
- Casual realtime games or "realtime with friends" products where fast iteration matters.

Tradeoffs:
- Imperfect fairness, occasional jitter, larger cheat surface.

### B) Server-authoritative tick (advanced)
- Clients send inputs.
- Server advances world state on a tick.
- Clients do prediction and reconciliation.

Use when:
- Competitive or twitch experiences where determinism and fairness matter.

Tradeoffs:
- More complexity, more compute, stricter timing design.

### Convex-specific guidance
- Prefer one writer per player state to reduce write conflicts.
- Keep room-level state and per-player state in separate docs/tables.
- Throttle updates aggressively and rely on interpolation in clients.

## 2) Rooms and presence

### Minimal room lifecycle
1. Create room (host becomes first member).
2. Join room by code.
3. Track presence (connected/disconnected/lastSeen).
4. Start game (host-only).
5. Leave room (if host leaves, transfer host or close room).

### Suggested data model
- `rooms`: `{ code, hostUserId, status, createdAt }`
- `roomMembers`: `{ roomId, userId, joinedAt, lastSeenAt, isConnected }`

### Presence updates
- Update `lastSeenAt` on heartbeat every 5-10 seconds.
- Treat offline as `now - lastSeenAt > threshold`.

### Anti-patterns
- Do not rewrite the full room doc for every member update.
- Do not store fast-moving per-player state in the room doc.

## 3) Player state sync

### Update rate
- Start at 10 Hz (100ms), move to 20 Hz only if needed.
- Never write per animation frame.
- Use client interpolation on receive.

### Suggested player-state doc
- `playerStates`: `{ roomId, userId, x, y, vx, vy, dir, updatedAt }`

### Minimum server validation
- Clamp positions to world bounds.
- Cap speed by velocity magnitude or max delta distance per update.

### Rendering guidance
- Keep local render state.
- On subscription update, set target state and interpolate over ~100-200ms.

## 4) Planning order for multiplayer

### Before starting
1. Define player count and room structure.
2. List state that must be realtime-synced.
3. Set latency tolerance and update frequency targets.

### Build order
1. Schema: rooms, players, game-state tables and indexes.
2. Presence system: online state, liveness heartbeat, reconnect behavior.
3. State sync: write/read paths, update cadence, reconciliation.
4. Conflict resolution: last-write-wins or domain-specific merge logic.

### Key design questions
- Maximum concurrent players per room?
- Disconnect/reconnect behavior and timeout thresholds?
- Host-authoritative room or peer-equal model?

### Common gameplay flow pattern
- room creation -> join -> presence -> game loop -> leave
- optimistic client updates with server reconciliation
- heartbeat/ping for liveness

## 5) Testing strategy

### Core strategy
1. Multi-client harness (two browser contexts minimum).
2. Latency simulation (network throttling).
3. Disconnect/reconnect tests (force close/reopen).

### Key assertions
- State sync: clients converge to same authoritative state.
- Presence: join/leave reflected quickly and correctly.
- Conflict resolution: simultaneous actions resolve predictably.
- Recovery: reconnect restores valid state.

### Tools
- Playwright multi-context tests.
- Convex dashboard state inspection.
- Network throttling for latency/jitter simulation.

### Smoke test flow (agent-browser)
1. Player A creates room and captures room code.
2. Player B joins with code.
3. Both clients show connected for both players.
4. Player A moves; Player B sees position update within ~500ms.

### Escalate to Playwright when
- Browser-driven smoke tests are flaky.
- You need stable baseline evidence in CI.

Playwright should assert:
- room join path
- presence timeout path
- position replication tolerance window

### Common test gotchas
- Rapid-fire action spam ("button mashing").
- Cleanup correctness on disconnect.
- Race conditions in concurrent mutations.

## 6) Assets and design workflow (options-first)

Goal: generate multiple distinct art directions, store outputs predictably, and choose deliberately.

### Storage convention
- Assets: `assets/generated/YYYY-MM-DD/<direction>/...`
- Metadata: `assets/generated/YYYY-MM-DD/<direction>/meta.json`
- Exploration notes: `docs/HISTORY.md`
- Final durable decisions: `docs/MEMORY.md`

### Workflow
1. Pick 3-5 visual directions before generating images.
2. Generate a small asset pack per direction:
   - background tile/scene
   - fish sprite idle
   - fish sprite bite/attack
   - UI/HUD mock
3. Present options with:
   - 1-2 sentence concept
   - 3-5 thumbnails/paths
   - tradeoffs (readability, production time, animation complexity)
4. After selecting a direction:
   - generate consistent higher-res packs/sprite sheets
   - optionally run background removal
   - lock palette and typography in `meta.json`
