## Video App Testing (Cheat Sheet)

### What to test (minimum)
- **Playback correctness**: start/pause/seek, buffering states, error states.
- **Codec/container coverage**: at least a representative set of formats you claim to support.
- **Bandwidth adaptation**: quality switches, buffering under constrained networks.
- **A/V sync**: drift over time.
- **Upload/processing** (if applicable): retries, timeouts, resumable uploads.

### Agentic-friendly testability (strongly recommended)
Agents can’t reliably “watch” and judge video. Add testability features:\n
- Provide a **frame/time stepper** in dev/test mode (pause, step +1 frame/+100ms).\n
- Expose current playback time, buffering state, selected rendition/bitrate as DOM text.\n
- Emit key events to an on-screen event log (play, pause, seek, stalled, ended).\n
- For animation pipelines, add deterministic “tick” controls and disable randomization.\n

### Recommended backpressure
- **Unit**: state machines, parsing, manifests.
- **Integration**: encode/transcode pipeline, storage, CDN paths.
- **Perf**: startup time, rebuffer ratio, memory usage.
- **Device matrix**: at least a minimal browser/OS coverage; some codec bugs are platform-specific.

### Evidence to capture
- Metrics: startup time, rebuffer %, bitrate chosen, error rates.
- Sample media fixtures + expected properties.

