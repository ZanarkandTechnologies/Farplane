---
title: Notify Telegram templates
status: active
owner: skills/notify
kind: reference
---

# Telegram Templates

Load this in N2 and N3 of `notify` (channel `telegram`). Use these as taste
calibration: replace their facts and template values; do not copy the scenario
blindly.

Decision request:

```text
*Choose the first-run experience for new Farplane projects*

We're redesigning what happens immediately after someone connects a project.
The goal is to help a new user reach their first useful task without already
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
python3 skills/notify/scripts/send_message.py \
  --thread-id "${CODEX_THREAD_ID:?CODEX_THREAD_ID required for reply routing}" \
  --text "Review needed: paste the short choices here, not only a local path." \
  --title "Review needed" \
  --parse-mode Markdown
```

Send a prepared file:

```bash
source /Users/kenjipcx/.codex/private/telegram.env
MESSAGE_FILE="/absolute/path/to/feedback-request.md"
python3 skills/notify/scripts/send_message.py \
  --thread-id "${CODEX_THREAD_ID:?CODEX_THREAD_ID required for reply routing}" \
  --file "$MESSAGE_FILE" \
  --title "Feedback request" \
  --parse-mode Markdown
```

Send a visual approval packet:

```bash
source /Users/kenjipcx/.codex/private/telegram.env
python3 skills/notify/scripts/send_message.py \
  --thread-id "${CODEX_THREAD_ID:?CODEX_THREAD_ID required}" \
  --photo "/absolute/path/to/approval-sheet.png" \
  --file "/absolute/path/to/approval-caption.txt" \
  --title "Visual approval" \
  --parse-mode none
```
