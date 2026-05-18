# Todos

- [ ] Read the selected ticket, Proof Contract, acceptance criteria, linked
  specs/docs, and any runtime target handoff.
- [ ] Use the generic [execute](../execute/SKILL.md) proof/writeback shape, but
  keep `$qa` focused on ticket-scoped evidence collection.
- [ ] If browser evidence is needed, use [agent-browser](../agent-browser/SKILL.md)
  as the browser tool surface and keep Codexter-specific artifact rules here.
- [ ] If a live app/API target is ambiguous, require a runtime record from
  [pr-runtime](../pr-runtime/SKILL.md) or record the blocker instead of guessing
  ports from chat.
- [ ] Create a run folder under
  `tickets/TASK-XXXX/artifacts/qa/<timestamp>-<slug>/`.
- [ ] Capture the relevant evidence: command outputs, screenshots, snapshots,
  console logs, page errors, API responses, traces, or generated artifacts.
- [ ] For browser proof, prefer a snapshot before interaction, screenshots for
  important states, and console/page-error logs when the UI is user-visible.
- [ ] For UI or visual judgment, hand screenshots and context to
  [visual-qa](../visual-qa/SKILL.md) as a separate judgment pass.
- [ ] Write `report.md` with the tested path, evidence links, pass/fail
  rationale, and any gaps.
- [ ] Write `result.json` with ticket id, phase, verdict, summary, and artifact
  paths.
- [ ] Update the ticket Evidence section with the strongest QA artifacts.
- [ ] If the proof is weak, confusing, or incomplete, return a revise/blocker
  verdict instead of claiming QA passed.
