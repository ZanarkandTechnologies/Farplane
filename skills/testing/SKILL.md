---
name: testing
version: 1.1.0
description: "Testing index skill for selecting backpressure and domain guidance."
tier: 2
source: local
---

# Testing Index

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Classify the system under test and the risk being controlled.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) to inspect
  existing scripts, prior tests, framework conventions, and known failure modes.
- [ ] Choose the cheapest meaningful backpressure: typecheck, lint, unit,
  integration, browser, visual, eval, smoke, or manual proof.
- [ ] Name what the selected test proves and what it does not prove.
- [ ] Run or specify the command/artifact expected by the caller.
- [ ] Capture logs, screenshots, traces, fixtures, or result files when proof
  needs to survive handoff.
- [ ] Use [advise](../advise/SKILL.md) when there are meaningful tradeoffs
  between speed, confidence, flake risk, and coverage.
- [ ] Use [review](../review/SKILL.md) before changing durable test strategy or
  claiming high-risk work is validated.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this skill as a lightweight router to testing guidance across domains.

## Core Pattern
1. Classify the system (CRUD web / API / AI / voice / video / canvas / multiplayer).
2. Pick backpressure (tests, typecheck, lint, build, evals).
3. Choose tools (Playwright where it fits; otherwise domain harnesses).
4. Capture evidence (logs, screenshots, fixtures, traces).

## Domain-Specific Testing
Each domain skill may include `references/how-to-test.md`. This index should list them:

- [index.md](references/index.md) (auto-generated)

## References (start here)
- [testing-strategy-decision-tree.md](references/testing-strategy-decision-tree.md) - When Playwright is enough vs when you need other test types.
- [agentic-testing-instrumentation.md](references/agentic-testing-instrumentation.md) - Make products testable by agents (hooks, steppers, overlays, multi-client harnesses).
- [crud-web-app.md](references/crud-web-app.md) - Typical web CRUD app testing.
- [api-backend.md](references/api-backend.md) - Contract, idempotency, load, observability.
- [ai-app.md](references/ai-app.md) - Evals, regression sets, prompt/agent behavior, non-determinism handling.
- [voice-app.md](references/voice-app.md) - STT/TTS, latency, device permissions, network.
- [video-app.md](references/video-app.md) - Playback/encoding, bandwidth adaptation, quality.
- [canvas-app.md](references/canvas-app.md) - Rendering correctness, perf, input events.
- [multiplayer-2p-game.md](references/multiplayer-2p-game.md) - Sync, determinism, cheating, latency.
