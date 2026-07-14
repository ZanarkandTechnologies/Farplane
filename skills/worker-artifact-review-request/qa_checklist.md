---
title: Worker Artifact Review Request QA
owner: worker-artifact-review-request
status: active
kind: qa-checklist
applies_to:
  - worker-artifact-reviews
  - telegram-review-requests
  - pulse-worker-handoffs
---

# Worker Artifact Review Request QA

Use this checklist before drafting the request and again before sending or
recording fallback.

```text
worker_artifact_review_request_check(packet, artifacts, route, receipt?)
  -> pass | violation | deferral
```

## Checks

- [ ] `artifact_exists_or_summary_available`: Every artifact exists, has a
  phone-openable URL, or has enough inline summary/excerpt for Telegram review.
- [ ] `archive_safe_refs`: Artifact refs are stable repo/ticket/archive-safe
  paths or URLs; local paths are labeled desktop-only.
- [ ] `phone_readable`: The message explains what changed, why it matters, and
  the reviewable substance without requiring desktop access.
- [ ] `one_reply_action`: Kenji can answer with one clear action such as
  approve, revise, reject, or A/B/C plus a short reason.
- [ ] `reply_route`: A thread/session route target exists, or fallback is
  recorded with the exact missing route/credential.
- [ ] `review_state_bound`: The request records artifact refs, thread ref,
  request time, Telegram status/message id, reminder count with matching
  reminder message ids, Phone Chaser count/dispatch ids/last dispatch time, and decision in the
  ticket-owned `progress.md` Review block.
- [ ] `no_secrets`: No tokens, credentials, private unrelated data, or unsafe
  command output appears in the message or receipt.
- [ ] `side_effect_boundary`: The message explicitly does not approve posting,
  publishing, spending, deploying, contacting externals, or account mutation.
- [ ] `no_duplicate_spam`: If a recent review request exists for the same
  artifact, the packet records why another reminder is necessary or skips it.
- [ ] `policy_action_only`: Reminder or Phone Chaser mode runs only when Pulse
  selected that exact action from structured turn thresholds, active hours,
  and caps; review queue size never triggers a chase.
- [ ] `automation_notification_authority`: Ticket-local no-credential,
  no-publication, or no-account-mutation scope does not suppress internal
  review notification credentials, and notification grants no broader action.
- [ ] `worker_released`: Initial request records a Telegram message id or
  blocker, sets `status: awaiting_review`, clears `claimed_by`, and releases
  the execution worker.
- [ ] `review_cycle_logged`: The caller-owned state records artifact refs,
  human question, route thread, Telegram status, reminder state, and decision.
- [ ] `receipt`: The caller-owned ticket/progress/report surface records sent,
  blocked, skipped status, or reminder plus message id, blocker, or fallback ref.

## Reviewer Prompt

```text
Review the worker artifact review packet against
skills/worker-artifact-review-request/qa_checklist.md and
skills/telegram-message/qa_checklist.md.

Return only failed checks, smallest required fixes, and whether the request is
safe to send or should be recorded as fallback.
```
