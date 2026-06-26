# Feedback Request

Optimization target:
`trust_distribution / landing_page_offer`

Objective:
Make the Farplane landing page offer sharper, more believable, and easier to
keep, revise, or reject quickly.

Worker thread:
`019f0424-a832-7712-b952-85b50222a716` / current worker thread

Artifact refs:
- Spec: `tickets/TASK-0236/artifacts/landing-page-offer-v1/LANDING_SPEC.md`
- Prototype HTML: `tickets/TASK-0236/artifacts/landing-page-offer-v1/index.html`
- Mobile screenshot: `tickets/TASK-0236/artifacts/landing-page-offer-v1/screenshots/mobile.png`
- Desktop screenshot: `tickets/TASK-0236/artifacts/landing-page-offer-v1/screenshots/desktop.png`

Question:
Keep, revise, or reject the offer and page direction?

Please write feedback to:
`tickets/TASK-0236/artifacts/landing-page-offer-v1/feedback.json`

Feedback shape:

```json
{
  "artifact_id": "landing-page-offer-v1",
  "score": null,
  "verdict": "keep | revise | reject | approve",
  "feedback": "Short reason.",
  "labels": ["optional", "tags"],
  "next_instruction": "What the next worker turn should do."
}
```

Pause policy:
Worker pauses after sending this request. Telegram replies should resume this
worker thread, then the worker appends feedback to `progress.md` and revises
the artifact before asking again.
