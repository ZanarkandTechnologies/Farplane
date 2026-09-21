# Init Advisor Phase Boundary


This skill follows Tier 0 phases inline. Use compact grounding before
finalizing project archetype, static charter, capability workflows, or metric objectives; use deeper
research only when stack commands, framework conventions, or market assumptions
may be stale. PRD authoring is downstream of the three-ticket business
foundation, not init completion.

`init_mode` controls completion semantics:

- `substrate`: create or preserve the Farplane project files, write any missing
  readiness gaps into `docs/bootstrap-brief.md`, and report
  `substrate_complete`.
- `full`: after substrate setup, call `harness-creator` for the operating-model
  pass. It owns the static charter, capability workflows, metric objectives, feedback loops, missing
  systems, metric objectives, and any later Goal Advisor handoff.

`human_intake` controls how init/migration fills human-meaning files:

- `skip`: scaffold or migrate files mechanically and write missing intent as
  readiness gaps in `docs/bootstrap-brief.md`.
- `offer` (default): when missing, placeholder, stale, or newly introduced
  files depend on human intent, offer a short intake before filling them.
- `required`: do not finalize meaning-heavy file content until the missing
  operator-owned params have been answered or recorded as blocked.

Use destination skill signatures as the question inventory. Route static
charter, capability workflow references, feedback loops, missing systems, and
objective shape to `harness-creator`; route metric meaning, directions, guards,
and proof providers to `metric-advisor`. When direct signature questions would
produce shallow or misleading answers, stop for focused operator clarification.
Record the intake choice and missing answers in `docs/bootstrap-brief.md`.

Do not treat file existence as readiness. Placeholder or stale split project
files mean "operating model still missing", not "initialized". Keep human
meaning, hard constraints, planning areas, and selected metric refs in
`farplane/harness.yaml`; keep reusable metric direction, freshness, and guard
rules in `farplane/metrics.yaml`; use
`goal-advisor` only after a ticket is concrete enough for a Goal Packet.

```text
setup_project_operating_model(bootstrap_brief, project_context,
                              existing_harness?, existing_capability_skills?,
                              existing_metrics?, human_intake?)
  -> readiness_status
   + human_intake_decision
   + first_missing_question?
   + focused_clarification_handoff?
   + harness_delta?
   + capability_skill_delta?
   + metric_objective_delta?
  + initial_metric_objectives?
   + goal_advisor_handoff?
```
