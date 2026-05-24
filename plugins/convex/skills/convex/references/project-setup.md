# Project Setup & Structure

## When to Use
Use this reference when starting a new Convex project or deciding how to organize your backend.

---

## Quick Setup

```bash
# 1. Create project
# Non-interactive scaffold (default): Next.js + Clerk template in current directory
pnpm create convex@latest . -- -t nextjs-clerk

# Cloud configuration (first run): MUST be done by a human in an interactive terminal
pnpm dlx convex@latest dev

# 2. Apply our conventions
npx tsx ~/.claude/skills/convex/scripts/setup-convex.ts ./convex
```

The script copies AGENTS.md template, creates utils/, sets up schema aggregation, and removes example files.

---

## Choosing Your Structure

| App Size | Entities | Structure | When |
|----------|----------|-----------|------|
| **Simple** | <5 tables | Flat files | Focused apps, MVPs |
| **Medium** | 5-15 tables | Hybrid | Growing apps |
| **Complex** | 15+ tables | System folders | Multi-domain apps |

---

## Simple Apps (Flat Structure)

One file per entity in the root:

```
convex/
├── _generated/
├── users.ts          # User queries/mutations
├── posts.ts          # Post queries/mutations  
├── comments.ts       # Comment queries/mutations
├── schema.ts         # All tables in one file
└── AGENTS.md
```

```typescript
// convex/schema.ts - Simple app
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    name: v.string(),
    email: v.string(),
  }).index("by_email", ["email"]),
  
  posts: defineTable({
    authorId: v.id("users"),
    title: v.string(),
    content: v.string(),
  }).index("by_author", ["authorId"]),
});
```

---

## Complex Apps (System Folders)

Organize by **domain/system**, not by type:

```
convex/
├── _generated/              # Auto-generated (never edit)
│
├── user_system/             # System: User management
│   ├── schema.ts            # Validators + table definitions
│   ├── auth_helpers.ts      # Auth utilities
│   └── profiles.ts          # Profile functions
│
├── chat_system/             # System: Real-time chat
│   ├── schema.ts
│   ├── threads.ts
│   └── messages.ts
│
├── orchestration/           # System: Task scheduling
│   ├── schema.ts
│   └── task_sessions.ts
│
├── utils/                   # Shared utilities (NOT a system)
│   └── helpers.ts
│
├── schema.ts                # Global schema (aggregates all)
├── AGENTS.md                # Backend documentation
└── convex.config.ts
```

### System Folder Template

```
<system_name>/
├── schema.ts           # REQUIRED: Validators, tables, types
├── <entity>.ts         # Functions per entity
└── <feature>.ts        # Feature-specific functions
```

### System Schema Template

```typescript
// convex/<system_name>/schema.ts
import { defineTable } from "convex/server";
import { v, Infer } from "convex/values";

// ============================================================================
// REUSABLE VALIDATORS
// ============================================================================

export const statusSchema = v.union(
  v.literal("pending"),
  v.literal("active"),
  v.literal("completed"),
);

// ============================================================================
// TABLE SCHEMAS
// ============================================================================

export const entitySchema = v.object({
  name: v.string(),
  status: statusSchema,
  createdAt: v.number(),
});

// ============================================================================
// TABLE DEFINITIONS
// ============================================================================

export const entities = defineTable(entitySchema)
  .index("by_status", ["status"]);

// ============================================================================
// EXPORTS
// ============================================================================

export const mySystemTables = { entities };

export type Status = Infer<typeof statusSchema>;
export type Entity = Infer<typeof entitySchema>;
```

### Global Schema Aggregation

```typescript
// convex/schema.ts
import { defineSchema } from "convex/server";
import { userSystemTables } from "./user_system/schema";
import { chatSystemTables } from "./chat_system/schema";

export default defineSchema({
  ...userSystemTables,
  ...chatSystemTables,
});
```

---

## When to Create a New System

✅ **Create a system when**:
- Domain is distinct (users vs. chat vs. billing)
- Tables are tightly related
- Feature will grow independently
- You have a reusable template

❌ **Don't create a system for**:
- Single utility function → use `utils/`
- One-off script → use root level
- <5 entities total → use flat structure

---

## Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| System folders | `snake_case` | `user_system/` |
| Function files | `snake_case.ts` | `user_tasks.ts` |
| Table names | `camelCase` | `userProfiles` |
| Validators | `camelCaseSchema` | `userProfileSchema` |
| Types | `PascalCase` | `UserProfile` |
| Indexes | `by_fieldName` | `by_userId` |

---

## Post-Setup Checklist

- [ ] Example files removed
- [ ] Directory structure chosen (flat vs systems)
- [ ] Global schema.ts configured
- [ ] AGENTS.md created
- [ ] First system/entity scaffolded

---

## Anti-patterns

- **Over-engineering**: Don't use systems for <5 entities
- **Under-engineering**: Don't use flat for 15+ entities  
- **Type-first organization**: Don't create `queries/`, `mutations/` folders
- **Missing schema exports**: Always export `*SystemTables` for aggregation

