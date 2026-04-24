# agent-browser: QA Workflows (Standard)

> Purpose: fast, agent-friendly browser QA without writing Playwright code.

## The “special” part

- **Ref-driven automation**: use `snapshot` to get deterministic refs (`@e1`, `@e2`), then act on refs.
- **Prefer `--json`**: machine-readable snapshots reduce ambiguity and flakiness for agents.
- **Multi-session**: `--session <name>` lets you drive multi-user flows without a custom harness.

## Workflow: Quick smoke test (no Playwright)

```bash
RUN_DIR="tickets/artifacts/TASK-XXXX/qa/$(date -u +%F_%H%M%S)_smoke"
mkdir -p "$RUN_DIR/screens" "$RUN_DIR/logs"

agent-browser open http://localhost:3000
agent-browser snapshot -i -c --json > "$RUN_DIR/snapshot.json"
# ...click/fill using @refs from the snapshot...
agent-browser wait --load networkidle
agent-browser screenshot "$RUN_DIR/screens/smoke.png"
agent-browser close
```

## Workflow: Two-user sanity check (sessions)

```bash
agent-browser --session A open http://localhost:3000
agent-browser --session B open http://localhost:3000

agent-browser --session A snapshot -i -c --json
agent-browser --session B snapshot -i -c --json

# ...drive both sessions using their own refs...

agent-browser session list
agent-browser --session A close
agent-browser --session B close
```

## Workflow: Capture evidence for `tickets/artifacts/TASK-XXXX/qa/`

```bash
RUN_DIR="tickets/artifacts/TASK-XXXX/qa/$(date -u +%F_%H%M%S)_smoke"
mkdir -p "$RUN_DIR/screens" "$RUN_DIR/logs"

agent-browser open http://localhost:3000
agent-browser snapshot -i -c --json > "$RUN_DIR/snapshot.json"
agent-browser screenshot "$RUN_DIR/screens/page.png"
agent-browser console > "$RUN_DIR/logs/console.txt" || true
agent-browser errors > "$RUN_DIR/logs/errors.txt" || true
agent-browser close
```

Notes:
- Prefer writing a short report markdown under `$RUN_DIR/report.md` and link to `screens/*`, `logs/*`, and `snapshot.json`.
- If you need *baseline comparisons*, use Playwright’s `toHaveScreenshot` (agent-browser screenshots are great for iteration + artifacts).
