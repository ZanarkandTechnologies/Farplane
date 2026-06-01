# Notion Task Projection Cases

## Resolved Tasks Write

Input:

```text
Create a Tasks ticket from a strong harness-scout adapt handoff. The operator
gave a project and area in the request.
```

Expected behavior:

- Set `destination=notion_tasks`.
- Resolve `Project` and `Areas` as relation handles or placeholder page URLs.
- Use the harness-scout handoff body, not just the video or post title.
- Fetch the written page and record readback with `project_present=true` and
  `areas_present=true`.

## Missing Routing

Input:

```text
Create a Tasks ticket, but no project, area, parent context, or private handle
can identify the route.
```

Expected behavior:

- Do not claim successful live Tasks writeback.
- Keep the proposal in the ledger or local inbox.
- Set `routing_status=routing_missing`.
- Report the missing routing fields as the blocker.

## Ledger-Only Proposal

Input:

```text
Record a defer or needs-benchmark proposal for later review.
```

Expected behavior:

- Use `destination=proposal_ledger` or `local_inbox`.
- Do not require Tasks `Project` or `Areas` fields.
- Keep the canonical URL/key as the unique ledger identity.
