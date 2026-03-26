# Convex Gotchas & Best Practices

## When to Use
Review this file before deploying to production and during code reviews. Based on [official best practices](https://docs.convex.dev/understanding/best-practices/) and [platform limits](https://docs.convex.dev/production/state/limits).

---

## Platform Limits

| Resource | Limit | Impact |
|----------|-------|--------|
| **Action timeout** | **10 minutes** | LLM calls, external APIs - use workflows for longer tasks |
| Mutation transaction | 8MB total | Large batch inserts may need splitting |
| Single document | 1MB | Use file storage for large blobs |
| Query/mutation result | 8MB | Paginate large results |
| Scheduler queue | 1000 per function | Batch scheduling for high volume |
| Arguments size | 8MB | Pass IDs, not large payloads |

> **Critical for LLM apps**: The 10-minute action limit means a single action cannot run multiple long LLM calls sequentially. Use workflows to checkpoint between calls.

---

## Best Practices Checklist

### ✅ Always Await Promises

```typescript
// ❌ BAD - floating promise, may fail silently
ctx.scheduler.runAfter(0, internal.tasks.process, { id });
ctx.db.patch(id, { status: "done" });

// ✅ GOOD
await ctx.scheduler.runAfter(0, internal.tasks.process, { id });
await ctx.db.patch(id, { status: "done" });
```

**Tip**: Enable `no-floating-promises` ESLint rule.

### ✅ Use Indexes, Not `.filter()`

```typescript
// ❌ BAD - scans entire table
const tomsMessages = await ctx.db
  .query("messages")
  .filter((q) => q.eq(q.field("author"), "Tom"))
  .collect();

// ✅ GOOD - uses index
const tomsMessages = await ctx.db
  .query("messages")
  .withIndex("by_author", (q) => q.eq("author", "Tom"))
  .collect();
```

### ✅ Limit `.collect()` Results

```typescript
// ❌ BAD - unbounded, could be millions
const allMovies = await ctx.db.query("movies").collect();

// ✅ GOOD - bounded with index
const recentMovies = await ctx.db
  .query("movies")
  .withIndex("by_createdAt")
  .order("desc")
  .take(100);

// ✅ GOOD - paginated
const movies = await ctx.db
  .query("movies")
  .paginate(paginationOpts);
```

### ✅ Include Table Name in `ctx.db` Calls

```typescript
// ❌ OLD style (deprecated)
await ctx.db.get(movieId);
await ctx.db.patch(movieId, { title: "Whiplash" });

// ✅ NEW style (required for custom IDs)
await ctx.db.get("movies", movieId);
await ctx.db.patch("movies", movieId, { title: "Whiplash" });
```

### ✅ Use Helper Functions, Not `ctx.runQuery`

```typescript
// ❌ BAD - unnecessary overhead in mutations
const user = await ctx.runQuery(internal.users.get, { userId });

// ✅ GOOD - plain TypeScript helper
import { getUser } from "./model/users";
const user = await getUser(ctx, userId);
```

**Exception**: Components require `ctx.runQuery/runMutation`.

### ✅ Batch `ctx.runMutation` in Actions

```typescript
// ❌ BAD - loses atomicity, N separate transactions
for (const item of items) {
  await ctx.runMutation(internal.items.insert, item);
}

// ✅ GOOD - single atomic transaction
await ctx.runMutation(internal.items.insertMany, { items });
```

### ✅ Only Schedule Internal Functions

```typescript
// ❌ BAD - public function exposed to scheduler abuse
await ctx.scheduler.runAfter(0, api.tasks.process, { id });

// ✅ GOOD - internal function
await ctx.scheduler.runAfter(0, internal.tasks.process, { id });
```

### ✅ Use Argument Validators

```typescript
// ❌ BAD - no validation
export const createTask = mutation({
  handler: async (ctx, args) => { ... }
});

// ✅ GOOD - explicit validators
export const createTask = mutation({
  args: {
    title: v.string(),
    priority: v.optional(v.number()),
  },
  handler: async (ctx, args) => { ... }
});
```

### ✅ Add Access Control

```typescript
// ❌ BAD - anyone can delete any task
export const deleteTask = mutation({
  args: { taskId: v.id("tasks") },
  handler: async (ctx, args) => {
    await ctx.db.delete("tasks", args.taskId);
  }
});

// ✅ GOOD - verify ownership
export const deleteTask = mutation({
  args: { taskId: v.id("tasks") },
  handler: async (ctx, args) => {
    const userId = await requireAuth(ctx);
    const task = await ctx.db.get("tasks", args.taskId);
    if (task?.ownerId !== userId) {
      throw new Error("Not authorized");
    }
    await ctx.db.delete("tasks", args.taskId);
  }
});
```

---

## LLM App Gotchas

### ⚠️ 10-Minute Action Timeout

Single action cannot run multiple slow LLM calls:

```typescript
// ❌ RISKY - may timeout
export const analyzeDocuments = action({
  handler: async (ctx, args) => {
    for (const doc of args.documents) {
      await llm.analyze(doc); // Each call takes 30s-2min
    }
  }
});

// ✅ GOOD - use workflow with checkpointing
export const analyzeWorkflow = workflow.define({
  handler: async (ctx, args) => {
    for (const doc of args.documents) {
      await ctx.runAction(internal.llm.analyzeSingle, { doc });
      // Workflow checkpoints between steps
    }
  }
});
```

### ⚠️ Rate Limit Handling

LLM providers enforce rate limits (RPM/TPM). Use batching patterns:

```typescript
// Use poolSize to control concurrency
const poolSize = 5; // 5 concurrent requests max

// Add delays between batches if needed
await ctx.scheduler.runAfter(
  60_000, // Wait 1 minute
  internal.research.processBatch,
  { batchNumber: nextBatch }
);
```

### ⚠️ No `setTimeout` in Convex

```typescript
// ❌ BAD - setTimeout doesn't work as expected
await new Promise(resolve => setTimeout(resolve, 5000));

// ✅ GOOD - use scheduler for delays
await ctx.scheduler.runAfter(
  5000,
  internal.tasks.continueProcessing,
  { taskId }
);

// ✅ GOOD - in workflows, just schedule next step
// Workflows handle this automatically with ctx.runAction
```

### ⚠️ Streaming + Long Responses

Long streaming responses need careful handling:

```typescript
// Use syncStreams from @convex-dev/agent
const result = await agent.run(ctx, { threadId }, { ... });
await syncStreams(ctx, streamArgs, result.thread);
```

---

## Documentation Conventions

### Header Comments (Required)

Every logic file MUST start with a header block:

```typescript
/**
 * MODULE NAME (Convex Mutations & Queries)
 * =========================================
 * 
 * Brief description of what this module handles.
 * 
 * KEY CONCEPTS:
 * -------------
 * - Core concept 1
 * - Important behavior or constraint
 * 
 * ARCHITECTURE:
 * -------------
 * - DB Storage: What data is stored
 * - Runtime: What is calculated dynamically
 * 
 * USAGE EXAMPLES:
 * ---------------
 * - Call functionName() to do X
 */
```

### Section Separators

```typescript
// ============================================================================
// REUSABLE VALIDATORS
// ============================================================================

// ============================================================================
// TABLE SCHEMAS
// ============================================================================

// ============================================================================
// MUTATIONS
// ============================================================================
```

### AGENTS.md

Create `convex/AGENTS.md` as backend source of truth:
- Update when architecture changes
- List each system with responsibility
- Document key patterns

See [AGENTS.example.md](AGENTS.example.md) for full template.

---

## Code Review Checklist

Before merging Convex code, check:

**Queries & Data**:
- [ ] No `.filter()` on queries (use `.withIndex`)
- [ ] `.collect()` only on bounded queries
- [ ] Table names in `ctx.db.get/patch/delete`

**Functions**:
- [ ] All promises awaited
- [ ] Argument validators on all public functions
- [ ] Access control on mutations
- [ ] Only internal functions scheduled

**Actions & Workflows**:
- [ ] No sequential `ctx.runMutation` in actions (batch them)
- [ ] Actions under 10 min (use workflows for longer)
- [ ] LLM calls have rate limit handling

**Documentation**:
- [ ] Header comments on logic files
- [ ] AGENTS.md updated if architecture changed

---

## Official Docs

- [Best Practices](https://docs.convex.dev/understanding/best-practices/)
- [Platform Limits](https://docs.convex.dev/production/state/limits)
- [Indexes](https://docs.convex.dev/database/indexes)
- [Error Handling](https://docs.convex.dev/functions/error-handling)

