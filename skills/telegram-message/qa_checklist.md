---
title: Telegram Message QA / Review Checklist
owner: telegram-message
status: active
kind: qa-checklist
applies_to:
  - telegram-notifications
  - feedback-requests
  - artifact-reviews
---

# Telegram Message QA / Review Checklist

Use this checklist before preparing a Telegram message and again before sending
or reporting fallback. For automated, sensitive, or material notifications, ask
an independent reviewer/subagent to inspect the message body first when
feasible.

```text
telegram_message_check(message, recipient, send_path, artifacts?, fallback?)
  -> pass | violation | deferral
```

## Preflight

- [ ] The intended recipient is Kenji, not an external customer, public channel,
  vendor, or unrelated contact.
- [ ] The message has a legitimate workflow reason: feedback request,
  automation status, blocker, artifact ready, or review request.
- [ ] The required user action is a single clear reply action, such as
  `pick A/B/C`, `approve`, `revise`, or `reject with one reason`.
- [ ] The message will be readable on a phone inside Telegram:
  - [ ] If asking for artifact feedback, the message includes the reviewable
    excerpt, options, or summary needed to decide.
  - [ ] Any link needed for review is phone-openable, not only a local
    filesystem path.
  - [ ] Local paths are allowed only as desktop refs after the self-contained
    content or phone-openable link.
- [ ] The message is short enough to scan in Telegram and does not paste a giant
  report when a compact decision prompt would work.
- [ ] No secrets, tokens, private credentials, or sensitive personal data are in
  the message body or command output.
- [ ] The send path uses environment or Keychain credentials only; token values
  are never written to files, commands in chat, or repo artifacts.
- [ ] A route target is available as caller-supplied `threadId`/`sessionId` or
  `CODEX_THREAD_ID`, so Telegram replies can be routed back to the originating
  Codex thread.

## Final Review

- [ ] Artifact-review messages are not local-path-only. If the only review
  surface is local, block sending and ask the caller to provide inline content,
  a phone-openable link, or a generated summary.
- [ ] The first screen of the Telegram message explains what this is, why it
  matters, and exactly how Kenji should reply.
- [ ] `TELEGRAM_CHAT_ID` is configured, and a token is available from
  environment or the configured Keychain path before attempting to send.
- [ ] The message is sent through `scripts/send_message.py` with
  `--thread-id`/`--session-id` or `CODEX_THREAD_ID`; the script must use the
  Farplane UI gateway path for replyable messages.
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
Focus on recipient correctness, secret safety, phone readability, artifact
viewability, reply action clarity, and side-effect bounds.
Do not send the message yourself.
```
