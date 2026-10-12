---
captured_at: 2026-08-15
kind: synthetic-repository-evidence-fixture
topic: streamed-tool-results
---

# StreamForge Repository Evidence

This deterministic fixture represents a captured current repository snapshot.
Its URLs and paths are supplied evidence for the eval, not live-web claims.

- Repository: https://github.com/streamforge-js/agent-stream
- Updated: 2026-08-09
- Release: `v4.3.1` on 2026-08-07
- Source root: `packages/core/src/stream/`

Literal query hits:

- `tool-call-delta` -> `packages/core/src/stream/parse-provider-event.ts`
- `ToolResultPart` -> `packages/core/src/stream/parts.ts`
- `AbortSignal` -> `packages/core/src/stream/run-tools.ts`
- `toolCallId` -> source and tests below

## File map

- `packages/core/src/stream/parse-provider-event.ts`: converts provider chunks
  to internal text and tool-call delta parts
- `packages/core/src/stream/tool-call-buffer.ts`: assembles JSON arguments by
  `toolCallId` and rejects an incomplete terminal payload
- `packages/core/src/stream/run-tools.ts`: validates arguments, executes tools,
  propagates abort, and emits result/error parts
- `packages/core/src/stream/parts.ts`: discriminated event contracts
- `packages/core/test/stream/tool-call-buffer.test.ts`: partial/multiple calls
- `packages/core/test/stream/run-tools.test.ts`: schema, throw, abort, timeout
- `packages/node/src/http/write-data-stream.ts`: Node response serialization

Direct source and test URLs:

- https://github.com/streamforge-js/agent-stream/blob/main/packages/core/src/stream/tool-call-buffer.ts
- https://github.com/streamforge-js/agent-stream/blob/main/packages/core/src/stream/run-tools.ts
- https://github.com/streamforge-js/agent-stream/blob/main/packages/core/test/stream/tool-call-buffer.test.ts
- https://github.com/streamforge-js/agent-stream/blob/main/packages/core/test/stream/run-tools.test.ts

```ts
export type ToolStreamPart =
  | { type: "tool-call-delta"; toolCallId: string; delta: string }
  | { type: "tool-call"; toolCallId: string; name: string; args: unknown }
  | { type: "tool-result"; toolCallId: string; result: unknown }
  | { type: "tool-error"; toolCallId: string; error: SerializedError };
```

`run-tools.ts` validates the assembled input before execution, races tool work
against the supplied abort signal and timeout, serializes thrown errors into a
`tool-error` part, and never resumes model generation after abort. Tests cover
interleaved deltas for two calls, invalid JSON, schema mismatch, thrown tools,
timeout, client abort, and successful continued generation.

## Local constraint

The target is a smaller Node service with one provider, an existing Web Stream
response, three explicitly registered tools, no UI protocol compatibility
promise, and no need for multi-step model continuation in the first release.
