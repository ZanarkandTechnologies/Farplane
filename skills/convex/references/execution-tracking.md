# Task Sessions Pattern

## When to Use
Use this pattern when building systems that track execution of long-running tasks across different environments (remote VMs, browsers, research workflows). Based on production code from Zanarkand.

## Official Docs
- [Workflows](https://docs.convex.dev/agents/workflows) - Multi-step agent tasks
- [Scheduling](https://docs.convex.dev/scheduling) - Delayed functions, cron jobs

## System Structure

```
convex/orchestration/
├── schema.ts           # Task session types, status, context schemas
├── task_sessions.ts    # CRUD operations, step logging
├── scheduler.ts        # Delayed tasks, cron jobs
└── <integration>/      # Type-specific handlers (remote_cua/, browser/, etc.)
```

## Core Concept: Unified Execution Tracking

Task sessions provide a **polymorphic** tracking system for different execution environments:

```typescript
// Different execution types share the same session structure
export const taskSessionTypeSchema = v.union(
  v.literal("remote_cua"),      // Remote computer use agent
  v.literal("browser"),          // Browser automation
  v.literal("deep_research"),    // Research workflow
  v.literal("workflow"),         // General workflow orchestration
);
```

## Schema Pattern

### Task Session (Base)
```typescript
export const taskSessionStatusSchema = v.union(
  v.literal("queued"),
  v.literal("running"),
  v.literal("awaiting_input"),
  v.literal("completed"),
  v.literal("failed"),
  v.literal("cancelled"),
);

export const taskSessionSchema = v.object({
  // Type & Context
  type: taskSessionTypeSchema,
  context: taskSessionContextSchema,  // Polymorphic (see below)
  
  // Status
  status: taskSessionStatusSchema,
  statusReason: v.optional(v.string()),
  
  // Input/Output
  inputPrompt: v.string(),
  startedAt: v.number(),
  completedAt: v.optional(v.number()),
  error: v.optional(v.string()),
  
  // Progress
  scratchpad: v.optional(v.string()),      // Agent working memory
  workflowProgress: v.optional(v.string()), // Human-readable status
  
  // Thread Linking
  threadId: v.optional(v.string()),         // Main chat thread
  taskThreadId: v.optional(v.string()),     // Task-specific thread
  parentThreadId: v.optional(v.string()),   // For sub-tasks
  toolCallId: v.optional(v.string()),       // Triggering tool call
  
  // Ownership
  ownerId: v.id("employees"),
});
```

### Polymorphic Context (Discriminated Union)
```typescript
export const remoteCuaContextSchema = v.object({
  type: v.literal("remote_cua"),
  morphId: v.string(),
  vncUrl: v.optional(v.string()),
  snapshotId: v.string(),
  mode: remoteSessionMode,
  apiKey: v.string(),
  claudeSessionId: v.optional(v.string()),
  vmStatus: v.optional(vmStatusSchema),
});

export const browserContextSchema = v.object({
  type: v.literal("browser"),
  browserSessionId: v.string(),
  targetUrl: v.optional(v.string()),
  apiKey: v.string(),
});

export const deepResearchContextSchema = v.object({
  type: v.literal("deep_research"),
  researchTarget: v.string(),
  dataCategories: v.array(v.string()),
});

export const taskSessionContextSchema = v.union(
  remoteCuaContextSchema,
  browserContextSchema,
  deepResearchContextSchema,
  workflowContextSchema,
);
```

## Step Logging Pattern

Track progress with append-only step logs:

```typescript
export const taskSessionStepSchema = v.object({
  taskSessionId: v.id("taskSessions"),
  stepName: v.string(),                   // e.g., "exec_command", "screenshot"
  message: v.optional(v.string()),        // Human-readable description
  detail: v.optional(v.string()),         // Detailed output/logs
  payload: v.optional(v.any()),           // Structured data
  progress: v.optional(v.number()),       // 0-100 percentage
  screenshotUrl: v.optional(v.string()), // Visual debugging
  createdAt: v.number(),
});
```

### Adding Steps
```typescript
export const addTaskSessionStep = internalMutation({
  args: {
    taskSessionId: v.id("taskSessions"),
    stepName: v.string(),
    message: v.optional(v.string()),
    payload: v.optional(v.any()),
    progress: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    const session = await ctx.db.get(args.taskSessionId);
    if (!session) throw new Error("Task session not found");

    const stepId = await ctx.db.insert("taskSessionSteps", {
      ...args,
      createdAt: Date.now(),
    });

    // Auto-update session status
    if (args.stepName === "completed" || args.stepName === "failed") {
      await ctx.db.patch(args.taskSessionId, {
        status: args.stepName === "completed" ? "completed" : "failed",
        completedAt: Date.now(),
      });
    } else if (session.status === "queued") {
      // First step moves to running
      await ctx.db.patch(args.taskSessionId, { status: "running" });
    }

    return stepId;
  },
});
```

## Delegation Pattern

Link tool calls to child threads/sessions:

```typescript
export const delegationSchema = v.object({
  toolCallId: v.string(),                 // From agent framework
  childThreadId: v.string(),              // Created child thread
  parentThreadId: v.string(),             // For navigation back
  taskSessionId: v.optional(v.id("taskSessions")),
  createdAt: v.number(),
});
```

## API Key Pattern

Generate simple API keys for remote agent authentication:

```typescript
function generateApiKey(): string {
  return `sk_${Math.random().toString(36).substring(2, 15)}${Math.random().toString(36).substring(2, 15)}`;
}

export const createTaskSession = internalMutation({
  args: taskSessionInputSchema,
  handler: async (ctx, args) => {
    let context = args.context;
    
    // Auto-generate API key if needed
    if (context.type === "remote_cua" || context.type === "browser") {
      if (!context.apiKey) {
        context = { ...context, apiKey: generateApiKey() };
      }
    }

    return await ctx.db.insert("taskSessions", {
      ...args,
      context,
      status: "queued",
      startedAt: Date.now(),
    });
  },
});
```

## Table Indexes

```typescript
export const taskSessionSystemTables = {
  taskSessions: defineTable(taskSessionSchema)
    .index("by_status", ["status"])
    .index("by_type", ["type"])
    .index("by_owner", ["ownerId"])
    .index("by_threadId", ["threadId"])
    .index("by_toolCallId", ["toolCallId"]),

  taskSessionSteps: defineTable(taskSessionStepSchema)
    .index("by_taskSession", ["taskSessionId"]),

  delegations: defineTable(delegationSchema)
    .index("by_tool_call", ["toolCallId"])
    .index("by_child_thread", ["childThreadId"])
    .index("by_parent_thread", ["parentThreadId"]),
};
```

## HTTP Endpoint Pattern

Allow remote agents to report progress via HTTP:

```typescript
// convex/http.ts
http.route({
  path: "/task-session/step",
  method: "POST",
  handler: httpAction(async (ctx, req) => {
    const { sessionId, apiKey, stepName, message, payload } = await req.json();
    
    // Verify API key
    const session = await ctx.runQuery(
      internal.orchestration.task_sessions.getTaskSession,
      { taskSessionId: sessionId }
    );
    if (!session || session.context.apiKey !== apiKey) {
      return new Response("Unauthorized", { status: 401 });
    }
    
    // Add step
    await ctx.runMutation(
      internal.orchestration.task_sessions.addTaskSessionStep,
      { taskSessionId: sessionId, stepName, message, payload }
    );
    
    return new Response("OK", { status: 200 });
  }),
});
```

## Key Patterns Summary

| Pattern | Purpose |
|---------|---------|
| Polymorphic context | Different execution types share base structure |
| Step logging | Append-only progress tracking |
| Delegations | Link tool calls to child threads |
| API keys | Authenticate remote agent callbacks |
| Status auto-update | Steps can trigger status changes |
| Thread linking | Connect sessions to chat threads |

