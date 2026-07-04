---
name: worker-artifact-review-request
description: "Turn completed worker artifacts into Telegram-ready Kenji review requests with archive-safe refs, reply routing, and a durable receipt."
tier: 2
source: local
template_uses:
  skill-template: "0.3.7"
  skill-qa-checklist: "0.1.0"
  skill-eval-task: "0.1.0"
allowed-tools: Read, Bash
eval: eval_task.json
qa_checklist: qa_checklist.md
---

# Worker Artifact Review Request

## Context

Use this skill when a worker has produced a local artifact, proof packet,
draft, demo, report, storyboard, rendered asset, or reviewable prep packet and
Kenji should review it from Telegram. This is a thin wrapper around
[telegram-message](../telegram-message/SKILL.md) for completed worker outputs.
It does not create a new approval queue, publish/post/spend/deploy/contact
externals, or grant permission for final gated actions.
When a prior Telegram artifact-review request is unanswered past the caller's
configured chase window, this skill may escalate to
[phone-chaser](../phone-chaser/SKILL.md) with a short Kenji-facing reminder
that asks for one reply action. Phone escalation is for ignored review pings or
urgent blockers, not for first-contact review requests.

The review request must be useful on a phone. If the only artifact reference is
a local path, include the essential summary, excerpt, options, or conclusion in
the Telegram body and keep the path as a desktop-only reference. If the content
is too large to summarize honestly, record a fallback instead of sending a
local-path-only message.

## Skill Signature

```text
worker_artifact_review_request(ticket, artifacts, worker_thread_ref,
                               review_question?, state?)
  -> feedback_request_ref + sent_message_or_fallback + progress_receipt

state:
  reads(ticket.md, artifact files, worker thread/handoff row?,
        qa_checklist.md, ../telegram-message/SKILL.md,
        ../telegram-message/qa_checklist.md,
        ../phone-chaser/SKILL.md when escalating unanswered Telegram,
        ../phone-chaser/qa_checklist.md when escalating unanswered Telegram)
  writes(optional ticket/progress receipt, review-cycle entry, or fallback file
         chosen by caller)

gates:
  feedback_policy_ask_when_artifact_ready; worker_thread_ref_bound;
  artifacts_exist; archive_safe_refs; phone_readable_summary;
  one_reply_action; telegram_send_attempted_or_blocker_recorded;
  no_secrets; no_external_side_effect_permission; receipt_recorded;
  turn_exit_gate_satisfied;
  phone_chaser_only_after_unanswered_telegram_or_urgent_blocker

routes:
  telegram-message | phone-chaser for unanswered Telegram escalation |
  optimize-with-human when the next loop optimizes human taste

fails:
  local_path_only_review; giant_report_dump; vague_reply_action;
  duplicate_review_spam; treating notification as publish/spend/deploy approval;
  no message id or fallback receipt; phone call without explicit Kenji-facing
  chase intent; worker stops waiting for Kenji without Telegram sent or blocker
```

## Phase Boundary

This skill follows Tier 0 phases inline. It borrows the `optimize-with-human`
turn-exit pattern for artifact review: when a worker needs Kenji's judgment,
the worker must bind the reply path, send the Telegram request, and write the
receipt before stopping. Use an independent reviewer only for sensitive,
automated, repeated, or high-risk notification failures.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the review packet.
  - [ ] Identify the ticket, worker thread/session ref, produced artifacts,
        review question, and final human gate if any.
  - [ ] Bind `feedback_channel=telegram`,
        `feedback_policy=ask_when_artifact_ready`, and
        `metric_provider=human_review` when the worker is waiting on Kenji.
  - [ ] Confirm the current context is the worker thread that should receive
        Telegram replies, or pass explicit `worker_thread_ref`.
  - [ ] Read `qa_checklist.md` before drafting the message.
  - [ ] Read `telegram-message/SKILL.md` and its `qa_checklist.md` when sending
        or reporting a send fallback.
- [ ] 2. Validate artifact refs.
  - [ ] Confirm each artifact exists or has a phone-openable URL.
  - [ ] Mark local filesystem paths as desktop-only and include enough inline
        content for Telegram review.
  - [ ] Do not expose secrets, tokens, credentials, or private unrelated data.
- [ ] 3. Draft a phone-readable request.
  - [ ] Start with ticket, artifact type, and why this matters now.
  - [ ] Include the smallest honest summary: hypothesis/method/result for
        experiments, claim/baseline/result for ablations, or hook/script/visual
        summary for content.
  - [ ] Ask one clear reply action: approve, revise, reject, choose A/B/C, or
        answer one named question.
  - [ ] State that publishing/posting/spend/deploy/external-contact still
        requires separate approval when relevant.
