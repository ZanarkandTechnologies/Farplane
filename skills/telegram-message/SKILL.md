---
name: telegram-message
description: "Turn short feedback, automation, blocker, or artifact-review updates into Telegram notifications that Kenji can understand and answer from Telegram."
tier: 1
source: local
capability:
  kind: integration
template_uses:
  skill-template: "0.3.6"
  skill-qa-checklist: "0.1.0"
  skill-eval-task: "0.2.0"
allowed-tools: Bash, Read
eval: evals/evals.json
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
telegram_message(message_intent, message_body?, original_source_url?,
                 artifact_refs?, media_paths?, state?)
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
  plain_language_context
  original_source_phone_openable
  one_clear_reply_action
  visual_review_uses_photo
  reminder_stakes_deadline_consequence
  reply_route_target_available
  sent_claim_has_gateway_receipt
  credentials_available_or_fallback_recorded

routes:
  optimize-with-human -> telegram-message

fails:
  local_path_only_artifact_review
  text_only_visual_artifact_review
  opaque_ticket_id_without_context
  shallow_option_summary
  missing_original_source_link
  context_free_reminder
  artificial_choice_for_open_judgment
  irrelevant_boundary_boilerplate
  unreceipted_send_claim
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
  - [ ] `original_source_url :=` the phone-openable original task, brief,
    proposal, or source page. Every sent message includes this labeled link.
    If no phone-openable original exists, report a fallback/blocker.
  - [ ] If the message references artifacts, decide what Kenji can actually
    read from Telegram on a phone.
  - [ ] If the decision is visual, bind one PNG/JPEG review image. Text,
    Markdown, and a desktop path are supporting copy, not the review surface.
  - [ ] If two workflows are difficult to distinguish in prose, bind a
    comparison image or include a compact step-by-step flow for each.
- [ ] 2. Read guardrails.
  - [ ] Read `qa_checklist.md` before preparing or sending the message.
  - [ ] Read `references/configuration.md` only when credential fallback details
    are needed.
- [ ] 3. Prepare a Telegram-native body.
  - [ ] Lead with the plain-language product, artifact, decision, or blocker;
    never make a ticket id carry the context.
  - [ ] Include enough background and reviewable substance for Kenji to
    understand what he is advising on without reconstructing the task.
  - [ ] For a decision, describe each real option as a concrete workflow,
    state what is at stake for the user or product, attach the comparison
    visual when one exists, and give one honest recommendation with its reason.
  - [ ] For an artifact-ready message, state what changed, what to inspect,
    and label each attached image, phone-openable artifact, and supporting file.
  - [ ] For a blocker or reminder, state in order: what is at stake, the exact
    blocker Kenji can resolve, why his judgment is needed, the required action,
    deadline, and what happens if the deadline passes. Do not force an A/B
    choice when open judgment is required.
  - [ ] End the review content with `*Original:* {original_source_url}`.
  - [ ] If only a local path exists, include the essential excerpt or do not
    send; report a fallback/blocker instead.
  - [ ] Ask one concrete reply action Kenji can answer in one Telegram reply.
  - [ ] For ticket feedback requests and reminders, prefer simple Telegram
    Markdown headings and emphasis so the decision is easier to scan on a
    phone.
  - [ ] Enforce side-effect boundaries without appending generic approval,
    deployment, or publication boilerplate unless that boundary materially
    affects the decision being requested.
  - [ ] Keep secrets, tokens, credentials, and sensitive private data out.
- [ ] 4. Send or fallback.
  - [ ] Resolve `thread_id := caller thread/session id || CODEX_THREAD_ID`.
    If no route target exists, do not send a replyable message; report a
    fallback/blocker.
  - [ ] Use `scripts/send_message.py`, which routes through the Farplane UI
    gateway by default so every sent message persists a Telegram message id ->
    thread/session route row.
  - [ ] Return `sent_message` and use words such as `sent`, `attached`, or
    `delivered` only after the gateway returns a message id and delivery kind.
    A drafted body, named file, simulated fixture, or intended command is not a
    send; return `fallback_report` with the missing file, route, credential, or
    receipt instead.
  - [ ] For a visual decision, use `--photo /absolute/path.png` with a short
    caption. A successful text message does not satisfy visual delivery.
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

