---
name: hitl-autoresearch
description: "Turn subjective artifact goals into human-in-the-loop autoresearch sessions with feedback requests, scoring, and resumable review."
tier: 3
group: self-improvement
source: local
allowed-tools: Read, Write, Grep, Glob, Bash
---

# HITL Autoresearch

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Identify the artifact family and short-horizon reviewable outcome.
- [ ] Choose the human feedback metric: usually `human_score` 0-10, higher is
  better.
- [ ] Write a single review question Kenji can answer quickly.
- [ ] Scaffold session files with `scripts/init_hitl_session.py`.
- [ ] Generate artifacts under `outputs/run-N/`.
- [ ] Write `feedback-request.md` with artifact paths, review question, and the
  expected `feedback.json` shape.
- [ ] Use the `telegram-message` primitive to notify Telegram when configured;
  otherwise report the local feedback request path.
- [ ] Stop cleanly while waiting for `feedback.json`; do not pretend the metric
  is available.
- [ ] Resume from `feedback.json`, keep/discard/revise, and log the result.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this skill when the operator wants agents to iterate on subjective
artifacts with fast human feedback, especially:

- marketing variants
- landing pages, banners, screenshots, demo videos, and scripts
- demo packaging
- outreach angles
- content hooks
- UI or visual options where Kenji wants to be online and give feedback

This is not for fully mechanical code metrics. Use `autoresearch-plan` directly
when the metric is already numeric and can run unattended. Use `goal-crafter`
when the task needs a native `/goal` rather than session artifacts.

## Mental Model

```text
HITLAutoresearch :=
  ArtifactGoal
+ VariantLoop
+ HumanFeedbackRequest
+ FeedbackScore
+ KeepDiscardDecision
+ NextVariant
```

The loop is useful when an agent can create many variants, but Kenji's judgment
is the fastest quality signal.

When composed inside `goal-crafter`'s Goal algebra, `hitl-autoresearch` is the
`Metric.human_feedback` and `Review.human_feedback` provider. It creates the
human feedback surface; native Goal mode owns continuation, and
`agent-qa-test` or `review` should own adversarial/mechanical proof when the
artifact also needs evidence beyond human judgment.

## Workflow

1. Identify the artifact family: demo, landing page, banner, video script,
   outreach angle, website, screenshot, or benchmark report.
2. Define a short-horizon outcome: one artifact set that can be reviewed today.
3. Define a feedback metric:
   - default: `human_score` from `feedback.json`, 0-10, higher is better
   - use binary `accepted` only when the output either passes or fails
4. Define the review question Kenji should answer.
5. Scaffold the session with `scripts/init_hitl_session.py`.
6. Run or hand off the session:
   - agent writes artifacts into `outputs/run-N/`
   - agent writes a concise `feedback-request.md`
   - agent uses `telegram-message` to send `feedback-request.md` when Telegram
     is configured
   - agent stops or waits for `feedback.json`
   - next run uses feedback to improve the next variant
7. Keep/discard variants by feedback score and stated rationale.
8. Finish only after the feedback source says `accepted`, `keep`, or the
   operator explicitly stops the loop. A request for feedback is a checkpoint,
   not completion.

## Session Shape

Each session directory should contain:

- `autoresearch.md` - goal, scope, human review contract
- `autoresearch.sh` - emits `METRIC human_score=<number>` from `feedback.json`
- `autoresearch.jsonl` - config and run history
- `feedback-request.md` - latest Telegram/request message
- `feedback.json` - written manually or by a future Telegram ingest bridge
- `outputs/` - generated artifacts

`feedback.json` shape:

```json
{
  "run": 1,
  "score": 8,
  "verdict": "keep",
  "feedback": "The hook is strong, but the demo needs a clearer operator pain.",
  "next_instruction": "Make the next version more specific to factory QA."
}
```

## Feedback Notification Contract

Telegram is optional but preferred. This skill does not own Telegram delivery;
use the `telegram-message` skill as the reusable notification primitive.

Expected Telegram environment, owned by `telegram-message`:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

If either variable is missing, write `feedback-request.md` and tell the operator
Telegram is not configured.

The feedback request must include:

- session name
- run number
- artifact paths or links
- the review question
- the exact `feedback.json` shape to paste back or save

## Reference Map

- [`references/goal-composition.md`](references/goal-composition.md) - split
  between Goal lifecycle ownership and HITL human-feedback ownership.

## Core Branches

- **Marketing/content:** metric is human score; artifact is text, image prompt,
  video script, or landing copy.
- **Demo packaging:** metric is human score; artifacts include screenshots,
  README, demo link/path, and outreach blurb.
- **UI/visual:** metric is human score plus visual QA notes; use `visual-qa`
  when an actual app surface changed.
- **Mechanical benchmark:** hand off to `autoresearch-plan`; do not add human
  feedback unless Kenji's judgment is the real metric.
- **Long delay needed:** create a heartbeat or automation outside this skill.
  Do not make an active `/goal` sleep for days.

## Top 3 Gotchas

1. Do not call subjective taste a mechanical metric. Make the human feedback
   file the metric source.
2. Do not force Kenji to write new prompts every time. Reuse the same session
   contract and only ask for the next review decision.
3. Do not let agents publish, send outreach, spend money, or make promises from
   a HITL loop. Human feedback is review, not external approval.
4. Do not treat screenshot delivery as the end of a HITL run. Screenshots create
   the review surface; human accept/revise feedback determines the next action.

## Judgment Questions

Use `advise` when these choices are not obvious:

- whether the loop should optimize one artifact deeply or generate many variants
- whether the review metric should be 0-10 score or binary accept/reject
- whether Telegram feedback is worth the extra setup versus local feedback files
- whether a task is better as native `/goal`, automation, or HITL autoresearch

## Outcome Contract

A completed setup produces:

- a session directory with valid `autoresearch.*` artifacts
- a first `feedback-request.md`
- a clear review question
- a launch instruction for the agent or operator

An executed loop produces:

- artifacts under `outputs/run-N/`
- a `feedback-request.md`, plus a Telegram notification when configured
- `feedback.json` or a blocked note waiting for it
- an updated run log with keep/discard decision
