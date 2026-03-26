## Testing Strategy Decision Tree

### Step 0: What kind of system is this?
- Web app (forms/pages/navigation)
- API backend (HTTP/RPC)
- AI app (LLM outputs/agents)
- Voice app (mic/speaker, STT/TTS, realtime)
- Video app (playback, encoding, streaming)
- Canvas app (custom rendering + input)
- Multiplayer (realtime networking + sync)

### Step 1: Is Playwright sufficient?
Playwright is great when:
- The primary value is in browser UX flows (navigation, forms, auth, CRUD).
- You can define stable selectors and deterministic flows.
- You can capture screenshots/traces as evidence.

Playwright is not sufficient alone when:
- Determinism is inherently low (LLMs, realtime networking).
- Hardware/OS constraints dominate (mic/camera, GPU, codecs).
- Performance budgets and timing are core requirements.

### Step 2: Pick backpressure types (mix as needed)
- **Unit tests**: deterministic logic, pure functions, small modules.
- **Integration tests**: DB + backend + services (real or test containers).
- **Contract tests**: API schema/shape compatibility across services.
- **E2E tests (Playwright)**: key user journeys.
- **Load/perf tests**: throughput, latency budgets, regressions.
- **Golden tests**: snapshot outputs, rendered frames, serialized state.
- **Human/LLM evals**: subjective criteria (tone, helpfulness, UX feel) where appropriate.

### Step 3: Evidence expectations (what “pass” looks like)
- CI logs show commands run + exit codes.
- For UI: Playwright traces/screenshots for failing cases.
- For AI: frozen eval sets + acceptance thresholds + drift monitoring.
- For realtime/media: latency histograms + quality metrics + device matrix notes.

