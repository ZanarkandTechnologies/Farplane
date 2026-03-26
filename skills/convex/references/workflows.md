# Workflow Patterns

## When to Use
Use these patterns for multi-agent orchestration, iterative refinement, batch processing, and complex research workflows. Based on official examples from [get-convex/agent](https://github.com/get-convex/agent/tree/main/example/convex/workflows).

## Official Docs
- [Workflows](https://docs.convex.dev/agents/workflows) - Multi-step agent tasks
- [Platform Limits](https://docs.convex.dev/production/state/limits) - **10 min action timeout**

---

## Actions vs Workflows: Decision Guide

> **Critical**: Actions timeout at 10 minutes. Workflows checkpoint between steps and can run indefinitely.

| Scenario | Use | Why |
|----------|-----|-----|
| Single LLM call (<2 min) | Action | Simple, direct |
| Multiple sequential LLM calls | **Workflow** | Checkpoints between calls |
| External API + DB write | Action | Quick round-trip |
| Research with 10+ LLM calls | **Workflow** | Exceeds 10 min limit |
| Parallel agent council | **Workflow** | Orchestrate fan-out/fan-in |
| Iterative refinement loop | **Workflow** | Multiple turns with checkpoints |
| Background job (batch processing) | **Workflow** | Resume on failure |

### When to Use Actions

```typescript
// ✅ Quick external call + DB write
export const fetchAndStore = action({
  handler: async (ctx, args) => {
    const data = await fetch(args.url); // Fast
    await ctx.runMutation(internal.data.store, { data });
  }
});

// ✅ Single LLM call
export const generateSummary = action({
  handler: async (ctx, args) => {
    const result = await llm.generate(args.prompt); // 30s-2min
    return result;
  }
});
```

### When to Use Workflows

```typescript
// ✅ Multiple LLM calls that could exceed 10 min total
export const deepResearch = workflow.define({
  handler: async (ctx, args) => {
    // Each step is checkpointed
    const plan = await ctx.runAction(internal.llm.createPlan, { topic });
    const research = await ctx.runAction(internal.llm.research, { plan });
    const synthesis = await ctx.runAction(internal.llm.synthesize, { research });
    return synthesis;
  }
});

// ✅ Parallel agents with aggregation
export const council = workflow.define({
  handler: async (ctx, args) => {
    const responses = await Promise.all([
      ctx.runAction(internal.agents.analyst, { problem }),
      ctx.runAction(internal.agents.creative, { problem }),
      ctx.runAction(internal.agents.pragmatist, { problem }),
    ]);
    return ctx.runAction(internal.agents.synthesize, { responses });
  }
});
```

---

## Rate Limit Handling for LLM Apps

LLM providers enforce rate limits (OpenAI: ~60 RPM, Anthropic: varies). Use these patterns:

### Controlled Concurrency (Batching)

```typescript
// Process 5 at a time to stay under 60 RPM
const batchSize = 5;

for (let i = 0; i < topics.length; i += batchSize) {
  const batch = topics.slice(i, i + batchSize);
  await Promise.all(batch.map(topic => 
    ctx.runAction(internal.research.analyze, { topic })
  ));
  // ~5 requests, then pause for next batch
}
```

### Delays Between Steps

```typescript
// In workflows, use scheduler for delays
export const rateLimitedWorkflow = workflow.define({
  handler: async (ctx, args) => {
    for (const item of args.items) {
      await ctx.runAction(internal.llm.process, { item });
      
      // Schedule delay before next item (if needed)
      if (needsDelay) {
        await ctx.scheduler.runAfter(
          60_000, // 1 minute
          internal.workflows.continueProcessing,
          { remaining: args.items.slice(1) }
        );
        return; // Exit, will resume from scheduled function
      }
    }
  }
});
```

### Exponential Backoff in Actions

```typescript
export const llmWithRetry = action({
  handler: async (ctx, args) => {
    let delay = 1000;
    for (let attempt = 0; attempt < 3; attempt++) {
      try {
        return await llm.generate(args.prompt);
      } catch (e) {
        if (e.status === 429) { // Rate limited
          await new Promise(r => setTimeout(r, delay));
          delay *= 2; // Exponential backoff
        } else {
          throw e;
        }
      }
    }
    throw new Error("Max retries exceeded");
  }
});
```

### Worker Pool Pattern

For maximum throughput within rate limits:

```typescript
// See Pattern 2b below for full implementation
const poolSize = 5; // Match your desired concurrency
// Workers pull from queue, always N requests in flight
```

---

## Setup

```typescript
import { WorkflowManager } from "@convex-dev/workflow";
import { components, internal } from "../_generated/api";

const workflow = new WorkflowManager(components.workflow);
```

---

## Pattern 1: Actor-Critique (Self-Improvement Loop)

LLM as a judge pattern for iterative refinement.

**Use Case**: Content generation, code review, quality assurance

```typescript
export const actorCritiqueWorkflow = workflow.define({
  args: {
    task: v.string(),
    threadId: v.string(),
    targetScore: v.optional(v.number()), // 0-10, defaults to 7
    maxIterations: v.optional(v.number()), // defaults to 3
  },
  returns: v.object({
    iterations: v.number(),
    finalScore: v.number(),
    output: v.string(),
    critiqueSummary: v.string(),
  }),
  handler: async (ctx, args) => {
    const targetScore = args.targetScore ?? 7;
    const maxIterations = args.maxIterations ?? 3;
    
    let iteration = 0;
    let currentOutput = "";
    let currentScore = 0;

    // Create separate thread for critiques
    const critiqueThreadId = await ctx.runMutation(
      internal.workflows.createCritiqueThread,
      { parentThreadId: args.threadId, task: args.task }
    );

    // Initial prompt to actor
    let actorPromptMsg = await saveMessage(ctx, components.agent, {
      threadId: args.threadId,
      prompt: `Task: ${args.task}\n\nComplete this task.`,
    });

    while (iteration < maxIterations) {
      iteration++;

      // Step 1: Actor generates
      const actorResult = await ctx.runAction(
        internal.workflows.actorGenerate,
        { promptMessageId: actorPromptMsg.messageId, threadId: args.threadId },
        { retry: true }
      );
      currentOutput = actorResult.text;

      // Step 2: Critic evaluates (structured output)
      const { object: critique } = await ctx.runAction(
        internal.workflows.criticEvaluate,
        { promptMessageId: critiquePromptMsg.messageId, threadId: critiqueThreadId },
        { retry: true }
      );
      currentScore = critique.score;

      // Step 3: Check threshold
      if (currentScore >= targetScore) break;

      // Step 4: Feed critique back to actor
      if (iteration < maxIterations) {
        actorPromptMsg = await saveMessage(ctx, components.agent, {
          threadId: args.threadId,
          prompt: `Score: ${currentScore}/10. Feedback: ${critique.feedback}
Improvements needed: ${critique.improvements.join(", ")}
Please revise.`,
        });
      }
    }

    return { iterations: iteration, finalScore: currentScore, output: currentOutput };
  },
});
```

**Key Components**:
```typescript
// Actor agent
const actorAgent = new Agent(components.agent, {
  name: "Actor Agent",
  instructions: `Complete tasks thoroughly. When receiving feedback, address each point.`,
  ...defaultConfig,
});

export const actorGenerate = actorAgent.asTextAction({
  stopWhen: stepCountIs(3),
});

// Critic agent with structured output
const criticAgent = new Agent(components.agent, {
  name: "Critic Agent",
  instructions: `Evaluate outputs fairly. Provide score 0-10 and actionable feedback.`,
  ...defaultConfig,
});

export const criticEvaluate = criticAgent.asObjectAction({
  schema: z.object({
    score: z.number().min(0).max(10),
    feedback: z.string(),
    improvements: z.array(z.string()),
    strengths: z.array(z.string()),
  }),
});
```

---

## Pattern 2: Batching (Rate Limit Management)

Three patterns for processing large workloads while respecting rate limits.

### 2a: Simple Batch (Fixed Chunks)

```typescript
// Process 5 at a time, wait for batch to complete, then next batch
export const batchResearchWorkflow = workflow.define({
  args: {
    topics: v.array(v.string()),
    threadId: v.string(),
    batchSize: v.optional(v.number()), // Default: 5
  },
  handler: async (ctx, args) => {
    const batchSize = args.batchSize ?? 5;
    const results = [];

    for (let i = 0; i < args.topics.length; i += batchSize) {
      const batch = args.topics.slice(i, i + batchSize);

      // Run batch in parallel
      const batchPromises = batch.map(async (topic) => {
        const promptMsg = await saveMessage(ctx, components.agent, {
          threadId: args.threadId,
          prompt: `Research: ${topic}`,
        });
        return ctx.runAction(internal.workflows.researchTopic, {
          promptMessageId: promptMsg.messageId,
          threadId: args.threadId,
        }, { retry: true });
      });

      const batchResults = await Promise.all(batchPromises);
      results.push(...batchResults);
    }

    return results;
  },
});
```

**Pros**: Simple, predictable rate  
**Cons**: Slowest item holds up batch

### 2b: Worker Pool (Efficient)

```typescript
// Maintain N concurrent workers, each grabs next item when done
export const poolResearchWorkflow = workflow.define({
  args: {
    topics: v.array(v.string()),
    threadId: v.string(),
    poolSize: v.optional(v.number()), // Default: 5
  },
  handler: async (ctx, args) => {
    const poolSize = args.poolSize ?? 5;
    const results = [];
    const queue = [...args.topics];
    let nextIndex = 0;

    const getNextJob = () => {
      if (nextIndex >= queue.length) return null;
      return queue[nextIndex++];
    };

    const worker = async () => {
      while (true) {
        const topic = getNextJob();
        if (!topic) break;
        const result = await processTopic(topic);
        results.push(result);
      }
    };

    // Start pool
    const workers = [];
    for (let i = 0; i < Math.min(poolSize, queue.length); i++) {
      workers.push(worker());
    }
    await Promise.all(workers);

    return results;
  },
});
```

**Pros**: Better throughput for varying item times  
**Cons**: Results out of order

### 2c: Nested Sub-workflows (Production Recommended)

```typescript
// Each item is its own sub-workflow for isolation and retryability
export const nestedBatchResearchWorkflow = workflow.define({
  args: {
    topics: v.array(v.string()),
    threadId: v.string(),
    batchSize: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    const batchSize = args.batchSize ?? 5;
    const results = [];

    for (let i = 0; i < args.topics.length; i += batchSize) {
      const batch = args.topics.slice(i, i + batchSize);

      // Each topic = its own sub-workflow
      const batchPromises = batch.map(async (topic) => {
        const research = await ctx.runWorkflow(
          internal.workflows.topicResearchSubWorkflow,
          { topic, threadId: args.threadId }
        );
        return { topic, research };
      });

      const batchResults = await Promise.all(batchPromises);
      results.push(...batchResults);
    }

    return results;
  },
});

// Sub-workflow has independent retry logic
export const topicResearchSubWorkflow = workflow.define({
  args: { topic: v.string(), threadId: v.string() },
  returns: v.string(),
  handler: async (ctx, args) => {
    // If this fails, only this sub-workflow retries
    const result = await ctx.runAction(...);
    return result.text;
  },
});
```

**Pros**: Fault tolerant, resumable, independent retries  
**Cons**: More complex

---

## Pattern 3: Council of Agents (Ensemble)

Fan out → Fan in → Select best (or synthesize).

**Use Case**: Complex decisions, diverse perspectives

```typescript
export const councilWorkflow = workflow.define({
  args: {
    problem: v.string(),
    threadId: v.string(),
    mode: v.optional(v.union(v.literal("best"), v.literal("synthesize"))),
  },
  handler: async (ctx, args) => {
    const mode = args.mode ?? "best";

    // Step 1: Fan out - all agents respond in parallel
    const councilMembers = [
      { name: "Analyst", action: internal.workflows.analystRespond },
      { name: "Creative", action: internal.workflows.creativeRespond },
      { name: "Pragmatist", action: internal.workflows.pragmatistRespond },
    ];

    const memberPromises = councilMembers.map(async (member) => {
      const promptMsg = await saveMessage(ctx, components.agent, {
        threadId: args.threadId,
        prompt: `Problem: ${args.problem}\n\nProvide your perspective.`,
      });
      const result = await ctx.runAction(member.action, {
        promptMessageId: promptMsg.messageId,
        threadId: args.threadId,
      }, { retry: true });
      return { agent: member.name, response: result.text };
    });

    const memberResponses = await Promise.all(memberPromises);

    // Step 2: Score each response (parallel)
    const scorePromises = memberResponses.map(async (response) => {
      const { object: scoring } = await ctx.runAction(
        internal.workflows.scoreResponse,
        { ... },
        { retry: true }
      );
      return { ...response, score: scoring.score };
    });

    const scoredResponses = await Promise.all(scorePromises);
    scoredResponses.sort((a, b) => b.score - a.score);

    // Step 3: Select or synthesize
    if (mode === "best") {
      return { finalAnswer: scoredResponses[0].response };
    } else {
      // Synthesize all perspectives
      const synthesis = await ctx.runAction(
        internal.workflows.synthesizeResponses,
        { responses: scoredResponses }
      );
      return { finalAnswer: synthesis.text };
    }
  },
});
```

---

## Pattern 4: Deep Agent (One-Turn-Per-Action)

Strict one-turn steps to stay within time limits, with completion injection.

**Use Case**: Long-running research, complex multi-step tasks

```typescript
const deepAgent = new Agent(components.agent, {
  name: "Deep Agent",
  instructions: `Research agent with scratchpad for progress tracking.
Use delegateToSubagent for complex sub-tasks.`,
  tools: {
    internetSearch,
    updateScratchpad,
    readScratchpad,
    delegateToSubagent,    // Signal for delegation
    subagentCompletion,    // Receives injected results
  },
  ...defaultConfig,
});

export const deepAgentWorkflow = workflow.define({
  args: { task: v.string(), threadId: v.string(), maxIterations: v.optional(v.number()) },
  handler: async (ctx, args) => {
    const maxIterations = args.maxIterations ?? 20;
    let iterations = 0;
    let promptMessageId;

    while (iterations < maxIterations) {
      iterations++;

      // Run single step
      const stepResult = await ctx.runAction(
        internal.workflows.runAgentStep,
        { promptMessageId, threadId: args.threadId }
      );

      // Handle parallel delegations
      const delegationCalls = stepResult.toolCalls.filter(
        tc => tc.toolName === "delegateToSubagent"
      );
      
      if (delegationCalls.length > 0) {
        // Run sub-workflows in parallel
        const results = await Promise.all(
          delegationCalls.map(async (tc) => {
            const output = await ctx.runWorkflow(
              internal.workflows.subagentWorkflow,
              { taskPrompt: tc.args.taskPrompt }
            );
            return { title: tc.args.taskTitle, output };
          })
        );

        // Inject results back into thread
        promptMessageId = await ctx.runAction(
          internal.workflows.injectSubagentResults,
          { threadId: args.threadId, results }
        );
        continue;
      }

      // Check completion
      if (stepResult.finishReason === "stop" && stepResult.toolCalls.length === 0) {
        break;
      }
    }

    return { iterations };
  },
});
```

**Key Technique - Completion Injection**:
```typescript
export const injectSubagentResults = internalAction({
  args: { threadId: v.string(), results: v.array(...) },
  handler: async (ctx, args) => {
    const toolCallId = `subagent-results-${Date.now()}`;

    // 1. Save assistant tool-call message
    await agent.saveMessage(ctx, {
      threadId: args.threadId,
      message: {
        role: "assistant",
        content: [{
          type: "tool-call",
          toolCallId,
          toolName: "subagentCompletion",
          args: { results: args.results },
        }],
      },
    });

    // 2. Save tool result message
    const { messageId } = await agent.saveMessage(ctx, {
      threadId: args.threadId,
      message: {
        role: "tool",
        content: [{
          type: "tool-result",
          toolCallId,
          toolName: "subagentCompletion",
          result: JSON.stringify({ results: args.results }),
        }],
      },
    });

    return messageId;
  },
});
```

---

## Pattern Summary

| Pattern | Use Case | Key Feature |
|---------|----------|-------------|
| Actor-Critique | Quality refinement | Self-improvement loop |
| Batch | Rate limit management | Fixed chunks |
| Pool | Efficient throughput | Worker queue |
| Nested Batch | Production workloads | Sub-workflow isolation |
| Council | Diverse perspectives | Fan out → Score → Select |
| Deep Agent | Long research | One-turn steps + injection |

## Source
- [get-convex/agent examples](https://github.com/get-convex/agent/tree/main/example/convex/workflows)

