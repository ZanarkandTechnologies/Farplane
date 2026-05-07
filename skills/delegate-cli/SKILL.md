---
name: delegate-cli
version: 0.1.0
description: Route bounded Codexter work to configured external coding-agent CLIs through explicit adapter/profile contracts, managed prompts, runtime logs, and ticket evidence handoff. Use when another local CLI/model/harness is stronger for a task but Codexter must keep ticket, QA, review, and integration authority.
allowed-tools: Read, Grep, Glob, Bash
---

# Delegate CLI

Use this skill to run an external coding-agent CLI as a bounded builder lane
without letting that CLI become Codexter's source of truth.

## Trigger Conditions

- A ticket or user ask says a different local CLI/model should own a bounded
  build pass.
- The work needs profile-specific skills, prompts, or model defaults.
- Codexter must capture logs, handoff notes, and optional diffs as ticket
  evidence.
- The external CLI should not push, deploy, publish, spend, or approve its own
  output.

## Workflow

1. Read the selected ticket or task artifact and confirm delegation is a build
   lane, not final authority.
2. Pick one configured profile such as `frontend-pi-kimi`; use `advise` when
   multiple profiles fit materially differently.
3. Run `python3 bin/delegate_cli_agent.py doctor --profile <profile> --json`
   to check the executable, templates, skills, and environment.
4. Run `python3 bin/delegate_cli_agent.py setup --profile <profile> --json`
   when the profile needs a managed skill/prompt bundle.
5. Load [prompt-engineering](../../rules/prompt-engineering.md) when the delegated prompt needs role, task, constraints, output format, examples, or structured-output discipline.
6. Run `python3 bin/delegate_cli_agent.py run --profile <profile> --ticket <ticket> --dry-run --json`
   first to inspect the rendered command and prompt.
7. Run without `--dry-run` only when the operator has allowed live CLI/model
   execution and any credentials/spend are acceptable.
8. Attach the generated handoff/logs/patch to ticket evidence and route the
   result back through Codexter QA/review.

## Core Decision Branches

- `frontend implementation or design polish` -> use `delegate-frontend`, which
  calls this skill with `frontend-pi-kimi`.
- `missing executable or credentials` -> keep the ticket blocked or run only
  `--dry-run`; do not install tools or spend money silently.
- `multiple live writers` -> prefer `--checkout worktree`; shared checkout is
  acceptable only for a single low-risk manual run.
- `new CLI family` -> add an adapter/profile pair and dry-run tests before
  describing it as shipped.

## Judgement Questions

Use `advise` when choosing:

- which external CLI/profile should own the build pass,
- shared checkout versus worktree mode,
- live run versus dry-run only,
- whether a new adapter belongs in this ticket or a follow-up.

## Top Gotchas

1. Do not let an external CLI mutate queue state, approve completion, push,
   deploy, publish, or spend without an explicit human gate.
2. Do not track generated `.harness/external-cli/` runtime bundles or secrets.
3. Do not ship a profile as active until the launcher can dry-run it and attach
   reproducible artifacts.
4. For Pi, `@file` is an attachment syntax, not a prompt-file execution syntax.
   The launcher must pass rendered prompt text as the `-p` message and reserve
   `@...` for true attachments. Recorded command artifacts should redact the
   prompt argument and point reviewers to `prompt.md`.

## Outcome Contract

Return or write:

- chosen profile and adapter,
- rendered command or live command result,
- runtime artifact directory,
- durable ticket artifact directory when a ticket was supplied,
- handoff/log/diff paths,
- next Codexter QA/review step.

## References

- [architecture.md](references/architecture.md)
- [workflows.md](references/workflows.md)
- [gotchas.md](references/gotchas.md)
- [prompt-engineering.md](../../rules/prompt-engineering.md)
