# Schema Design Patterns

## When to Use
Use this reference when designing database schemas, creating validators, and organizing type definitions in Convex.

## Split Schema Pattern

Each system defines its own schema and exports tables for the global schema:

```typescript
// convex/user_system/schema.ts
import { defineTable } from "convex/server";
import { v, Infer } from "convex/values";

// Define validators and tables...

export const userSystemTables = {
  userProfiles,
  userTasks,
  userSecrets,
};
```

```typescript
// convex/schema.ts (global)
import { defineSchema } from "convex/server";
import { userSystemTables } from "./user_system/schema";
import { chatSystemTables } from "./chat_system/schema";

export default defineSchema({
  ...userSystemTables,
  ...chatSystemTables,
});
```

## Validator Reuse Patterns

### Base Validator → Function Args/Returns

Define a base validator, then derive variants using `.omit()`, `.extend()`, `.pick()`, and `.partial()`:

```typescript
// Base schema (matches database structure)
export const userTasksSchema = v.object({
  threadId: v.string(),
  employeeId: v.id("employees"),
  userId: v.string(),
  message: v.string(),
  status: userTaskStatusSchema,
  priority: v.optional(notificationPrioritySchema),
  response: v.optional(v.string()),
  respondedAt: v.optional(v.number()),
  createdAt: v.number(),
});

// For creating: omit auto-generated fields
const createUserTaskArgsSchema = userTasksSchema
  .omit("createdAt", "response", "respondedAt")
  .extend({
    priority: notificationPrioritySchema, // Make required for new tasks
  });

// For returns: extend with system fields
const userTaskDocumentSchema = userTasksSchema.extend({
  _id: v.id("userTasks"),
  _creationTime: v.number(),
});

// For updates: partial of updatable fields
const userTaskPatchSchema = v.object({
  status: userTaskStatusSchema,
  response: v.optional(v.string()),
  respondedAt: v.optional(v.number()),
}).partial();
```

### Method Reference

| Method | Purpose | Example |
|--------|---------|---------|
| `.omit("field1", "field2")` | Remove fields | `schema.omit("createdAt")` |
| `.extend({ newField: v.string() })` | Add/override fields | `schema.extend({ _id: v.id("table") })` |
| `.pick("field1", "field2")` | Keep only specified | `schema.pick("name", "email")` |
| `.partial()` | Make all fields optional | For PATCH operations |

## Discriminated Unions

Use `v.union()` with `v.literal()` for type-safe variants:

```typescript
export const userTaskTypeSchema = v.union(
  v.literal("approval"),
  v.literal("review"),
  v.literal("question"),
  v.literal("permission"),
  v.literal("task_completed"),
  v.literal("rate_alert"),
);

// For complex discriminated unions with different shapes:
const resultSchema = v.union(
  v.object({
    kind: v.literal("error"),
    errorMessage: v.string(),
  }),
  v.object({
    kind: v.literal("success"),
    value: v.number(),
  }),
);
```

## Type Exports

Always export TypeScript types alongside validators:

```typescript
import { v, Infer } from "convex/values";

export const userTypeSchema = v.union(
  v.literal("regular"),
  v.literal("pro"),
  v.literal("admin"),
);

export const userProfileSchema = v.object({
  userId: v.string(),
  name: v.optional(v.string()),
  email: v.string(),
  type: userTypeSchema,
});

// Type exports for frontend/TypeScript usage
export type UserType = Infer<typeof userTypeSchema>;
export type UserProfile = Infer<typeof userProfileSchema>;
```

## Response Validators

Create reusable response validators for common patterns:

```typescript
// ID response patterns
export const userIdResponseSchema = v.object({
  userId: v.string(),
});

export const userProfileIdResponseSchema = v.object({
  userProfileId: v.id("userProfiles"),
});

// Document with system fields (for query returns)
export const userSecretDocumentSchema = userSecretsSchema.extend({
  _id: v.id("userSecrets"),
  _creationTime: v.number(),
});
```

## Indexing Strategy

```typescript
export const userTasks = defineTable(userTasksSchema)
  .index("by_threadId", ["threadId"])
  .index("by_status", ["status"])
  .index("by_userId", ["userId"])
  .index("by_employeeId", ["employeeId"])
  // Compound indexes for specific queries
  .index("by_type_and_reference", ["type", "referenceId"])
  .index("by_employee_and_reference", ["employeeId", "type", "referenceId"]);
```

**Index Naming**: Always prefix with `by_` followed by field names.

**Compound Indexes**: Order matters - fields must be queried in the same order they're defined.

## Schema Organization Template

```typescript
/**
 * [System Name] - Schema Definitions
 * 
 * [Description of what this system handles]
 */

import { defineTable } from "convex/server";
import { v, Infer } from "convex/values";

// ============================================================================
// REUSABLE VALIDATORS
// ============================================================================

export const statusSchema = v.union(...);

// ============================================================================
// TABLE SCHEMAS
// ============================================================================

export const entitySchema = v.object({...});

// ============================================================================
// TABLE DEFINITIONS
// ============================================================================

export const entities = defineTable(entitySchema)
  .index("by_status", ["status"]);

// ============================================================================
// SYSTEM TABLES EXPORT
// ============================================================================

export const mySystemTables = {
  entities,
};

// ============================================================================
// TYPE EXPORTS
// ============================================================================

export type Status = Infer<typeof statusSchema>;
export type Entity = Infer<typeof entitySchema>;

// ============================================================================
// FUNCTION ARGS/RETURNS VALIDATORS
// ============================================================================

export const entityDocumentSchema = entitySchema.extend({
  _id: v.id("entities"),
  _creationTime: v.number(),
});

export const createEntityArgsSchema = entitySchema.omit("createdAt");
```

## Anti-patterns

- **No validators in functions**: Always define validators in schema.ts, import in function files
- **Inline type definitions**: Use `Infer<typeof schema>` instead of manual types
- **Missing system fields**: Always include `_id` and `_creationTime` in document return validators
- **Flat schema file**: Don't put all tables in root schema.ts - use split schemas
- **Duplicate validators**: If a validator is used in multiple systems, consider a shared schema
