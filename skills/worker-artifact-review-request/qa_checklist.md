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
- [ ] `feedback_policy_bound`: The request records
  `feedback_channel=telegram`, `feedback_policy=ask_when_artifact_ready`, and
  `worker_thread_ref` when Kenji's reply should continue the worker thread.
- [ ] `no_secrets`: No tokens, credentials, private unrelated data, or unsafe
  command output appears in the message or receipt.
- [ ] `side_effect_boundary`: The message explicitly does not approve posting,
  publishing, spending, deploying, contacting externals, or account mutation.
- [ ] `no_duplicate_spam`: If a recent review request exists for the same
  artifact, the packet records why another reminder is necessary or skips it.
- [ ] `phone_chaser_escalation`: Phone escalation is used only after an
  unanswered Telegram review request or urgent Kenji-facing blocker, asks for
  one concrete action, and records a sanitized dispatch receipt or blocker.
- [ ] `turn_exit_gate`: A waiting worker records a Telegram message id, or a
  concrete blocker proving why Telegram could not be sent; a non-terminal
  feedback turn sends the next review request or blocker before stopping.
- [ ] `review_cycle_logged`: The caller-owned state records artifact refs,
  human question, expected signal, feedback channel/policy, route thread,
  Telegram status, and next action after reply.
- [ ] `receipt`: The caller-owned ticket/progress/report surface records sent,
  blocked, skipped status, or phone-chaser escalation plus message id,
  dispatch id, blocker, or fallback ref.

## Reviewer Prompt

```text
Review the worker artifact review packet against
skills/worker-artifact-review-request/qa_checklist.md and
skills/telegram-message/qa_checklist.md. If phone escalation is used, also
apply skills/phone-chaser/qa_checklist.md.

Return only failed checks, smallest required fixes, and whether the request is
safe to send or should be recorded as fallback.
```
