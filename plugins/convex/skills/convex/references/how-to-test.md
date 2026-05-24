# How to Test Convex Features

## Testing Strategy
1. **Unit tests**: Test individual functions with `convex-test`.
2. **Integration tests**: Test mutations and queries together.
3. **E2E tests**: Playwright for full user flows.

## Key Areas
- Schema validation (required fields, types).
- Authorization rules (who can read/write).
- Real-time updates (subscriptions trigger on changes).
- Error handling (invalid inputs, missing data).

## Tools
- `convex-test` for backend logic.
- Playwright for frontend + backend integration.
- Manual verification in Convex dashboard.

## Common Gotchas
- Mutations are transactional; test rollback behavior.
- Queries are cached; test cache invalidation.
- Actions are not transactional; test idempotency.
