# Todos

- [ ] Read the active ticket and the linked proof before judging anything.
- [ ] Read the ticket `Proof Contract` and carry declared metrics, rubric gates, hard gates, and evidence obligations into the review.
- [ ] Read the [review rubric index](./references/review-rubric-index.md) and choose the families that actually fit this ticket.
- [ ] If code, cleanup, integration, or evidence trust is in scope, read the [desloppify guide](./references/desloppify.md) before scoring.
- [ ] Inspect the changed surface and the minimum neighboring code, docs, invariants, or interfaces needed to test consistency.
- [ ] If UI judgment is needed, use the [Visual QA](../visual-qa/SKILL.md) skill rather than faking visual review inside this skill.
- [ ] If the ticket claims screenshots, traces, logs, or QA artifacts, qualify that evidence before passing review.
- [ ] If the ticket declares metrics, verify the metric result is traceable to a command, artifact, or autoresearch log before using it as evidence.
- [ ] Rank substantive findings by severity and confidence instead of returning generic questions.
- [ ] Write the review result with scores, verdict, hard-gate failures if any, and the concrete next action, then make sure the ticket links it from `Evidence`.
