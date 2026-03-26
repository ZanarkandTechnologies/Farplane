# Chat & AI Agents Patterns

## When to Use
Use these patterns when building AI-powered chat systems with Convex Agents. Based on production code from Zanarkand.

## Official Docs
- [Agents Overview](https://docs.convex.dev/agents) - Full agent documentation
- [Threads](https://docs.convex.dev/agents/threads) - Thread management
- [Streaming](https://docs.convex.dev/agents/streaming) - Real-time responses
- [Tools](https://docs.convex.dev/agents/tools) - Agent capabilities
- [Human Agents](https://docs.convex.dev/agents/human-agents) - Human-in-the-loop

## System Structure

```
convex/chat_system/
├── schema.ts           # Thread types, status schemas
├── chats.ts            # Main chat logic, streaming, thread management
├── chat_node.ts        # Node.js actions (if needed)
├── thread_titles.ts    # Auto-generate titles from conversation
├── prompts.ts          # System prompt templates
└── scratchpad.ts       # Agent working memory (optional)
```

## Thread Schema Pattern

```typescript
// convex/chat_system/schema.ts
import { defineTable } from "convex/server";
import { v, Infer } from "convex/values";

export const chatTypeSchema = v.union(
  v.literal("dm"),         // Direct Message with an Agent
  v.literal("team"),       // Team Channel
  v.literal("project"),    // Project Thread
  v.literal("task"),       // Task Thread (sub-conversation)
  v.literal("general"),    // General/Fallback
);

export const chatStatusTypeSchema = v.union(
  v.literal("info"),
  v.literal("success"),
  v.literal("question"),
  v.literal("warning"),
  v.literal("none"),
);

export const chatStatusObjectSchema = v.object({
  message: v.string(),     // e.g., "researching...", "writing report"
  type: chatStatusTypeSchema,
});

export const chatSchema = v.object({
  threadId: v.string(),    // Agent framework thread ID
  userId: v.string(),
  type: chatTypeSchema,
  title: v.optional(v.string()),
  
  // Polymorphic references (context)
  employeeId: v.optional(v.id("employees")),
  teamId: v.optional(v.id("teams")),
  projectId: v.optional(v.id("projects")),
  parentThreadId: v.optional(v.string()), // For sub-threads
  
  // Agent status
  status: v.optional(chatStatusObjectSchema),
  scratchpad: v.optional(v.string()),  // Agent working memory
  lastStatusUpdate: v.optional(v.number()),
});

export const chats = defineTable(chatSchema)
  .index("by_threadId", ["threadId"])
  .index("by_userId", ["userId"])
  .index("by_employeeId", ["userId", "employeeId"])
  .index("by_parentThreadId", ["parentThreadId"]);

export const chatSystemTables = { chats };
```

## Agent Setup Pattern

```typescript
// convex/chat_system/chats.ts
import { Agent, stepCountIs } from "@convex-dev/agent";
import { components } from "../_generated/api";
import { usageHandler } from "../usage_tracking/usage_handler";

export const chatAgent = new Agent(components.agent, {
  name: "Chat Agent",
  languageModel: chatModel,
  providerOptions: chatModelProviderOptions,
  stopWhen: [stepCountIs(50)],  // Prevent runaway loops
  usageHandler: usageHandler,   // Track token usage
});
```

## Thread Creation Pattern

```typescript
export const createChatbotThread = mutation({
  args: {
    type: v.optional(chatTypeSchema),
    employeeId: v.optional(v.id("employees")),
    title: v.optional(v.string()),
  },
  returns: v.object({ threadId: v.string() }),
  handler: async (ctx, args) => {
    const userId = await requireAuth(ctx);
    const type = args.type || "general";
    
    // Create agent thread
    const { threadId } = await chatAgent.createThread(ctx, {
      userId,
      // Additional metadata as needed
    });

    // Store our chat record
    await ctx.db.insert("chats", {
      threadId,
      userId,
      type,
      title: args.title || "New Chat",
      employeeId: args.employeeId,
    });

    return { threadId };
  },
});
```

## Streaming Response Pattern

```typescript
import { syncStreams, vStreamArgs } from "@convex-dev/agent";

export const streamChatbotResponse = internalAction({
  args: {
    threadId: v.string(),
    ...vStreamArgs,
  },
  returns: v.string(),
  handler: async (ctx, args) => {
    // Resolve system prompt dynamically
    const systemPrompt = await resolveSystemPrompt(ctx, args.threadId);
    
    // Load tools for this agent
    const tools = await loadToolsForAgent(ctx, args.threadId);
    
    // Run with streaming
    const result = await chatAgent.run(
      ctx,
      { threadId: args.threadId },
      {
        systemPrompt,
        tools,
      }
    );
    
    // Sync streams to frontend
    await syncStreams(ctx, args, result.thread);
    
    return result.thread.threadId;
  },
});
```

## Status Updates Pattern

Show agent activity in real-time:

```typescript
// Update status during processing
export const updateChatStatus = internalMutation({
  args: {
    threadId: v.string(),
    status: chatStatusObjectSchema,
  },
  handler: async (ctx, args) => {
    const chat = await ctx.db
      .query("chats")
      .withIndex("by_threadId", (q) => q.eq("threadId", args.threadId))
      .first();
    
    if (chat) {
      await ctx.db.patch(chat._id, {
        status: args.status,
        lastStatusUpdate: Date.now(),
      });
    }
  },
});

// Usage in agent action
await ctx.runMutation(internal.chat_system.chats.updateChatStatus, {
  threadId,
  status: { message: "researching...", type: "info" },
});
```

## Parent/Child Thread Pattern

For task delegation to sub-agents:

```typescript
/**
 * THREAD ARCHITECTURE
 * 
 * 1. MAIN THREAD (threadId)
 *    User ↔ Main Agent
 *    - User messages visible
 *    - Agent responses visible
 *    - Task completion cards shown here
 * 
 * 2. TASK THREAD (child)
 *    Main Agent ↔ Sub-Agent
 *    - Created for delegated tasks
 *    - Technical details, progress
 *    - NOT visible to user directly
 */

export const createTaskThread = mutation({
  args: {
    parentThreadId: v.string(),
    taskDescription: v.string(),
  },
  returns: v.object({ threadId: v.string() }),
  handler: async (ctx, args) => {
    // Get parent chat for context
    const parentChat = await ctx.db
      .query("chats")
      .withIndex("by_threadId", (q) => q.eq("threadId", args.parentThreadId))
      .first();
    
    if (!parentChat) throw new Error("Parent thread not found");

    const { threadId } = await taskAgent.createThread(ctx, {
      userId: parentChat.userId,
    });

    await ctx.db.insert("chats", {
      threadId,
      userId: parentChat.userId,
      type: "task",
      title: args.taskDescription,
      parentThreadId: args.parentThreadId,
    });

    return { threadId };
  },
});
```

## Auto-Title Generation Pattern

```typescript
// convex/chat_system/thread_titles.ts
export const generateThreadTitle = internalAction({
  args: { threadId: v.string() },
  handler: async (ctx, args) => {
    // Get recent messages
    const messages = await ctx.runQuery(
      internal.chat_system.chats.getRecentMessages,
      { threadId: args.threadId, limit: 5 }
    );
    
    // Generate title with LLM
    const title = await generateTitle(messages);
    
    // Update chat
    await ctx.runMutation(internal.chat_system.chats.updateChatTitle, {
      threadId: args.threadId,
      title,
    });
  },
});

// Schedule title update after first message
await ctx.scheduler.runAfter(
  5000, // 5 seconds after conversation starts
  internal.chat_system.thread_titles.generateThreadTitle,
  { threadId }
);
```

## Typed UIMessage Pattern

```typescript
import { UIMessage, InferUITools } from "ai";

// Define metadata shape
const chatMetadataSchema = v.object({
  employeeId: v.optional(v.id("employees")),
});
type ChatMetadata = Infer<typeof chatMetadataSchema>;

// Typed message for frontend
export type ChatUIMessage = UIMessage<
  ChatMetadata,
  ChatDataPart,
  InferUITools<AllAgentTools>
>;
```

## Key Patterns Summary

| Pattern | Purpose |
|---------|---------|
| Thread types | Distinguish DM, team, project, task contexts |
| Status updates | Show real-time agent activity |
| Parent/child threads | Delegate tasks to sub-agents |
| Streaming | Real-time response delivery |
| Auto-titles | Generate titles from conversation |
| Scratchpad | Agent working memory per thread |

