---
ticket_id: TASK-0216
title: "Generated Goal Prompt: Shared GraphIR and Configurable Projections"
status: draft
owner: codex
created_at: 2026-06-24T11:00:33+0800
updated_at: 2026-06-24T11:00:33+0800
refs:
  - ticket.md
  - program.md
  - progress.md
---

# Native Goal Prompt Preview

Use this prompt only after the operator approves `tickets/TASK-0216/ticket.md`.

```text
/goal Implement TASK-0216 end to end.

Context:
- Repo: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
- Ticket: tickets/TASK-0216/ticket.md
- Program: tickets/TASK-0216/program.md
- Progress log: tickets/TASK-0216/progress.md

Objective:
Introduce a shared GraphIR and configurable projection system for Farplane's
generated graph surfaces while preserving the existing public graph artifact
paths and wrapper commands.

Implement:
1. Read the ticket/program/progress files and the linked generator/docs files.
2. Capture current generated counts for skill, harness, and lifecycle graphs.
3. Add shared graph modules under skills/skill-maintenance/scripts/:
   - graph_ir.py
   - graph_projection.py
   - graph_projection_config.py
4. Port lifecycle, skill, and harness graph generators to use the shared IR and
   named projection configs.
5. Preserve these default outputs:
   - skills/skill-maintenance/graph/skill-graph.json
   - skills/skill-maintenance/graph/skill-graph.js
   - skills/skill-maintenance/graph/skill-docs.json
   - skills/skill-maintenance/graph/skill-docs.js
   - skills/skill-maintenance/graph/harness-graph.json
   - skills/skill-maintenance/graph/harness-graph.js
   - docs/doc-audit/generated/doc-reference-report.md
   - skills/skill-maintenance/graph/farplane-lifecycle-graph.json
   - skills/skill-maintenance/graph/farplane-lifecycle-graph.js
6. Keep default lifecycle ticket nodes flattened to TASK-* file patterns.
7. Update graph docs to explain GraphIR, projection sources, named profiles,
   and why lifecycle is a sibling projection instead of a skill-graph child.
8. Run the proof checklist in ticket.md.
9. Put verification output summaries and any intentional graph count/schema
   changes in progress.md.
10. Request material review and save the report at
    tickets/TASK-0216/artifacts/review.md before completion.

Hard constraints:
- Do not add a daemon, database, watcher, UI rewrite, or hidden runtime.
- Do not move generated graph artifacts out of skills/skill-maintenance/graph/.
- Do not change graph output schemas unless required; document any intentional
  delta in progress.md.
- Do not self-approve material completion without review evidence.
```
