## API Backend Testing (Cheat Sheet)

### What to test (minimum)
- **Contract**: request/response shape, status codes, error shapes.
- **Idempotency**: retries on POST/PUT where applicable.
- **Auth**: token/session validation, scopes/roles, forbidden cases.
- **Pagination**: cursors/limits, ordering stability.
- **Concurrency**: double-submit, race conditions, optimistic locking if used.

### Recommended backpressure
- **Unit**: business rules, parsing/validation.
- **Integration**: real handlers + test DB, plus external service stubs.
- **Contract tests**: OpenAPI/JSON schema if present.
- **Load/perf**: latency budget on critical endpoints.

### Evidence to capture
- Golden error payloads (so error handling doesn’t silently regress).
- Logs with request IDs; traces if available.

