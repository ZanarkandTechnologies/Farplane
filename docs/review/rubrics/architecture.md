# Architecture

`review` is the TAS contract surface for tickets and completed work. It
selects rubric families, inspects the smallest useful changed and neighboring
surface, and writes a structured verdict.

Frontend review uses multiple lanes:

- `ui-quality` judges visible product quality, taste, and fit to intent.
- `frontend-guidelines` records source-fresh Web Interface Guidelines results
  from `web-design-guidelines`.
- `frontend-code-maintainability` judges React/component structure, file length,
  hooks, state ownership, comments, DRY, and testable seams.
- `visual-qa` judges rendered UI proof when screenshots or browser state are in
  scope.

Keep those lanes separate so agent reviews can be compared instead of averaged
into one vague UI TAS.

## Quality Signal Layers

Farplane separates inspection, measurement, judgment, and learning so feedback
stays explainable.

```text
qa_checklist(artifact) -> checklist_results + violations + evidence_note
metric_advice(objective, evidence) -> measurement_contract | no_metric_reason
review(artifact, rubric, evidence) -> TAS + reasons + failed_checks + next_action
reward_event(output, judgment) -> verdict + evidence + repair_hint
```

- QA checklists are executable inspection prompts for a skill or artifact.
- Metrics are optional measurement contracts, usually owned by goals, products,
  projects, or experiments rather than ordinary skill maintenance.
- Rubrics are decision policies that classify readiness from evidence.
- Reward events preserve the verdict, reasons, failed checks, and repair hints
  so later skill or project updates can learn without collapsing feedback into a
  scalar score.

Do not promote every checklist item into a metric. Do not treat a metric as a
review verdict. Use numbers only when they make a decision clearer without
destroying the repair context.
