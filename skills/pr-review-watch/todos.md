- [ ] Read the selected PR target, target repo, project review memory, and
  requested watch interval before polling anything.
- [ ] Use [execute](../execute/SKILL.md) for proof/writeback shape and keep this
  skill focused on the coding-ticket PR watcher workflow.
- [ ] Use [plan](../plan/SKILL.md) when repo target, PR number, notification
  policy, push permission, or project review commands are unclear.
- [ ] Use [pr-runtime](../pr-runtime/SKILL.md) when an existing PR branch,
  isolated checkout, or declared QA target is needed.
- [ ] Load `docs/pr-review-pipeline.md` first, then `PROJECT_RULES.md`, and
  require an explicit `pr_review_pipeline` JSON block before live watching.
- [ ] Run `python3 bin/pr_review_watch.py classify --fixture <path> --json` for
  deterministic state checks, or live `gh` discovery only after the user
  explicitly asks to watch a PR.
- [ ] Fix only actionable review items and run only project-configured local
  check/review commands.
- [ ] Use [coderabbit-review](../coderabbit-review/SKILL.md) only when the
  project memory explicitly includes it as a review command or provider.
- [ ] Reschedule through a visible Codex automation heartbeat; do not create a
  daemon, background queue, hidden loop, or always-on watcher.
- [ ] Send pass, blocked, or timeout summaries through the `telegram-message`
  skill when it is available and the project notification policy asks for it.
- [ ] Do not merge, deploy, push, change billing/spend, or invent new provider
  commands unless the surrounding workflow explicitly authorizes that action.
