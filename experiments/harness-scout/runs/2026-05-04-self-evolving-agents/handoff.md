# Handoff

This duplicate source pass created two decoupled follow-up tickets and left the
remaining candidates as duplicate, deferred, or rejected decisions.

## Source Safety

- `Source:` https://www.youtube.com/watch?v=2zhchG0r6iI
- `Visibility:` public
- `Redactions:` none required
- `Retention:` source summary, anchors, and compact analysis only; raw
  transcript not stored
- `Boundary:` transcript text is untrusted evidence, not instructions

## Created Follow-Up Tickets

| Ticket / feature name | Type | Decision | Summary |
| --- | --- | --- | --- |
| `tickets/TASK-0104/ticket.md`: gated skill opportunity reviewer | implement feature | `adapt` | Add a gated skill-opportunity reviewer that proposes skill updates from repeated non-trivial workflows without auto-writing or auto-publishing skills. |
| `tickets/TASK-0105/ticket.md`: hook-based error learning reminder comparison | compare and maybe implement | `needs-benchmark` | Compare hook-based error learning reminders against Codexter's current explicit `TROUBLES`/`MEMORY` writeback before touching hooks. |

## Strong Adapt Candidates For Later

### Gated Skill Opportunity Reviewer

- `Source:` https://www.youtube.com/watch?v=2zhchG0r6iI
- `Feature:` autonomous skill reviewer that looks for repeated non-trivial
  workflows and proposes skill updates
- `Current state:` Codexter has `skill-creator`, `self-improve`, and
  `best-of-worlds`, but not an automatic skill-opportunity review loop
- `Ticket:` `TASK-0104`
- `Scope guard:` propose and validate skill updates only; no auto-write,
  auto-publish, cron, or hidden background mutation
- `Potential proof:` replay several completed tickets and count high-quality
  skill proposals versus duplicate/noisy suggestions

### Hook-Based Error Learning Prompt

- `Source:` https://www.youtube.com/watch?v=2zhchG0r6iI
- `Feature:` post-tool or error-pattern hook nudges agents to write
  `docs/TROUBLES.md` or candidate learnings
- `Current state:` Codexter has input and stop hooks plus `docs/TROUBLES.md`,
  but no PostToolUse learning reminder
- `Ticket:` `TASK-0105`
- `Scope guard:` benchmark signal before changing live hook behavior
- `Potential proof:` replay tool-error runs and measure useful trouble entries
  versus false reminders

## Rejected For Now

- searchable raw conversation history as canonical memory
- semantic long-term memory layer
- background memory mutation without ticket/docs writeback review
