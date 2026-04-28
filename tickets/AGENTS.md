# Tickets Module

Local rules for the ticket contract.

- Frontmatter is for operational state only: identity, queue state, execution
  gates, `next_action`, and one-line `last_verification`.
- The body owns narrative and proof: plan, `Refs`, `Evidence`, and explanatory
  blocker detail.
- Keep durable links in `Refs`, not in frontmatter. See `MEM-0066`.
- Keep detailed commands, artifact links, and result narratives in `Evidence`,
  not in `last_verification`. See `MEM-0066`.
- `blocked_by` stays machine-readable ticket IDs; `Blockers` explains the human
  context.
- Do not add a second state block in the body or recreate frontmatter fields
  under another heading.
