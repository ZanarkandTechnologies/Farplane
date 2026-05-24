# Convex Backend Coding Standards

> **CRITICAL RULE**: Always update this file (`convex/AGENTS.md`) when making significant architectural changes (e.g., adding new systems, changing the domain structure, or modifying core patterns). This file serves as the source of truth for the backend's layout.

## Backend Architecture Map

The backend is structured into distinct **Systems** within the `convex/` directory.

### 1. [First System] (`convex/[system_name]/`)
**Responsibility**: [What this system manages]
- `schema.ts`: Domain-specific validators and table definitions.
- `[entity].ts`: [Brief description of functions]

<!-- Add more systems as you build them -->

---

## Documentation Rules

- **Header Documentation (REQUIRED)**: Every logic file MUST start with a comprehensive block comment.
  - **Title**: Clear module name.
  - **Description**: What the module handles.
  - **Key Concepts**: Core logic, data models, or specific behaviors.
  - **Architecture**: DB structure vs. runtime calculation.
  - **Usage Examples**: Common patterns for calling functions in this file.
- **Inline Docs**: Complex logic inside functions should be commented inline.
- **No Legacy Code**: Delete unused code immediately.

### Example Header Documentation
```typescript
/**
 * MODULE NAME (Convex Mutations & Queries)
 * =========================================
 * 
 * This module handles [description].
 * 
 * KEY CONCEPTS:
 * -------------
 * - [Concept 1]
 * - [Concept 2]
 * 
 * ARCHITECTURE:
 * -------------
 * - DB Storage: [What is stored]
 * - Runtime: [What is calculated dynamically]
 * 
 * USAGE EXAMPLES:
 * ---------------
 * - [Use case]: Call [function]() to [do something]
 */
```

## Validator Reuse Pattern

Each system should have its own `schema.ts` file with reusable validators. Functions import and extend these validators using `.omit()`, `.pick()`, `.extend()`, and `.partial()`.

### Example

**Schema file** (`convex/[system]/schema.ts`):
```typescript
import { defineTable } from "convex/server";
import { v, Infer } from "convex/values";

export const entitySchema = v.object({
    name: v.string(),
    status: v.string(),
    createdAt: v.number(),
});

export const entities = defineTable(entitySchema)
    .index("by_status", ["status"]);

export const [system]Tables = {
    entities,
};

export type Entity = Infer<typeof entitySchema>;
```

**Function file** (`convex/[system]/entities.ts`):
```typescript
import { entitySchema } from "./schema";

// Omit fields set automatically
const createEntityArgsSchema = entitySchema.omit("createdAt");

// Extend with system fields for return types
const entityDocumentSchema = entitySchema.extend({
    _id: v.id("entities"),
    _creationTime: v.number(),
});
```

