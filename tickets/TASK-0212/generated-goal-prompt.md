/goal Run the following files as one Goal Packet.

Files:
- tickets/TASK-0212/ticket.md
- tickets/TASK-0212/program.md
- tickets/TASK-0212/progress.md
- docs/templates/registry.jsonl
- rules/template-registry.toml
- skills/skill-creator/references/SKILL_TEMPLATE.md
- skills/skill-maintenance/scripts/generate_template_intelligence.py
- skills/skill-maintenance/scripts/check_skills.py
- bin/validators/sync_template_registry.py
- bin/validators/check_farplane_project_files.py
- farplane/manifest.json
- ../Farplane-UI/farplane/manifest.json

Task: Complete the desired outcomes defined across the listed files. Preserve
the ticket scope: standardize on `template_uses` as the single consumer field,
extend existing template registry and skill-maintenance rollout reporting, and
avoid creating a separate schema registry or broad all-doc metadata pass.

Logging: Before ending each turn, append a compact structured entry to
`tickets/TASK-0212/progress.md` with actions, changed files, command evidence,
drift verdict, next action, and blockers.

Metric: Mechanical. Satisfy the Done / Proof in `tickets/TASK-0212/ticket.md`
and the proof policy in `tickets/TASK-0212/program.md`.

After each turn: Compare progress against the listed files, preserve unrelated
dirty worktree changes, continue within the current local implementation window
while useful, otherwise stop complete or stop blocked with concrete evidence.

Budget: Local implementation window; no deploy, spend, push, destructive
cleanup, or account changes.

Proof route: Run the validators and tests named in the ticket. Use reviewer if
available before final completion; otherwise record the review gap.

Final evidence: final response includes rollout counts, command results, files
changed, blocker/risk notes, and the next concrete step.

Approval: Approved by operator request on 2026-06-23; run now.
