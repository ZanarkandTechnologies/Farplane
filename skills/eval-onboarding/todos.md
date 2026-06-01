# Todos

- [ ] Confirm the eval target, user-visible behavior, and smallest useful
  pass/fail claim.
- [ ] Keep the fixture set clean-room: use invented tasks, synthetic repos, and
  generic file names; do not inspect or copy private example systems.
- [ ] If the operator wants inspiration from a private example, capture only
  sanitized, high-level pattern notes and convert them into new clean-room
  tasks.
- [ ] Use [testing](../testing/SKILL.md) to choose the cheapest meaningful
  proof level before adding harness machinery.
- [ ] Define the JSON task schema, rubric fields, expected artifacts, and
  runner contract.
- [ ] Create or adapt 3-5 starter tasks that cover happy path, edge path,
  failure path, and regression/canary path.
- [ ] Decide whether the eval needs `agent-behavior-test` run capture or
  `agent-qa-test` adversarial evidence review.
- [ ] Run or document one smoke command that proves the harness can load tasks
  and emit a run report.
- [ ] Use [execute](../execute/SKILL.md) for final proof/writeback when eval
  files are added to a repo.
