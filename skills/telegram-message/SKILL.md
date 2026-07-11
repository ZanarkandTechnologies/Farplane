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
        details are needed, caller artifact when using --file,
        CODEX_THREAD_ID or caller-supplied thread/session id)
  writes(none by default; caller may persist message files)

gates:
  recipient_is_kenji
  no_secrets
  telegram_viewable
  one_clear_reply_action
  reply_route_target_available
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
  - [ ] For ticket feedback requests and reminders, prefer simple Telegram
    Markdown headings and emphasis so the decision is easier to scan on a
    phone.
  - [ ] Keep secrets, tokens, credentials, and sensitive private data out.
- [ ] 4. Send or fallback.
  - [ ] Resolve `thread_id := caller thread/session id || CODEX_THREAD_ID`.
    If no route target exists, do not send a replyable message; report a
    fallback/blocker.
  - [ ] Use `scripts/send_message.py`, which routes through the Farplane UI
    gateway by default so every sent message persists a Telegram message id ->
    thread/session route row.
  - [ ] Use `TELEGRAM_CHAT_ID` from environment or `~/.farplane/config.json`,
    and `TELEGRAM_BOT_TOKEN` from environment, Keychain, or gateway config.
  - [ ] Use `--parse-mode Markdown` for simple, controlled Markdown such as
    ticket feedback requests; use `--parse-mode none` for raw text or
    unsafe artifact excerpts.
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
*{short title}*

*Why this matters:* {one sentence}

*Options:*
A. {self-contained option}
B. {self-contained option}
C. {self-contained option}

*Reply with:* A, B, C, revise, or reject + one short reason.

_Desktop ref:_ {local desktop path marked "desktop-only"}
```

Ticket feedback/reminder shape:

```text
*{ticket}: {short decision title}*

*Review artifact:* {artifact type, e.g. social-thread premise / customer-facing idea}
*Skill/workflow:* {owner skill -> concrete workflow, e.g. social-content -> Twitter/X thread planning}
*Target:* {artifact, skill, customer action, or experiment surface}
*Stage:* {planning | execution | revision}; {publish/build boundary}
*Not judging:* {common confusions, e.g. video, product build, final copy, external posting}

*Context:* {one sentence}

*Premise:* {customer-facing premise}

*Why it might work:* {one compact reason}

*Question:* {the exact decision Kenji is making}

*Reply with:* approve, revise, or reject + one short reason.

_Desktop ref:_ {local path, desktop-only}
```

Send inline text:

```bash
source /Users/kenjipcx/.codex/private/telegram.env
python3 scripts/send_message.py \
  --thread-id "${CODEX_THREAD_ID:?CODEX_THREAD_ID required for reply routing}" \
  --text "Review needed: paste the short choices here, not only a local path." \
  --title "Review needed" \
  --parse-mode Markdown
```

Send a prepared file:

```bash
source /Users/kenjipcx/.codex/private/telegram.env
MESSAGE_FILE="/absolute/path/to/feedback-request.md"
python3 scripts/send_message.py \
  --thread-id "${CODEX_THREAD_ID:?CODEX_THREAD_ID required for reply routing}" \
  --file "$MESSAGE_FILE" \
  --title "Feedback request" \
  --parse-mode Markdown
```

## Gotchas

- A path like `tickets/TASK-0240/artifacts/foo.md` is not phone-viewable. Send
  the content needed to decide, a phone-openable URL, or a fallback/blocker.
- Telegram Markdown is not GitHub Markdown. Keep formatting simple: `*bold*`,
  `_italic_`, short bullets, and plain local paths. If a message includes
  arbitrary code, JSON, dense file paths, or generated text with lots of
  underscores/asterisks/brackets, send raw text with `--parse-mode none`
  instead.
- Do not send giant reports; compress to the smallest reviewable decision plus
  the one reply action.
- Sending Telegram does not imply permission to publish, message customers,
  spend money, deploy, or perform external side effects beyond notifying Kenji.
- Do not bypass the gateway with raw Telegram API sends for replyable messages.
  A sent message without a persisted route row cannot route Kenji's reply back
  to the originating Codex thread.

## Reference Map

- [references/configuration.md](references/configuration.md) - read when
  credential source, Keychain fallback, or missing-configuration behavior is
  needed.

## Output

- `sent_message`: one Telegram message sent through the Farplane UI Telegram
  gateway, with its reply route persisted.
- `fallback_report`: clear reason Telegram was skipped, missing, blocked, or
  not viewable enough to send.
