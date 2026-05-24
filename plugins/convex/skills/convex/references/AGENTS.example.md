# Convex Backend Coding Standards

> **CRITICAL RULE**: Always update this file (`convex/AGENTS.md`) when making significant architectural changes (e.g., adding new systems, changing the domain structure, or modifying core patterns). This file serves as the source of truth for the backend's layout.

## Backend Architecture Map

The backend is structured into distinct **Systems** within the `convex/` directory. This supports the "AI Office" concept where different agents or components manage specific domains.

### 1. Office System (`convex/office_system/`)
**Responsibility**: Manages the physical/spatial and organizational structure of the virtual office.
- `companies.ts`: Top-level organization management.
- `teams.ts`: Groups of employees. Tracks `clusterPosition` for 3D layout.
- `employees.ts`: Individual users within a company.
- `desks.ts`: Workstation assignments. **Note**: Desk positions are calculated dynamically relative to team clusters, not stored individually as objects.
- `office_objects.ts`: Logic for general 3D items (plants, furniture, team clusters).
- `kpis.ts`: Key Performance Indicators for the office.
- `schema.ts`: Domain-specific validators.

### 2. User System (`convex/user_system/`)
**Responsibility**: Handles user-centric data and authentication helpers.
- `auth_helpers.ts`: Utilities for verifying user identity (Clerk integration).
- `user_tasks.ts`: Management of individual user tasks/todos.
- `schema.ts`: Domain-specific validators.

### 3. Chat System (`convex/chat_system/`)
**Responsibility**: Real-time communication channels and AI interactions.
- *(Currently under development/placeholder)*: Will contain logic for channels, messages, and AI responses.

### 4. Office Objects (`convex/office_objects/`)
**Responsibility**: Shared definitions for 3D entities.
- `schema.ts`: Defines validators for `meshTypes` and `officeObjects` used by logic in `office_system`.

### 5. Orchestration (`convex/orchestration/`)
**Responsibility**: Handles delegation of tasks to external systems and task scheduling.
- `scheduler.ts`: Delayed tasks and cron job scheduling for agents.
- `task_sessions.ts`: Unified task execution session system - tracks all types of task executions (remote CUA, browser, deep research, workflows) with step logging and status management.
- `remote_cua_node.ts`: Remote Computer Use Agent - Morph Cloud integration for spinning up VMs and executing commands. Creates and manages `taskSessions` of type `remote_cua`.
- `schema.ts`: Task session schemas, delegation tracking, and orchestration validators.

### 6. Self-Improvement System (`convex/self_improvement_system/`)
**Responsibility**: Agent experimentation, benchmarking, and self-improvement infrastructure.
- `schema.ts`: Schema for benchmarks, tasks, experiments, and results.
- `seedTasks.ts`: Seeds benchmarks (BuildBench, WriteBench) and their tasks.
- `benchmarks.ts`: CRUD operations for benchmarks and benchmark-to-team assignments.

**Key Tables**:
- `benchmarks`: Collections of tasks (e.g., "BuildBench", "WriteBench").
- `benchmarkTasks`: Individual tasks (setup → instruction → expectedResult/metrics).
- `benchmarkTeamAssignments`: Many-to-many relationship linking benchmarks to teams.
- `experiments`: Test a hypothesis by comparing configs across tasks.
- `matches`: 1v1 comparisons (for tournament/round-robin arena formats).
- `runResults`: Score for each config on each task (links to taskSessions in orchestration).

**Experiment Flow**:
1. Create experiment with hypothesis + configs to test
2. Pick arena format: `best_score`, `tournament`, or `round_robin`
3. Configs execute tasks (tracked in `taskSessions`)
4. `runResults` capture scores; `matches` track 1v1 comparisons
5. Experiment `results` show winner + ranking + analysis
- `writing`: Reports, articles (writingConfig: format, wordCount, tone)
- `research`: Market research, analysis (researchConfig: topic, sources)
- `data`: Data analysis, spreadsheets (dataConfig: inputFormat, outputFormat)
- `design`, `automation`, `communication`, `custom`

### 7. Utilities & Config (`convex/`)
- `utils/`: Shared helper functions (e.g., `layout.ts` for spatial calculations).
- `ai.config.ts`: Configuration for AI behaviors (models, embedding config).
- `auth.config.ts`: Clerk authentication setup.
- `schema.ts`: **Global Schema** that aggregates tables from all systems.

---

## Documentation Rules

- **Header Documentation (REQUIRED)**: Every logic file (e.g., `desks.ts`, `employees.ts`) **MUST** start with a comprehensive block comment.
  - **Title**: Clear module name.
  - **Description**: What the module handles.
  - **Key Concepts**: Core logic, data models, or specific behaviors (e.g., dynamic positioning).
  - **Architecture**: DB structure vs. runtime calculation.
  - **Usage Examples**: Common patterns for calling functions in this file.
- **Inline Docs**: Complex logic inside functions should be commented inline.
- **`.docs/context.md`**: Use for high-level tracking; do not create separate summary files.
- **No Legacy Code**: Delete unused code immediately.

### Example Header Documentation
```typescript
/**
 * DESKS MANAGEMENT (Convex Mutations & Queries)
 * ==============================================
 * 
 * This module handles all desk-related operations in the office system.
 * Desks track employee-to-workstation assignments within teams.
 * 
 * KEY CONCEPTS:
 * -------------
 * - Each desk has a stable ID for reliable employee assignment tracking
 * - Desk positions are CALCULATED DYNAMICALLY in the UI (not stored)
 * 
 * ARCHITECTURE:
 * -------------
 * - DB Storage: deskId + teamId + deskIndex + employeeId
 * - UI Rendering: Calculate position using getDeskPosition(...)
 * 
 * USAGE EXAMPLES:
 * ---------------
 * - Creating desks: Call createDesksForTeam() when team is created
 * - Assigning employee: Call assignEmployeeToDesk() to occupy a desk
 */
```

## Validator Reuse Pattern

Each module should have its own `schema.ts` file with reusable validators. Functions import and extend these validators using `.omit()`, `.pick()`, `.extend()`, and `.partial()`.

### Example

**Schema file** (`convex/user_system/schema.ts`):
```typescript
export const userTasksSchema = v.object({
    threadId: v.string(),
    userId: v.string(),
    status: userTaskStatusSchema,
    createdAt: v.number(),
});

export const userTasks = defineTable({
    ...userTasksSchema.fields,
});
```

**Function file** (`convex/user_system/user_tasks.ts`):
```typescript
import { userTasksSchema } from "./schema";

// Omit fields set automatically
const createUserTaskArgsSchema = userTasksSchema.omit("createdAt");

// Extend with system fields for return types
const userTaskDocumentSchema = userTasksSchema.extend({
    _id: v.id("userTasks"),
    _creationTime: v.number(),
});

export const createUserTask = internalMutation({
    args: createUserTaskArgsSchema,
    returns: v.union(userTaskDocumentSchema, v.null()),
    handler: async (ctx, args) => { /* ... */ },
});
```

## Reference Examples

- **Documentation**: See `convex/office_system/desks.ts` for a full header example.
- **Validators**: See `convex/user_system/schema.ts` and `convex/user_system/user_tasks.ts`.
