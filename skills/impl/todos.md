# Todos

- [ ] Read the selected ticket and linked docs before launching any lanes.
- [ ] Use the generic [execute](../execute/SKILL.md) interface as the Tier 2
  contract, but keep `$impl` coding-ticket specific.
- [ ] Confirm the ticket is actually ready for build orchestration rather than still needing planning.
- [ ] Use the relevant [research](../research/SKILL.md) method when execution
  depends on official behavior, local invariants, examples, or peer norms.
- [ ] Read the ticket `Proof Contract` and carry its metrics, rubric gates, hard gates, and required evidence into lane prompts.
- [ ] Aim the run at whole-ticket completion; do not voluntarily shrink a
  coherent ticket into an internal "part 1".
- [ ] Decide which lanes are needed for this ticket: builder, reviewer, QA, and evidence-check.
- [ ] If the `Proof Contract` links an autoresearch session, run `autoresearch-exec` as a bounded execution subphase; otherwise keep autoresearch out of the run.
- [ ] Make the delegated `worker_name`, `main_artifact_path`, and `grounding_summary` explicit before delegating.
- [ ] Launch the visible lanes and keep their responsibilities distinct.
- [ ] When review starts, use the [execute](../execute/SKILL.md) proof/review
  shape instead of improvising a vague review pass.
- [ ] When UI evidence needs judgment, use the [Visual QA](../visual-qa/SKILL.md) skill.
- [ ] Integrate lane outputs back into the ticket and keep completion claims in the orchestrator, not the workers.
- [ ] If the verdict says repeat the same ticket, re-enter the same `$impl` flow instead of silently jumping to another ticket.
