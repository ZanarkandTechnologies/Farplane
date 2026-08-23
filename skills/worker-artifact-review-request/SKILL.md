---
name: worker-artifact-review-request
description: "Turn a ticket artifact into an initial or due Telegram review request, then write worker-free review state."
tier: 2
source: local
capability:
  kind: integration
template_uses:
  skill-template: "0.3.7"
  skill-qa-checklist: "0.1.0"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Bash
eval: evals/evals.json
qa_checklist: qa_checklist.md
---

# Worker Artifact Review Request

## Context

Use this skill when a ticket has a reviewable artifact or Work Pulse has
selected one due reminder from an existing review ledger. It is a thin wrapper
around [telegram-message](../telegram-message/SKILL.md). It does not create an
approval queue, reserve a worker while waiting, or grant authority to post,
publish, spend, deploy, contact externals, or mutate accounts.

The initial artifact-producing turn sends once, writes `progress.md`, changes
the ticket to `status: awaiting_review`, clears `claimed_by`, and exits. A later
Pulse may call this skill for a policy-derived Telegram reminder or Phone
Chaser escalation without assigning an execution worker. Review WIP is
planning backpressure, not a reminder trigger. The structured
`farplane/bindings.yaml#operator.review_chase_policy` is the explicit automation
decision: it owns bounded turn thresholds, active hours, caps, and notification
authority. This skill never infers escalation from queue size.

Telegram review delivery is an internal automation side effect. A worker
ticket's `no credentials`, `no publication`, or `no account mutation` boundary
does not prohibit the review wrapper from using automation-owned Telegram or
Phone Chaser credentials. Those notifications grant no authority to publish,
contact customers, spend, deploy, or mutate public accounts.

## Skill Signature

```text
worker_artifact_review_request(ticket, artifacts, thread_ref,
                               review_question, original_source_url,
                               mode = initial | reminder | phone_escalation,
                               review_state?)
  -> send_receipt + progress_delta + ticket_delta

state:
  reads(ticket.md, artifacts, progress.md?,
        farplane/bindings.yaml#operator.review_chase_policy?,
        telegram-message/SKILL.md, qa_checklist.md)
  writes(progress.md Review block, ticket status/claim, send receipt)

gates:
  artifacts_exist; archive_safe_refs; phone_readable_summary;
  original_source_phone_openable;
  visual_artifact_has_image; visual_delivery_receipt_is_photo;
  one_reply_action; reply_thread_bound; no_duplicate_send;
  policy_action_is_due_when_mode!=initial; no_secrets;
  no_external_action_permission; receipt_recorded

fails:
  local_path_only_review; missing_original_source_link; vague_reply_action;
  duplicated_message_copy; queue_size_as_chase_trigger;
  text_only_visual_review; awaiting_review_without_required_media;
  worker_reserved_while_waiting; repeated_not_due_reminder;
  phone_escalation_outside_policy;
  notification_treated_as_final-action approval
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the review packet.
  - [ ] Read the ticket, artifact, `progress.md`, review question, thread ref,
        final human gate, and `qa_checklist.md`.
  - [ ] Read `telegram-message/SKILL.md` and its checklist before sending.
  - [ ] Resolve one phone-openable `original_source_url` for the original task,
        brief, proposal, or source page. For reminders, reuse it from the Review
        block; do not reconstruct it from a local path.
  - [ ] For `mode=reminder` or `phone_escalation`, require the exact due action
        selected by Pulse from the structured chase policy; otherwise return
        `skipped_not_due`.
- [ ] 2. Validate the review surface.
  - [ ] Confirm artifact refs exist or are phone-openable.
  - [ ] If the artifact or decision is visual, require a real PNG/JPEG review
        image and inspect its dimensions before delivery. Markdown is draft
        support only.
  - [ ] Mark local paths desktop-only and include the smallest honest inline
        summary, excerpt, result, or options.
  - [ ] Pass the review facts, original source URL, artifact refs, and media
        paths to `telegram-message`; let that skill own the human-facing prose.
  - [ ] Ask exactly one reply action and preserve external-action gates.
- [ ] 3. Send once and write state.
  - [ ] Send the initial request through Telegram or record an exact transport
        blocker. Do not treat ticket-local credential restrictions as a
        notification blocker.
  - [ ] For visual review, send the image through `telegram-message --photo`
        and require a photo message receipt. Until then keep the producer state
        at `storyboard_draft_ready` (or equivalent), never `awaiting_review`.
  - [ ] For an initial request, write the Review block below, set
        `status: awaiting_review`, clear `claimed_by`, and release the worker.
  - [ ] For a Telegram reminder, increment `reminder_count` and record the
        send receipt. For phone escalation, call `phone-chaser`, increment
        `phone_chaser_count`, and record its sanitized dispatch receipt or
        blocker. Never perform more than the policy-selected action.
  - [ ] Apply `qa_checklist.md` again before returning.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Review State

The mutable review ledger lives in `progress.md`, not ticket frontmatter:

```yaml
## Review

