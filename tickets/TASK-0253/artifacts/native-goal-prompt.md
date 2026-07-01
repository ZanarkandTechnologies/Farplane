# TASK-0253 Native Goal Prompt

```text
/goal Run the following files as one Goal Packet.
Files:
- tickets/TASK-0253/ticket.md
- tickets/TASK-0253/program.md
- tickets/TASK-0253/progress.md
- tickets/TASK-0253/artifacts/native-goal-prompt.md
- farplane/goals.md
- farplane/bindings.md
- farplane/ops-memory.md
- bin/core/farplane_metrics.py
- bin/tests/test_farplane_metrics.py
- docs/farplane-framework/project-files.md
- docs/farplane-framework/pulse-and-interval-loop.md
- skills/interval-update/references/interval-update.md
- skills/x-account/references/metrics-snapshot.md
- skills/instagram-account/references/metrics-snapshot.md

Task: Complete TASK-0253. Implement the lean SMART goal KPI snapshot model:
goal axes own inline SMART goals; metric providers are a simple catalog; daily
source snapshots can use metrics.<kpi>.value readings with optional item
breakdowns; charts derive daily_diff from readings; existing observation-list
snapshots remain compatible during migration.

Logging: Before ending each turn, append a compact structured entry to
tickets/TASK-0253/progress.md with actions, files changed, verification,
drift verdict, next action, and blockers.

Metric: Satisfy tickets/TASK-0253/ticket.md Done and QA Strategy plus
tickets/TASK-0253/program.md proof policy. Use focused tests, snapshot smoke,
docs/skill checks, and data-shape inspection. Do not self-certify any
judgment-heavy final claim if reviewer evidence is required by the ticket.

After each turn: Compare progress against the listed files, continue within
the current implementation window when useful, otherwise stop complete or stop
blocked. Do not create a deterministic parser for farplane/ops-memory.md. Do
not add a distribution.md/projects.md surface. Do not echo secrets.

Final checkpoint: Before stop_complete, run the focused verification commands,
update ticket.md and progress.md with evidence and residual risk, and report
Grounding: local files and local-only implementation evidence unless external
docs were needed.
```
