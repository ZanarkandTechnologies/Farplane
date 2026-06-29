---
skill: taste-loop
kind: skill-maintenance-audit
mode: harden_skill
created_at: 2026-06-28
status: draft
evidence:
  - tickets/TASK-0240/ticket.md
  - tickets/TASK-0240/progress.md
  - tickets/TASK-0240/artifacts/telegram-message-TL-EXP-003.txt
---

# Worker Visibility And Reminder Hardening

## Behavior Delta

Expected: Taste Loop should not claim a worker is waiting for feedback unless
the worker thread is app-visible, searchable, and has verified send/fallback
proof. When feedback is stale, it should send a bounded phone-viewable reminder
from the visible worker thread.

Observed: TASK-0240 recorded replacement worker
`019f09c4-ecda-7423-a80c-7ab5a8e53788` and `TL-EXP-003` as waiting for feedback,
but Codex app thread search did not find that worker by id or title. The
existing Taste Loop contract also lacked reminder behavior for stale waiting
feedback.

## Changes

- Added `worker_thread_visible_or_blocked` and
  `stale_feedback_reminded_or_deferred` gates to `SKILL.md`.
- Added a `Feedback Reminder Contract` with reminder interval, max reminders,
  phone-viewable message requirement, and progress/memory writeback.
- Updated the heartbeat prompt and `farplane/automations.md` so worker titles
  include ticket/workflow/experiment, waiting state requires visibility proof,
  and stale feedback triggers a bounded reminder.
- Added eval reference points for phantom worker prevention and reminder
  behavior.
- Marked TASK-0240 blocked until `TL-EXP-003` is recovered through a visible
  worker thread and verified send or fallback proof.

## QA Notes

- Source owner preserved: repo-owned `skills/taste-loop`, not installed copy.
- First-load behavior changed because worker visibility and reminders are
  normal-path safety gates.
- Reminder behavior is bounded by `reminder_after_hours` and
  `max_reminders_per_feedback`; it is not a hidden daemon.
- Installed copy must be refreshed after validation before judging live
  automation behavior.