artifact_refs:
  - tickets/TASK-XXXX/artifacts/example.md
original_source_url: https://phone-openable.example/tasks/TASK-XXXX
thread_ref: codex-thread-ref
requested_at: 2026-07-11T12:00:00Z
telegram_status: sent
telegram_message_id: telegram-message-id
telegram_delivery_kind: photo
reminder_count: 0
telegram_reminder_message_ids: []
phone_chaser_count: 0
phone_chaser_dispatch_ids: []
last_phone_chaser_at:
decision:
```

When a direct Telegram reply wakes the bound thread, that thread records the
decision, changes status to `active`, `done`, or `rejected`, and continues or
closes the ticket. The inactive persistent thread and awaiting ticket are not
workers. Only an active execution turn consumes worker capacity.

## Message Input Packet

This wrapper supplies facts and state. `telegram-message` owns the final copy
and its gold-message calibration.

```yaml
message_intent: review_request | blocker
original_source_url: https://phone-openable.example/tasks/TASK-XXXX
message_body_facts:
  context:
  result_or_blocker:
  stakes:
  review_focus:
  recommendation:
  deadline:
  consequence_if_unanswered:
requested_reply:
artifact_refs: []
media_paths: []
```

```yaml
worker_artifact_review:
  mode: initial | reminder | phone_escalation
  status: sent | blocked | skipped_duplicate | skipped_not_due
  ticket:
  thread_ref:
  original_source_url:
  artifacts: []
  requested_reply:
  telegram_message_id:
  telegram_delivery_kind: text | photo
  fallback_ref:
  blocker:
```

## Gotchas

- Do not send a local-path-only review request.
- Do not promote visual work to `awaiting_review` from prose, Markdown, or a
  text-message receipt. The image file and photo receipt are mandatory.
- Do not keep a worker alive after the request is recorded.
- Do not derive reminders from review queue length.
- Do not let a ticket-local credential boundary suppress automation-owned
  review notifications.
- Do not dispatch Phone Chaser outside configured thresholds, active hours,
  recipient boundaries, receipt-backed repeat intervals, or caps.
- Do not create child review tickets; the original ticket and progress ledger
  own the decision.
- Do not confuse human artifact review with a delayed market/metric check-in
  unless human feedback is explicitly the experiment reward.

## Reference Map

- [telegram-message](../telegram-message/SKILL.md) - delivery and phone-readable
  message rules.
- [pulse-update](../pulse-update/SKILL.md) - chooses at most one due reminder
  and dispatches due signal check-ins.
- [qa_checklist.md](qa_checklist.md) - start/finish guardrail.

## Output

- Telegram send/fallback receipt.
- Updated `progress.md` Review state.
- Initial ticket transition to `awaiting_review` with no live claim, or bounded
  Telegram/phone ledger update with no worker assignment.
