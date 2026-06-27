---
name: telegram-message
description: "Turn short feedback, automation, blocker, or artifact-review updates into Telegram notifications that Kenji can understand and answer from Telegram."
tier: 1
source: local
template_uses:
  skill-template: "0.3.6"
  skill-qa-checklist: "0.1.0"
  skill-eval-task: "0.1.0"
allowed-tools: Bash, Read
eval: eval_task.json
qa_checklist: qa_checklist.md
---

# Telegram Message

## Context

Use this skill when a workflow needs to notify Kenji on Telegram. This is a
small reusable primitive; higher-level skills such as `optimize-with-human`
write the request, then call this skill to deliver it.

Telegram is often read on a phone. A notification must be useful inside
Telegram itself. Do not send a message whose only review surface is a local
filesystem path unless the message also includes the decision content or a
phone-openable URL.

Never write Telegram token values into a skill, repo file, session file, or
chat output.

## Skill Signature

```text
telegram_message(message_intent, message_body?, artifact_refs?, state?)
  -> sent_message | fallback_report

state:
  reads(qa_checklist.md, references/configuration.md when credential fallback
        details are needed, caller artifact when using --file)
  writes(none by default; caller may persist message files)

gates:
  recipient_is_kenji
  no_secrets
  telegram_viewable
  one_clear_reply_action
  credentials_available_or_fallback_recorded

routes:
  optimize-with-human -> telegram-message

fails:
  local_path_only_artifact_review
  vague_reply_shape
  giant_report_dump
  secret_or_token_exposure
  external_customer_or_public_channel
```

```text
TelegramViewMode =
  inline_summary       # enough content in Telegram to decide now
  phone_openable_link  # public/private URL accessible from phone
  fallback_only        # do not send; record local fallback/blocker
```

## Phase Boundary

This skill performs its phases inline. Use an independent reviewer only for
material, automated, sensitive, or repeated notification failures.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the message request.
  - [ ] `recipient := Kenji`.
  - [ ] `message_intent := feedback_request | automation_status | blocker |
    artifact_ready | review_request`.
  - [ ] `view_mode := inline_summary | phone_openable_link | fallback_only`.
  - [ ] If the message references artifacts, decide what Kenji can actually
    read from Telegram on a phone.
- [ ] 2. Read guardrails.
  - [ ] Read `qa_checklist.md` before preparing or sending the message.
  - [ ] Read `references/configuration.md` only when credential fallback details
    are needed.
- [ ] 3. Prepare a Telegram-native body.
  - [ ] Include the reviewable content, choices, or a phone-openable link.
  - [ ] If only a local path exists, include the essential excerpt or do not
    send; report a fallback/blocker instead.
  - [ ] Ask one concrete reply action Kenji can answer in one Telegram reply.
  - [ ] Keep secrets, tokens, credentials, and sensitive private data out.
- [ ] 4. Send or fallback.
  - [ ] Use `TELEGRAM_CHAT_ID` from environment and `TELEGRAM_BOT_TOKEN` from
    environment or the configured Keychain fallback only.
  - [ ] Send with `scripts/send_message.py` using `--text`, `--file`, or stdin.
  - [ ] Use `--parse-mode Markdown` only for simple Markdown; use
    `--parse-mode none` for raw text.
  - [ ] If Telegram is not configured, report the fallback artifact path instead
    of blocking unrelated workflow progress.
- [ ] 5. Finish gate.
  - [ ] Apply `qa_checklist.md` again before sending or reporting fallback.
  - [ ] For material or automated notifications, use independent review of the
    message body when feasible.
  - [ ] Report whether the message was sent, skipped, or blocked, and why.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Artifact-review message shape:

```text
{short title}

Why this matters: {one sentence}

Options:
A. {self-contained option}
B. {self-contained option}
C. {self-contained option}

Reply with: A, B, C, revise, or reject + one short reason.

Ref: {phone-openable URL or local desktop path marked "desktop-only"}
```

Send inline text:

```bash
source /Users/kenjipcx/.codex/private/telegram.env
python3 scripts/send_message.py --text "Review needed: paste the short choices here, not only a local path."
```

Send a prepared file:

```bash
source /Users/kenjipcx/.codex/private/telegram.env
python3 scripts/send_message.py --file feedback-request.md --parse-mode none
```

## Gotchas

- A path like `tickets/TASK-0240/artifacts/foo.md` is not phone-viewable. Send
  the content needed to decide, a phone-openable URL, or a fallback/blocker.
- Do not send giant reports; compress to the smallest reviewable decision plus
  the one reply action.
- Sending Telegram does not imply permission to publish, message customers,
  spend money, deploy, or perform external side effects beyond notifying Kenji.

## Reference Map

- [references/configuration.md](references/configuration.md) - read when
  credential source, Keychain fallback, or missing-configuration behavior is
  needed.

## Output

- `sent_message`: one Telegram message sent through `scripts/send_message.py`.
- `fallback_report`: clear reason Telegram was skipped, missing, blocked, or
  not viewable enough to send.