Use these as taste calibration. Replace their facts and template values; do not
copy the scenario blindly.

Decision request:

```text
*Choose the first-run experience for new Farplane projects*

We're redesigning what happens immediately after someone connects a project.
The goal is to help a new user reach their first useful Pulse without already
understanding Farplane's ticket system.

*What's at stake:* This decides whether a new user reaches a useful first task
or lands on an empty board without knowing what to do next.

*Guided setup:* Connect project -> describe goal -> Farplane proposes the first
ticket -> user reviews it.

*Instant workspace:* Connect project -> open empty board -> user creates the
first ticket manually.

*Comparison:* {attach_photo: onboarding-flow-comparison.png}
*Original:* {phone_openable_original_url}

I recommend Guided setup because it teaches Farplane through action instead of
documentation.

*Reply with:* Guided or Instant, plus any condition that would change your
answer.
```

Artifact-ready review:

```text
*Review the redesigned onboarding flow*

The prototype now takes a first-time user from "connect project" to a
reviewable first ticket in three screens.

*What to inspect:* Is the next action obvious on every screen? Does the proposed
ticket feel useful rather than generic?

*Visual walkthrough:* {attach_photo: onboarding-approval-sheet.png}
*Interactive prototype:* {phone_openable_artifact_url}
*Supporting file:* {phone_openable_file_url}
*Original:* {phone_openable_original_url}

*Reply with:* approve, or revise + what felt unclear.
```

Blocker or reminder:

```text
*Onboarding user test is blocked - input needed by {deadline_local}*

*What's at stake:* We cannot finish the onboarding flow or run the scheduled
user test until the example project content is defined.

*Blocked by:* The worker needs your judgment on what a credible first project
should contain; this cannot be inferred safely from the task.

*What I need from you:* Open the task and describe the project example you
would trust as a new user.

*Deadline:* {deadline_local}
*If unanswered:* The ticket pauses and the user test moves to
{next_available_window}; no default will be invented.

*Original:* {phone_openable_original_url}
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

Send a visual approval packet:

```bash
source /Users/kenjipcx/.codex/private/telegram.env
python3 scripts/send_message.py \
  --thread-id "${CODEX_THREAD_ID:?CODEX_THREAD_ID required}" \
  --photo "/absolute/path/to/approval-sheet.png" \
  --file "/absolute/path/to/approval-caption.txt" \
  --title "Visual approval" \
  --parse-mode none
```

## Gotchas

- A path like `tickets/TASK-0240/artifacts/foo.md` is not phone-viewable. Send
  the content needed to decide, a phone-openable URL, or a fallback/blocker.
- A ticket id or artifact name is not context. Lead with the plain-language
  decision, result, or blocker, and include the phone-openable original link.
- A storyboard, design, image, or video-frame review is visual. Never replace
  its required PNG/JPEG with a prose summary, Markdown storyboard, or link.
- Telegram Markdown is not GitHub Markdown. Keep formatting simple: `*bold*`,
  `_italic_`, short bullets, and plain local paths. If a message includes
  arbitrary code, JSON, dense file paths, or generated text with lots of
  underscores/asterisks/brackets, send raw text with `--parse-mode none`
  instead.
- Do not send giant reports; compress to the smallest reviewable decision plus
  the one reply action.
- Do not append approval, deploy, publish, or spend disclaimers mechanically.
  State a boundary only when the requested reply could reasonably be mistaken
  for broader authority; always enforce the boundary regardless of wording.
- Never infer delivery from a prepared message or supplied filename. A send
  claim requires the gateway message id and delivery kind in the receipt.
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

- `sent_message`: one Telegram text or photo message sent through the Farplane
  UI gateway, with a returned message id, reply route, and delivery kind
  persisted. Without that receipt, this output is invalid.
- `fallback_report`: clear reason Telegram was skipped, missing, blocked, or
  not viewable enough to send.
