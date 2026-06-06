---
name: pr-review-watch
version: 0.1.0
description: Watch an explicitly selected GitHub pull request until configured review agents and checks pass, using project-local review memory, bounded heartbeat polling, fix loops, and terminal Telegram notifications.
tier: 3
group: coding
source: local
allowed-tools: Read, Glob, Grep, Bash
common_chains:
  after: ["pr-runtime", "coderabbit-review"]
---

# PR Review Watch

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

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
- [ ] Use adaptive backoff from `docs/specs/adaptive-backoff.md` for repeated
  wait states unless project memory declares a narrower PR-specific cadence.
- [ ] Run `python3 bin/pr_review_watch.py classify --fixture <path> --json` for
  deterministic state checks, or live `gh` discovery only after the user
  explicitly asks to watch a PR.
- [ ] Fix only actionable review items and run only project-configured local
  check/review commands.
- [ ] Use [coderabbit-review](../coderabbit-review/SKILL.md) only when the
  project memory explicitly includes it as a review command or provider.
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

- [pr-runtime](../pr-runtime/SKILL.md) decides whether the PR branch needs an
  isolated checkout or runtime record.
- [coderabbit-review](../coderabbit-review/SKILL.md) runs a heavyweight local
  CodeRabbit pass only when project memory asks for it.
- [execute](../execute/SKILL.md) supplies the proof/writeback shape for ticketed
  implementation and evidence.

## Trigger Conditions

- "watch this PR every 10 minutes until checks pass"
- "keep fixing CodeRabbit/Cursor/GitHub review comments on this PR"
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
3. Use `pr-runtime` when an existing PR branch should be isolated from the
   shared checkout.
4. Run:

   ```bash
   python3 bin/pr_review_watch.py classify --repo <repo> --pr <number> --json
   ```

5. Inspect the `WatchVerdict`:
   - `pass`: run terminal notification with the PR URL and stop.
   - `blocked`: write blocker details, notify with the PR URL when configured,
     and stop.
   - `wait`: create a visible Codex automation heartbeat with the next interval.
   - `actionable`: fix only the listed items, run configured checks, then
     reclassify.
6. Use `coderabbit-review` only when the config names CodeRabbit as a review
   command/provider. Do not make it a universal PR gate.
7. On timeout, summarize the last verdict and notify with the PR URL when
   configured.

## Automation Heartbeat

The watcher does not sleep in a hidden loop. When the verdict is `wait`, use the
Codex app automation tool to schedule one follow-up with the prompt from
[`templates/codex-automation-prompt.md`](templates/codex-automation-prompt.md).

Use the `human_review` profile in
[`docs/specs/adaptive-backoff.md`](../../docs/specs/adaptive-backoff.md) unless
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
