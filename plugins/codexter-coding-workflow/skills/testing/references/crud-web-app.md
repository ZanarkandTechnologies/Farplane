## CRUD Web App Testing (Cheat Sheet)

### What to test (minimum)
- **Auth**: login/logout, session persistence, permission checks.
- **Core flows**: create/read/update/delete for each primary entity.
- **Validation**: required fields, format validation, server-side validation errors.
- **States**: loading, empty, error, offline/timeout handling.
- **Security basics**: authorization boundaries (cannot access others’ data).

### Recommended backpressure
- **Unit**: validation helpers, formatters, reducers/state.
- **Integration**: API routes or backend handlers with test DB.
- **E2E (Playwright)**: 2–5 golden flows that represent the product.

### Evidence to capture
- Playwright traces on failure.
- Screenshots for key views (helps detect UI regressions).

### Common failure modes
- Flaky selectors → stabilize `data-testid` and avoid text-only selectors.
- Hidden race conditions → await network + UI stability before asserting.

