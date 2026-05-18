# Todos

- [ ] Confirm the loop is same-session, bounded, reversible, and has an
  explicit local completion check.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) to identify the
  current artifact, proof command, and last failed condition.
- [ ] Run one iteration at a time: inspect, change, verify, update state.
- [ ] Stop when the completion check passes, a real blocker appears, or the
  user changes scope.
- [ ] Preserve unrelated dirty work and avoid hidden automation.
- [ ] Use [advise](../advise/SKILL.md) when continuing would trade off safety,
  scope, spend, or runtime risk.
- [ ] Use [review](../review/SKILL.md) before making a material completion
  claim after a loop.
