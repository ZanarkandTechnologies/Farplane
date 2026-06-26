---
kind: goal-program
ticket_id: TASK-0236
owner: taste-loop
status: active
created_at: 2026-06-26T21:34:52+08:00
---

# TASK-0236 Program

## Loop Shape

```text
artifact_worker_thread(ticket, program, progress, worker_thread)
  -> artifact_attempt
   + optimize_with_human_feedback_request
   + feedback_driven_revision
```

## Files

- `tickets/TASK-0236/ticket.md`
- `tickets/TASK-0236/program.md`
- `tickets/TASK-0236/progress.md`
- `farplane/products.md`
- `skills/landing-page/SKILL.md`
- `skills/optimize-with-human/SKILL.md`

## Selected Workflow

```text
product_lane: trust_distribution
workflow_id: landing_page_offer
owner: landing-page
reviewable_artifact: landing page draft, HTML, screenshot, or private preview
feedback_question: keep / revise / reject the offer and page direction
```

## Worker Instructions

1. Read the files listed above.
2. Use `$landing-page` to create or revise one Farplane landing-page artifact.
3. Make the artifact reviewable on a phone:
   - preferred: public/mobile-viewable private preview URL;
   - acceptable fallback: screenshot or image evidence in Markdown;
   - local-only localhost URL is smoke proof only, not the sole Telegram review
     surface.
4. Use `$optimize-with-human` with:

```text
target = "trust_distribution / landing_page_offer"
objective = "make the Farplane landing page offer sharper, more believable, and easier to keep/revise/reject quickly"
channel = telegram
feedback_policy = ask_when_artifact_ready
worker_thread_ref = current Codex thread
feedback_type = decision
question = "keep / revise / reject the offer and page direction?"
```

5. Send Kenji a short Telegram feedback request from this worker context.
6. When Kenji replies in this thread, append the feedback to `progress.md`,
   revise the artifact, and ask again only when the next version is ready.

## Budget

- Artifact attempts: 3
- Worker thread: 1
- Human questions per attempt: 1
- Spend/publish/customer contact: none
- External deploy: only if a private preview path is already configured and no
  new account, spend, or public launch is involved

## Stop Conditions

- Stop as complete when Kenji replies `keep`, `approve`, or equivalent and the
  accepted artifact ref is recorded.
- Stop as paused when waiting for Kenji feedback after a valid review request.
- Stop as blocked when no phone-viewable evidence can be produced.
- Stop as budget exhausted after 3 artifact attempts.

## Progress Policy

Append one compact entry to `progress.md` for:

- worker thread creation;
- artifact attempt;
- Telegram request;
- feedback received;
- revision decision;
- blocker or completion.
