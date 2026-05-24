## Voice App Testing (Cheat Sheet)

### What to test (minimum)
- **Permissions**: mic permission prompts, denied/blocked flows.
- **Latency**: time-to-first-audio, end-to-end roundtrip for realtime.
- **STT accuracy**: test corpus with accents/noise; confirm “good enough” threshold.
- **TTS quality**: voice selection, clipping, pacing, interruptions.
- **Network**: packet loss, reconnect behavior, offline handling.

### Recommended backpressure
- **Unit**: audio pipeline logic, buffering, state machines.
- **Integration**: STT/TTS provider stubs + retries + fallback behavior.
- **Device matrix**: at least one real-device pass per major OS/browser.
- **Perf**: CPU usage, memory growth over a long session.

### Evidence to capture
- Short audio fixtures (input + expected transcript properties).
- Logs with timestamps for latency breakdown.

