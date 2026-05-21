# Todos

- [ ] Resolve exactly one active ticket and confirm the remaining work is
  genuinely closeout, not missing implementation.
- [ ] Use the generic [execute](../execute/SKILL.md) interface's proof and
  writeback shape, but keep `close-ticket` coding-ticket closeout specific.
- [ ] Update the ticket writeback: evidence, linked docs, handoff, next action,
  and `last_verification`.
- [ ] Update durable docs that changed in the final pass: `docs/HISTORY.md`,
  `docs/MEMORY.md`, `docs/TROUBLES.md`, README, or the nearest `AGENTS.md`.
- [ ] Run the feature closeout consistency sweep for relevant surfaces:
  `README.md`, `ARCHITECTURE.md`, `docs/specs/README.md`,
  `docs/skills/README.md`, `docs/skills/registry.jsonl`,
  `docs/features/registry.jsonl`, and nearest module `README.md`/`AGENTS.md`.
- [ ] If the final proof or linked review artifact is stale, re-enter the
  [execute](../execute/SKILL.md) proof/review closeout shape before closing
  the ticket.
- [ ] Run the repo-local validators and final checks that actually match the
  touched surfaces.
- [ ] Use the [Commit Message](../commit-message/SKILL.md) skill for the commit
  subject.
- [ ] If heavy explicit pre-push review is needed, use
  [CodeRabbit Review](../coderabbit-review/SKILL.md).
- [ ] Commit only the intended closeout slice.
- [ ] Push only when the user or workflow explicitly calls for publishing.
- [ ] Leave the ticket clearly archive-ready, committed, blocked, or still in
  documenting with one concrete next action.