- [ ] 4. Send or record fallback.
  - [ ] Use `telegram-message` for the actual send when route target and
        credentials are available; do not treat a local fallback as equivalent
        when Telegram can be attempted.
  - [ ] If a previous Telegram review request is unanswered beyond the caller's
        configured chase window, use `phone-chaser` with one short action
        request and record the dispatch receipt or blocker.
  - [ ] If Telegram cannot be sent or the artifact is not phone-reviewable,
        record a fallback with exact blocker, evidence that the send route or
        review surface failed, and next repair.
  - [ ] Avoid duplicate reminder spam; include last notification if visible.
- [ ] 5. Write the receipt.
  - [ ] Record sent/skipped/blocked, Telegram message id or fallback path,
        worker thread ref, artifact refs, and requested reply action in the
        caller's ticket/progress/report surface.
  - [ ] Append or update a review-cycle entry before stopping:
        artifact refs, human question, expected signal, Telegram status,
        message id or blocker, and next action after reply.
  - [ ] Satisfy the turn exit gate: waiting workers must have a Telegram
        message id or explicit blocker; non-terminal feedback turns must send
        the next review request or blocker; terminal turns must record the
        terminal reason.
  - [ ] Apply `qa_checklist.md` again before declaring the request ready.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Turn Exit Gate

Before a worker stops while Kenji's judgment is needed, satisfy exactly one
exit:

```text
waiting_for_review:
  telegram_message_sent == true
  and telegram_message_id is recorded
  and worker_thread_ref is the reply route
  or blocker_ref explains why Telegram could not be sent

review_processed_non_terminal:
  next_artifact_ref is visible
  and next_review_request_sent == true
  or blocker_ref explains why the next artifact/request cannot be produced

terminal:
  terminal_reason in [approve, accept, reject, revise_complete, blocker]
  and ticket/progress/report state records the decision
```

This mirrors `optimize-with-human`: a worker must not go quiet after producing
an artifact or after processing Kenji feedback. If the worker changes an
artifact in response to `revise` or `reject`, it must send the next Telegram
review request or a blocker that tells Kenji what is needed next.

## Review Cycle Contract

Record this shape in the caller-owned ticket, progress file, or report before
stopping:

```yaml
worker_artifact_review_cycle:
  phase: planning | execution | completion
  artifact_refs:
    - path:
      role:
  human_question:
  expected_signal: approve | accept | revise | reject | choose | answer
  worker_thread_ref:
  feedback_channel: telegram
  feedback_policy: ask_when_artifact_ready
  telegram:
    status: sent | blocked | skipped_duplicate
    message_id:
    blocker:
  next_after_reply:
```

## Templates

Artifact review request:

```text
*{ticket}: {artifact title}*

*Why review now:* {one sentence}
*Artifact:* {type + one-line result}
*Summary:* {phone-readable decision content}
*Desktop ref:* {absolute or repo path marked desktop-only}

*Reply with:* approve, revise, or reject + one short reason.
*Boundary:* This does not approve {post/publish/spend/deploy/etc.}; that stays gated.
```

Receipt:

```yaml
worker_artifact_review:
  status: sent | blocked | skipped_duplicate
  ticket:
  worker_thread_ref:
  artifacts:
  requested_reply:
  telegram_message_id:
  phone_chaser_dispatch_id:
  fallback_ref:
  blocker:
```

Phone chaser escalation:

```text
Kenji. {ticket} is waiting on your review after an unanswered Telegram. Reply
{approve/revise/reject/choose A or B} in the worker thread so Pulse can move.
```

## Gotchas

- Do not send a Telegram message that only says "review this path".
- Do not paste the full artifact when a short result, choice, or excerpt is the
  actual review surface.
- Do not treat a Telegram review request as permission to publish, post, spend,
  deploy, contact anyone, or mutate an external account.
- Do not create a separate approval queue when the open worker thread can own
  Kenji's reply.
- Do not stop a worker as "waiting for Kenji" unless the turn exit gate has a
  Telegram message id or a concrete blocker proving why Telegram could not be
  sent.

## Reference Map

- [../telegram-message/SKILL.md](../telegram-message/SKILL.md) - load when
  sending or recording a send fallback.
- [../telegram-message/qa_checklist.md](../telegram-message/qa_checklist.md) -
  load with Telegram Message for phone readability, route target, and side
  effect safety.
- [qa_checklist.md](qa_checklist.md) - read at start and finish for this
  wrapper's artifact-review guardrails.

## Output

- A Telegram send result with message id, or a fallback/blocker receipt.
- A caller-owned progress/ticket/report receipt linking the artifact refs and
  requested reply action.
