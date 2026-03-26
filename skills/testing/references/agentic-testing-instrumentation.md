## Agentic Testing Instrumentation (Make the app testable)

Agents can’t “understand” a UI the way humans do. When testing is hard, the fix is often to add *testability features*.

### 1) Always add stable selectors
- Add `data-testid` for any critical interactive element and any assertion target.
- Prefer `getByTestId`, `getByRole`, `getByLabel` in Playwright.

### 2) Add a debug overlay for complex UIs
For canvas/diagram/video/complex layouts, add a debug overlay in dev/test modes:
- Draw bounding boxes around focus objects
- Render labels/IDs
- Expose the selected object ID as text in the DOM (so the agent can assert it)

### 3) Add “stepper” controls for animations / timelines
If the UI is animated (video, canvas animation, transitions), create a deterministic test mode:
- Pause/step forward one frame or one logical tick at a time
- Expose current time/frame/tick as DOM text
- Make progression explicit so agents can assert intermediate states

### 4) Expose internal state in a test-only way
Add a test-only API (guarded by env flag) such as:
- `window.__TEST__ = { getState, setState, seed, reset }`
- Or a `/test/seed` endpoint for fixtures
- Or a hidden debug panel enabled only in `NODE_ENV=test`

### 5) Multiplayer: always provide a multi-client harness
Agents must be able to run two (or more) clients simultaneously.
Recommended patterns:
- In Playwright: launch two browser contexts/pages (`pageA`, `pageB`) and drive both.\n
- Add “join room by code” flows that work deterministically.\n
- Expose room ID and player IDs in the DOM.\n
- Provide a fast “bot mode” or scripted input mode for one side if needed.\n

### 6) Observability-as-backpressure
If a behavior is hard to assert visually, assert via instrumentation:
- event logs rendered in DOM for key events\n
- counters/metrics displayed in DOM\n
- serialized state snapshots in DOM\n

### Golden rule
If the agent can’t reliably assert it, add instrumentation until it can.

