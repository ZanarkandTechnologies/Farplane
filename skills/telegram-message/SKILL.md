---
name: telegram-message
description: "Turn short HITL, automation, blocker, or artifact-review updates into Telegram notifications using configured environment variables."
tier: 1
source: local
allowed-tools: Bash, Read
---

# Telegram Message

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Confirm the message is for Kenji, not an external customer or public
  channel.
- [ ] Confirm the message contains no secrets or private credentials.
- [ ] Use `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` from environment only.
- [ ] Send with `scripts/send_message.py` using `--text`, `--file`, or stdin.
- [ ] If Telegram is not configured, report the fallback artifact path instead
  of blocking unrelated workflow progress.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this skill when a workflow needs to notify Kenji on Telegram.

This is a small reusable primitive. Higher-level skills such as
`hitl-autoresearch` should write their own message body, then call this skill to
send it.

## Requirements

Environment variables must be available to the shell that sends the message:

- `TELEGRAM_CHAT_ID`

`TELEGRAM_BOT_TOKEN` may be provided in the environment, but the preferred local
default is macOS Keychain item `codex-telegram-bot-token`.

Never write token values into a skill, repo file, session file, or chat output.

## Workflow

1. Prepare a short message body or a message file.
2. Keep secrets out of the message.
3. Run `scripts/send_message.py` with either `--text` or `--file`.
4. If `TELEGRAM_CHAT_ID` is missing, or no token exists in env or Keychain,
   report that Telegram is not configured and leave the message in the caller's
   local artifact, such as `feedback-request.md`.
5. If Telegram returns an error, report the HTTP/API failure and do not retry in
   a tight loop.

## Commands

Send inline text:

```bash
source /Users/kenjipcx/.codex/private/telegram.env
python3 scripts/send_message.py --text "Review needed: outputs/run-1/index.html"
```

Send a file:

```bash
source /Users/kenjipcx/.codex/private/telegram.env
python3 scripts/send_message.py --file feedback-request.md
```

Use `--parse-mode Markdown` only when the message is simple Markdown. Use
`--parse-mode none` for raw text.

## Reference Map

- [`references/configuration.md`](references/configuration.md) - credential
  source and missing-configuration fallback rules.

## Core Branches

- **HITL feedback request:** send the generated review message file.
- **Automation status:** send a concise success/blocker summary.
- **Artifact ready:** send local paths or public links plus the review question.
- **Missing Telegram config:** do not block the whole workflow if a local review
  request file exists; report the fallback.

## Top 3 Gotchas

1. Do not hardcode or print Telegram secrets.
2. Do not send giant reports; send a summary and link/path to the artifact.
3. Do not use Telegram sending as permission to publish, message customers,
   spend money, or perform external side effects beyond notifying Kenji.

## Outcome Contract

The skill either:

- sends one Telegram message and prints a success line, or
- exits with a clear reason that Telegram is not configured or failed.
