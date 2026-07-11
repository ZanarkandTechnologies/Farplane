---
name: worker-artifact-review-request
description: "Turn a ticket artifact into an initial or due Telegram review request, then write worker-free review state."
tier: 2
source: local
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
Pulse may call this skill for the first due reminder without assigning an
execution worker. Review WIP is planning backpressure, not a reminder trigger.
Phone escalation remains an explicit operator/automation decision routed to
`phone-chaser`; this skill does not infer it from queue size.

## Skill Signature

```text
worker_artifact_review_request(ticket, artifacts, thread_ref,
                               review_question, mode = initial | reminder,
                               review_state?)
  -> send_receipt + progress_delta + ticket_delta

state:
  reads(ticket.md, artifacts, progress.md?,
        farplane/bindings.yaml#operator.review_chase_policy?,
        telegram-message/SKILL.md, qa_checklist.md)
  writes(progress.md Review block, ticket status/claim, send receipt)

gates:
  artifacts_exist; archive_safe_refs; phone_readable_summary;
  one_reply_action; reply_thread_bound; no_duplicate_send;
  reminder_is_due_when_mode=reminder; no_secrets;
  no_external_action_permission; receipt_recorded

fails:
  local_path_only_review; vague_reply_action; queue_size_as_chase_trigger;
  worker_reserved_while_waiting; repeated_not_due_reminder;
  notification_treated_as_final-action approval
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the review packet.
  - [ ] Read the ticket, artifact, `progress.md`, review question, thread ref,
        final human gate, and `qa_checklist.md`.
  - [ ] Read `telegram-message/SKILL.md` and its checklist before sending.
  - [ ] For `mode=reminder`, require an undecided Review block whose
        `next_reminder_at` is due; otherwise return `skipped_not_due`.
- [ ] 2. Validate the review surface.
  - [ ] Confirm artifact refs exist or are phone-openable.
  - [ ] Mark local paths desktop-only and include the smallest honest inline
        summary, excerpt, result, or options.
  - [ ] Ask exactly one reply action and preserve external-action gates.
- [ ] 3. Send once and write state.
  - [ ] Send through Telegram or record an exact fallback/blocker.
  - [ ] For an initial request, write the Review block below, set
        `status: awaiting_review`, clear `claimed_by`, and release the worker.
  - [ ] For a reminder, increment `reminder_count`, record the send receipt,
        and set the next configured reminder time or clear it when capped.
  - [ ] Apply `qa_checklist.md` again before returning.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Review State

The mutable review ledger lives in `progress.md`, not ticket frontmatter:

```yaml
## Review

artifact_refs:
  - tickets/TASK-XXXX/artifacts/example.md
thread_ref: codex-thread-ref
requested_at: 2026-07-11T12:00:00Z
next_reminder_at: 2026-07-12T12:00:00Z
reminder_count: 0
escalation_used: false
decision:
```

When a direct Telegram reply wakes the bound thread, that thread records the
decision, changes status to `active`, `done`, or `rejected`, and continues or
closes the ticket. The inactive persistent thread and awaiting ticket are not
workers. Only an active execution turn consumes worker capacity.

## Request Shape

```text
*{ticket}: {artifact title}*

*Why review now:* {one sentence}
*Result:* {phone-readable decision content}
*Desktop ref:* {path, explicitly desktop-only}

*Reply with:* approve, revise, or reject + one short reason.
*Boundary:* This does not approve {post/publish/spend/deploy/etc.}.
```

```yaml
worker_artifact_review:
  mode: initial | reminder
  status: sent | blocked | skipped_duplicate | skipped_not_due
  ticket:
  thread_ref:
  artifacts: []
  requested_reply:
  telegram_message_id:
  fallback_ref:
  blocker:
```

## Gotchas

- Do not send a local-path-only review request.
- Do not keep a worker alive after the request is recorded.
- Do not derive reminders from review queue length.
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
- Initial ticket transition to `awaiting_review` with no live claim, or reminder
  ledger update with no worker assignment.
