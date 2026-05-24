# Todos

- [ ] Read the selected ticket, demo requirement, and latest QA artifacts before
  creating demo output.
- [ ] Use [qa](../qa/SKILL.md) as the source of truth for evidence; do not
  invent a demo from unverified behavior.
- [ ] Decide the lightest presentable format: annotated screenshot report,
  HTML summary, slide/storyboard pack, short clip, or video walkthrough.
- [ ] If QA evidence is missing or not presentable, request a QA rerun or use
  [agent-browser](../agent-browser/SKILL.md) only for a narrow missing browser
  capture.
- [ ] Package demo outputs under
  `tickets/TASK-XXXX/artifacts/demo/<timestamp>-<slug>/`.
- [ ] Annotate what changed, why it matters, and which QA artifact proves each
  visible claim.
- [ ] Write `result.json` with ticket id, phase, verdict, summary, and artifact
  paths.
- [ ] Update the ticket Evidence section with demo artifact links.
- [ ] If the demo is not presentation-ready, return a revise/blocker verdict
  instead of marking demo complete.
