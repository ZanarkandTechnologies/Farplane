---
title: Feedback Acknowledgement Next Step
owner: taste-loop
status: active
kind: audit
created_at: 2026-06-29
---

# Feedback Acknowledgement Next Step

## Trigger

Kenji replied to an earlier TL-EXP-003 Telegram reminder with confusion about
whether the artifact was a video, product, inner skill, or idea. The worker
response correctly treated the message as `revise` feedback, but then stopped
after acknowledgement:

- it clarified that the artifact was a `social-content:twitter-thread`
  planning proposal for Pocket Intern;
- it recorded that no social thread should be drafted;
- it did not ask for the next instruction or send a revised review request.

## Root Cause

The existing Taste Loop and optimize-with-human contracts covered feedback
request quality, feedback logging, and stale reminders. They did not explicitly
define the Telegram acknowledgement contract after fresh `revise` or `reject`
feedback. That left a worker free to send a true but terminal-sounding response
even when the loop still needed operator direction.

## Change

- `optimize-with-human/SKILL.md` now requires non-terminal fresh feedback to
  either send the next review request or ask for the next instruction.
- `taste-loop/SKILL.md` and `templates/heartbeat-prompt.md` now require workers
  to restate the corrected review object and continue after `revise`/`reject`.
- `telegram-message/qa_checklist.md` now rejects acknowledgement-only replies
  unless the loop is terminal.
- `taste-loop/eval_task.json` and `telegram-message/eval_task.json` now include
  regression points for this behavior.

## Expected Behavior

For non-terminal `revise` or `reject` feedback, the Telegram reply should have
this shape:

```text
Recorded as revise.

Clarified review object:
- Review artifact: social-thread premise / customer-facing idea
- Skill/workflow: social-content -> Twitter/X thread planning
- Product: AGI Toy Shop / Pocket Intern
- Stage: planning only
- Not judging: video, product build, final copy, or external posting

Next: should I revise the request using that framing, switch artifacts, or stop
this experiment?
```

## Verification

Run:

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
```
