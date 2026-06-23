# TASK-0213 Generated Native Goal Prompt

```text
/goal Run the following files as one Goal Packet.
Files:
- tickets/TASK-0213/ticket.md
- tickets/TASK-0213/program.md
- tickets/TASK-0213/progress.md
- docs/farplane-framework/README.md
- docs/farplane-framework/deep-init-critical-path.md
- docs/farplane-framework/project-files.md
- docs/specs/filesystem-lifecycle.md
- docs/specs/doc-governance.md
- docs/specs/steer-pulse-automation.md
- docs/specs/goal-loop-contract.md
- docs/MEMORY.md
- docs/TROUBLES.md
- docs/LESSONS.md
- hooks.json
- skills/skill-maintenance/scripts/generate_harness_graph.py
- skills/skill-maintenance/scripts/generate_skill_graph.py
- skills/skill-maintenance/graph/README.md

Task: Complete TASK-0213 end to end. Implement the friendly Farplane lifecycle documentation hub, graph contract, hooks/runtime page, semantic lifecycle graph generator, generated graph artifacts, and focused tests exactly as scoped by the listed ticket and program. Preserve the ticket's Scope, Delta, Done / Proof, Run Hints, Goal Packet, and stop conditions. Do not implement Farplane UI rendering, activate automations, add hidden schedulers, or auto-compact durable memory files.

Logging: Before ending each turn, append a compact structured entry to tickets/TASK-0213/progress.md with trigger, intent, actions, files changed, artifacts, metric sample, drift verdict, next action, and blocker. Link artifacts instead of pasting raw command output.

Metric: Use the hybrid metric in tickets/TASK-0213/program.md. Required proof is mechanical command pass plus material documentation/schema review when reviewer is available. Required checks include:
- python3 -m py_compile skills/skill-maintenance/scripts/generate_farplane_lifecycle_graph.py
- python3 -m unittest skills/skill-maintenance/scripts/test_generate_farplane_lifecycle_graph.py
- python3 skills/skill-maintenance/scripts/generate_farplane_lifecycle_graph.py --check
- python3 bin/validators/check_doc_refs.py

After each turn: Compare progress against tickets/TASK-0213/ticket.md and tickets/TASK-0213/program.md. Continue within the current local implementation window if the next action is clear. Stop complete only after all Done / Proof items pass and final evidence is linked. Stop blocked if parser ambiguity cannot be represented with confidence levels or curated refs, if tests fail after attempted repair, if required local files are missing, or if the scope would require UI rendering, external services, deploy, push, destructive git actions, or secrets.

Budget: local shared checkout, no deploy, no push, no spend, no external accounts. Use focused local Python and doc validators. Keep edits scoped to TASK-0213 docs, graph generator/tests/artifacts, and graph README.

Proof route: mechanical checks first. Use reviewer before final completion if available for documentation-quality / framework-contract / graph-schema review. Self-certification is allowed for command execution only; final documentation/schema sufficiency should use reviewer when possible or explicitly record reviewer-unavailable residual risk.

Final evidence: final response must link the changed docs, generated graph JSON, test/check results summarized in progress.md, and review artifact or explicit review-unavailable note. No screenshot evidence is required because this ticket does not implement a UI.

Approval: The operator explicitly requested creating a Goal to implement this end to end. This Goal Packet is approved for local implementation within the listed constraints.
```
