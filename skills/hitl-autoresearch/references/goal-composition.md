# Goal Composition

When `hitl-autoresearch` is invoked inside a Goal, it supplies human feedback
rather than owning the whole continuation loop.

Use this split:

- Goal mode owns continuation and blocked-stop reporting.
- `hitl-autoresearch` owns the feedback request, `feedback.json` shape, and
  `human_score` or `accepted` metric.
- Agent QA or final review should still be used when the artifact needs
  mechanical evidence beyond human judgment.
