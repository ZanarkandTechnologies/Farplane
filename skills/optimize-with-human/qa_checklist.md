---
title: "Optimize With Human QA Checklist"
owner: optimize-with-human
status: active
kind: qa-checklist
created_at: 2026-06-27
updated_at: 2026-07-31
---

# Optimize With Human QA Checklist

Use this checklist before pausing, stopping, or handing off a human-feedback
optimization turn.

```text
optimize_with_human_qa(goal_packet, phase, artifact_refs, notification_result)
  -> pass | fail | blocked
```

## Preflight

1. `goal_packet_present`
   - Pass: `ticket.md`, `program.md`, and `progress.md` are present or named
     before a feedback request is sent; multi-turn experiment-backed packets
     also name `hypothesis-tree.json`.
   - Fail: the loop relies on chat memory or a standalone Telegram request.

2. `phase_bound`
   - Pass: the request names `phase=planning` or `phase=execution`.
   - Fail: the loop does not know whether it is asking for idea feedback or
     execution feedback.

3. `execution_has_approved_plan`
   - Pass: execution feedback includes `approved_plan_ref`, or the artifact is
     explicitly a tiny planning test.
   - Fail: the loop spends execution work without an approved concept, brief,
     or plan reference.

4. `experiment_proposal_logged`
   - Pass: the selected hypothesis is current in `hypothesis-tree.json` when
     enabled, and `progress.md` has its proposal receipt with phase, skill delta
     candidate, rollout batch, and expected feedback before the request goes out.
   - Fail: the worker asks for feedback before recording what it is testing.

5. `reply_path_bound`
   - Pass: the current context is the worker thread that should receive
     Telegram replies, or `worker_thread_ref` is explicit.
   - Fail: the parent heartbeat sends a feedback request that should resume a
     different worker.

6. `artifact_reviewable`
   - Pass: the request includes an artifact URL, screenshot, file, preview, or
     clear blocker.
   - Fail: Kenji is asked to judge a summary, plan, skill name, or local-only
     URL that is not usable on the intended device.

7. `planning_proposal_sufficient`
   - Pass: non-trivial planning feedback includes audience/buyer, taste insight,
     artifact shape, core angle, execution beats, why it could win, cringe
     risks, references or taste pack, feedback question, and next step if
     approved.
   - Fail: Kenji is asked to choose from only titles, hooks, or shallow angles
     when the artifact needs a real proposal.

8. `phone_friendly_surface`
   - Pass: visual or website feedback includes a public/mobile-viewable URL,
     attached screenshot, Farplane UI-ready preview, or explicit fallback.
   - Fail: the only feedback surface is `localhost` or an inaccessible local
     path.

9. `question_is_small`
   - Pass: the request asks one compact decision, rating, ranking, label, or
     taste note.
   - Fail: the request asks for broad strategy, multiple unrelated decisions,
     or a prompt Kenji must invent from scratch.

10. `feedback_schema_bound`
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

4. `experiment_result_logged`
   - Pass: after feedback, the tree node is updated first when enabled, and the
     follow-up progress entry records verdict, result, tree mutation, next phase
     action, and promotion decision.
   - Fail: the loop records only that a message was sent.

5. `skill_promotion_guard`
   - Pass: first rejection keeps changes local, reruns, or discards; source
     skill hardening is only proposed after repeated same-phase failures or a
     reusable approved pattern.
   - Fail: the worker edits a skill, prompt, or template directly from one
     rejection.

6. `terminal_reason_clear`
   - Pass: terminal stops name `keep`, `approve`, `convergence`, `budget`, or
     `blocker`.
   - Fail: the loop claims completion without a terminal reason.

7. `tree_selection_is_lean`
   - Pass: experiment-backed loops use one ordinal compounding-leverage choice,
     no tournament or persisted rank; human variant ranking remains only an
     observation inside a selected experiment.
   - Fail: the feedback variants become a second hypothesis-selection engine.
