# Native Goal Prompt: TASK-0251

```text
/goal Run the following files as one Goal Packet.

Files:
- tickets/TASK-0251/ticket.md
- tickets/TASK-0251/program.md
- tickets/TASK-0251/progress.md
- tickets/TASK-0251/artifacts/review/impl-plan-review.md
- farplane/goals.md
- farplane/products.md
- farplane/harness.md
- docs/farplane-framework/pulse-and-interval-loop.md
- skills/pulse-update/SKILL.md
- skills/interval-update/SKILL.md
- skills/interval-update/references/workflows/priority-planning.md
- skills/interval-update/templates/interval-report.md
- .farplane/automation/heartbeat-policy.json

Task: Implement TASK-0251 exactly as defined by the listed ticket, program, and reviewed implementation plan. Add `farplane/ops-memory.md` as the flexible active operating memory, teach Pulse and Interval contracts to read/refresh it, and document the stable-truth / active-memory / tickets / receipts split. Do not introduce a roadmap registry, project schema, database, UI, hidden scheduler, automation cadence change, live cap change, KPI/goals/products rewrite, or broad ticket metadata migration.

Logging: Before ending each turn, append a compact structured entry to `tickets/TASK-0251/progress.md` when ticket state, files, proof, or blockers change.

Metric: Pass the Done conditions and QA Strategy in `tickets/TASK-0251/ticket.md` plus the Proof Policy in `tickets/TASK-0251/program.md`. The metric provider is hybrid: validator pass, focused grep/readback, artifact presence, and reviewer completion verdict.

QA proof route: local validators and manual readback first, then reviewer completion review. Self-certification is forbidden for final completion.

Final checkpoint: Before stop_complete, run the ticket validators/checks listed in QA Strategy where applicable, update ticket/progress with evidence links, request reviewer completion review, and block/revise if the review is below TAS-A or names a required repair.

After each turn: Compare progress against the listed files and continue while useful inside this execution window. Stop blocked if the ops-memory boundary contradicts stable project files, validators cannot pass, or completion review fails without a small repair path.

Grounding: This is local-only Farplane harness contract work. Final response must include `Grounding: local files`.

Approval: approved by operator request after reviewer TAS-A impl-plan review.
```
