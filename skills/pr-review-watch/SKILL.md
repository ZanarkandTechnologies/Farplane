---
name: pr-review-watch
version: 0.1.0
description: "Turn an explicit GitHub PR into bounded polling, review-memory checks, fix loops, and notification-ready status until checks pass."
tier: 3
group: coding
source: local
allowed-tools: Read, Glob, Grep, Bash
common_chains:
  after: ["review"]
---

# PR Review Watch

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Read the selected PR target, target repo, project review memory, and
  requested watch interval before polling anything.
- [ ] Use the native execution phase for proof/writeback shape and keep this
  skill focused on the coding-ticket PR watcher workflow.
- [ ] Use the native planning phase when repo target, PR number, notification
  policy, push permission, or project review commands are unclear.
- [ ] Use the checkout assigned to the current Codex task. Treat a different
  checkout or runtime target as explicit caller input rather than creating
  Farplane runtime state.
- [ ] Load `docs/pr-review-pipeline.md` first, then `PROJECT_RULES.md`, and
  require an explicit `pr_review_pipeline` JSON block before live watching.
- [ ] Use adaptive backoff from `docs/features/FEAT-0065-pulse-and-interval-automation.md` for repeated
  wait states unless project memory declares a narrower PR-specific cadence.
- [ ] Run `python3 skills/pr-review-watch/scripts/pr_review_watch.py classify --fixture <path> --json` for
  deterministic state checks, or live `gh` discovery only after the user
  explicitly asks to watch a PR.
- [ ] Fix only actionable review items and run only project-configured local
  check/review commands.
- [ ] Use [review](../review/SKILL.md) or the configured reviewer lane for
  material review commands; do not invoke external review CLIs from this skill.
- [ ] Reschedule through a visible Codex automation heartbeat; do not create a
  daemon, background queue, hidden loop, or always-on watcher.
- [ ] Send pass, blocked, or timeout summaries with the PR URL through the
  `telegram-message` skill when it is available and the project notification
  policy asks for it.
- [ ] Do not merge, deploy, push, change billing/spend, or invent new provider
  commands unless the surrounding workflow explicitly authorizes that action.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this skill when the operator asks Farplane to watch an already-open pull
request and keep responding to asynchronous review comments or status checks.
The workflow is explicit and bounded: one selected PR, one project-local review
contract, one heartbeat at a time.

This skill composes existing Farplane surfaces:

- [review](../review/SKILL.md) or the configured reviewer lane handles material
  review findings when project memory asks for review.
- the native execution phase supplies the proof/writeback shape for ticketed
  implementation and evidence.

## Trigger Conditions

- "watch this PR every 10 minutes until checks pass"
- "keep fixing reviewer/Cursor/GitHub review comments on this PR"
- "poll PR 123 and message me when it passes or blocks"
- "run the PR review watcher"

## Project Memory Contract

Before live polling, read `docs/pr-review-pipeline.md` in the target repo. If it
does not exist, read `PROJECT_RULES.md`. One of those files must contain a
fenced JSON block with `pr_review_pipeline`.

Minimal shape:

```json
{
  "pr_review_pipeline": {
    "providers": ["github"],
    "poll_interval_minutes": 10,
    "max_iterations": 12,
    "pass_conditions": {
      "require_checks_pass": true,
      "require_no_actionable_comments": true,
      "require_approval": false
    },
    "fix_commands": ["npm test"],
    "review_commands": [],
    "notification_policy": {
      "telegram": true,
      "terminal_states": ["pass", "blocked", "timeout"]
    }
  }
}
```

Use [`templates/pr-review-pipeline.md`](templates/pr-review-pipeline.md) as the
copyable project-local contract.

## Workflow

1. Resolve the target repo and PR number. If the user did not provide a PR
   number, discover the active PR from the current branch with GitHub CLI.
2. Read project memory and load the `pr_review_pipeline` config.
3. Run:

   ```bash
   python3 skills/pr-review-watch/scripts/pr_review_watch.py classify --repo <repo> --pr <number> --json
   ```

4. Inspect the `WatchVerdict`:
   - `pass`: run terminal notification with the PR URL and stop.
   - `blocked`: write blocker details, notify with the PR URL when configured,
     and stop.
   - `wait`: create a visible Codex automation heartbeat with the next interval.
   - `actionable`: fix only the listed items, run configured checks, then
     reclassify.
5. Run only project-configured local checks and Farplane reviewer-agent review
   commands. Do not make external review CLIs a universal PR gate.
6. On timeout, summarize the last verdict and notify with the PR URL when
   configured.

## Automation Heartbeat

The watcher does not sleep in a hidden loop. When the verdict is `wait`, use the
Codex app automation tool to schedule one follow-up with the prompt from
[`templates/codex-automation-prompt.md`](templates/codex-automation-prompt.md).

Use the `human_review` profile in
[`docs/features/FEAT-0065-pulse-and-interval-automation.md`](../../docs/features/FEAT-0065-pulse-and-interval-automation.md) unless
project memory declares a stricter interval. Honor provider or CI timing hints
first, widen repeated unchanged pending checks up to the configured cap, and
reset or shorten the next wait when checks, approvals, comments, or review
states change.

The heartbeat prompt must include:

- repo path
- PR number
- current iteration and max iterations
- previous verdict JSON or artifact path
- allowed fix/review commands
- notification policy
- PR URL from the normalized snapshot when available

## Outcome Contract

Return or write:

- selected repo and PR number
- config source path
- normalized snapshot or fixture path
- `WatchVerdict` JSON
- commands run for fixes and review
- heartbeat scheduled, terminal notification sent with PR URL, or explicit
  reason skipped
- blocker details when blocked

## Guardrails

- No hidden daemon, always-on watcher, cloud scheduler, queue runner, or
  background polling process.
- No automatic push, merge, deploy, destructive git operation, or provider
  command invention.
- Unit proof uses fixture snapshots; live GitHub polling is integration behavior
  and depends on local `gh` auth.
- Telegram notification is best-effort and terminal-state only.
- Project rules own local commands. This skill coordinates; it does not guess a
  repo's validation suite.
