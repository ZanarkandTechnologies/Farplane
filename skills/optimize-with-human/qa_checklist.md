---
title: "Optimize With Human QA Checklist"
owner: optimize-with-human
status: active
kind: qa-checklist
created_at: 2026-06-27
---

# Optimize With Human QA Checklist

Use this checklist before pausing, stopping, or handing off a human-feedback
optimization turn.

```text
optimize_with_human_qa(goal_packet, artifact_refs, notification_result)
  -> pass | fail | blocked
```

## Preflight

1. `reply_path_bound`
   - Pass: the current context is the worker thread that should receive
     Telegram replies, or `worker_thread_ref` is explicit.
   - Fail: the parent heartbeat sends a feedback request that should resume a
     different worker.

2. `artifact_reviewable`
   - Pass: the request includes an artifact URL, screenshot, file, preview, or
     clear blocker.
   - Fail: Kenji is asked to judge a summary, plan, skill name, or local-only
     URL that is not usable on the intended device.

3. `phone_friendly_surface`
   - Pass: visual or website feedback includes a public/mobile-viewable URL,
     attached screenshot, Farplane UI-ready preview, or explicit fallback.
   - Fail: the only feedback surface is `localhost` or an inaccessible local
     path.

4. `question_is_small`
   - Pass: the request asks one compact decision, rating, ranking, label, or
     taste note.
   - Fail: the request asks for broad strategy, multiple unrelated decisions,
     or a prompt Kenji must invent from scratch.

5. `feedback_schema_bound`
   - Pass: the request names how verdict/score/feedback/labels/next instruction
     will be recorded.
   - Fail: the loop cannot tell how to use the feedback after it arrives.

## Final Review

1. `telegram_or_fallback_sent`
   - Pass: if waiting for feedback, a `telegram-message` send succeeded, or a
     visible fallback/blocker is recorded.
   - Fail: the worker stops while expecting feedback but sent no usable request.

2. `post_feedback_exit_gate`
   - Pass: after non-terminal feedback, the worker produced a next artifact and
     sent the next Telegram request, or sent a blocker.
   - Fail: the worker patched files or generated work after feedback and then
     went quiet.

3. `progress_logged`
   - Pass: `progress.md` records the request, message status, feedback received,
     next action, or terminal reason.
   - Fail: the thread state exists only in chat.

4. `terminal_reason_clear`
   - Pass: terminal stops name `keep`, `approve`, `convergence`, `budget`, or
     `blocker`.
   - Fail: the loop claims completion without a terminal reason.
