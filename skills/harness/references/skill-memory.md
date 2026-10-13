# Self Improve Goal Packet Ownership

Material self-improvement uses the standard GitHub issue Goal Packet:

```text
<owner/repo#n> issue body: ticket sections + ## Goal program + ## Current Goal state (launcher in its own comment)
<owner/repo#n> Goal turn comments
.farplane/goal-advisor/issue-<n>/hypothesis-tree.json
```

`goal-advisor` instantiates
[`goal-program-template.md`](goal-program-template.md) into `## Goal program`
and posts the native prompt as a `**Goal launcher**` comment. The packet starts
`approval: pending`; execution begins only after the operator approves the
current ticket sections, Goal program, `## Current Goal state` scaffold, and
prompt. `compiled_from_ticket_sha` makes stale packets block and regenerate.

The target skill does not own lifecycle state. Pre-existing
`skills/<target>/self-improve/*` files are legacy experiment notes only unless
an explicit separate contract owns them; harness never reads, writes,
generates, parses, or migrates them as Goal state.

Use Goal turn comments for compact turn observations. Link generated Eval
runs rather than copying bulky output or creating a structured event schema.
