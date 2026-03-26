<!-- markdownlint-disable-file -->

# Convex Testing (Unit Tests with `convex-test` + Vitest)

This reference describes how to write **fast unit tests for Convex functions** (queries/mutations/actions/HTTP actions) using the official `convex-test` library and Vitest.

## When to Use This

- **Use `convex-test`** for backend logic regression tests:
  - Validation + auth rules
  - DB writes/reads and indexes
  - Complex mutations and scheduling logic
  - HTTP actions routed through `http.ts`
- **Still do manual testing** for anything dependent on real backend limits, latency, or external services.

## Install Dependencies

From your project root:

```bash
npm install --save-dev convex-test vitest @edge-runtime/vm
```

## Add NPM Scripts

In `package.json`:

```json
{
  "scripts": {
    "test": "vitest",
    "test:once": "vitest run",
    "test:debug": "vitest --inspect-brk --no-file-parallelism",
    "test:coverage": "vitest run --coverage --coverage.reporter=text"
  }
}
```

## Configure Vitest (Edge Runtime)

Create `vitest.config.ts` in the project root:

```ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "edge-runtime",
    server: { deps: { inline: ["convex-test"] } },
  },
});
```

## Create a Test File

Create a file in `convex/` ending with `.test.ts`, e.g. `convex/rooms.test.ts`.

### Basic pattern (schema + modules)

```ts
import { convexTest } from "convex-test";
import { describe, expect, it } from "vitest";
import schema from "./schema";
import { api } from "./_generated/api";

const modules = import.meta.glob("./**/*.ts");

describe("rooms.get", () => {
  it("returns null for missing room", async () => {
    const t = convexTest(schema, modules);
    // Replace with a real call for your project; this is just the skeleton.
    // const room = await t.query(api.rooms.get, { roomId: ... });
    // expect(room).toBeNull();
    expect(true).toBe(true);
  });
});
```

### Calling functions

- `t.query(api.foo.bar, args)`
- `t.mutation(api.foo.bar, args)`
- `t.action(api.foo.bar, args)`
- Internal fns via `internal` from `./_generated/api`

```ts
import { convexTest } from "convex-test";
import { test, expect } from "vitest";
import { api, internal } from "./_generated/api";
import schema from "./schema";

const modules = import.meta.glob("./**/*.ts");

test("call functions", async () => {
  const t = convexTest(schema, modules);
  // await t.query(api.example.get, {});
  // await t.mutation(internal.example.seed, {});
  expect(true).toBe(true);
});
```

## Auth / Identity

Use `t.withIdentity(...)` to test authenticated behavior.

```ts
import { convexTest } from "convex-test";
import { expect, test } from "vitest";
import schema from "./schema";
import { api } from "./_generated/api";

const modules = import.meta.glob("./**/*.ts");

test("auth behavior", async () => {
  const t = convexTest(schema, modules);
  const asAlice = t.withIdentity({ name: "Alice" });

  // await asAlice.mutation(api.rooms.create, { name: "Alice" });
  // const result = await asAlice.query(api.rooms.get, { roomId: ... });
  // expect(result).not.toBeNull();
  expect(asAlice).toBeDefined();
});
```

## Direct DB Setup / Assertions (`t.run`)

Use `t.run(async (ctx) => ...)` to seed data or assert on DB state without needing a dedicated function.

```ts
import { convexTest } from "convex-test";
import { expect, test } from "vitest";
import schema from "./schema";

const modules = import.meta.glob("./**/*.ts");

test("direct db insert", async () => {
  const t = convexTest(schema, modules);
  const doc = await t.run(async (ctx) => {
    // await ctx.db.insert("rooms", { ... });
    return await ctx.db.query("rooms").first();
  });
  expect(doc).toBeNull();
});
```

## HTTP Actions (`t.fetch`)

If your project has `convex/http.ts` routing, test it like:

```ts
import { convexTest } from "convex-test";
import { expect, test } from "vitest";
import schema from "./schema";

const modules = import.meta.glob("./**/*.ts");

test("http route", async () => {
  const t = convexTest(schema, modules);
  const res = await t.fetch("/some/path", { method: "POST" });
  expect(res.status).toBe(200);
});
```

## Scheduled Functions + Fake Timers

Use Vitest fake timers and:
- `t.finishInProgressScheduledFunctions()`
- `t.finishAllScheduledFunctions(vi.runAllTimers)`

```ts
import { convexTest } from "convex-test";
import { expect, test, vi } from "vitest";
import schema from "./schema";
import { api } from "./_generated/api";

const modules = import.meta.glob("./**/*.ts");

test("scheduled functions", async () => {
  vi.useFakeTimers();
  const t = convexTest(schema, modules);

  // await t.mutation(api.scheduler.someMutationThatSchedulesWork, {});
  vi.runAllTimers();
  await t.finishAllScheduledFunctions(vi.runAllTimers);

  expect(true).toBe(true);
  vi.useRealTimers();
});
```

## Notes / Limitations

- `convex-test` is a **mock backend**; it does not enforce all real Convex limits.
- Don’t rely on exact error message strings from the real backend.
- Always keep at least one **manual end-to-end sanity test** path for critical gameplay flows.

## References

- Convex docs: Testing (`convex-test`) — see official documentation section.
- `convex-test` repo test suite (for more examples).

