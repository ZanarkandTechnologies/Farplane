# Todos

- [ ] Read the selected ticket and linked docs before launching any lanes.
- [ ] Confirm the ticket is actually ready for build orchestration rather than still needing planning.
- [ ] Aim the run at whole-ticket completion; do not voluntarily shrink a
  coherent ticket into an internal "part 1".
- [ ] Decide which lanes are needed for this ticket: builder, reviewer, QA, and evidence-check.
- [ ] Make the delegated `worker_name`, `main_artifact_path`, and `grounding_summary` explicit before delegating.
- [ ] Launch the visible lanes and keep their responsibilities distinct.
- [ ] When review starts, use the [Review](../review/SKILL.md) skill instead of improvising a vague review pass.
- [ ] When UI evidence needs judgment, use the [Visual QA](../visual-qa/SKILL.md) skill.
- [ ] Integrate lane outputs back into the ticket and keep completion claims in the orchestrator, not the workers.
- [ ] If the verdict says repeat the same ticket, re-enter the same `$impl` flow instead of silently jumping to another ticket.
