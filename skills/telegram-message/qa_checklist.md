---
title: Telegram Message QA / Review Checklist
owner: telegram-message
status: active
kind: qa-checklist
applies_to:
  - telegram-notifications
  - feedback-requests
---

# Telegram Message QA / Review Checklist

Use this checklist before preparing a Telegram message and again before sending
or reporting fallback. For automated, sensitive, or material notifications, ask
an independent reviewer/subagent to inspect the message body first when feasible.

```text
telegram_message_check(message, recipient, send_path, fallback?)
  -> pass | violation | deferral
```

## Preflight

- [ ] The intended recipient is Kenji, not an external customer, public channel,
  vendor, or unrelated contact.
- [ ] The message has a legitimate workflow reason: feedback request,
  automation status, blocker, artifact ready, or review request.
- [ ] The message body is short and points to local artifacts or links instead
  of pasting large reports.
- [ ] No secrets, tokens, private credentials, or sensitive personal data are in
  the message body or command output.
- [ ] The send path uses environment or Keychain credentials only; token values
  are never written to files, commands in chat, or repo artifacts.

## Final Review

- [ ] `TELEGRAM_CHAT_ID` is configured, and a token is available from environment
  or the configured Keychain path before attempting to send.
- [ ] `scripts/send_message.py` is used with `--text`, `--file`, or stdin.
- [ ] Markdown parse mode is used only for simple Markdown; raw text uses
  `--parse-mode none`.
- [ ] Telegram failure or missing configuration is reported clearly without
  blocking unrelated workflow progress.
- [ ] Sending this message does not imply permission to publish, contact
  customers, spend money, deploy, or perform other external side effects.

## Reviewer Prompt

```text
Review the Telegram message against skills/telegram-message/qa_checklist.md.
Return pass, violation, or deferral for each failed check.
Focus on recipient correctness, secret safety, brevity, and side-effect bounds.
Do not send the message yourself.
```
