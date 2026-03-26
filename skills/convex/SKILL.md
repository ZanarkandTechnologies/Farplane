---
name: convex
version: 3.1.0
description: "Convex reactive backend development. Decision tree for references + links to official docs."
---

# Convex Skill

Build type-safe, real-time backend applications with Convex.

## Quick Setup

```bash
# Non-interactive scaffold (default): Next.js + Clerk template in current directory
pnpm create convex@latest . -- -t nextjs-clerk

# Cloud configuration (first run): MUST be done by a human in an interactive terminal
pnpm dlx convex@latest dev

# Apply our conventions after `convex/` exists
npx tsx ~/.claude/skills/convex/scripts/setup-convex.ts ./convex
```

## Critical setup rule (prevents agent hangs)
- If a Convex CLI command tries to prompt (e.g. “Choose a client”, “Project name”, login flow) and the environment is non-interactive, the agent must **stop and ask the human to run it**.

---

## Always-Load Core (first pass)

Use this section by default before loading deep references.

### Default build order checklist
- [ ] Confirm feature scope and whether schema/index changes are required.
- [ ] Define schema and indexes in `convex/schema.ts` first.
- [ ] Implement backend logic in this order: query/mutation -> action/workflow (if needed).
- [ ] Integrate frontend hooks/components after backend contracts are stable.
- [ ] Write tests before final review and production checks.

### Default test strategy checklist
- [ ] Unit tests for backend helpers and function logic (`convex-test` where applicable).
- [ ] Integration tests for query/mutation flows and auth boundaries.
- [ ] Realtime checks for subscription updates and eventual convergence.
- [ ] E2E coverage for critical user flows (Playwright preferred for stability).
- [ ] Failure-path coverage for invalid input, missing records, and retries.

### Production gotchas quicklist
- Actions time out at 10 minutes; use workflows for long multi-step jobs.
- Prefer indexes (`withIndex`) over table scans (`filter`) for non-trivial reads.
- Avoid unbounded `collect()`; cap results (`take`) or paginate.
- Use internal functions for scheduling targets, not public API functions.
- Batch writes in one mutation when atomicity matters; avoid N sequential mutation calls from actions.
- Always await async calls (including scheduler/db operations) to avoid silent failures.

---

## What Reference Do I Need?

| I'm doing... | Load this |
|--------------|-----------|
| Starting a new project | `project-setup.md` |
| Designing schemas/tables | `schema-patterns.md` |
| Adding auth/users | `user-system.md` |
| Building AI chat | `ai-chat.md` |
| Long-running tasks (>10 min) | `workflows.md` |
| Tracking task execution | `execution-tracking.md` |
| Adding integrations | `components.md` |
| Building realtime multiplayer | `multiplayer.md` |
| Setting up Polar payments | `polar-setup.md` |
| Setting up Resend emails | `resend-setup.md` |
| Writing backend unit tests | `testing.md` |
| **Code review / production** | `gotchas.md` ⚠️ |

---

## Official Docs

> Delegate to `documentation-searcher` agent with URL for deep dives.

**Must Read**:
- [Best Practices](https://docs.convex.dev/understanding/best-practices) - **Always review**
- [Platform Limits](https://docs.convex.dev/production/state/limits) - **10 min action timeout**

### Platform
- [Functions](https://docs.convex.dev/functions) - Queries, mutations, actions
- [Database](https://docs.convex.dev/database) - Schema, indexes, relationships
- [Realtime](https://docs.convex.dev/realtime) - Live subscriptions
- [Authentication](https://docs.convex.dev/auth) - Auth setup and patterns
- [Scheduling](https://docs.convex.dev/scheduling) - Cron jobs, delayed functions
- [File Storage](https://docs.convex.dev/file-storage) - Upload and serve files
- [Search](https://docs.convex.dev/search) - Full-text and vector search
  - [Vector Search](https://docs.convex.dev/search/vector-search) - Embeddings, similarity
  - [Full Text Search](https://docs.convex.dev/search/text-search) - Keyword search
- [Components](https://docs.convex.dev/components) - Modular, reusable backends

### AI & Agents
- [AI Code Gen](https://docs.convex.dev/ai) - LLM-friendly guidelines
- [Agents Overview](https://docs.convex.dev/agents) - Building AI agents
- [Getting Started](https://docs.convex.dev/agents/getting-started)
- [Threads](https://docs.convex.dev/agents/threads) - Conversation management
- [Messages](https://docs.convex.dev/agents/messages) - Message handling
- [Streaming](https://docs.convex.dev/agents/streaming) - Real-time responses
- [Tools](https://docs.convex.dev/agents/tools) - Agent capabilities
- [LLM Context](https://docs.convex.dev/agents/context) - Context management
- [RAG](https://docs.convex.dev/agents/rag) - Retrieval augmented generation
- [Workflows](https://docs.convex.dev/agents/workflows) - Multi-step agent tasks
- [Human Agents](https://docs.convex.dev/agents/human-agents) - Human-in-the-loop
- [Rate Limiting](https://docs.convex.dev/agents/rate-limiting)
- [Usage Tracking](https://docs.convex.dev/agents/usage-tracking)

**Examples Repo**: https://github.com/get-convex/agent/tree/main/example/convex

---

## Reference Files

### Project Setup
- [project-setup.md](references/project-setup.md) - Init, structure choice, naming

### Schema & Data  
- [schema-patterns.md](references/schema-patterns.md) - Validators, split schemas, types

### System Patterns
- [user-system.md](references/user-system.md) - Auth helpers, profiles, secrets
- [ai-chat.md](references/ai-chat.md) - Threads, streaming, status updates
- [execution-tracking.md](references/execution-tracking.md) - Task sessions, steps

### Orchestration
- [workflows.md](references/workflows.md) - Actions vs workflows, batching, rate limits

### Integrations
- [components.md](references/components.md) - Component bundles overview
- [polar-setup.md](references/polar-setup.md) - Subscription billing setup
- [resend-setup.md](references/resend-setup.md) - Email delivery with React Email

### Multiplayer Realtime
- [multiplayer.md](references/multiplayer.md) - Architecture, room/presence lifecycle, state sync, planning, testing, and assets workflow

### Production Readiness
- [gotchas.md](references/gotchas.md) - **Limits, best practices checklist, LLM gotchas**

### Testing
- [testing.md](references/testing.md) - `convex-test` + Vitest setup and patterns

### Templates & Examples
- [AGENTS.template.md](assets/AGENTS.template.md) - Blank template for new projects
- [AGENTS.example.md](references/AGENTS.example.md) - Full example from Zanarkand

---

## When to Add a Reference File

| Scenario | Action |
|----------|--------|
| Pure Convex feature | Link to official docs |
| Our convention on top of Convex | Create reference file |
| Pattern from production codebase | Use transfer-learn to extract |
| Gotcha we discovered | Add to relevant reference file |

## Workflow

1. **New Project** → `project-setup.md`
2. **Schema Design** → `schema-patterns.md`
3. **Adding Features** → Check system patterns (user, chat, execution)
4. **Integrations** → `components.md` overview, then:
   - **Payments** → `polar-setup.md`
   - **Email** → `resend-setup.md`
5. **Realtime Multiplayer** → `multiplayer.md`
6. **AI/Long Tasks** → `workflows.md` (actions vs workflows decision)
7. **Before Deploy** → `gotchas.md` checklist
