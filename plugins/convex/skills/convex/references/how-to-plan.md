# How to Plan Convex Features

## Before You Start
1. Check if schema changes are needed (tables, indexes).
2. Identify which mutations/queries/actions are required.
3. Determine if you need scheduled functions or crons.

## Planning Order
1. **Schema first**: Define tables and indexes in `convex/schema.ts`.
2. **Backend logic**: Mutations, queries, then actions.
3. **Frontend integration**: Hooks and components that consume the backend.

## Key Questions
- Does this feature need real-time reactivity?
- Are there authorization rules to enforce?
- Will this require file storage or HTTP actions?

## Common Patterns
- CRUD operations: schema → mutation → query → UI
- Real-time sync: schema → query with live subscription → UI
- Background jobs: action → scheduled function → mutation
