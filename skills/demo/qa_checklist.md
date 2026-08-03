---
template_id: skill-qa-checklist
template_version: "0.1.1"
feature_refs:
  - FEAT-0008
  - FEAT-0057
consumer_scope: skill
applies_to:
  - skills/demo/SKILL.md
---

# Demo QA Checklist

Use before recap production and again before marking the demo complete.

## Checklist

- [ ] The selected ticket has passing QA, and every recap claim maps to a
  ticket, diagram, test, QA capture, or review artifact.
- [ ] The narrative visibly follows `Before`, `After`, one concrete `Example`,
  and no more than three `Key decisions`, followed by compact proof and honest
  residual risk for a lead-engineer audience.
- [ ] The production uses verified assets only, adds no generated visuals by
  default, and performs no external spend without explicit authorization.
- [ ] `final.mp4` passes media probing plus representative frame and audible
  narration inspection; duration is normally 45–90 seconds and the result is
  understandable without reading the ticket. For material feature work, the
  reviewed `final.mp4` is handed to `$close-ticket` as the first selected media
  item and first issue comment.
- [ ] Independent demo, video, and evidence review reaches TAS-A before
  `result.json` says `pass`, and ticket/progress links are written back.
